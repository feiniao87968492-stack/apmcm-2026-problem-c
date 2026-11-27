"""Compare fixed score rankings for selecting recordings for manual review."""
import numpy as np
import pandas as pd

from q1_q4_cost import PASS_SETS, PROBABILITY_MODELS


def expected_yield(scores, positive, budget):
    if budget == 0:
        return 0.0
    cutoff = np.partition(scores, len(scores) - budget)[len(scores) - budget]
    above = scores > cutoff
    tied = scores == cutoff
    return positive[above].sum() + (budget - above.sum()) * positive[tied].sum() / tied.sum()


def yields(scores, positive, budget):
    return {"random": budget * positive.sum() / len(positive),
            **{name: expected_yield(values, positive, budget) for name, values in scores.items()}}


def write(output, archive):
    rows = pd.read_csv(archive / "q1_q4_cost_predictions.csv")
    fold_rates = pd.read_csv(archive / "q1_q4_prevalence_folds.csv")
    groups = [group.index.to_numpy() for _, group in rows.groupby("recording_group", sort=True)]
    n = len(rows)
    assert n == 105 and len(groups) == 15
    rng = np.random.default_rng(20261126)
    draws = [np.concatenate([groups[i] for i in sample])
             for sample in rng.integers(len(groups), size=(300, len(groups)))]
    summaries, contrasts = [], []
    for label, calls in PASS_SETS.items():
        positive = rows.actual.isin(calls).to_numpy()
        rates = fold_rates.loc[fold_rates.pass_set.eq(label)].set_index("fold").prevalence
        scores = {"prevalence": rows.fold.map(rates).to_numpy(),
                  **{model: rows[f"{model}_{label}"].to_numpy() for model in PROBABILITY_MODELS}}
        assert all(np.isfinite(values).all() for values in scores.values())
        for budget in (10, 25, 50):
            point = yields(scores, positive, budget)
            sampled = []
            for indices in draws:
                resampled_budget = (2 * budget * len(indices) + n) // (2 * n)
                sampled.append(yields({name: values[indices] for name, values in scores.items()},
                                      positive[indices], resampled_budget))
            sampled = pd.DataFrame(sampled)
            for model, value in point.items():
                summaries.append({"pass_set": label, "budget": budget, "model": model,
                                  "expected_yield": value, "positives": positive.sum(),
                                  "share_found": value / positive.sum()})
            for model in (*PROBABILITY_MODELS, "prevalence"):
                references = ("random",) if model == "prevalence" else ("random", "prevalence")
                for reference in references:
                    low, high = np.quantile(sampled[model] - sampled[reference], [.025, .975])
                    contrasts.append({"pass_set": label, "budget": budget, "model": model,
                                      "reference": reference, "excess_yield": point[model] - point[reference],
                                      "low95": low, "high95": high, "draws": len(draws)})
    output.mkdir(parents=True, exist_ok=True)
    for name, records in (("yield", summaries), ("contrasts", contrasts)):
        pd.DataFrame(records).to_csv(output / f"q4_score_review_{name}.csv", index=False,
                                     lineterminator="\n")
