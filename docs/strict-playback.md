# Strict playback holdout and crossed resampling

The protocol was frozen at 9e95367. Results are at 5c951ca.

## Unseen date and natural tracks

The 12 folds hold out all 139 pairs once. Each training fold excludes other dates' pairs that share a natural track with its test date. Training coverage is 97–127 pairs, test coverage is 4–20, and 3–26 other-date pairs are purged per fold. Each test fold contains 2–8 held natural tracks. One test trial has an eight-state mask absent from its training fold. The common control stimulus remains shared.

| Model | Pooled mask log loss | Any-response Brier |
|---|---:|---:|
| Stimulus-specific half-count frequencies | 1.1250 | 0.1778 |
| Full multinomial | 1.2993 | 0.1698 |
| Pairwise mask model | 1.1417 | 0.1681 |

The smoothed baseline leads on mask log loss and the pairwise model leads on Brier. The full model supplies standardized estimates. [Coverage](../results/strict_q3_coverage.csv) · [Scores](../results/strict_q3_scores.csv)

## Joint response within an experiment

The natural and control trial margins use their own distances and covariates. A single penalized log odds ratio fitted on training pairs allocates probability among the four joint states subject to those margins. Fitted log odds ratios range from 0.464 to 1.597 across folds. Pair log loss is 1.0587 under independence and 1.0431 under the shared odds ratio. The paired difference is −0.0155 with a date-block percentile interval of [−0.0322, +0.0024]. The marginal Brier is 0.1698 for both methods by construction. Conditional independence remains the joint prediction reference under the frozen rule. A common association can reflect group-level conditions, trial order or other shared factors. [Fold estimates](../results/strict_q3_pair_folds.csv) · [Paired interval](../results/strict_q3_pair_contrast.csv)

## Crossed sampling for Q4

Each pair receives the product of its independently drawn date and natural-track cluster counts. The 300 accepted draws contain 25–96 unique pairs, 3–11 dates and 7–23 natural tracks, with medians of 59, 8 and 15. The procedure holds the common cutoff definition fixed and recomputes its draw-specific value. Date and crossed sampling agree on all 18 decisions at 80% attainment. Experiment-pair sampling instead passes clean modulated calls at 100 m and clean two-voice calls at 150 m. At 150 m for clean two-voice, support is 91.0%, 78.7% and 76.7% under experiment-pair, date and crossed sampling, respectively. The corresponding margin intervals are [−0.031, 0.187], [−0.114, 0.242] and [−0.154, 0.291]. These sensitivities condition on the observed 12 dates and 28 natural tracks. [Margin results](../results/strict_q4_margins.csv) · [Draw coverage](../results/strict_q4_crossed_coverage.csv)
