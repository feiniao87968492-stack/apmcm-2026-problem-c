# Round 2 ablation results

The published baseline is a0d8a74. Experimental choices are frozen in [model-spec.md](model-spec.md#improvement-round-2-freeze) and implemented at ab7622b. Each difference uses a paired 95% percentile interval from 300 draws. No model crossed its prespecified replacement threshold.

## Q1. Shallow boosted trees

| Model | Grouped macro F1 | Two-voice recall |
|---|---:|---:|
| Six-feature logistic | 0.314 | 2/24 (0.083) |
| Shallow forest | 0.370 | 1/24 (0.042) |
| Shallow XGBoost | 0.383 | 4/24 (0.167) |

XGBoost's F1 difference was +0.069 [−0.017, +0.126] versus logistic and +0.014 [−0.069, +0.098] versus forest. The corresponding recall differences were +0.083 [−0.098, +0.226] and +0.125 [0.000, +0.231]. All estimates use the same frozen recording folds and six complete features. The intervals condition on fixed held-out predictions. Retain logistic because both F1 intervals include zero, and continue using the recorded labels downstream. [Predictions](../results/round2_q1_predictions.csv) · [Paired scores](../results/round2_q1_comparison.csv)

## Q2. Omit one acoustic representation

Radii are in metres. Each cell is ordered flat, modulated, two-voice. The two retained metrics receive equal weights.

| Threshold | All metrics | Omit spectrogram | Omit amplitude spectrum | Omit envelope |
|---|---|---|---|---|
| 0.40 | 113.5 / 181.7 / 203.9 | 100.6 / 174.5 / 193.0 | 97.7 / 163.7 / 185.0 | 139.9 / 200.3 / 233.1 |
| 0.50 | 84.7 / 144.6 / 169.7 | 70.5 / 135.0 / 158.8 | 71.9 / 124.0 / 153.2 | 108.9 / 167.3 / 197.0 |
| 0.60 | 62.6 / 109.2 / 141.3 | 41.3 / 96.7 / 130.7 | 49.0 / 90.3 / 122.2 | 85.8 / 139.7 / 166.5 |
| 0.70 | 35.4 / 77.7 / 79.3 | 22.7 / 67.9 / 12.2 | 31.7 / 65.8 / 12.0 | 67.5 / 106.8 / 140.7 |

The two-voice > modulated > flat point order holds through 0.60 for every omission. At 0.70, omitting either spectrogram or amplitude spectrum changes the order to modulated > flat > two-voice. The paired two-voice radius changes at 0.70 are −67.08 m [−68.57, −65.49] without spectrogram, −67.24 m [−68.80, −65.59] without amplitude spectrum and +61.40 m [+59.23, +63.33] without envelope. The independent wide-row resampling intervals remain conditional on unknown acquisition units. Retain the full representation set. [All 48 radii, paired intervals, point ranks and support flags](../results/round2_q2_radii.csv)

## Q3. Playback predictor blocks

Losses are mean held-out fold scores. Each delta is candidate minus the previous row. Negative differences favor the candidate.

| Model | Mask log loss | Paired change [95%] | Any-response Brier | Paired change [95%] |
|---|---:|---|---:|---|
| Stimulus-only empirical frequency | 1.1768 | — | 0.1715 | — |
| Stimulus-only logistic | 1.1822 | +0.0054 [+0.0025, +0.0083] | 0.1715 | +0.00003 [−0.00053, +0.00052] |
| Add distance | 1.1757 | −0.0065 [−0.0393, +0.0352] | 0.1663 | −0.0052 [−0.0124, +0.0016] |
| Add assigned call and stimulus interaction | 1.2217 | +0.0460 [−0.0020, +0.0946] | 0.1704 | +0.0041 [−0.0011, +0.0090] |
| Add context and group size | 1.2450 | +0.0232 [−0.0182, +0.0803] | 0.1542 | −0.0162 [−0.0271, −0.0041] |

Context and group size jointly improve the Brier score in this block order. The mask-score interval for the same step crosses zero. All covariate blocks fall short of the frozen two-metric rule. Retain the stimulus-only empirical comparator and the full model for standardized descriptions. These comparisons depend on block order and use fixed held-out predictions, resampling whole pairs within each fold. [Fold scores](../results/round2_q3_fold_scores.csv) · [Paired differences](../results/round2_q3_comparison.csv)

## Q4. Does propagation fidelity improve held-out response predictions?

| Model | Binary log loss | Any-response Brier |
|---|---:|---:|
| Distance-adjusted behavior | 0.49059 | 0.15567 |
| Add fidelity and its natural-stimulus interaction | 0.49540 | 0.15663 |
| Paired difference [95%] | +0.00481 [−0.00269, +0.01244] | +0.00096 [−0.00093, +0.00281] |

Both models use the same 252 in-support rows from 135 experiments, including 117 complete pairs. The augmented model misses the joint improvement rule. The fidelity values come from independent propagation data and are fully determined by call type and distance at prediction time. Across playback rows, Pearson correlation with log(1 + distance) is −0.657. Within call it is −0.984, −0.845 and −0.759 for flat, modulated and two-voice, respectively. Log(1 + distance) and call indicators explain 84.3% of fitted fidelity variation in a descriptive linear regression. The augmented model can express a nonlinear or call-specific distance effect, so the comparison evaluates predictive value at the fixed model form.

Keep the distance-adjusted behavior model and interpret the existing product of fidelity and response as an operational scenario index. Its factors share distance-related variation, so multiplication can compound distance attenuation already represented by the response model. The product has no calibrated probability interpretation and its radii do not identify a protection distance. [Paired scores](../results/round2_q4_comparison.csv) · [Support](../results/round2_q4_coverage.csv) · [Covariate dependence](../results/round2_q4_collinearity.csv)

## Reproduction and verification

At ab7622b, a clean checkout ran `python main.py --data <attachment-dir> --output regenerated` under an isolated Python 3.10.11 environment installed from requirements.txt, including XGBoost 3.2.0. The 49 CSV and JSON files matched the repository byte-for-byte and the six PNGs matched by decoded pixels. A standalone independent implementation checked the frozen folds, all four numerical comparisons and the adoption decisions. [Independent verification](../reviews/round2-verification.md)
