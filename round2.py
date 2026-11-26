"""Second-round ablations on the frozen recording and experiment folds."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

import q1
import q2
import q3


def interval(values):
    return np.quantile(values, [.025, .975], axis=0)


def q1_boost(data, output, seed, n_boot):
    oof = pd.read_csv(output / "q1_oof_predictions.csv")
    frame = pd.read_csv(next(data.glob("Data01*.csv")))
    values = frame.loc[:, q1.FEATURES].to_numpy()
    labels = pd.Categorical(frame.CallType, categories=q1.CALLS).codes
    predicted = np.empty_like(labels)
    folds = oof.fold.to_numpy()
    for fold in np.unique(folds):
        test = folds == fold
        model = XGBClassifier(
            n_estimators=100, max_depth=2, learning_rate=.05, min_child_weight=3,
            reg_lambda=1, reg_alpha=0, subsample=1, colsample_bytree=1,
            tree_method="hist", device="cpu", objective="multi:softprob",
            n_jobs=1, random_state=seed,
        )
        model.fit(values[~test], labels[~test])
        predicted[test] = model.predict(values[test])
    oof["xgboost"] = np.asarray(q1.CALLS)[predicted]
    oof[["row", "fold", "recording_group", "actual", "shared_features", "random_forest", "xgboost"]].to_csv(
        output / "round2_q1_predictions.csv", index=False,
    )

    group = oof.recording_group.to_numpy()
    group_rows = [np.flatnonzero(group == value) for value in np.unique(group)]
    rng = np.random.default_rng(seed)
    samples = []
    for indices in rng.integers(len(group_rows), size=(n_boot, len(group_rows))):
        rows = np.concatenate([group_rows[i] for i in indices])
        if np.unique(labels[rows]).size == len(q1.CALLS):
            samples.append(rows)

    actual = oof.actual.to_numpy()
    names = ("shared_features", "random_forest", "xgboost")
    point, draws = {}, {}
    for name in names:
        prediction = oof[name].to_numpy()
        point[name] = q1.comparison_scores(actual, prediction)[[0, 3]]
        draws[name] = np.array([
            q1.comparison_scores(actual[rows], prediction[rows])[[0, 3]] for rows in samples
        ])
    records = []
    for candidate, baseline in (("xgboost", "shared_features"), ("xgboost", "random_forest")):
        difference = point[candidate] - point[baseline]
        delta_low, delta_high = interval(draws[candidate] - draws[baseline])
        baseline_low, baseline_high = interval(draws[baseline])
        candidate_low, candidate_high = interval(draws[candidate])
        for i, metric in enumerate(("macro_f1", "two_voice_recall")):
            records.append({
                "candidate": candidate, "baseline": baseline, "metric": metric,
                "baseline_score": point[baseline][i], "baseline_low": baseline_low[i],
                "baseline_high": baseline_high[i], "candidate_score": point[candidate][i],
                "candidate_low": candidate_low[i], "candidate_high": candidate_high[i],
                "difference": difference[i], "difference_low": delta_low[i], "difference_high": delta_high[i],
                "draws": len(samples),
            })
    comparison = pd.DataFrame(records)
    comparison["adopt_xgboost"] = bool(
        comparison.loc[comparison.metric.eq("macro_f1"), "difference_low"].gt(0).all()
        and comparison.loc[comparison.metric.eq("two_voice_recall"), "difference"].ge(0).all()
    )
    comparison.to_csv(output / "round2_q1_comparison.csv", index=False)


def q2_omissions(propagation, output):
    records = []
    for call, (means, mean_draws) in propagation["metric_means_and_draws"].items():
        weights = {"none": q2.WEIGHTS["equal"]}
        for i, metric in enumerate(q2.METRICS):
            weights[metric] = [.5 if j != i else 0 for j in range(len(q2.METRICS))]
        knots = {name: q2.fit_knots(means, weight) for name, weight in weights.items()}
        boot = {name: [q2.fit_knots(draw, weight) for draw in mean_draws] for name, weight in weights.items()}
        for threshold in q2.THRESHOLDS:
            baseline, baseline_status = q2.radius(knots["none"], threshold)
            baseline_draws = np.array([q2.radius(k, threshold)[0] for k in boot["none"]])
            for name, values in knots.items():
                estimate, status = q2.radius(values, threshold)
                estimates, statuses = zip(*(q2.radius(k, threshold) for k in boot[name]))
                low, high = interval(estimates)
                delta_low, delta_high = interval(np.asarray(estimates) - baseline_draws)
                records.append({
                    "call": call, "omitted": name, "threshold": threshold,
                    "baseline_m": baseline, "baseline_status": baseline_status,
                    "radius_m": estimate, "status": status, "bounded_low_m": low, "bounded_high_m": high,
                    "bounded_difference_m": estimate - baseline, "difference_low_m": delta_low,
                    "difference_high_m": delta_high, "draws_below_support": statuses.count("below_support"),
                    "draws_above_support": statuses.count("above_support"),
                })
    radii = pd.DataFrame(records)
    radii["point_rank"] = radii.groupby(["omitted", "threshold"]).radius_m.rank(
        method="min", ascending=False,
    ).astype(int)
    radii.to_csv(output / "round2_q2_radii.csv", index=False)


def playback_matrices(frame):
    contexts = tuple(sorted(frame.loc[frame.Type.eq("call"), "Context"].unique()))
    x = q3.features(frame, contexts)
    # Match the original stimulus, call, interaction, context, distance and group columns.
    columns = {
        "stimulus_logistic": [0],
        "add_distance": [0, x.shape[1] - 2],
        "add_call": [0, 1, 2, 3, 4, x.shape[1] - 2],
    }
    return {name: x[:, indices] for name, indices in columns.items()} | {"add_context_group": x}


def mask_scores(probabilities, y):
    return np.column_stack((
        -np.log(probabilities[np.arange(len(y)), y].clip(1e-12)),
        (1 - probabilities[:, 0] - (y != 0)) ** 2,
    ))


def report_playback_scores(scores, metrics, output, question, seed, n_boot):
    """Compute fold means and jointly resample held-out experiments within folds."""
    names = scores.columns.get_level_values("model").unique().tolist()
    observed = scores.groupby(level="fold").mean()
    observed.stack(level="model", future_stack=True).reset_index().to_csv(
        output / f"round2_{question}_fold_scores.csv", index=False,
    )
    point = observed.mean()
    rng = np.random.default_rng(seed)
    boot = []
    for _, fold in scores.groupby(level="fold", sort=True):
        groups = [block.to_numpy().sum(axis=0) for _, block in fold.groupby(level="pair")]
        counts = fold.groupby(level="pair").size().to_numpy()
        indices = rng.integers(len(groups), size=(n_boot, len(groups)))
        boot.append(np.asarray(groups)[indices].sum(axis=1) / counts[indices].sum(axis=1)[:, None])
    draw_frame = pd.DataFrame(np.mean(boot, axis=0), columns=scores.columns)
    records = []
    for candidate, baseline in zip(names[1:], names):
        until = len(records)
        for metric in metrics:
            left, right = (metric, baseline), (metric, candidate)
            low, high = interval(draw_frame[right] - draw_frame[left])
            records.append({
                "baseline": baseline, "candidate": candidate, "metric": metric,
                "baseline_score": point[left], "candidate_score": point[right],
                "difference": point[right] - point[left], "difference_low": low, "difference_high": high,
            })
        supported = all(row["difference_high"] < 0 for row in records[until:])
        for row in records[until:]:
            row["joint_gain"] = supported
    pd.DataFrame(records).to_csv(output / f"round2_{question}_comparison.csv", index=False)


def q3_blocks(frame, matrices, folds, output, seed, n_boot):
    y = frame["mask"].to_numpy()
    stimuli = frame.Type.to_numpy()
    metrics = ("mask_log_loss", "any_response_brier")
    names = ["stimulus_frequency", *matrices]
    row_scores = np.empty((len(frame), len(metrics), len(names)))
    for train, test in folds:
        frequencies = np.empty((len(test), len(q3.MASKS)))
        for stimulus in q3.STIMULI:
            training_masks = y[train[stimuli[train] == stimulus]]
            frequencies[stimuli[test] == stimulus] = (
                np.bincount(training_masks, minlength=len(q3.MASKS)) / len(training_masks)
            )
        row_scores[test, :, 0] = mask_scores(frequencies, y[test])
        for i, matrix in enumerate(matrices.values(), 1):
            row_scores[test, :, i] = mask_scores(q3.fit_masks(matrix[train], y[train], matrix[test]), y[test])
    scores = score_frame(frame, folds, row_scores, metrics, names)
    report_playback_scores(scores, metrics, output, "q3", seed, n_boot)


def score_frame(frame, folds, scores, metrics, names, supported=None):
    fold_ids = np.zeros(len(frame), dtype=int)
    for fold, (_, test) in enumerate(folds, 1):
        fold_ids[test] = fold
    pairs = pd.factorize(frame.expID, sort=True)[0]
    index = pd.MultiIndex.from_arrays([fold_ids, pairs], names=["fold", "pair"])
    columns = pd.MultiIndex.from_product([metrics, names], names=["metric", "model"])
    result = pd.DataFrame(scores.reshape(len(frame), -1), index=index, columns=columns)
    return result if supported is None else result.loc[supported]


def q4_fidelity(frame, distance_model, folds, propagation, output, seed, n_boot):
    distances = frame.Distance.to_numpy()
    supported = (distances >= 20) & (distances <= 150)
    fidelity = np.zeros(len(frame))
    # Evaluate the fitted propagation knots at the true distances on the log scale.
    for call, (means, _) in propagation["metric_means_and_draws"].items():
        part = supported & frame.assigned_call.eq(call).to_numpy()
        fidelity[part] = q2.interpolated(distances[part], q2.fit_knots(means, q2.WEIGHTS["equal"]))
    y = frame["mask"].ne(0).to_numpy()
    natural = frame.Type.eq("call").to_numpy()
    augmented = np.column_stack([distance_model, fidelity, fidelity * natural])
    metrics = ("binary_log_loss", "any_response_brier")
    names = ("distance_behavior", "add_fidelity")
    row_scores = np.full((len(frame), len(metrics), len(names)), np.nan)
    coverage = []
    for fold, (train, test) in enumerate(folds, 1):
        train = train[supported[train]]
        test = test[supported[test]]
        test_pairs = frame.iloc[test].expID
        coverage.append({
            "fold": fold, "test_rows": len(test), "test_pairs": test_pairs.nunique(),
            "complete_test_pairs": int(test_pairs.value_counts().eq(2).sum()),
            "test_natural_rows": int(natural[test].sum()), "test_responses": int(y[test].sum()),
        })
        for i, matrix in enumerate((distance_model, augmented)):
            model = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000))
            model.fit(matrix[train], y[train])
            p = model.predict_proba(matrix[test])[:, 1]
            row_scores[test, :, i] = np.column_stack((
                -np.log(np.where(y[test], p, 1 - p).clip(1e-12)),
                (p - y[test]) ** 2,
            ))
    scores = score_frame(frame, folds, row_scores, metrics, names, supported)
    report_playback_scores(scores, metrics, output, "q4", seed, n_boot)
    pd.DataFrame(coverage).to_csv(output / "round2_q4_coverage.csv", index=False)
    log_distance = np.log1p(distances)
    call_columns = pd.get_dummies(frame.assigned_call).loc[:, list(q2.CALLS[1:])]
    design = np.column_stack([log_distance, call_columns])
    diagnostics = []
    for label in ("all", *q2.CALLS):
        selected = supported if label == "all" else supported & frame.assigned_call.eq(label).to_numpy()
        diagnostic_design = design[selected] if label == "all" else design[selected, :1]
        target = fidelity[selected]
        diagnostics.append({
            "call": label, "rows": int(selected.sum()),
            "pearson_with_log_distance": np.corrcoef(log_distance[selected], target)[0, 1],
            "linear_r_squared": LinearRegression().fit(diagnostic_design, target).score(diagnostic_design, target),
        })
    pd.DataFrame(diagnostics).to_csv(output / "round2_q4_collinearity.csv", index=False)


def run(data, output, seed, n_boot, propagation):
    q1_boost(data, output, seed, n_boot)
    q2_omissions(propagation, output)
    frame = q3.load_playbacks(data)
    matrices = playback_matrices(frame)
    folds = list(GroupKFold(5).split(frame, groups=frame.expID))
    q3_blocks(frame, matrices, folds, output, seed + 2, n_boot)
    q4_fidelity(frame, matrices["add_context_group"], folds, propagation, output, seed + 3, n_boot)
