"""Compare released Q3 behavior estimators in Q4 scenarios."""
import numpy as np
import pandas as pd

import noise_scenarios
import q3
from control_subtraction import area_results, reference, score_curves
from creative_q3 import fit_structured
from spatial_annulus import average, limits


def alternatives(frame, distance, sampled_dates):
    contexts = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    weights = contexts.to_numpy()
    names = tuple(contexts.index)
    design = q3.features(frame, names)
    target = q3.features(q3.probability_grid(distance, names, 8), names)
    masks = frame["mask"].to_numpy()
    shape = (len(q3.STIMULI), len(q3.CALLS), len(distance), len(names), len(q3.MASKS))
    blocks = [np.flatnonzero(frame.Date.eq(d)) for d in sorted(frame.Date.unique())]

    def predict(rows):
        structured = fit_structured(design[rows], masks[rows], target, interactions=True)
        pairwise = 1 - structured.reshape(shape)[..., 0] @ weights
        frequencies = []
        for stimulus in q3.STIMULI:
            counts = np.bincount(masks[rows[frame.Type.to_numpy()[rows] == stimulus]], minlength=8)
            probabilities = (counts + .5) / (counts.sum() + 4)
            frequencies.append(1 - probabilities[0])
        constant = np.broadcast_to(np.asarray(frequencies)[:, None, None], pairwise.shape)
        return np.stack((pairwise, constant))

    point = predict(np.arange(len(frame)))
    draws = np.stack([predict(np.concatenate([blocks[i] for i in dates])) for dates in sampled_dates], axis=1)
    return point, draws


def coverage(frame):
    for call in q3.CALLS:
        for distance in q3.REPRESENTATIVE:
            nearby = frame.assigned_call.eq(call) & frame.Distance.sub(distance).abs().le(25)
            for stimulus in q3.STIMULI:
                part = frame.loc[nearby & frame.Type.eq(stimulus)]
                responses = part["mask"].ne(0).sum()
                yield dict(call=call, distance_m=distance, stimulus=stimulus, trials=len(part),
                           responses=responses, dates=part.Date.nunique(),
                           sparse=len(part) < 5 or responses < 5)


def run(frame, sampled_dates, propagation, behavior, date_predictions,
        parameters, sampled_parameters, output):
    distance, calls = propagation["distance"], propagation["calls"]
    iso, iso_draws = propagation["fidelity"], propagation["draws"]
    fidelity = noise_scenarios.fidelity(distance, parameters, 0)
    sampled = noise_scenarios.fidelity(distance, sampled_parameters, 0)
    a_point = np.stack((behavior["natural"], behavior["control"]))
    gross_reference = reference(iso, a_point[0]), reference(iso_draws, date_predictions[:, 0])
    alternative_point, alternative_draws = alternatives(frame, distance, sampled_dates)
    area, gaps, points = [], [], []
    baseline_area, baseline_support = {}, {}
    models = ("full_multinomial", "pairwise_mask", "smoothed_stimulus")
    for model, point, draws in zip(models, (a_point, *alternative_point),
                                   (date_predictions, *alternative_draws)):
        own_reference = reference(iso, point[0]-point[1]), reference(iso_draws, draws[:, 0]-draws[:, 1])
        for loss, link in ((0., "clean"), (.20, "coupled")):
            gross, net = score_curves(fidelity, *point, loss, loss > 0)
            gross_draws, net_draws = score_curves(sampled, draws[:, 0], draws[:, 1], loss, loss > 0)
            fields = dict(model=model, loss=loss, link=link)
            scores = (("gross", gross, gross_draws), ("net", net, net_draws))
            for score, values, samples in scores:
                key = (link, score)
                means, draw_means = average(values, distance, True), average(samples, distance, True)
                base, base_draws = baseline_area.setdefault(key, (means, draw_means))
                delta, draw_delta = means - base, draw_means - base_draws
                start = len(area)
                area_results(area, gaps, dict(fields, score=score), calls, distance, values, samples)
                for i, row in enumerate(area[start:]):
                    row.update(delta_vs_A=delta[i], **limits(draw_delta[:, i], "delta_vs_A"))
                for row in gaps[-3:]:
                    i, j = calls.index(row["first"]), calls.index(row["second"])
                    row.update(delta_vs_A=delta[i]-delta[j],
                               **limits(draw_delta[:, i]-draw_delta[:, j], "delta_vs_A"))

            definitions = (("gross", gross, gross_draws, gross_reference),
                           ("net_shared", net, net_draws, gross_reference),
                           ("net_own", net, net_draws, own_reference))
            for definition, values, samples, (cutoff, cutoffs) in definitions:
                for i, call in enumerate(calls):
                    for d in q3.REPRESENTATIVE:
                        j = np.searchsorted(distance, d)
                        margin = values[i, j] - cutoff
                        draw_margins = samples[:, i, j] - cutoffs
                        n = len(cutoffs)
                        count = np.count_nonzero(draw_margins >= 0)
                        passes = 5 * count >= 4 * n
                        base_count, base_passes = baseline_support.setdefault(
                            (link, definition, call, d), (count, passes),
                        )
                        points.append(dict(fields, definition=definition, call=call, distance_m=d,
                                           cutoff=cutoff, margin=margin, point_attains=margin >= 0,
                                           **limits(draw_margins, "margin"), draws=n,
                                           count=count, support=count/n, passes_80=passes,
                                           support_change_vs_A=(count-base_count)/n,
                                           decision_changed_vs_A=passes != base_passes))
    for name, records in (("area", area), ("area_gaps", gaps), ("points", points),
                          ("coverage", coverage(frame))):
        pd.DataFrame(records).to_csv(output / f"behavior_ablation_{name}.csv", index=False)
