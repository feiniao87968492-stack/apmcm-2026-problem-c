# Group size in paired playback and Q4

The specification froze at `45165bd` and the comparisons ran at `c21e0fe`. Strata use the natural trial's recorded size. Intervals resample whole dates and weight by the number of eligible pairs.

| Natural group size | Natural and control responses in all pairs | Natural minus control, percentage points [95%] | Same distance and size, pairs | Matched difference [95%] |
|---|---|---:|---:|---:|
| At most 4 | 47/54 and 8/54 | 72.2 [62.1, 83.2] | 26 | 73.1 [59.3, 88.0] |
| 5–12 | 23/36 and 5/36 | 50.0 [34.5, 63.8] | 9 | 33.3 [0.0, 66.7] |
| At least 13 | 20/49 and 5/49 | 30.6 [21.2, 45.0] | 14 | 21.4 [−10.9, 56.4] |

The point differences decline with size in both summaries. The 49-pair comparison controls recorded distance and group size within pairs. Differences between strata remain descriptive. [Paired counts, discordance and intervals](../results/group_size_pair_contrasts.csv)

| Strict date/track holdout model | Binary log loss | Any-response Brier |
|---|---:|---:|
| Existing binary logit | 0.5530 | 0.1789 |
| Complementary log-log with fixed unit coefficient on log(n) | 0.7376 | 0.2353 |
| Complementary log-log with estimated log(n) coefficient | 0.5488 | 0.1784 |

Free minus fixed gives −0.1888 [−0.2417, −0.1228] in log loss and −0.0568 [−0.0738, −0.0393] in Brier. Free minus logit gives −0.00418 [−0.01885, 0.01030] and −0.00052 [−0.00320, 0.00196], so the frozen joint rule retains logit. The free coefficient varies from −0.533 to −0.298 across folds. The fixed offset follows from independent equal per-bird response at given covariates. The held-out comparison checks the resulting restriction on group probabilities. Each group reports one binary outcome, leaving the within-group response count, dependence and individual probabilities unidentified. [Strict fold scores and coefficients](../results/group_size_strict_folds.csv) · [Paired score comparisons](../results/group_size_strict_scores.csv)

| Birds | Clean settings passing 80%, out of 9 | 20% coupled settings passing, out of 9 | Two-voice at 100 m, coupled attainment | Expected responder bounds in that setting |
|---:|---:|---:|---:|---:|
| 2 | 7 | 4 | 93.0% | [0.681, 1.362] |
| 8 | 4 | 2 | 50.3% | [0.548, 4.384] |
| 20 | 2 | 0 | 22.3% | [0.432, 8.635] |

All sizes use the same original eight-bird cutoff (point value 0.2876), context weights and paired acoustic/date draws. At each fixed distance, call and loss the paired margin intervals versus eight birds are above zero for two birds and below zero for twenty. The falling any-response probability can coexist with a rising upper bound on the expected count. At 100 m for two-voice, within ±25 m the exact-size natural trial counts are 1, 0 and 2 and the corresponding stratum counts are 9, 6 and 10. At the 150 m support boundary there are zero local natural trials at any exact target size. Use these as standardized scenario comparisons with sparse local support. [All Q4 settings, intervals and paired differences](../results/group_size_q4.csv) · [Coverage by stimulus, call and size](../results/group_size_q4_coverage.csv)
