"""Evaluate Q4 monitoring decisions on the frozen Q1 holdouts."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from statsmodels.miscmodels.ordinal_model import OrderedModel

from q1 import CALLS, FEATURES, FROZEN_TEST_GROUPS
from q1_q4_labels import KEYS, load_scores


PASS_SETS = {"tv": ("tv",), "mod_tv": ("mod", "tv")}
PROBABILITY_MODELS = ("multinomial", "binary", "ordinal")
HARD_RULES = ("hard_logistic", "hard_xgboost")
COSTS = ((1, 1), (1, 3), (3, 1))


def predict(data, archive):
    path, = data.glob("Data01*.csv")
    frame = pd.read_csv(path)
    group_keys = frame.Date.astype(str) + " | " + frame.Location.astype(str)
    _, groups = np.unique(group_keys, return_inverse=True)
    actual = frame.CallType.to_numpy()
    order = pd.Categorical(actual, categories=CALLS, ordered=True).codes
    x = frame.loc[:, FEATURES].to_numpy()
    result = pd.DataFrame({"row": np.arange(1, len(frame) + 1), "fold": 0,
                           "recording_group": groups, "actual": actual})
    for fold, held in enumerate(FROZEN_TEST_GROUPS, 1):
        test = np.isin(groups, held)
        train = ~test
        result.loc[test, "fold"] = fold
        scaler = StandardScaler().fit(x[train])
        training, testing = scaler.transform(x[train]), scaler.transform(x[test])
        multi = LogisticRegression(C=1, max_iter=1000).fit(training, actual[train])
        probabilities = multi.predict_proba(testing)
        result.loc[test, "hard_logistic"] = multi.predict(testing)
        ordinal = OrderedModel(order[train], training, distr="logit").fit(
            method="bfgs", maxiter=1000, gtol=1e-8, disp=False,
        )
        if not ordinal.mle_retvals["converged"]:
            raise RuntimeError(f"Ordinal model failed to converge in fold {fold}")
        ordered_probabilities = ordinal.model.predict(ordinal.params, exog=testing)
        for label, calls in PASS_SETS.items():
            binary = LogisticRegression(C=1, max_iter=1000).fit(
                training, np.isin(actual[train], calls),
            )
            result.loc[test, f"binary_{label}"] = binary.predict_proba(testing)[:, 1]
            result.loc[test, f"ordinal_{label}"] = ordered_probabilities[:, np.isin(CALLS, calls)].sum(axis=1)
            result.loc[test, f"multinomial_{label}"] = probabilities[:, np.isin(multi.classes_, calls)].sum(axis=1)
        for i, call in enumerate(multi.classes_):
            result.loc[test, f"base_probability_{call}"] = probabilities[:, i]

    prior = pd.read_csv(archive / "q1_class_prior_predictions.csv")
    site = pd.read_csv(archive / "q1_location_predictions.csv")
    for previous in (prior, site):
        pd.testing.assert_frame_equal(result[KEYS], previous[KEYS])
    pd.testing.assert_series_equal(result.hard_logistic, prior.logistic, check_names=False)
    pd.testing.assert_series_equal(result.hard_logistic, site.logistic_original, check_names=False)
    columns = [f"base_probability_{call}" for call in CALLS]
    np.testing.assert_allclose(result[columns], prior[columns], atol=1e-12, rtol=0)
    result["hard_xgboost"] = site.xgboost_original
    selected = frame.Location.eq("FalseBay")
    np.testing.assert_array_equal(selected, site.location.eq("FalseBay"))
    result = result.loc[selected].reset_index(drop=True)
    assert len(result) == 105 and result.recording_group.nunique() == 15
    assert result.ordinal_tv.le(result.ordinal_mod_tv).all()
    return result.drop(columns=columns)


def evaluate(rows):
    groups = [group.index.to_numpy() for _, group in rows.groupby("recording_group", sort=True)]
    rng = np.random.default_rng(20261126)
    draws = [np.concatenate([groups[i] for i in sample])
             for sample in rng.integers(len(groups), size=(300, len(groups)))]
    scores, decisions, contrasts = [], [], []
    for label, calls in PASS_SETS.items():
        truth = rows.actual.isin(calls).to_numpy()
        probabilities = {m: rows[f"{m}_{label}"].to_numpy() for m in PROBABILITY_MODELS}
        for model, p in probabilities.items():
            clipped = np.clip(p, 1e-15, 1 - 1e-15)
            scores.append({"pass_set": label, "model": model,
                           "brier": np.mean((p - truth)**2),
                           "log_loss": -np.mean(np.where(truth, np.log(clipped), np.log1p(-clipped)))})
        for fp_cost, miss_cost in COSTS:
            cutoff = fp_cost / (fp_cost + miss_cost)
            label_fields = {"pass_set": label, "false_pass_cost": fp_cost, "missed_pass_cost": miss_cost}
            actions = {m: rows[m].isin(calls).to_numpy() for m in HARD_RULES}
            actions.update({m: p >= cutoff for m, p in probabilities.items()})
            costs = {}
            for model, pass_action in actions.items():
                false_pass = pass_action & ~truth
                missed_pass = ~pass_action & truth
                costs[model] = fp_cost * false_pass + miss_cost * missed_pass
                decisions.append({**label_fields, "model": model,
                                  "probability_cutoff": cutoff if model in probabilities else None,
                                  "false_pass": false_pass.sum(), "missed_pass": missed_pass.sum(),
                                  "true_pass": truth.sum(), "true_nonpass": (~truth).sum(),
                                  "mean_cost": costs[model].mean()})
            for model in PROBABILITY_MODELS:
                for reference in HARD_RULES:
                    change = costs[model] - costs[reference]
                    lower, upper = np.quantile([change[idx].mean() for idx in draws], [.025, .975])
                    contrasts.append({**label_fields, "model": model, "reference": reference,
                                      "delta_mean_cost": change.mean(), "low95": lower, "high95": upper,
                                      "draws": len(draws)})
    return map(pd.DataFrame, (scores, decisions, contrasts))


def write(data, output, archive):
    scores = load_scores(archive)
    for scenario, loss, distance, label in (
        ("coupled", .2, 100., "tv"), ("clean", 0., 150., "tv"),
        ("clean", 0., 100., "mod_tv"), ("coupled", .2, 50., "mod_tv"),
    ):
        points = scores.xs((scenario, loss, distance))
        assert set(points.index[points.meets_cutoff]) == set(PASS_SETS[label])
    rows = predict(data, archive)
    scoring, decisions, contrasts = evaluate(rows)
    primary = decisions.query("pass_set == 'tv' and false_pass_cost == 1 and missed_pass_cost == 1")
    original = primary.loc[primary.model.eq("hard_logistic")].iloc[0]
    assert (original.false_pass, original.missed_pass) == (6, 19)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in (("predictions", rows), ("scores", scoring),
                        ("decisions", decisions), ("contrasts", contrasts)):
        table.to_csv(output / f"q1_q4_cost_{name}.csv", index=False, lineterminator="\n")
