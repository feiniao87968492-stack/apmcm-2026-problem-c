# Creative modeling results

The [design and adoption rules](model-spec.md#creative-modeling-freeze) were frozen at b47de34. The experiments are at 5a00f56. Predictive intervals are paired 95% percentile intervals from 300 resamples of held-out experiment pairs within folds.

## Q3 pairwise behavior models

| Model | Eight-mask log loss | Any-response Brier |
|---|---:|---:|
| Empirical stimulus-only | 1.1768 | 0.1715 |
| Released full multinomial | 1.2450 | 0.1542 |
| Two-stage | 1.2660 | 0.1626 |
| Interaction-free log-linear | 1.1348 | 0.1637 |
| Pairwise log-linear | 1.0947 | 0.1549 |

Adding co-occurrence improves both scores against the ablation, with differences −0.0401 [−0.0686, −0.0130] for mask loss and −0.00885 [−0.01416, −0.00376] for Brier. Against the full multinomial the differences are −0.1502 [−0.4090, −0.0279] and +0.00071 [−0.00640, +0.00704]. Against stimulus-only the mask-loss interval crosses zero. Retain the full model under the joint adoption rule. The conditional co-occurrence log odds ratios are 1.077 [0.452, 1.692] for head–vocal, 0.896 [0.217, 1.654] for head–approach and 0.674 [−0.016, 1.408] for vocal–approach. [Predictive comparisons](../results/creative_q3_comparison.csv) · [Interaction coefficients](../results/creative_q3_interactions.csv)

## Q4 background and fidelity gate

| Fit | Binary log loss | Any-response Brier |
|---|---:|---:|
| Published binary logistic | 0.4906 | 0.1557 |
| Control background plus ungated excess | 0.4733 | 0.1478 |
| Control background plus fixed smooth gate | 0.5075 | 0.1634 |

Relative to the released binary model, the fixed gate changes log loss by +0.0169 [−0.0182, +0.0544] and Brier by +0.00769 [−0.00331, +0.01871]. Relative to the ungated model it changes log loss by +0.0342 [−0.0021, +0.0637] and Brier by +0.01555 [+0.00211, +0.02621]. Keep the published model as the reference. The imposed center 0.50 and width 0.05 describe a recognition scenario. Representative standardized probabilities are available for each call at 50, 100 and 150 m. [Comparison to released binary model](../results/creative_gate_vs_binary_comparison.csv) · [Comparison to ungated excess](../results/creative_gate_vs_ungated_comparison.csv) · [Representative probabilities](../results/creative_gate_representative.csv)

## Q4 inversion of the common-cutoff scenarios

Every cell shows the acoustic-only and coupled loss percentages with at least 80% conditional support, in that order. The grid ends at 20%. Clean failure means fewer than 80% of clean draws meet the common cutoff.

| Call | 50 m | 100 m | 150 m |
|---|---|---|---|
| Flat | 18.0 / 10.4 | Clean failure / Clean failure | Clean failure / Clean failure |
| Modulated | ≥20 / ≥20 | 9.0 / 5.0 | Clean failure / Clean failure |
| Two-voice | ≥20 / ≥20 | ≥20 / 16.4 | 9.7 / 5.2 |

At 150 m two-voice has a clean point margin of +0.0797. At 20% loss that margin is +0.0062 under acoustic loss alone and −0.0451 under coupling. The point loss limits are ≥20% and 12.2%. The paired-draw 80% support limits are 9.7% and 5.2%. Twenty-seven of 300 draws already fall below the clean cutoff there. Both bounded draw-limit intervals span 0–20% in this cell, reflecting clean failures and search truncation. The loss estimates depend on the assumed response link, common cutoff and study support. [All 18 settings, point margins, limits and intervals](../results/creative_q4_inverse_loss.csv)

## Q1 within-group peak frequency

| Test | Informative groups | Weighted difference, Hz [95% interval] | Holm p |
|---|---:|---|---:|
| Omnibus | 11 | Centered-rank statistic 8808.5 | 0.0052 |
| Flat minus modulated | 8 | +206.92 [61.09, 292.29] | 0.0100 |
| Flat minus two-voice | 5 | +297.85 [150.54, 453.98] | 0.0052 |
| Modulated minus two-voice | 6 | +32.15 [−201.99, 203.60] | 0.7562 |

Group 14 contributes +84.42 Hz and +155.50 Hz to the first two pooled differences, respectively. The permutation conditions on the original class counts inside each matched recording group and Holm covers four tests. The prominence of Fpeak in earlier results motivated the feature choice, so this evidence stays exploratory. The six-feature logistic model remains the benchmark. [Tests](../results/creative_q1_fpeak_tests.csv) · [Group counts and contributions](../results/creative_q1_fpeak_groups.csv)
