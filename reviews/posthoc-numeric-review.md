# Post hoc independent numerical verification

**Verdict PASS.** I checked the results at `1ac4bbd` against the specification at `43c39e6` and the archived creative release `493bb98`. The verification used the original attachments and archived fold predictions with standalone calculations. I refit the ungated model with a numerical-gradient optimizer and reconstructed the propagation and behavior bootstrap draws from the original attachments.

## Q3. Smoothed comparator and focal contribution

I recovered all 278 held-out rows in the original five experiment folds. In each training stimulus stratum I independently counted the eight masks and applied the frozen half-count formula. The five held-out fold scores and both 300-draw paired intervals reproduced. The smoothed stimulus comparator gives mask log loss 1.107782 and any-response Brier 0.171833. The pairwise model gives 1.094711 and 0.154860. The paired loss differences are −0.013071 [−0.064427, 0.047568] and −0.016973 [−0.026645, −0.004699]. The comparison misses the joint rule.

I found exactly one focal row at fold 1, pair 138, natural stimulus with observed mask 4, among 56 fold-1 rows. Each original benchmark assigned it zero probability and the pairwise model assigned 0.00879434. For mask log loss, the focal contribution is −0.081776 of the pairwise-minus-empirical difference of −0.082110. Scoring the remaining rows with the original fold denominators reproduces the remainder of −0.000333. The corresponding focal contributions against the full and two-stage models are the same, with remainders −0.068468 and −0.089468. Smoothing raises the focal benchmark probability to 0.00434783 and lowers its contribution to −0.002516, with a remainder of −0.010555. All eight tabulated decompositions reproduce with every original row represented in the reported aggregate. [Paired comparison](../results/posthoc_q3_smoothed_comparison.csv) · [Focal contributions](../results/posthoc_q3_focal_contribution.csv)

## Q4. Ungated excess

Independent grouped refits on the same 252 supported rows reproduced each fold's binary and ungated loss pairs and the two direct paired intervals within numerical optimizer tolerance. The ungated-minus-binary differences are −0.017332 [−0.042515, 0.012071] in log loss and −0.007867 [−0.013556, −0.000890] in Brier. Brier improves under this post hoc comparison, and the log-loss interval crosses zero. The joint rule is unmet. [Direct paired comparison](../results/posthoc_q4_ungated_comparison.csv) · [Fold scores](../results/posthoc_q4_ungated_fold_scores.csv)

## Q4. Inverse loss limits

I rebuilt the 300 propagation draws and the 300 paired full and reduced behavior fits. I independently found the continuous point and draw-specific loss crossings and rounded each down to the frozen grid. This reproduced all 108 reported limits, margins, clean and ceiling support fractions, and status values. The 18 full-model, 80%-support rows match the creative release exactly on all shared quantities.

At 150 m with coupled loss, the two-voice loss limits at 70%, 80% and 90% support are 8.4%, 5.2% and 1.2% using the full curve. Using the reduced curve, they are 5.5%, 3.4% and a clean failure at 90% support. At 100 m under acoustic-only loss, two-voice reaches the 20% search ceiling with either behavior fit at each support criterion. These examples preserve the difference between a clean failure and a result at the search boundary. [Inverse sensitivity](../results/posthoc_q4_inverse_sensitivity.csv) · [Archived inverse comparison](../results/creative_q4_inverse_loss.csv)
