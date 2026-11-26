"""Frozen acoustic feature and recorded onset comparisons."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import q1
import q3


def acoustic(data, output, seed, n_boot):
    frame = pd.read_csv(next(data.glob("Data01*.csv")))
    raw = frame[list(q1.FEATURES)].to_numpy()
    duration, fundamental, peak, low, middle, high = raw.T
    if not np.all(raw > 0) or not np.all(high > low):
        raise ValueError("Acoustic features must be positive with positive spectral IQR.")
    designs = {
        "original": raw, "all_log": np.log(raw),
        "ratios_skew": np.column_stack([np.log(duration), np.log(fundamental),
            np.log(peak / fundamental), np.log(middle / fundamental), np.log(high / low),
            (high + low - 2 * middle) / (high - low)]),
    }
    y = frame.CallType.to_numpy()
    labels = frame.Date.astype(str) + " | " + frame.Location.astype(str)
    _, groups = np.unique(labels, return_inverse=True)
    predictions = {}
    for name, design in designs.items():
        pred = np.empty_like(y)
        for group_ids in q1.FROZEN_TEST_GROUPS:
            test = np.isin(groups, group_ids)
            clf = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000))
            pred[test] = clf.fit(design[~test], y[~test]).predict(design[test])
        predictions[name] = pred
    rows = [np.flatnonzero(groups == k) for k in np.unique(groups)]
    sampled = [np.concatenate([rows[i] for i in draw]) for draw in
               np.random.default_rng(seed).integers(len(rows), size=(n_boot, len(rows)))]
    sampled = [idx for idx in sampled if len(np.unique(y[idx])) == 3]
    point = {k: q1.comparison_scores(y, p)[[0, 3]] for k, p in predictions.items()}
    baseline = np.array([q1.comparison_scores(y[i], predictions["original"][i])[[0, 3]] for i in sampled])
    selected = max(("all_log", "ratios_skew"), key=lambda name: point[name][0])
    records = []
    for name, p in predictions.items():
        draw = np.array([q1.comparison_scores(y[i], p[i])[[0, 3]] for i in sampled])
        low, high = np.quantile(draw - baseline, [.025, .975], axis=0)
        delta = point[name] - point["original"]
        for j, metric in enumerate(("macro_f1", "two_voice_recall")):
            records.append({
                "model": name, "metric": metric, "score": point[name][j], "baseline": point["original"][j],
                "difference": delta[j], "difference_low": low[j], "difference_high": high[j],
                "selected_alternative": name == selected,
                "adopt_alternative": name == selected and low[0] > 0 and delta[1] >= 0,
                "draws": len(sampled),
            })
    pd.DataFrame(records).to_csv(output / "onset_q1_acoustic.csv", index=False)
    pd.DataFrame({"actual": y, "recording_group": groups, **predictions}).to_csv(
        output / "onset_q1_predictions.csv", index=False,
    )


def conditional_latency(frame, x, folds, output):
    records = []
    for behavior in q3.BEHAVIORS:
        valid = frame[behavior + "YesNo"].eq(1).to_numpy()
        y = frame[behavior + "Latency"].to_numpy()
        for scheme, splits in folds.items():
            predictions = np.full((len(y), 2), np.nan)
            for train, test in splits:
                train, test = train[valid[train]], test[valid[test]]
                if not len(train) or not len(test):
                    continue
                model = make_pipeline(StandardScaler(), Ridge(alpha=5))
                model.fit(x[train], np.log1p(y[train]))
                predictions[test, 0] = np.median(y[train])
                predictions[test, 1] = np.maximum(0, np.expm1(model.predict(x[test])))
            for stimulus in ("all", *q3.STIMULI):
                selected = valid if stimulus == "all" else valid & frame.Type.eq(stimulus).to_numpy()
                scored = selected & np.isfinite(predictions[:, 0])
                mae = np.abs(predictions[scored] - y[scored, None]).mean(axis=0) if scored.any() else [np.nan] * 2
                records.append({
                    "scheme": scheme, "behavior": behavior, "stimulus": stimulus,
                    "observed": selected.sum(), "scored": scored.sum(),
                    "median_mae_s": mae[0], "ridge_mae_s": mae[1], "ridge_minus_median_s": mae[1] - mae[0],
                })
    pd.DataFrame(records).to_csv(output / "onset_q3_latency.csv", index=False)


def fit_timing(x, y, evaluation):
    model = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000)).fit(x, y)
    p = np.zeros((len(evaluation), 4))
    p[:, model.classes_] = model.predict_proba(evaluation)
    return p


def timing(frame, x, contexts, weights, folds, sampled_dates, output):
    onset = []
    for behavior in q3.BEHAVIORS:
        observed = frame[behavior + "YesNo"].eq(1).to_numpy()
        values = frame[behavior + "Latency"].to_numpy()
        if not np.all(np.isfinite(values[observed]) & (values[observed] >= 0)):
            raise ValueError("Observed behavior requires a nonnegative recorded onset.")
        onset.append(np.where(observed, values, np.inf))
    earliest = np.min(onset, axis=0)
    y = np.searchsorted([5, 15, np.finfo(float).max], earliest, side="left")
    labels = frame.Type.to_numpy()
    scores = []
    for scheme, splits in folds.items():
        empirical = np.empty((len(y), 4))
        full = np.empty_like(empirical)
        for train, test in splits:
            for stimulus in q3.STIMULI:
                train_y = y[train[labels[train] == stimulus]]
                empirical[test[labels[test] == stimulus]] = (np.bincount(train_y, minlength=4) + .5) / (len(train_y) + 2)
            full[test] = fit_timing(x[train], y[train], x[test])
        for name, p in (("smoothed_stimulus", empirical), ("multinomial", full)):
            scores.append({
                "scheme": scheme, "model": name, "folds": len(splits), "trials": len(y),
                "log_loss": -np.log(p[np.arange(len(y)), y].clip(1e-12)).mean(),
                "multiclass_brier": ((p - np.eye(4)[y])**2).sum(axis=1).mean(),
            })
    pd.DataFrame(scores).to_csv(output / "onset_q3_timing_scores.csv", index=False)

    grid = q3.probability_grid(np.asarray(q3.REPRESENTATIVE), contexts, 8)
    evaluation = q3.features(grid, contexts)
    shape = (len(q3.STIMULI) * len(q3.CALLS) * len(q3.REPRESENTATIVE), len(contexts), 4)

    def standardized(rows):
        p = fit_timing(x[rows], y[rows], evaluation).reshape(shape)
        return np.einsum("gck,c->gk", p, weights).cumsum(axis=1)[:, :3]

    groups = [np.flatnonzero(frame.Date.eq(date)) for date in sorted(frame.Date.unique())]
    point = standardized(np.arange(len(y)))
    draws = np.array([standardized(np.concatenate([groups[i] for i in draw])) for draw in sampled_dates])
    low, high = np.quantile(draws, [.025, .975], axis=0)
    records = []
    for i, row in enumerate(grid.drop_duplicates(["Type", "assigned_call", "Distance"]).itertuples()):
        local = (frame.Type.eq(row.Type) & frame.assigned_call.eq(row.assigned_call)
                 & frame.Distance.sub(row.Distance).abs().le(25))
        for j, label in enumerate(("by_5_s", "by_15_s", "any_recorded")):
            records.append({
                "stimulus": row.Type, "call": row.assigned_call, "distance_m": row.Distance,
                "outcome": label, "probability": point[i, j], "date_low": low[i, j], "date_high": high[i, j],
                "local_trials": local.sum(), "local_recorded_onsets": np.count_nonzero(local & (y < 3)),
            })
    pd.DataFrame(records).to_csv(output / "onset_q3_cumulative.csv", index=False)


def run(data, frame, sampled_dates, output, seed, n_boot):
    acoustic(data, output, seed, n_boot)
    counts = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    contexts = tuple(counts.index)
    x = q3.features(frame, contexts)
    folds = {
        "expID": list(GroupKFold(5).split(x, groups=frame.expID)),
        "date": list(LeaveOneGroupOut().split(x, groups=frame.Date)),
    }
    conditional_latency(frame, x, folds, output)
    timing(frame, x, contexts, counts.to_numpy(), folds, sampled_dates, output)
