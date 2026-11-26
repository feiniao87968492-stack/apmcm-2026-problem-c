# Post hoc sensitivity checks

The checks were motivated by the creative release 493bb98 and frozen before computation at 43c39e6. The original results remain available. Confidence intervals below are paired 95% percentiles from 300 resamples of held-out pairs within folds.

## Q3. Sparse mask and smoothed stimulus baseline

The full sample contains 278 held-out rows. In fold 1, the natural stimulus for pair 138 has mask 4, approach only. Its observed mask probability is zero in the unsmoothed stimulus, full multinomial and two-stage models, 0.00435 in the smoothed stimulus model and 0.00879 in the pairwise model.

Against the original stimulus-only comparator, the pairwise mask loss changes by −0.08211. The focal row contributes −0.08178 to the mean across folds, with −0.00033 from the remaining rows. Against the full multinomial and two-stage models, the same focal contribution accounts for part of total changes −0.15024 and −0.17124. The remaining contributions are −0.06847 and −0.08947 respectively.

With 0.5 added to every mask count in each training stimulus group, mask loss is 1.10778 for the baseline and 1.09471 for pairwise, a difference of −0.01307 [−0.06443, +0.04757]. The focal row contributes −0.00252 to this difference. Brier changes from 0.17183 to 0.15486, or −0.01697 [−0.02665, −0.00470]. The smoothed sensitivity fails the joint adoption rule. [Paired scores](../results/posthoc_q3_smoothed_comparison.csv) · [Row contributions](../results/posthoc_q3_focal_contribution.csv)

## Q4. Direct ungated excess comparison

On the original in-range folds, log loss changes from 0.49059 for the published binary logistic to 0.47325 for ungated excess, a difference of −0.01733 [−0.04251, +0.01207]. Brier changes from 0.15567 to 0.14780, a difference of −0.00787 [−0.01356, −0.00089]. The original two-metric adoption rule retains the published reference. [Fold scores and paired intervals](../results/posthoc_q4_ungated_comparison.csv)

## Q4. Support criteria and behavior curves

The full-model 80% calculations reproduce the creative release. All limits use the same full-model common cutoff, including its draw-specific version.

| Two-voice at 150 m | 70% support | 80% support | 90% support |
|---|---:|---:|---:|
| Full, acoustic-only | 15.2% | 9.7% | 2.4% |
| Full, coupled | 8.4% | 5.2% | 1.2% |
| Reduced, acoustic-only | 10.1% | 6.3% | Clean failure |
| Reduced, coupled | 5.5% | 3.4% | Clean failure |

At 80% support, the reduced curve increases flat limits at 50 m from 18.0% and 10.4% to at least 20% and 15.9% under acoustic-only and coupled scenarios. At 100 m it increases modulated limits from 9.0% and 5.0% to 17.0% and 9.7%, while the coupled two-voice limit decreases from 16.4% to 13.6%. Thus the support criterion and behavior model change some operational scenario judgments. The table distinguishes clean failures from settings that reach the 20% search ceiling. [All 108 settings](../results/posthoc_q4_inverse_sensitivity.csv)
