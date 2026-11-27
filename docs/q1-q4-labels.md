# Q1 label errors in Q4 monitoring

The four rules use the same 105 FalseBay holdouts from 15 recording dates. For each true class, the observed label frequencies weight the Q4 point score and threshold decision of each assigned class. Subtracting the true-class score gives mean assignment bias. The false-pass and missed-pass shares both use the full true-class count as their denominator. The common gross cutoff is 0.2875982. The true-label rule has zero bias and zero errors at all 18 cells. [Frozen protocol](model-spec.md#q1-labels-in-q4-monitoring-freeze) · [Confusion counts and row proportions](../results/q1_q4_label_confusion.csv)

| Q4 point scenario | Classes passing at 50 m | 100 m | 150 m |
|---|---|---|---|
| Clean | All three | Modulated, two-voice | Two-voice |
| 20% coupled loss | Modulated, two-voice | Two-voice | None |

| Setting and true class | Error | Original logistic | Full prior correction | Original XGBoost |
|---|---|---:|---:|---:|
| Clean 100 m or coupled 50 m, flat | False pass | 47.7% | 56.8% | 45.5% |
| Clean 100 m or coupled 50 m, modulated | Missed pass | 55.0% | 45.0% | 42.5% |
| Clean 100 m or coupled 50 m, two-voice | Missed pass | 42.9% | 42.9% | 33.3% |
| Clean 150 m or coupled 100 m, flat | False pass | 6.8% | 34.1% | 11.4% |
| Clean 150 m or coupled 100 m, modulated | False pass | 7.5% | 22.5% | 12.5% |
| Clean 150 m or coupled 100 m, two-voice | Missed pass | 90.5% | 71.4% | 85.7% |

At coupled 100 m, the true two-voice score is 0.2971 and the mean assignment biases are −0.0832, −0.0731 and −0.0729 in column order. The 95% paired intervals for missed passes are 79.6–100%, 49.0–98.2% and 69.2–100%. Full prior correction reduces the missed-pass point estimate by 19.0 percentage points versus logistic, while increasing false passes among true flat and modulated calls. These estimates identify where automatic labeling could redirect monitoring attention toward failing classes and away from the only passing class. At clean 50 m and coupled 150 m, all classes are on the same side of the cutoff, so label assignments change scores without changing passage. All three rules overassign scores to flat calls on average and underassign scores to modulated and two-voice calls in all six scenarios. [All 72 rows with score bias and paired intervals](../results/q1_q4_label_monitoring.csv)

All 300 paired date resamples contain all three true classes. Applying one held-out confusion distribution per rule across distances and losses is a monitoring scenario assumption. The intervals reflect uncertainty from label error under the fixed predictions and Q4 curves. The 150 m comparisons are at the shared support boundary.

```sh
python main.py --data . --output generated --q1-q4-labels
```

This command uses the committed prediction and curve tables. [Independent recomputation](../reviews/q1-q4-label-verification.md)
