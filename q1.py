"""Q1: summarize acoustic features and validate call-type classification by recording group."""
import json
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.multitest import multipletests


CALLS = ("flat", "mod", "tv")
FEATURES = ("Duration", "F01", "Fpeak", "Q25", "Q50", "Q75")
LABELS = ("Flat", "Modulated", "Two-voice")
FEATURE_LABELS = ("Duration", "Fundamental", "Peak", "Q25", "Q50", "Q75")


def macro_f1(actual, predicted):
    return f1_score(actual, predicted, labels=CALLS, average="macro", zero_division=0)


def describe(frame, output):
    records = []
    tests = []
    for feature in (*FEATURES, "PulseRate", "F02"):
        samples = {call: frame.loc[frame.CallType == call, feature].dropna() for call in CALLS}
        for call, sample in samples.items():
            quantiles = sample.quantile([.25, .5, .75]).to_numpy()
            total = int((frame.CallType == call).sum())
            records.append({
                "feature": feature, "call": call, "n": len(sample), "missing": total - len(sample),
                "mean": sample.mean(), "sd": sample.std(), "q25": quantiles[0],
                "median": quantiles[1], "q75": quantiles[2],
            })
        if feature == "F02":
            continue
        if all(len(sample) for sample in samples.values()):
            statistic, p_value = kruskal(*samples.values())
            tests.append({
                "feature": feature, "test": "Kruskal-Wallis", "left": "all", "right": "",
                "n_left": sum(map(len, samples.values())), "n_right": np.nan,
                "statistic": statistic, "p_value": p_value, "rank_biserial": np.nan,
            })
        for left, right in combinations(CALLS, 2):
            a, b = samples[left], samples[right]
            if a.empty or b.empty:
                continue
            statistic, p_value = mannwhitneyu(a, b, alternative="two-sided", method="asymptotic")
            tests.append({
                "feature": feature, "test": "Mann-Whitney U", "left": left, "right": right,
                "n_left": len(a), "n_right": len(b), "statistic": statistic,
                "p_value": p_value, "rank_biserial": 2 * statistic / (len(a) * len(b)) - 1,
            })
    summary = pd.DataFrame(records)
    summary.to_csv(output / "q1_feature_summary.csv", index=False)
    tests = pd.DataFrame(tests)
    for _, indices in tests.groupby("test").groups.items():
        tests.loc[indices, "p_holm"] = multipletests(tests.loc[indices, "p_value"], method="holm")[1]
    tests.to_csv(output / "q1_rank_tests.csv", index=False)
    return summary


def validate(frame, output, seed, n_boot):
    target = frame.CallType.to_numpy()
    groups = (frame.Date.astype(str) + " | " + frame.Location.astype(str)).to_numpy()
    values = frame.loc[:, FEATURES].to_numpy()
    pulse_values = frame.loc[:, (*FEATURES, "PulseRate")].to_numpy()
    f02_present = frame.F02.notna().to_numpy()
    predicted = np.empty_like(target)
    missingness = np.empty_like(target)
    with_pulse = np.empty_like(target)
    majority = np.empty_like(target)
    split_id = np.zeros(len(frame), dtype=int)
    rng = np.random.default_rng(seed)
    repeats = 40
    perturbed = np.empty((len(FEATURES), repeats, len(frame)), dtype=target.dtype)
    split = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
    for fold, (train, test) in enumerate(split.split(values, target, groups), start=1):
        if set(groups[train]) & set(groups[test]):
            raise ValueError("Recording groups overlap between training and validation")
        estimator = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        estimator.fit(values[train], target[train])
        predicted[test] = estimator.predict(values[test])
        pulse_estimator = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                                        LogisticRegression(max_iter=1000))
        pulse_estimator.fit(pulse_values[train], target[train])
        with_pulse[test] = pulse_estimator.predict(pulse_values[test])
        common_class = pd.Series(target[train]).value_counts().idxmax()
        majority[test] = common_class
        missingness[test] = common_class
        for present in (False, True):
            matching_train = train[f02_present[train] == present]
            if len(matching_train):
                matching_test = test[f02_present[test] == present]
                missingness[matching_test] = pd.Series(target[matching_train]).value_counts().idxmax()
        split_id[test] = fold
        for j in range(len(FEATURES)):
            permutation = values[test].copy()
            for replicate in range(repeats):
                permutation[:, j] = rng.permutation(values[test, j])
                perturbed[j, replicate, test] = estimator.predict(permutation)

    pd.DataFrame({
        "row": np.arange(1, len(frame) + 1), "fold": split_id, "actual": target,
        "shared_features": predicted, "with_imputed_pulse": with_pulse,
        "f02_availability": missingness, "majority": majority,
    }).to_csv(output / "q1_oof_predictions.csv", index=False)
    fold_counts = pd.crosstab(split_id, target).reindex(columns=CALLS, fill_value=0)
    fold_counts["recording_groups"] = pd.Series(groups).groupby(split_id).nunique()
    fold_counts.rename_axis("fold").to_csv(output / "q1_fold_counts.csv")

    unique_groups = np.unique(groups)
    group_rows = [np.flatnonzero(groups == group) for group in unique_groups]
    draws = [
        np.concatenate([group_rows[i] for i in rng.integers(len(group_rows), size=len(group_rows))])
        for _ in range(n_boot)
    ]
    metrics = []
    for name, predictions in (
        ("shared_features", predicted), ("with_imputed_pulse", with_pulse),
        ("f02_availability", missingness), ("majority", majority),
    ):
        scores = [macro_f1(target[rows], predictions[rows]) for rows in draws if len(set(target[rows])) == 3]
        low, high = np.quantile(scores, [.025, .975]) if scores else (np.nan, np.nan)
        metrics.append({
            "model": name, "macro_f1": macro_f1(target, predictions),
            "group_bootstrap_low": low, "group_bootstrap_high": high,
            "draws_with_all_classes": len(scores), "n_recordings": len(frame),
            "n_groups": len(unique_groups),
        })
    pd.DataFrame(metrics).to_csv(output / "q1_metrics.csv", index=False)

    baseline_score = macro_f1(target, predicted)
    importance = []
    for feature, repetitions in zip(FEATURES, perturbed):
        losses = [baseline_score - macro_f1(target, predictions) for predictions in repetitions]
        importance.append({"feature": feature, "macro_f1_loss": np.mean(losses), "shuffle_sd": np.std(losses, ddof=1)})
    importance = pd.DataFrame(importance)
    importance.to_csv(output / "q1_feature_importance.csv", index=False)

    matrix = confusion_matrix(target, predicted, labels=CALLS)
    pd.DataFrame(matrix, index=CALLS, columns=CALLS).rename_axis("actual").to_csv(output / "q1_confusion.csv")
    return matrix, importance


