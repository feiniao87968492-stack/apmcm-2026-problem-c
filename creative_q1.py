"""Within-date-and-site permutation tests for peak frequency."""
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from statsmodels.stats.multitest import multipletests

from q1 import CALLS


N_PERMUTATIONS = 9999


def group_blocks(frame):
    groups = frame.Date.astype(str) + " | " + frame.Location.astype(str)
    labels = pd.Categorical(frame.CallType, categories=CALLS).codes
    peaks = frame.Fpeak.to_numpy(dtype=float)
    if np.any(labels < 0) or not np.all(np.isfinite(peaks)):
        raise ValueError("The blocked Fpeak analysis requires known call labels and complete peak frequencies")
    _, ids = np.unique(groups, return_inverse=True)
    return [(i, labels[ids == i], peaks[ids == i]) for i in np.unique(ids)]


def label_permutations(labels, rng):
    pool = np.broadcast_to(labels, (N_PERMUTATIONS, len(labels)))
    return rng.permuted(pool, axis=1)


def monte_carlo_p(observed, simulated):
    # Treat floating-point variations of a tied statistic as ties.
    extreme = (simulated > observed) | np.isclose(simulated, observed, rtol=1e-12, atol=1e-12)
    return (1 + np.count_nonzero(extreme)) / (N_PERMUTATIONS + 1)


def omnibus(blocks, rows, seed):
    rng = np.random.default_rng(seed)
    observed = np.zeros(len(CALLS))
    simulated = np.zeros((N_PERMUTATIONS, len(CALLS)))
    informative_count = 0
    for group, labels, peaks in blocks:
        counts = np.bincount(labels, minlength=len(CALLS))
        informative = np.count_nonzero(counts) >= 2
        ranks = rankdata(peaks) - (len(peaks) + 1) / 2
        group_totals = np.bincount(labels, weights=ranks, minlength=len(CALLS))
        rows.append({
            "test": "omnibus", "recording_group": group, "informative": informative,
            **{f"n_{call}": count for call, count in zip(CALLS, counts)},
            **{f"centered_rank_sum_{call}": total for call, total in zip(CALLS, group_totals)},
        })
        if informative:
            informative_count += 1
            observed += group_totals
            permuted = label_permutations(labels, rng)
            for i in range(len(CALLS)):
                simulated[:, i] += (permuted == i) @ ranks
    statistic = np.sum(observed ** 2)
    return {
        "test": "omnibus", "statistic": statistic, "informative_groups": informative_count,
        "p_raw": monte_carlo_p(statistic, np.sum(simulated ** 2, axis=1)),
    }


def pair_test(blocks, left, right, rows, seed, n_boot):
    rng = np.random.default_rng(seed)
    test = f"{CALLS[left]}_vs_{CALLS[right]}"
    simulated_numerator = np.zeros(N_PERMUTATIONS)
    contributions, weights = [], []
    for group, labels, peaks in blocks:
        counts = np.bincount(labels, minlength=len(CALLS))
        n_left, n_right = counts[left], counts[right]
        has_both = n_left > 0 and n_right > 0
        row = {
            "test": test, "recording_group": group, "informative": has_both,
            **{f"n_{call}": count for call, count in zip(CALLS, counts)},
        }
        if has_both:
            include = (labels == left) | (labels == right)
            values = peaks[include]
            is_left = labels[include] == left
            weight = n_left * n_right / len(values)
            center = n_left / len(values) * values.sum()
            weighted_difference = values[is_left].sum() - center
            contributions.append(weighted_difference)
            weights.append(weight)
            simulated_numerator += (label_permutations(is_left, rng) @ values) - center
            row.update({
                "pair_weight": weight, "mean_difference_hz": weighted_difference / weight,
                "weighted_difference_hz": weighted_difference,
            })
        rows.append(row)
    contributions = np.asarray(contributions)
    weights = np.asarray(weights)
    effect = contributions.sum() / weights.sum()
    simulated = np.abs(simulated_numerator / weights.sum())
    observed = abs(effect)
    bootstrap_rng = np.random.default_rng(seed)
    groups = bootstrap_rng.integers(len(weights), size=(n_boot, len(weights)))
    sampled = contributions[groups].sum(axis=1) / weights[groups].sum(axis=1)
    lower, upper = np.quantile(sampled, [0.025, 0.975])
    return {
        "test": test, "left": CALLS[left], "right": CALLS[right], "statistic": observed,
        "informative_groups": len(weights), "difference_hz": effect, "lower_hz": lower,
        "upper_hz": upper, "p_raw": monte_carlo_p(observed, simulated),
    }


def run(data, output, seed, n_boot):
    path, = data.glob("Data01*.csv")
    blocks = group_blocks(pd.read_csv(path))
    rows = []
    results = [omnibus(blocks, rows, seed)]
    for left, right in combinations(range(len(CALLS)), 2):
        results.append(pair_test(blocks, left, right, rows, seed, n_boot))
    tests = pd.DataFrame(results)
    tests["permutations"] = N_PERMUTATIONS
    tests["p_holm"] = multipletests(tests.p_raw, method="holm")[1]
    tests.to_csv(output / "creative_q1_fpeak_tests.csv", index=False)
    groups = pd.DataFrame(rows)
    groups["normalized_pair_contribution_hz"] = (
        groups.weighted_difference_hz / groups.groupby("test").pair_weight.transform("sum")
    )
    groups.to_csv(output / "creative_q1_fpeak_groups.csv", index=False)
