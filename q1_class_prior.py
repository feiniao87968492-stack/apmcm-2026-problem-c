"""Compare Q1 decision priors on the original grouped holdouts."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_score
from sklearn.preprocessing import StandardScaler

from q1 import CALLS, FEATURES, FROZEN_TEST_GROUPS, comparison_scores, macro_f1


BASELINE = "logistic"
PRIMARY = "full_prior"
N_BOOT = 300
SEED = 20261126


def predict(frame):
    actual = frame.CallType.to_numpy()
    groups = frame.Date.astype(str) + " | " + frame.Location.astype(str)
    unique_groups, group_ids = np.unique(groups, return_inverse=True)
    if len(unique_groups) != sum(map(len, FROZEN_TEST_GROUPS)):
        raise ValueError("Expected the 16 frozen Q1 recording groups")
    features = frame.loc[:, FEATURES].to_numpy()
    classes = np.array(sorted(CALLS))
    probabilities = np.empty((len(frame), len(classes)))
    proportions = np.empty_like(probabilities)
    fold_ids = np.zeros(len(frame), dtype=int)
    predictions = {rule: np.empty_like(actual) for rule in
                   (BASELINE, "half_prior", PRIMARY, "weighted_logistic")}

    for fold, test_groups in enumerate(FROZEN_TEST_GROUPS, start=1):
        test = np.isin(group_ids, test_groups)
        train = ~test
        scaler = StandardScaler().fit(features[train])
        x_train, x_test = scaler.transform(features[train]), scaler.transform(features[test])
        y_train = actual[train]
        prior = np.array([(y_train == call).mean() for call in classes])
        base = LogisticRegression(C=1, max_iter=1000).fit(x_train, y_train)
        weighted = LogisticRegression(C=1, max_iter=1000).fit(
            x_train, y_train, sample_weight=1 / (len(classes) * prior[np.searchsorted(classes, y_train)]),
        )
        p = base.predict_proba(x_test)
        fold_ids[test] = fold
        probabilities[test] = p
        proportions[test] = prior
        predictions[BASELINE][test] = base.predict(x_test)
        predictions["half_prior"][test] = classes[(p / np.sqrt(prior)).argmax(axis=1)]
        predictions[PRIMARY][test] = classes[(p / prior).argmax(axis=1)]
        predictions["weighted_logistic"][test] = weighted.predict(x_test)

    out = pd.DataFrame({"row": np.arange(1, len(frame) + 1), "fold": fold_ids,
                        "recording_group": group_ids, "actual": actual, **predictions})
    for i, call in enumerate(classes):
        out[f"train_prior_{call}"] = proportions[:, i]
        out[f"base_probability_{call}"] = probabilities[:, i]
    return out


def summarize(oof):
    actual = oof.actual.to_numpy()
    two_voice = actual == "tv"
    group_ids = oof.recording_group.to_numpy()
    group_rows = [np.flatnonzero(group_ids == group) for group in np.unique(group_ids)]
    rng = np.random.default_rng(SEED)
    draws = [
        np.concatenate([group_rows[i] for i in sample])
        for sample in rng.integers(len(group_rows), size=(N_BOOT, len(group_rows)))
    ]
    draws = [rows for rows in draws if len(set(actual[rows])) == len(CALLS)]

    base = oof[BASELINE].to_numpy()
    base_f1 = macro_f1(actual, base)
    base_draws = np.array([macro_f1(actual[rows], base[rows]) for rows in draws])
    base_tp = np.count_nonzero(two_voice & (base == "tv"))
    base_fp = np.count_nonzero(~two_voice & (base == "tv"))
    metrics = []
    for rule in (BASELINE, "half_prior", PRIMARY, "weighted_logistic"):
        predicted = oof[rule].to_numpy()
        f1, *recalls = comparison_scores(actual, predicted)
        scores = [macro_f1(actual[rows], predicted[rows]) for rows in draws]
        low, high = np.quantile(scores - base_draws, [.025, .975])
        labeled_tv = predicted == "tv"
        tp = np.count_nonzero(two_voice & labeled_tv)
        fp = np.count_nonzero(~two_voice & labeled_tv)
        meets = low > 0 and tp >= base_tp
        metrics.append({
            "rule": rule, "macro_f1": f1, "delta_macro_f1": f1 - base_f1,
            "delta_low": low, "delta_high": high,
            **{f"recall_{call}": recall for call, recall in zip(CALLS, recalls)},
            "tv_precision": precision_score(two_voice, labeled_tv, zero_division=0),
            "tv_true_positive": tp, "tv_false_positive": fp,
            "delta_tv_true_positive": tp - base_tp, "delta_tv_false_positive": fp - base_fp,
            "base_tv_ap": average_precision_score(two_voice, oof.base_probability_tv)
            if rule == BASELINE else None,
            "tv_fraction": two_voice.mean(), "bootstrap_draws": len(draws),
            "meets_primary_checks": meets if rule != BASELINE else None,
            "adopted": meets if rule == PRIMARY else False,
        })
    metrics[0]["adopted"] = not metrics[2]["adopted"]
    return pd.DataFrame(metrics)


def run(data, output, baseline):
    path, = data.glob("Data01*.csv")
    frame = pd.read_csv(path)
    if set(frame.CallType) != set(CALLS) or frame.loc[:, FEATURES].isna().any().any():
        raise ValueError("Expected all three calls and complete common acoustic features")
    oof = predict(frame)
    columns = ["row", "fold", "recording_group", "actual", BASELINE]
    archived = pd.read_csv(baseline).rename(columns={"shared_features": BASELINE})
    pd.testing.assert_frame_equal(oof[columns], archived[columns])

    output.mkdir(parents=True, exist_ok=True)
    oof.to_csv(output / "q1_class_prior_predictions.csv", index=False, lineterminator="\n")
    summarize(oof).to_csv(output / "q1_class_prior_metrics.csv", index=False, lineterminator="\n")
