"""Compare gross and signed control-subtracted Q4 scores."""
from itertools import combinations

import numpy as np
import pandas as pd

import noise_scenarios
from q3 import REPRESENTATIVE
from q4 import environment, radius
from spatial_annulus import average, limits


def reference(fidelity, response):
    return (fidelity[..., 0] * response[..., 0]).mean(axis=-1) / 2


def score_curves(fidelity, natural, control, loss, coupled):
    gross, _ = environment(fidelity, natural, control if coupled else natural, loss, 0)
    acoustic = fidelity * (1 - loss)
    excess = natural - control
    response = noise_scenarios.response(natural, control, loss, coupled)
    net = acoustic * (response - control)
    np.testing.assert_allclose(gross - net, acoustic * control, atol=1e-12, rtol=0)
    factor = np.where((excess > 0) & coupled, (1 - loss)**2, 1 - loss)
    np.testing.assert_allclose(net, fidelity * excess * factor, atol=1e-12, rtol=0)
    return gross, net


def area_results(rows, gaps, fields, calls, distance, point, draws):
    areas = average(point, distance, area=True)
    sampled = average(draws, distance, area=True)
    for i, call in enumerate(calls):
        rows.append(dict(fields, call=call, mean=areas[i], rank=1 + (areas > areas[i]).sum(),
                         **limits(sampled[:, i], "mean")))
    for i, j in combinations(range(len(calls)), 2):
        gaps.append(dict(fields, first=calls[i], second=calls[j], gap=areas[i]-areas[j],
                         **limits(sampled[:, i]-sampled[:, j], "gap")))


def run(propagation, behavior, date_predictions, parameters, sampled_parameters, output):
    distance, calls = propagation["distance"], propagation["calls"]
    p_n, p_c = behavior["natural"], behavior["control"]
    b_n, b_c = date_predictions[:, 0], date_predictions[:, 1]
    iso, iso_draws = propagation["fidelity"], propagation["draws"]
    gross_ref = reference(iso, p_n), reference(iso_draws, b_n)
    net_ref = reference(iso, p_n-p_c), reference(iso_draws, b_n-b_c)
    fidelity = noise_scenarios.fidelity(distance, parameters, 0)
    sampled = noise_scenarios.fidelity(distance, sampled_parameters, 0)
    area, gaps, radii, points, decisions = [], [], [], [], []
    comparisons = (("gross", "net_shared"), ("gross", "net_own"), ("net_shared", "net_own"))
    for loss, link in ((0., "clean"), (.20, "acoustic_only"), (.20, "coupled")):
        gross, net = score_curves(fidelity, p_n, p_c, loss, link == "coupled")
        gdraw, ndraw = score_curves(sampled, b_n, b_c, loss, link == "coupled")
        fields = dict(loss=loss, link=link)
        for name, point, draws in (("gross", gross, gdraw), ("net", net, ndraw)):
            area_results(area, gaps, dict(fields, score=name), calls, distance, point, draws)
        for i, call in enumerate(calls):
            counts = {}
            for name, point, draws, (cutoff, cutoffs) in (
                ("gross", gross, gdraw, gross_ref),
                ("net_shared", net, ndraw, gross_ref),
                ("net_own", net, ndraw, net_ref),
            ):
                row = dict(fields, definition=name, call=call, cutoff=cutoff)
                point_radius, status = radius(distance, point[i], cutoff)
                bound_draws, flags = zip(*(radius(distance, curve, ref)
                                           for curve, ref in zip(draws[:, i], cutoffs)))
                radii.append(dict(row, radius_m=point_radius, status=status,
                                  **limits(bound_draws, "radius_m"),
                                  draws_below=flags.count("below_support"),
                                  draws_above=flags.count("above_support")))
                for d in REPRESENTATIVE:
                    j = np.searchsorted(distance, d)
                    margins = draws[:, i, j] - cutoffs
                    count = np.count_nonzero(margins >= 0)
                    counts[name, d] = count
                    margin = point[i, j]-cutoff
                    points.append(dict(row, distance_m=d, margin=margin, point_attains=margin >= 0,
                                       **limits(margins, "margin"), draws=len(cutoffs),
                                       count=count, support=count / len(cutoffs),
                                       passes_80=5 * count >= 4 * len(cutoffs)))
            for first, second in comparisons:
                for d in REPRESENTATIVE:
                    n = len(gross_ref[1])
                    a, b = counts[first, d], counts[second, d]
                    before, after = 5*a >= 4*n, 5*b >= 4*n
                    decisions.append(dict(fields, call=call, distance_m=d, reference=first,
                                          alternative=second, reference_support=a/n,
                                          alternative_support=b/n, support_change=(b-a)/n,
                                          reference_passes=before, alternative_passes=after,
                                          decision_changed=before != after))
    outputs = dict(area=area, area_gaps=gaps, radii=radii, points=points, decisions=decisions)
    for name, rows in outputs.items():
        pd.DataFrame(rows).to_csv(output / f"control_subtraction_{name}.csv", index=False)
