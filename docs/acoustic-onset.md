# Acoustic transformations and recorded onset

The protocol at 195a5af was frozen before fitting. Inputs and results are described in [the specification](model-spec.md#acoustic-transformations-and-recorded-onset-freeze).

## Q1 feature representations

| Features | Macro F1 | Paired difference versus original, 95% interval | Two-voice recall |
|---|---:|---|---:|
| Original | 0.3144 | Reference | 2/24 |
| All log | 0.2865 | −0.0279 [−0.0704, +0.0082] | 1/24 |
| Log ratios and skewness | 0.3223 | +0.0079 [−0.0601, +0.0631] | 2/24 |

All fits use the original grouped folds and standardized logistic regression. Retain the original features under the frozen paired criterion. [Paired metrics](../results/onset_q1_acoustic.csv)

## Q3 conditional onset

Pooled time MAE in seconds, with median followed by ridge in each cell.

| Behavior | Observed onsets | expID holdout | Date holdout |
|---|---:|---|---|
| Head raising | 68 | 1.324 / 1.472 | 1.324 / 1.459 |
| Vocalizing | 81 | 3.035 / 2.975 | 3.019 / 3.068 |
| Approach | 23 | 5.370 / 5.499 | 5.804 / 6.865 |

Ridge has no behavior for which MAE improves under both holdouts. Its existing conditional timing curves are descriptive. Control approach remains unestimable because no approach was observed. [Stimulus-specific sample counts and scores](../results/onset_q3_latency.csv)

## Q3 earliest recorded onset

| Split | Smoothed stimulus log loss / Brier | Multinomial log loss / Brier |
|---|---|---|
| expID | 0.7277 / 0.4075 | 0.7347 / 0.3965 |
| Date | 0.7390 / 0.4147 | 0.7644 / 0.4198 |

Neither split shows simultaneous improvement on both scores. The standardized multinomial estimates remain exploratory. For example, natural two-voice responses by 5 and 15 s at 150 m are 0.419 [0.150, 0.699] and 0.563 [0.273, 0.793], based on two nearby natural trials. The corresponding control probabilities are 0.053 [0.004, 0.140] and 0.062 [0.005, 0.153], with one nearby control and zero recorded responses in that window. These probabilities describe events recorded in the supplied trials. [Scores](../results/onset_q3_timing_scores.csv) · [All cumulative probabilities and date intervals](../results/onset_q3_cumulative.csv)
