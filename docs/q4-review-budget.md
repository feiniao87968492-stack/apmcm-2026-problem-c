# Manual review budget for Q4 monitoring

At 100 m under 20% coupled loss, only two-voice clears the common gross cutoff. The original hard logistic decisions on 105 FalseBay holdouts contain six false passes and 19 missed passes. Review corrects a selected row to its true label at unit cost. The two fixed queues use the held-out two-voice probability. Overall error probability ranks original nonpasses by p_tv and original passes by 1 − p_tv in a single queue. The nonpass-first queue processes the former before the latter. Both use descending scores and ascending source row ID for ties. [Frozen protocol](model-spec.md#q4-monitoring-review-budget-freeze)

Each entry gives residual false passes / missed passes, with rates in parentheses. The two denominators are 84 and 21. Random counts are exact expectations under uniform sampling without replacement.

| Budget | Random expectation | Overall error probability | Nonpass first |
|---:|---:|---:|---:|
| 0 | 6 (7.1%) / 19 (90.5%) | 6 (7.1%) / 19 (90.5%) | 6 (7.1%) / 19 (90.5%) |
| 10 | 5.43 (6.5%) / 17.19 (81.9%) | 1 (1.2%) / 18 (85.7%) | 6 (7.1%) / 18 (85.7%) |
| 25 | 4.57 (5.4%) / 14.48 (68.9%) | 0 (0%) / 18 (85.7%) | 6 (7.1%) / 14 (66.7%) |
| 50 | 3.14 (3.7%) / 9.95 (47.4%) | 0 (0%) / 8 (38.1%) | 6 (7.1%) / 5 (23.8%) |
| 105 | 0 (0%) / 0 (0%) | 0 (0%) / 0 (0%) | 0 (0%) / 0 (0%) |

| Budget | Overall error probability minus random, false / missed | Nonpass first minus random, false / missed |
|---:|---:|---:|
| 10 | −4.43 / +0.81 | +0.57 / +0.81 |
| 25 | −4.57 / +3.52 | +1.43 / −0.48 |
| 50 | −3.14 / −1.95 | +2.86 / −4.95 |

Differences at budgets 0 and 105 are zero. At 25 reviews, ranking by overall error probability removes every false pass and leaves more missed passes than the random expectation. At 50 reviews it reduces both errors relative to random. Prioritizing original nonpasses at 50 recovers three more missed passes than overall error ranking and leaves six false passes. The fixed-sample rankings assume the five models' held-out probabilities are comparable across folds. The experiment assumes perfect human correction of the selected recordings. [All counts, rates and percentage-point differences](../results/q4_review_budget_results.csv) · [Row rankings](../results/q4_review_budget_ranks.csv)

```sh
python main.py --data . --output generated --q4-review-budget
```

The command uses the committed prediction and curve tables. [Independent verification](../reviews/q4-review-budget-verification.md)
