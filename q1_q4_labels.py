"""Propagate held-out call labels into the archived gross effectiveness curves."""
import numpy as np
import pandas as pd

from q1 import CALLS


RULES = ("truth", "logistic", "full_prior", "xgboost")
KEYS = ["row", "fold", "recording_group", "actual"]


def load_labels(archive):
    site = pd.read_csv(archive / "q1_location_predictions.csv")
    prior = pd.read_csv(archive / "q1_class_prior_predictions.csv")
    merged = site.merge(prior[KEYS + ["logistic", "full_prior"]], on=KEYS, validate="one_to_one")
    pd.testing.assert_series_equal(merged.logistic, merged.logistic_original, check_names=False)
    if len(merged) != 108:
        raise ValueError("Expected 108 matched holdout predictions")
    labels = merged.loc[merged.location.eq("FalseBay")].copy()
    if len(labels) != 105 or labels.recording_group.nunique() != 15:
        raise ValueError("Expected 105 recordings from 15 FalseBay dates")
    return labels.assign(truth=labels.actual, xgboost=labels.xgboost_original)


def load_scores(archive):
    curves = pd.read_csv(archive / "q4_comparison_curves.csv")
    common = curves[curves.threshold_policy.eq("common")]
    early = common.loc[common.response_link.eq("clean") & common.distance_m.eq(20)]
    cutoff = early["index"].mean() / 2
    selected = common.loc[
        common.distance_m.isin((50, 100, 150))
        & (common.response_link.eq("clean") | (common.response_link.eq("coupled") & common.loss.eq(.2)))
    ]
    keys = ["response_link", "loss", "distance_m", "call"]
    fields = ["index", "clean_cutoff", "meets_cutoff"]
    figure = pd.read_csv(archive / "q4_loss_comparison.csv").set_index(keys)
    scores = selected.set_index(keys)[fields].sort_index()
    pd.testing.assert_frame_equal(scores, figure.loc[scores.index, fields])
    np.testing.assert_allclose(scores.clean_cutoff, cutoff, rtol=0, atol=1e-15)
    np.testing.assert_array_equal(scores["index"] >= scores.clean_cutoff, scores.meets_cutoff)
    if len(scores) != 18:
        raise ValueError("Expected 18 archived call-by-scenario scores")
    return scores


def confusion(labels):
    calls = list(CALLS)
    group_counts = []
    for _, group in labels.groupby("recording_group", sort=True):
        group_counts.append([
            pd.crosstab(group.actual, group[rule]).reindex(index=calls, columns=calls, fill_value=0)
            .to_numpy()
            for rule in RULES
        ])
    group_counts = np.asarray(group_counts)
    counts = group_counts.sum(axis=0)
    rng = np.random.default_rng(20261126)
    selections = rng.integers(len(group_counts), size=(300, len(group_counts)))
    draws = group_counts[selections].sum(axis=1)
    draws = draws[(draws[:, 0].sum(axis=-1) > 0).all(axis=1)]
    return counts, draws / draws.sum(axis=-1, keepdims=True)


def run(archive, output):
    counts, sampled = confusion(load_labels(archive))
    scores = load_scores(archive)
    totals = counts.sum(axis=-1, keepdims=True)
    ratios = counts / totals
    confusion_rows = [
        {"rule": rule, "true_call": true, "assigned_call": label, "count": counts[i, j, k],
         "true_count": totals[i, j, 0], "proportion": ratios[i, j, k]}
        for i, rule in enumerate(RULES)
        for j, true in enumerate(CALLS)
        for k, label in enumerate(CALLS)
    ]
    results = []
    for (scenario, loss, distance), setting in scores.groupby(level=[0, 1, 2], sort=False):
        setting = setting.droplevel([0, 1, 2]).reindex(CALLS)
        values = setting["index"].to_numpy()
        passes = setting.meets_cutoff.to_numpy()
        for j, true in enumerate(CALLS):
            effects = np.column_stack((
                values - values[j],
                passes & ~passes[j],
                ~passes & passes[j],
            ))
            point = ratios[:, j] @ effects
            low, high = np.quantile(sampled[:, :, j] @ effects, [.025, .975], axis=0)
            np.testing.assert_array_equal(np.vstack((point[0], low[0], high[0])), 0)
            for i, rule in enumerate(RULES):
                record = {
                    "scenario": scenario, "loss": loss, "distance_m": distance, "true_call": true,
                    "rule": rule, "true_count": totals[i, j, 0], "cutoff": setting.clean_cutoff.iloc[j],
                    "true_score": values[j], "true_pass": passes[j],
                    "mean_assigned_score": values[j] + point[i, 0], "bootstrap_draws": len(sampled),
                }
                for k, metric in enumerate(("score_bias", "false_pass", "missed_pass")):
                    record.update({metric: point[i, k], f"{metric}_low": low[i, k],
                                   f"{metric}_high": high[i, k]})
                results.append(record)
    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(confusion_rows).to_csv(output / "q1_q4_label_confusion.csv", index=False,
                                        lineterminator="\n")
    pd.DataFrame(results).to_csv(output / "q1_q4_label_monitoring.csv", index=False,
                                 lineterminator="\n")