def plot_summary(summary, matrix, importance, output):
    figure, axes = plt.subplots(1, 3, figsize=(12.2, 4.0), layout="constrained",
                                gridspec_kw={"width_ratios": (1.35, 1, 1.05)})
    colors = ("#217675", "#be6131", "#64509a")
    positions = np.arange(len(FEATURES))
    plot_rows = []
    summary_features = (*FEATURES, "F02", "PulseRate")
    summary_labels = (*FEATURE_LABELS, "Second fund.", "Pulse rate")
    for j, feature in enumerate(summary_features):
        rows = summary.loc[summary.feature == feature].set_index("call").loc[list(CALLS)]
        origin = rows["q25"].min()
        scale = rows["q75"].max() - origin
        for k, call in enumerate(CALLS):
            row = rows.loc[call]
            if row["n"] == 0:
                continue
            low, median, high = (row[["q25", "median", "q75"]].to_numpy(float) - origin) / scale
            axes[0].errorbar(median, j + .2 * (k - 1), xerr=[[median - low], [high - median]],
                             fmt="o", color=colors[k], markersize=3, capsize=2,
                             label=LABELS[k] if j == 0 else None)
            plot_rows.append({
                "panel": "feature_distributions", "feature": feature, "call": call, "value": median,
                "low": low, "high": high, "scale_origin": origin, "scale_width": scale,
            })
    axes[0].set(yticks=np.arange(len(summary_features)), yticklabels=summary_labels,
                xlabel="Scaled quartiles and median",
                title="A  Acoustic feature distributions")
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower center", bbox_to_anchor=(.5, -0.28), ncol=3, fontsize=7, frameon=False)

    axes[1].imshow(matrix, cmap="BuGn", vmin=0)
    axes[1].set(xticks=np.arange(3), xticklabels=LABELS, yticks=np.arange(3), yticklabels=LABELS,
                ylabel="Recorded class", xlabel="Predicted class", title="B  Grouped validation")
    axes[1].tick_params(axis="x", labelrotation=22)
    for i, actual in enumerate(CALLS):
        for j, predicted in enumerate(CALLS):
            count = int(matrix[i, j])
            axes[1].text(j, i, count, ha="center", va="center",
                         color="white" if count >= matrix.max() * .66 else "#173232")
            plot_rows.append({"panel": "confusion", "call": actual, "predicted": predicted, "value": count})

    axes[2].barh(positions, importance["macro_f1_loss"], xerr=importance["shuffle_sd"],
                 color="#546b89", capsize=2)
    axes[2].set(yticks=positions, yticklabels=FEATURE_LABELS, xlabel="Macro-F1 decrease",
                title="C  Permutation importance")
    axes[2].invert_yaxis()
    axes[2].axvline(0, color="#35404b", linewidth=.8)
    for row in importance.itertuples():
        plot_rows.append({"panel": "importance", "feature": row.feature, "value": row.macro_f1_loss,
                          "shuffle_sd": row.shuffle_sd})
    for axis in axes:
        axis.spines[["top", "right"]].set_visible(False)
    figure.savefig(output / "q1_acoustics.png", dpi=300)
    plt.close(figure)
    pd.DataFrame(plot_rows).to_csv(output / "q1_acoustics.csv", index=False)
    (output / "q1_acoustics.meta.json").write_text(json.dumps({
        "source": "Data01",
        "caption": "Acoustic feature summaries and five-fold grouped validation of call type.",
        "feature_summary": "Medians and quartiles use a common per-feature scale across call types with observed values.",
        "permutation_importance": "Mean and standard deviation across 40 shuffles within each held-out fold.",
        "groups": "Recording date and location.",
        "pulse_rate": "Unavailable for flat calls. Restricted to a secondary classifier with fold-local median imputation, and an observed modulated versus two-voice comparison.",
        "metric_intervals": "Percentile bootstrap over recording groups of fixed out-of-fold predictions.",
        "rank_tests": "Sample-level descriptive inference. Recordings within a date and location may be dependent.",
    }, indent=2) + "\n", encoding="utf-8")


def run(data, output, seed, n_boot):
    path, = data.glob("Data01*.csv")
    frame = pd.read_csv(path)
    if set(frame.CallType) != set(CALLS) or frame.loc[:, FEATURES].isna().any().any():
        raise ValueError("Expected all three calls and complete common acoustic features")
    summary = describe(frame, output)
    matrix, importance = validate(frame, output, seed, n_boot)
    plot_summary(summary, matrix, importance, output)

