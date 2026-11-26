# Final follow-up results

The [frozen specification](model-spec.md#final-follow-up-freeze) is at 634bd20 and the implementation and outputs are at 13c5be8. Loss differences are candidate minus baseline. Intervals are paired 95% percentiles from 300 draws, except for the deterministic group-deletion ranges.

## Q1. Recording-group influence

All 108 predictions stay fixed. For each row below, the range spans the 16 ways to omit one recording group from scoring. Group numbers are zero-based identifiers from the frozen folds.

| Macro F1 contrast | All groups | Deletion range | Largest absolute shift |
|---|---:|---:|---|
| Forest minus logistic | +0.0554 | +0.0328 to +0.0732 | Group 14, −0.0225 |
| XGBoost minus logistic | +0.0690 | +0.0474 to +0.0916 | Group 2, +0.0226 |
| XGBoost minus forest | +0.0136 | −0.0116 to +0.0351 | Group 1, −0.0252 |

Group 14 contains seven flat, 13 modulated and five two-voice calls. Its removal also reduces the XGBoost-minus-logistic difference by 0.0216. Group 2 contains eight flat, seven modulated and two two-voice calls. Removing group 1 (six flat and three two-voice) or group 11 (three two-voice) reverses the XGBoost versus forest macro F1 ordering. Both tree models retain positive F1 differences against logistic under every single deletion. The XGBoost two-voice recall advantage over logistic spans +0.0476 to +0.1364, and over forest +0.0952 to +0.1500. Forest minus logistic ranges from −0.0526 to 0 for that recall. The paired bootstrap adoption rule still favors retaining logistic. [All group counts, contrasts and score shifts](../results/final_q1_group_influence.csv)

## Q3. Two-stage playback prediction

| Model | Mask log loss | Any-response Brier |
|---|---:|---:|
| Stimulus-only empirical | 1.17682 | 0.17151 |
| Full single-stage multinomial | 1.24496 | 0.15415 |
| Two-stage prediction | 1.26596 | 0.16255 |
| Two-stage minus full [95%] | +0.02100 [+0.00114, +0.03589] | +0.00840 [+0.00426, +0.01223] |

The two-stage model combines an any-response probability with a conditional distribution trained among responders. Both metrics worsen relative to the full single-stage model, so retain the existing full model for standardized comparisons. The stimulus-only empirical model remains the better mask-score comparator. [Fold scores](../results/final_q3_fold_scores.csv) · [Paired comparisons](../results/final_q3_comparison.csv)

## Q4. Reduced stimulus-and-distance curve

The reduced curve's binary log loss is 0.50912 versus 0.48361 for the full fit, a change of +0.02551 [−0.00715, +0.05871]. Its Brier score is 0.16631 versus 0.15415, a change of +0.01216 [−0.00039, +0.02371]. Neither metric meets the adoption rule. The integrated scores use the same Q2 curve and the original full-model threshold under both behavior models. Both curves evaluate the eight-bird reference and use the same paired resamples. The reduced curve depends only on stimulus and distance.

With the common cutoff, the clean full and reduced radii are 82.4 to 93.8 m for flat, 139.3 to at least 150 m for modulated, and at least 150 m for two-voice under both models. At 20% coupled loss, the corresponding changes are 41.8 to 47.2, 77.2 to 80.8 and 116.2 to 86.1 m. The two-voice paired difference in the last comparison is −30.1 m, with a bounded interval of [−80.6, +23.6] m.

The two curves agree on point cutoff attainment in 83 of the 90 distance-by-scenario-by-cutoff cases. All seven changes occur in clean or loss scenarios. Under 20% loss, two-voice switches from meeting to falling below both cutoffs at 150 m with acoustic loss alone and at 100 m with a coupled response. The remaining changes are clean modulated at 150 m under the common cutoff, modulated at 100 m under the call-specific cutoff with acoustic-only loss, and flat at 50 m under the call-specific cutoff with coupled loss. The behavior specification therefore changes some monitoring interpretations. Keep the full curve and treat these comparisons as scenarios over the 20–150 m support. [All paired radius estimates and intervals](../results/final_q4_radii.csv) · [Fixed-distance decisions](../results/final_q4_cutoff_attainment.csv) · [Held-out score differences](../results/final_q4_comparison.csv)
