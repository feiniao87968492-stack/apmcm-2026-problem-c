"""Evaluate sensitivity to the second recording location on the frozen Q1 folds."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from q1 import CALLS, FEATURES, FROZEN_TEST_GROUPS, macro_f1
from round2 import q1_boost_estimator


SEED = 20261126
METRICS = ("macro_f1", "tv_correct", "tv_false_positive")


def scores(actual, predicted):
    return (
        macro_f1(actual, predicted),
        np.count_nonzero((actual == "tv") & (predicted == "tv")),
        np.count_nonzero((actual != "tv") & (predicted == "tv")),
    )


def predict(frame, archived):
    key = frame.Date.astype(str) + " | " + frame.Location.astype(str)
    _, groups = np.unique(key, return_inverse=True)
    folds = np.zeros(len(frame), dtype=int)
    for fold, test_groups in enumerate(FROZEN_TEST_GROUPS, start=1):
        folds[np.isin(groups, test_groups)] = fold
    actual = frame.CallType.to_numpy()
    out = pd.DataFrame({"row": np.arange(1, len(frame) + 1), "fold": folds,
                        "recording_group": groups, "actual": actual})
    pd.testing.assert_frame_equal(out, archived[out.columns])
    main_site = frame.Location.eq("FalseBay").to_numpy()
    if len(frame) != 108 or main_site.sum() != 105 or not np.array_equal(~main_site, groups == 11):
        raise ValueError("Expected the frozen FalseBay and Seapoint samples")

    features = frame.loc[:, FEATURES].to_numpy()
    classes = np.array(CALLS)
    labels = pd.Categorical(actual, categories=CALLS).codes
    for training in ("original", "delete"):
        out[f"logistic_{training}"] = ""
        out[f"xgboost_{training}"] = ""
        for fold in range(1, len(FROZEN_TEST_GROUPS) + 1):
            test = folds == fold
            train = ~test
            if training == "delete":
                train = train & main_site
                test = test & main_site
            logistic = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000))
            logistic.fit(features[train], actual[train])
            boost = q1_boost_estimator(SEED).fit(features[train], labels[train])
            out.loc[test, f"logistic_{training}"] = logistic.predict(features[test])
            out.loc[test, f"xgboost_{training}"] = classes[boost.predict(features[test])]
    pd.testing.assert_series_equal(out.logistic_original, archived.shared_features, check_names=False)
    pd.testing.assert_series_equal(out.xgboost_original, archived.xgboost, check_names=False)
    np.testing.assert_array_equal(
        out.loc[(folds == 4) & main_site, ["logistic_original", "xgboost_original"]],
        out.loc[(folds == 4) & main_site, ["logistic_delete", "xgboost_delete"]],
    )
    out["location"] = frame.Location
    out["random_forest_archived"] = archived.random_forest
    return out


def main_site_scores(oof):
    actual = oof.actual.to_numpy()
    groups = oof.recording_group.to_numpy()
    date_rows = [np.flatnonzero(groups == group) for group in np.unique(groups)]
    rng = np.random.default_rng(SEED)
    draws = [
        np.concatenate([date_rows[i] for i in sample])
        for sample in rng.integers(len(date_rows), size=(300, len(date_rows)))
    ]
    draws = [rows for rows in draws if len(set(actual[rows])) == len(CALLS)]
    point, sampled = {}, {}
    for name in ("logistic_original", "xgboost_original", "logistic_delete", "xgboost_delete"):
        prediction = oof[name].to_numpy()
        point[name] = np.array(scores(actual, prediction))
        sampled[name] = np.array([scores(actual[rows], prediction[rows]) for rows in draws])

    estimates = pd.DataFrame.from_dict(point, orient="index", columns=METRICS).rename_axis("variant")
    comparisons = []
    for candidate, reference in (("xgboost_original", "logistic_original"),
                                 ("xgboost_delete", "logistic_delete"),
                                 ("logistic_delete", "logistic_original"),
                                 ("xgboost_delete", "xgboost_original")):
        difference = point[candidate] - point[reference]
        low, high = np.quantile(sampled[candidate] - sampled[reference], [.025, .975], axis=0)
        for metric, change, left, right in zip(METRICS, difference, low, high):
            comparisons.append({"candidate": candidate, "reference": reference, "metric": metric,
                                "difference": change, "low": left, "high": right, "draws": len(draws)})
    return estimates.reset_index(), pd.DataFrame(comparisons)


def run(data, output, baseline):
    path, = data.glob("Data01*.csv")
    archived = pd.read_csv(baseline / "round2_q1_predictions.csv")
    q1_archive = pd.read_csv(baseline / "q1_oof_predictions.csv")
    pd.testing.assert_frame_equal(archived.drop(columns="xgboost"), q1_archive[archived.columns[:-1]])
    oof = predict(pd.read_csv(path), archived)
    main = oof[oof.location.eq("FalseBay")]
    metrics, contrasts = main_site_scores(main)
    ranking = pd.DataFrame([
        {"scoring_rows": sample, "model": name, "macro_f1": macro_f1(scoring.actual, scoring[column])}
        for sample, scoring in (("all", oof), ("FalseBay", main))
        for name, column in (("logistic", "logistic_original"), ("random_forest", "random_forest_archived"),
                             ("xgboost", "xgboost_original"))
    ])
    output.mkdir(parents=True, exist_ok=True)
    for name, table in (("predictions", oof), ("metrics", metrics), ("contrasts", contrasts),
                        ("scoring_only", ranking)):
        table.to_csv(output / f"q1_location_{name}.csv", index=False, lineterminator="\n")
