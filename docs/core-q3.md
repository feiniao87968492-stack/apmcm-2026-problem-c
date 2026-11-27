# Core Q3 playback models

The 12 held dates contain all 139 experiment pairs and 278 trials. Each training fold excludes any pair whose natural track appears on its test date. Both rows of each pair share the resulting assignment. Scores pool trials with equal weight. Intervals resample whole held dates using 10,000 draws with seed 20261209. [Frozen design](model-spec.md#core-q3-strict-masks-and-observable-timing-freeze)

## Response combinations

| Mask model | Log loss | Any-response Brier |
|---|---:|---:|
| Stimulus half-count frequencies | 1.12504 | 0.17778 |
| Released full multinomial | 1.29934 | 0.16978 |
| Structured pairwise mask | 1.14169 | 0.16809 |
| Shrunk hurdle | 1.11170 | 0.16670 |
| Rank-one tilt | 1.10210 | 0.16383 |
| Nested frequency–hurdle pool | 1.11237 | 0.17002 |

The rank-one tilt gives the lowest point estimate on both scores. Its log-loss difference from the full multinomial is −0.19724 [−0.37271, −0.06733], with a Brier difference of −0.00595 [−0.01852, +0.00371]. Against frequencies, the differences are −0.02294 [−0.07811, +0.04142] and −0.01395 [−0.03193, +0.00558], respectively. Every candidate misses the frozen requirement for both paired upper limits to be below zero against both references. The full multinomial remains the distance-specific mask model. The nested pool assigns the hurdle weight 0.50 on six held dates and 0.75 on the other six. [Pooled scores](../results/core_q3_mask_scores.csv) · [Paired intervals](../results/core_q3_mask_deltas.csv) · [Per-date scores](../results/core_q3_mask_date_scores.csv) · [Fold coverage and pooling](../results/core_q3_coverage.csv)

The tail check excludes pairs with either arm at least 125 m from training. It scores 52 trials across eight dates, including 33 trials actually at 125 m or farther. In the tail pairs the rank-one tilt changes log loss by +0.03315 [−0.12016, +0.20126] and Brier by −0.02180 [−0.04693, +0.01171] against the released model. Across the 33 long trials, both differences have intervals spanning zero. Near 150 m, defined as 125–175 m, two-voice contributes two natural trials with two events and one control trial with zero events. Pooled validation has limited coverage for that distance and call. [Tail scores and intervals](../results/core_q3_mask_deltas.csv) · [Local coverage](../results/core_q3_support.csv)

## Observable event time through 60 s

Each behavior and the earliest event of any behavior use cells at zero, (0,5], (5,15], (15,30], (30,60], and no event by 60 s. The likelihood includes every trial. Integrated Brier uses the 5, 15, 30 and 60 s cumulative risks with interval weights 5/60, 10/60, 15/60 and 30/60. This finite-window estimand records whether and when the group responded during observation.

| Endpoint | Baseline log loss / integrated Brier | Hazard | Finite-window two-part |
|---|---:|---:|---:|
| Any | 0.85567 / 0.17649 | 0.85772 / 0.17525 | 0.86224 / 0.17677 |
| Head raising | 0.67536 / 0.16613 | 0.67301 / 0.15867 | 0.67524 / 0.15911 |
| Vocalizing | 0.66236 / 0.14530 | 0.67339 / 0.14314 | 0.65847 / 0.14327 |
| Approach | 0.34304 / 0.06430 | 0.34817 / 0.06542 | 0.34005 / 0.06433 |

All paired log-loss intervals versus the half-count stimulus timing model span zero. This selects the stimulus-only distribution for all four endpoints. Conditional onset MAE for the training-median reference is 2.188 s for any event, 1.331 s for head raising, 3.082 s for vocalizing and 5.587 s for approach. The two alternatives give 2.177 s for any event, 1.324 s for head raising and 5.630 s for approach. Vocal MAE is 3.080 s for the hazard and 3.141 s for the two-part model. Conditional MAE is computed only when an event is observed. The control arm has zero observed approaches. The selected model's small nonzero approach probabilities for control come from half-count smoothing. [Timing scores](../results/core_q3_timing_scores.csv) · [Paired intervals](../results/core_q3_timing_deltas.csv) · [Per-date timing scores](../results/core_q3_timing_date_scores.csv)

The full-data prediction grid uses eight birds and the empirical frequencies of the three natural-trial contexts. Every timing fit exports cumulative probabilities at 0, 5, 15, 30 and 60 s. The any-event grid covers 20–150 m in 0.5 m steps for Q4. The individual behaviors use 50, 100 and 150 m. Selected stimulus-only time predictions are constant across distance and call type within each arm. For any event the selected natural probabilities at 5, 15, 30 and 60 s are 0.5282, 0.6373, 0.6479 and 0.6514, and controls are 0.1197, 0.1303, 0.1338 and 0.1444. These time predictions are an arm-level benchmark for Q4. [Prediction grid](../results/core_q3_predictions.csv) · [Local event support](../results/core_q3_support.csv)

## Reproduction and Q4 interface

    python core_q3.py --data "<attachment directory>/date" --output generated

For Q4, select `endpoint=Any`, the required `window_s` and `selected=True` from the `family=timing` rows. For the released mask comparison, select `family=mask`, `model=full_multinomial` and `window_s=60`. `predict_mask(frame, evaluation, model, contexts)` returns probabilities for masks 0–7. `predict_timing(frame, evaluation, model, contexts, endpoint)` returns probabilities for the five event cells and the final no-event cell, in that order. Both use the passed training data.
