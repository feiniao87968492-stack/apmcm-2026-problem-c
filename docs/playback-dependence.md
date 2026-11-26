# Playback dependence and trial precision

The [specification](model-spec.md#playback-dependence-and-design-precision-freeze) was frozen in fa1b026 before computing the results at 4c1b3a3.

## Holdout by date and by natural playback track

Each split evaluates all 278 trials in 139 intact experiments. Date folds contain 4–20 held-out pairs and natural-track folds contain 1–10. One held-out trial has an unseen behavior mask in each scheme. Every assigned call class is represented in training in both schemes.

| Holdout | Model | Pooled mask log loss | Pooled Brier |
|---|---|---:|---:|
| 12 dates | Smoothed stimulus frequencies | 1.11371 | 0.17507 |
| 12 dates | Full multinomial | 1.24106 | 0.16569 |
| 12 dates | Pairwise log-linear | 1.11803 | 0.16546 |
| 28 natural tracks | Smoothed stimulus frequencies | 1.11151 | 0.17335 |
| 28 natural tracks | Full multinomial | 1.22271 | 0.15727 |
| 28 natural tracks | Pairwise log-linear | 1.08875 | 0.15681 |

Dates and tracks are held out separately. A natural track is assigned to both trials in its experiment, with the shared control stimulus still present across track folds. Under date holdout, 119 of 139 test pairs use a natural track available in training. Under track holdout, every test pair comes from a date represented in training. The pairwise model has the lowest point Brier in both cases. Its mask loss improves on both comparisons for track holdout, while the smoothed baseline scores slightly better on date holdout. The full model remains the reference for standardized scenarios. [Pooled scores](../results/dependence_q3_pooled.csv) · [Fold scores and coverage](../results/dependence_q3_folds.csv)

## Date blocks in Q4

The 95% margins were wider under whole-date resampling in all 18 settings. The same behavior fit anchors the point margins. The propagation draws are paired by index with either behavior sampling scheme. The common clean cutoff is recomputed in each draw.

| Clean setting | Experiment-pair support | Date-block support | Pair margin interval | Date margin interval |
|---|---:|---:|---|---|
| Modulated at 100 m | 90.3% | 76.0% | [−0.040, 0.190] | [−0.074, 0.306] |
| Two-voice at 150 m | 91.0% | 78.7% | [−0.031, 0.187] | [−0.114, 0.242] |

These settings fall below 80% support under date resampling. The other clean decisions and all nine 20% coupled-loss decisions agree between schemes. Date resampling is conditional on 12 observed dates and the reuse of playback tracks. [All margins and attainment counts](../results/dependence_q4_margins.csv)

## Trial precision

The design gives each of six call-by-distance cells ten matched pairs per noise arm. The average contrast weights the six elevated-minus-reference noise contrasts equally. Its normal-approximation precision assumes independent cells and the earlier clean response marginals in both arms.

| Working paired correlation | 120-pair average half-width | 120-pair worst cell half-width | Minimum pairs for all cells at or below 0.20 | Pairs under equal allocation |
|---:|---:|---:|---:|---:|
| −0.25 | 0.2193 | 0.5540 | 870 | 924 |
| 0 | 0.1994 | 0.5025 | 724 | 768 |
| +0.25 | 0.1788 | 0.4450 | 582 | 600 |

The minimum preserves equal noise arms inside each cell. The 0.20 half-width is a planning target for each individual cell. [Precision and totals](../results/dependence_q4_trial_summary.csv) · [Cell requirements](../results/dependence_q4_trial_cells.csv)
