"""Evaluate ideal manual review of held-out labels in the 100 m Q4 scenario."""
import numpy as np
import pandas as pd

from q1_q4_labels import load_labels, load_scores


BUDGETS = (0, 10, 25, 50, 105)


def run(archive, output):
    labels = load_labels(archive).set_index("row").sort_index()
    scores = load_scores(archive).xs(("coupled", .20, 100.0))
    passing = scores.index[scores.meets_cutoff].tolist()
    if passing != ["tv"]:
        raise ValueError("Expected only two-voice to pass the archived gross cutoff")

    ranks = labels[["fold", "logistic", "base_probability_tv"]].copy()
    ranks["original_pass"] = ranks.logistic.isin(passing)
    probability = ranks.base_probability_tv
    ranks["error_score"] = np.where(ranks.original_pass, 1 - probability, probability)
    orders = {
        "error_probability": ranks.sort_values(["error_score", "row"], ascending=[False, True]).index,
        "nonpass_first": ranks.sort_values(
            ["original_pass", "error_score", "row"], ascending=[True, False, True],
        ).index,
    }
    for rule, order in orders.items():
        ranks[f"{rule}_rank"] = pd.Series(np.arange(1, len(order) + 1), index=order)

    actual_pass = labels.actual.isin(passing)
    errors = pd.DataFrame({
        "false_pass": ranks.original_pass & ~actual_pass,
        "missed_pass": ~ranks.original_pass & actual_pass,
    })
    denominators = pd.Series({"false_pass": int((~actual_pass).sum()),
                              "missed_pass": int(actual_pass.sum())})
    baseline = errors.sum()
    np.testing.assert_array_equal(denominators, [84, 21])
    np.testing.assert_array_equal(baseline, [6, 19])

    rows = []
    for budget in BUDGETS:
        expectation = baseline * (len(labels) - budget) / len(labels)
        residual = {"random": expectation}
        for rule, order in orders.items():
            residual[rule] = errors.loc[order[budget:]].sum()
        if budget in (0, len(labels)):
            for counts in residual.values():
                np.testing.assert_array_equal(counts, expectation)
        for rule, counts in residual.items():
            for kind, population in denominators.items():
                change = counts[kind] - expectation[kind]
                rows.append({
                    "budget": budget, "rule": rule, "error": kind, "denominator": population,
                    "remaining_count": counts[kind], "remaining_rate": counts[kind] / population,
                    "random_expected_count": expectation[kind],
                    "delta_count_vs_random": change, "delta_pp_vs_random": 100 * change / population,
                })

    ranks["actual"] = labels.actual
    ranks = ranks.join(errors)
    output.mkdir(parents=True, exist_ok=True)
    ranks.to_csv(output / "q4_review_budget_ranks.csv", lineterminator="\n")
    pd.DataFrame(rows).to_csv(output / "q4_review_budget_results.csv", index=False, lineterminator="\n")
