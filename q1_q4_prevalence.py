"""Benchmark archived Q4 monitoring decisions without acoustic features."""
import numpy as np
import pandas as pd

from q1_q4_cost import PASS_SETS, evaluate
from q1_q4_labels import KEYS


def write(output, archive):
    whole = pd.read_csv(archive / "q1_location_predictions.csv")
    rows = pd.read_csv(archive / "q1_q4_cost_predictions.csv")
    held_out = whole.loc[whole.location.eq("FalseBay")].reset_index(drop=True)
    pd.testing.assert_frame_equal(rows[KEYS], held_out[KEYS])
    prevalence = []
    for label, calls in PASS_SETS.items():
        rates = {}
        for fold in sorted(whole.fold.unique()):
            train = whole.loc[whole.fold.ne(fold)]
            count = int(train.actual.isin(calls).sum())
            rates[fold] = count / len(train)
            prevalence.append({"pass_set": label, "fold": fold, "training_rows": len(train),
                               "training_passes": count, "prevalence": rates[fold]})
        rows[f"prevalence_{label}"] = rows.fold.map(rates)
    scores, decisions, contrasts = evaluate(rows, include_prevalence=True)
    keys = ["pass_set", "false_pass_cost", "missed_pass_cost", "model"]
    original = pd.read_csv(archive / "q1_q4_cost_decisions.csv").set_index(keys)
    pd.testing.assert_frame_equal(decisions.set_index(keys).loc[original.index], original)
    original_scores = pd.read_csv(archive / "q1_q4_cost_scores.csv").set_index(["pass_set", "model"])
    pd.testing.assert_frame_equal(scores.set_index(["pass_set", "model"]).loc[original_scores.index],
                                  original_scores)
    baseline = scores.loc[scores.model.eq("prevalence")].set_index("pass_set")
    for metric in ("brier", "log_loss"):
        scores[f"delta_{metric}"] = scores[metric] - scores.pass_set.map(baseline[metric])
    contrasts["superior_to_prevalence"] = contrasts.high95.lt(0)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in (("folds", pd.DataFrame(prevalence)), ("scores", scores),
                        ("decisions", decisions), ("contrasts", contrasts)):
        table.to_csv(output / f"q1_q4_prevalence_{name}.csv", index=False, lineterminator="\n")
