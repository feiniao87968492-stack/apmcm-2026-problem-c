"""Stress-test the clean two-voice net decision beyond retained playback distances."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import expit, logit

import physical_attenuation
import q3
from control_subtraction import reference
from distance_deletion import pair_filters, refit
from distance_deletion_mc import DATE_SEED, PREFIXES, acoustics

DISTANCES = np.array([20, 100, 150])
CALL = q3.CALLS.index("tv")
ANCHORS = np.array([100, 120])
DRAWS = PREFIXES[-1]
REQUIRED = 4 * DRAWS // 5


def tolerances(logits, fidelity, cutoff, slopes, qualifies):
    """Return the largest admissible drift for each point or draw."""
    roots = np.full(len(fidelity), -np.inf)
    limiting = expit(logits)
    limiting[:, slopes < 0] = 0
    limiting[:, slopes > 0] = 1
    unbounded = fidelity * (limiting[:, 0] - limiting[:, 1]) >= cutoff
    roots[qualifies & unbounded] = np.inf
    for i in np.flatnonzero(qualifies & ~unbounded):
        def margin(drift):
            natural, control = expit(logits[i] + slopes * drift)
            return fidelity[i] * (natural - control) - cutoff[i]

        # The baseline decision uses the original probabilities. Preserve
        # attainment if the logit round trip rounds an exact zero below it.
        if margin(0) <= 0:
            roots[i] = 0
            continue
        upper = 1.
        while margin(upper) > 0:
            upper *= 2
        roots[i] = brentq(margin, 0, upper, xtol=1e-14)
    return roots


def evaluate(probabilities, fidelity, cutoff):
    logits = logit(probabilities)
    baseline_margin = fidelity * (probabilities[:, 0] - probabilities[:, 1]) - cutoff
    qualifies = baseline_margin >= 0
    count = int(qualifies[1:].sum())
    assert qualifies[0] and count == 4002
    yield dict(scenario="zero_drift", binding="baseline", lambda_max=0., odds_factor=1.,
               p_n=probabilities[0, 0], p_c=probabilities[0, 1], delta_p_n=0., delta_p_c=0.,
               point_margin=baseline_margin[0], count=count, support=count / DRAWS, valid_draws=DRAWS)
    scale = np.log2(DISTANCES[-1] / ANCHORS)
    for name, signs in (("natural_only", (-1, 0)), ("control_only", (0, 1)),
                        ("both", (-1, 1))):
        slopes = scale * signs
        roots = tolerances(logits, fidelity, cutoff, slopes, qualifies)
        point_root = roots[0]
        support_root = np.partition(roots[1:], DRAWS - REQUIRED)[DRAWS - REQUIRED]
        limit = min(point_root, support_root)
        # Use inclusive root comparisons at equality to avoid residual
        # rounding, then check direct counts on either side of the root.
        at = int(np.count_nonzero(roots[1:] >= limit))
        beyond = int(np.count_nonzero(roots[1:] > limit))
        epsilon = 1e-8
        for drift in (limit - epsilon, limit + epsilon):
            p = expit(logits[1:] + slopes * drift)
            direct = np.count_nonzero(fidelity[1:] * (p[:, 0] - p[:, 1]) >= cutoff[1:])
            assert direct == np.count_nonzero(roots[1:] >= drift)
        point = np.where(slopes != 0, expit(logits[0] + slopes * limit), probabilities[0])
        change = point - probabilities[0]
        yield dict(scenario=name, binding="support" if support_root < point_root else
                   "point" if point_root < support_root else "both", lambda_max=limit,
                   lambda_point=point_root, lambda_support=support_root, odds_factor=np.exp(limit),
                   p_n=point[0], p_c=point[1], delta_p_n=change[0], delta_p_c=change[1],
                   point_margin=fidelity[0] * (point[0] - point[1]) - cutoff[0],
                   count=at, count_just_above=beyond, support=at / DRAWS, valid_draws=DRAWS)


def run(data, output, baseline):
    frame = q3.load_playbacks(data)
    weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    n_dates = frame.Date.nunique()
    sampled = np.random.default_rng(DATE_SEED).integers(n_dates, size=(DRAWS, n_dates))
    filters, _ = pair_filters(frame)
    retained = frame.loc[filters["drop_union"] & frame.assigned_call.eq("tv")]
    np.testing.assert_array_equal(retained.groupby("Type").Distance.max().reindex(q3.STIMULI), ANCHORS)
    full_point, full_draws = refit(frame, filters["full"], sampled, weights, distances=DISTANCES)
    point, draws = refit(frame, filters["drop_union"], sampled, weights, distances=DISTANCES)
    iso, fidelity = acoustics(data, DISTANCES)

    q2 = pd.read_csv(baseline / "q2_propagation.csv")
    iso_point = q2.loc[q2.distance_m.eq(20)].set_index("call").loc[list(q3.CALLS), ["fidelity"]]
    parameters = pd.read_csv(baseline / "physical_q2_parameters.csv").query("model == 'shared_g'")
    parameters = parameters.set_index("call").loc[list(q3.CALLS), ["ceiling", "scale_m", "exponent"]]
    point_fidelity = physical_attenuation.curve(DISTANCES, parameters.to_numpy())[CALL, -1]
    cutoff = np.r_[reference(iso_point.to_numpy(), full_point[0] - full_point[1]),
                   reference(iso, full_draws[:, 0] - full_draws[:, 1])]
    acoustic = np.r_[point_fidelity, fidelity[:, CALL, -1]]
    probabilities = np.vstack((point[:, CALL, -1], draws[:, :, CALL, -1]))
    assert np.isfinite(probabilities).all() and np.isfinite(cutoff).all() and np.isfinite(acoustic).all()
    archived = pd.read_csv(baseline / "distance_deletion_points.csv").query(
        "model == 'drop_union' and call == 'tv' and distance_m == 150 "
        "and link == 'clean' and definition == 'net_own'"
    ).iloc[0]
    margin = acoustic[0] * (probabilities[0, 0] - probabilities[0, 1]) - cutoff[0]
    np.testing.assert_allclose([*probabilities[0], cutoff[0], margin],
                               archived[["p_n", "p_c", "cutoff", "margin"]].to_numpy(dtype=float),
                               atol=1e-12, rtol=0)
    result = pd.DataFrame(evaluate(probabilities, acoustic, cutoff))
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False, float_format="%.15g")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path, help="Contest attachment CSV directory")
    parser.add_argument("--output", default=Path("results/q4_extrapolation_drift.csv"), type=Path)
    parser.add_argument("--baseline", default=Path("results"), type=Path)
    args = parser.parse_args()
    run(args.data, args.output, args.baseline)
