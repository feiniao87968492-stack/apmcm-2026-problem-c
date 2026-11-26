# Matched distance, loss limits and behavior weights

The [frozen specification](model-spec.md#distance-matching-and-behavioral-score-freeze) is at c4bf42f. The results are at f6e5984.

## Q3. Paired responses by relative playback distance

| Natural distance relative to control | Pairs | Same group size | Natural / control responses | Natural-only / control-only | Natural minus control, percentage points (95% date-block interval) |
|---|---:|---:|---:|---:|---:|
| Same | 49 | 49 | 33 / 8 | 27 / 2 | 51.0 [37.5, 64.2] |
| Nearer | 52 | 52 | 38 / 6 | 32 / 0 | 61.5 [51.7, 69.5] |
| Farther | 38 | 36 | 19 / 4 | 15 / 0 | 39.5 [24.3, 55.7] |

The same-distance count and discordant counts were known at freeze. All 300 date draws represented every stratum. The observed gap persists with distance and group size matched. The strata remain descriptive comparisons of the observed trials. [Paired counts and intervals](../results/matching_q3_strata.csv)

## Q4. Inverse limits with two resampling schemes

Each cell lists acoustic-only / coupled loss limits in percent at 80% support. The intersection requires both schemes to pass at each loss. Fail means clean support already falls below 80%. A value of ≥20 reaches the search ceiling.

| Call and distance | Experiment-pair | Date block | Intersection |
|---|---:|---:|---:|
| Flat, 50 m | 18.0 / 10.4 | 6.0 / 3.3 | 6.0 / 3.3 |
| Flat, 100 and 150 m | Fail | Fail | Fail |
| Modulated, 50 m | ≥20 / ≥20 | ≥20 / ≥20 | ≥20 / ≥20 |
| Modulated, 100 m | 9.0 / 5.0 | Fail | Fail |
| Modulated, 150 m | Fail | Fail | Fail |
| Two-voice, 50 m | ≥20 / ≥20 | ≥20 / ≥20 | ≥20 / ≥20 |
| Two-voice, 100 m | ≥20 / 16.4 | ≥20 / 12.2 | ≥20 / 12.2 |
| Two-voice, 150 m | 9.7 / 5.2 | Fail | Fail |

The date analysis reuses the original propagation draws and refits conditioned on the 12 observed playback dates. The estimated loss limits are operational scenarios. [Limits, statuses and endpoint support](../results/matching_q4_loss_limits.csv)

## Q4. Ecological weights for behavior masks

Each index has its own common cutoff at half its mean clean index at 20 m. The cutoffs are 0.28760 for any response, 0.17104 for equal behavior weights and 0.15970 for head/vocal/approach weights 0.2/0.4/0.4. Both weighted indices preserve the any-response ranks at each tested distance and preserve the radius ordering under clean and 20% acoustic-only conditions.

At clean 150 m, two-voice support is 91.0% for any response, 57.3% for equal weights and 78.7% for the 0.2/0.4/0.4 weights. Its point estimate passes all three thresholds. Under 20% acoustic-only loss, two-voice at 100 m drops below 80% only under the equal-weight index (62.7% versus 95.7% for any response). At 150 m both weighted point estimates fall below their cutoffs and support is below 80% for all three indices. The corresponding two-voice radii are at least 150, 116.5 and 140.4 m. The any-response index remains the operational reference. [Fixed-distance margins and attainment](../results/matching_q4_weighted_points.csv) · [Radii and bounds](../results/matching_q4_weighted_radii.csv)
