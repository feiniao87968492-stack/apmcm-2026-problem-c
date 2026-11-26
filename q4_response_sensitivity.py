"""Invert the Q4 response-retention scenario at 6 dB and 100 m."""
from itertools import product

import numpy as np
import pandas as pd

import noise_scenarios
import q2
from control_subtraction import reference
from q4_envelope_attainment import DRAWS, REQUIRED
from q4_matched_noise import GRID, MATCH
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities

LEVELS = (0., .25, .50, .75, 1.)
TOL = 1e-12
PROBE = 1e-7
DISTANCES = GRID[:MATCH+1]


def counts_at(score, cutoff, ratio, level, slack=0.):
    retained = score * ratio * np.where(score > 0, ratio**level, 1.)
    return int(np.count_nonzero(np.all(retained >= cutoff * (1-slack), axis=1)))


def evaluate(score, cutoff, ratio):
    score, ratio = np.broadcast_arrays(score, ratio)
    tolerances = np.full_like(score, -np.inf)
    positive = score > 0
    loss = positive & (ratio < 1)
    thresholds = np.broadcast_to(cutoff, score.shape)
    tolerances[loss] = np.log(thresholds[loss]/score[loss]) / np.log(ratio[loss]) - 1
    tolerances[positive & (ratio == 1) & (score >= cutoff)] = np.inf
    per_draw = tolerances.min(axis=1)
    limit = np.partition(per_draw, DRAWS-REQUIRED)[DRAWS-REQUIRED]
    checkpoints = [counts_at(score, cutoff, ratio, level) for level in LEVELS]
    result = dict(zip(("count_0", "count_025", "count_05", "count_075", "count_1"), checkpoints))
    if checkpoints[0] < REQUIRED:
        return dict(result, status="infeasible", max_lambda=np.nan)
    if checkpoints[-1] >= REQUIRED:
        return dict(result, status="cap", max_lambda=1., count_at_limit=checkpoints[-1])

    at_limit = counts_at(score, cutoff, ratio, limit, slack=TOL)
    assert 0 <= limit < 1 and at_limit >= REQUIRED
    result.update(status="boundary", max_lambda=limit, count_at_limit=at_limit)
    if limit+PROBE <= 1:
        beyond = counts_at(score, cutoff, ratio, limit+PROBE)
        assert beyond < REQUIRED
        result.update(probe_lambda=limit+PROBE, count_beyond=beyond)
    return result


def write(data, output, baseline):
    curves, shared = acoustic_fidelities(data, distances=DISTANCES, include_shared=True)
    tv = q2.CALLS.index("tv")
    parameters = shared[1:, tv, None, :]
    local = (noise_scenarios.fidelity(DISTANCES, parameters, 6) /
             noise_scenarios.fidelity(DISTANCES, parameters, 0))[:, 0]
    assert np.all((local > 0) & (local <= 1))
    weakest = np.minimum.reduce([curve[1:, tv] for curve in curves.values()])
    archived = pd.read_csv(baseline / "q4_matched_noise_targets.csv").query("distance_m == 100")
    archived = archived.set_index(["model", "spatial", "link"])
    rows = []
    for model, probabilities in behavior_probabilities(data, distances=DISTANCES):
        excess = probabilities[:, 0] - probabilities[:, 1]
        if model == "full":
            cutoff = reference(curves["isotonic"], excess)[1:, None]
            assert np.all(np.isfinite(cutoff) & (cutoff > 0))
        score = weakest * excess[1:, tv]
        assert np.isfinite(score).all()
        for spatial, rule in product(("local", "uniform"), ("prefix", "endpoint")):
            ratio = local if spatial == "local" else local[:, -1:]
            result = evaluate(score if rule == "prefix" else score[:, -1:], cutoff,
                              ratio if rule == "prefix" else ratio[:, -1:])
            if rule == "prefix":
                for name, link in (("count_0", "acoustic_only"), ("count_1", "coupled")):
                    assert result[name] == archived.loc[(model, spatial, link), "count_6db"]
                prefix_limit = result["max_lambda"]
            rows.append(dict(model=model, spatial=spatial, rule=rule, distance_m=100, db=6,
                             draws=DRAWS, **result,
                             endpoint_minus_prefix=result["max_lambda"]-prefix_limit if rule == "endpoint" else 0.))
    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output / "q4_response_sensitivity.csv", index=False, lineterminator="\n")
