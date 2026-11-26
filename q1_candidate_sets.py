"""Evaluate call-type candidate sets on held-out recording groups."""
from argparse import ArgumentParser
from fractions import Fraction
from math import ceil
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from q1 import CALLS, FEATURES

LEVELS = (Fraction(4, 5), Fraction(9, 10))
RULES = ("pooled_row", "equal_group", "group_max")
FIXED = ("top_1", "top_2")


def probabilities(x, y, fit):
    present = np.unique(y[fit])
    result = np.zeros((len(x), len(CALLS)))
    if len(present) == 1:
        result[:, present[0]] = 1
    else:
        model = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000))
        model.fit(x[fit], y[fit])
        result[:, model.classes_] = model.predict_proba(x)
    return result


def quantiles(score, group, level):
    row_rank = ceil((len(score) + 1) * level)
    pooled = np.sort(score)[row_rank - 1] if row_rank <= len(score) else np.inf
    ids, counts = np.unique(group, return_counts=True)
    n_with_test = len(ids) + 1
    weights = {g: Fraction(1, n_with_test * int(n)) for g, n in zip(ids, counts)}
    mass, weighted, weighted_rank = Fraction(0), np.inf, len(score) + 1
    for rank, j in enumerate(np.argsort(score, kind="stable"), 1):
        mass += weights[group[j]]
        if mass >= level:
            weighted, weighted_rank = score[j], rank
            break
    maxima = sorted(score[group == g].max() for g in ids)
    max_rank = ceil(n_with_test * level)
    maximum = maxima[max_rank - 1] if max_rank <= len(maxima) else np.inf
    return ((pooled, row_rank), (weighted, weighted_rank), (maximum, max_rank))


def count_sets(included, true, held, rule, nominal=None):
    covered = included[np.arange(len(true)), true]
    size = included.sum(axis=1)
    tv = true == CALLS.index("tv")
    return dict(group=held, rule=rule, nominal=nominal, trials=len(true), covered=covered.sum(),
                all_covered=int(covered.all()), sets_labels=size.sum(), singleton_errors=((size == 1) & ~covered).sum(),
                two_voice_trials=tv.sum(), two_voice_covered=(covered & tv).sum(),
                **{f"size_{k}": (size == k).sum() for k in range(len(CALLS) + 1)})


def held_out(frame):
    keys = frame.Date.astype(str) + " | " + frame.Location.astype(str)
    unique, ids = np.unique(keys, return_inverse=True)
    if len(unique) != 16:
        raise ValueError("Expected the 16 contest recording groups.")
    groups = np.arange(len(unique))
    x = frame.loc[:, FEATURES].to_numpy()
    y = pd.Categorical(frame.CallType, categories=CALLS).codes
    rng = np.random.default_rng(20261126)
    thresholds, folds = [], []
    for held in groups:
        order = rng.permutation(groups[groups != held])
        fit_ids, cal_ids = order[:6], order[6:]
        fit, cal, test = np.isin(ids, fit_ids), np.isin(ids, cal_ids), ids == held
        score = 1 - probabilities(x, y, fit)
        ranking = np.argsort(score[test], axis=1, kind="stable")
        for k, rule in enumerate(FIXED, 1):
            included = np.zeros_like(score[test], dtype=bool)
            np.put_along_axis(included, ranking[:, :k], True, axis=1)
            folds.append(count_sets(included, y[test], held, rule))
        calibration_scores = score[cal, y[cal]]
        for level in LEVELS:
            for rule, (threshold, rank) in zip(RULES, quantiles(calibration_scores, ids[cal], level)):
                folds.append(count_sets(score[test] <= threshold, y[test], held, rule, float(level)))
                thresholds.append(dict(group=held, rule=rule, nominal=float(level), rank=rank,
                                       threshold=threshold, fit_groups=" ".join(map(str, fit_ids)),
                                       calibration_groups=" ".join(map(str, cal_ids)),
                                       fit_trials=fit.sum(), calibration_trials=cal.sum(), test_trials=test.sum()))
    return pd.DataFrame(folds), pd.DataFrame(thresholds)


def metric_inputs(fold):
    one = np.ones(len(fold), dtype=int)
    return {
        "trial_coverage": (fold.covered, fold.trials),
        "equal_group_coverage": (fold.covered / fold.trials, one),
        "whole_group_coverage": (fold.all_covered, one),
        "mean_size": (fold.sets_labels, fold.trials),
        "singleton_error_rate": (fold.singleton_errors, fold.size_1),
        "singleton_error_count": (fold.singleton_errors, None),
        "two_voice_coverage": (fold.two_voice_covered, fold.two_voice_trials),
        **{f"size_{k}_count": (fold[f"size_{k}"], None) for k in range(len(CALLS) + 1)},
        **{f"size_{k}_share": (fold[f"size_{k}"], fold.trials) for k in range(len(CALLS) + 1)},
    }


def summarize(folds):
    groups = folds.group.nunique()
    draws = np.random.default_rng(20261127).integers(groups, size=(4800, groups))
    summary, samples = [], {}
    for (rule, level), fold in folds.groupby(["rule", "nominal"], dropna=False, sort=False):
        nominal = None if pd.isna(level) else level
        for metric, (numerator, denominator) in metric_inputs(fold.sort_values("group")).items():
            num = np.asarray(numerator)
            boot_total = num[draws].sum(axis=1)
            total = num.sum()
            if denominator is None:
                boot, value, count = boot_total, total, None
            else:
                den = np.asarray(denominator)
                boot_den = den[draws].sum(axis=1)
                boot = np.full(len(draws), np.nan)
                np.divide(boot_total, boot_den, out=boot, where=boot_den > 0)
                count = den.sum()
                value = total / count if count else np.nan
            samples[rule, nominal, metric] = (value, boot)
            summary.append(dict(rule=rule, nominal=nominal, metric=metric, value=value,
                                numerator=total, denominator=count, **limits(boot)))
    paired = []
    for (rule, nominal, metric), (value, boot) in samples.items():
        for comparator in (("top_1",) if rule == "top_2" else FIXED if rule in RULES else ()):
            base, base_boot = samples[comparator, None, metric]
            paired.append(dict(rule=rule, nominal=nominal, metric=metric, comparator=comparator,
                               delta=value-base, **limits(boot-base_boot)))
    return pd.DataFrame(summary), pd.DataFrame(paired)


def limits(values):
    valid = values[np.isfinite(values)]
    low, high = np.quantile(valid, [.025, .975]) if len(valid) else (np.nan, np.nan)
    return dict(low95=low, high95=high, valid_draws=len(valid))


def run(data, output):
    path, = data.glob("Data01*.csv")
    folds, thresholds = held_out(pd.read_csv(path))
    summary, paired = summarize(folds)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in (("folds", folds), ("thresholds", thresholds), ("summary", summary), ("paired", paired)):
        table.to_csv(output / f"q1_candidate_sets_{name}.csv", index=False, lineterminator="\n")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", default=Path("results"), type=Path)
    args = parser.parse_args()
    run(args.data, args.output)
