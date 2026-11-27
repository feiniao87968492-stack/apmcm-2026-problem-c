"""Compare three 100 m prefix criteria under intermittent noise."""
import numpy as np
import pandas as pd

import q2
from control_subtraction import reference
from q4_envelope_attainment import DRAWS, REQUIRED
from q4_response_sensitivity import DISTANCES, LEVELS
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities


EXCESS_POWER = 10**.6 - 1
SCORE_RULES = ("mean_score", "continuous_mean_power")


def boundary(count):
    low, high = 0., 1.
    while high - low > 1e-10:
        middle = (low + high) / 2
        if count(middle) >= REQUIRED:
            low = middle
        else:
            high = middle
    return low, high


def compare(model, clean_score, cutoff, excess_ratio, clean_archive, noisy_archive):
    def score_at(f):
        squared_ratio = (1 + excess_ratio) / (1 + (1 + f * EXCESS_POWER) * excess_ratio)
        return clean_score * np.where(clean_score > 0, squared_ratio, np.sqrt(squared_ratio))

    noisy_score = score_at(1.)

    def passes(score):
        return (score >= cutoff[:, None]).all(axis=1)

    clean = int(passes(clean_score).sum())
    noisy = int(passes(noisy_score).sum())
    assert clean == clean_archive and noisy == noisy_archive and clean >= REQUIRED > noisy
    scores = {
        "mean_score": lambda f: clean_score + f * (noisy_score - clean_score),
        "continuous_mean_power": score_at,
    }

    def count(rule, f):
        return int(passes(scores[rule](f)).sum())

    rows = []
    for f in LEVELS:
        mean = passes(scores["mean_score"](f))
        continuous = passes(score_at(f))
        assert (mean | ~continuous).all()
        for rule, value in (("mean_score", int(mean.sum())),
                            ("continuous_mean_power", int(continuous.sum())),
                            ("state_indicators", (1-f)*clean + f*noisy)):
            rows.append(dict(model=model, rule=rule, f=f, count_or_expected=value,
                             share=value/DRAWS, passes_80=value >= REQUIRED))

    limits = []
    for rule in SCORE_RULES:
        maximum, failing = boundary(lambda f: count(rule, f))
        at, beyond = count(rule, maximum), count(rule, failing)
        assert at >= REQUIRED > beyond
        limits.append(dict(model=model, rule=rule, max_f=maximum, count_at_limit=at,
                           failing_f=failing, count_at_failing=beyond))
    assert limits[0]["max_f"] >= limits[1]["max_f"]
    maximum = (clean-REQUIRED)/(clean-noisy)
    limits.append(dict(model=model, rule="state_indicators", max_f=maximum,
                       count_at_limit=REQUIRED, failing_f=None, count_at_failing=None))
    return rows, limits


def write(data, output, archive):
    curves, shared = acoustic_fidelities(data, distances=DISTANCES, include_shared=True)
    tv = q2.CALLS.index("tv")
    _, scale, exponent = shared[1:, tv].T
    excess_ratio = (DISTANCES / scale[:, None])**exponent[:, None]
    weakest = np.minimum.reduce([curve[1:, tv] for curve in curves.values()])
    clean_archive = pd.read_csv(archive / "q4_consecutive_counts.csv").query(
        "scenario == 'clean' and shape == 'all_four' and distance_m == 100"
    ).set_index("model").prefix_count
    noisy_archive = pd.read_csv(archive / "q4_matched_noise_targets.csv").query(
        "distance_m == 100 and spatial == 'local' and link == 'coupled'"
    ).set_index("model").count_6db
    rows, limits = [], []
    for model, probabilities in behavior_probabilities(data, distances=DISTANCES):
        excess = probabilities[:, 0] - probabilities[:, 1]
        if model == "full":
            cutoff = reference(curves["isotonic"], excess)[1:]
            assert np.all(np.isfinite(cutoff) & (cutoff > 0))
        checks, bounds = compare(model, weakest*excess[1:, tv], cutoff, excess_ratio,
                                 clean_archive.loc[model], noisy_archive.loc[model])
        rows.extend(checks)
        limits.extend(bounds)
    output.mkdir(parents=True, exist_ok=True)
    for suffix, records in (("checks", rows), ("limits", limits)):
        pd.DataFrame(records).to_csv(output / f"q4_intermittent_noise_{suffix}.csv",
                                     index=False, lineterminator="\n")
