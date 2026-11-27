# Independent verification of Q2 partial pooling

**Pass.** I rebuilt the equal-weight fidelity targets from Data03–Data11 and independently generated the 300 wide-row draws at seed 20261127. I preserved each row's distance columns, sampled independently by representation and advanced the random stream for the archived aligned-row sensitivity between calls with matching missingness masks. Each fit and its held-out target use the same draw. Training stops at 32, 64 and 128 m for the 64, 128 and 256 m holdouts, respectively. [Frozen specification](../docs/model-spec.md#q2-partial-pooling-of-attenuation-exponents-freeze)

I used bounded nonlinear least squares with analytic derivatives for the shared, separate and partially pooled fits, with ftol, xtol and gtol all set to 1e-11. For partial pooling the residual vector contains the fidelity errors divided by the square root of the number of training cells, and the centered log exponents multiplied by the square root of (lambda divided by three). The shared fit initializes the partially pooled parameters. I independently solved the full-fit crossing formula and applied the 4–256 m bounds. I reconciled all 45 holdouts, 80 score rows, 224 contrasts and 60 fit rows from ae5f218. Maximum absolute discrepancies were 9.6e-7 for predictions, scores and contrast entries, 9.6e-6 for exponents, 5.7e-4 m for scales and 7.8e-7 m for full-fit radii. Crossing statuses agree. These small numerical differences arise from using analytic derivatives in the independent optimization. [Holdouts](../results/q2_partial_pooling_holdouts.csv) · [Scores](../results/q2_partial_pooling_scores.csv) · [Contrasts](../results/q2_partial_pooling_contrasts.csv) · [Fits and radii](../results/q2_partial_pooling_fits.csv)

| Fit | RMSE pooled across 128 and 256 m | Paired difference vs shared [95% interval] | Paired difference vs separate [95% interval] |
|---|---:|---:|---:|
| Shared | 0.11236 | | |
| Separate | 0.10859 | | |
| Lambda 0.0025 | 0.10703 | −0.00532 [−0.00726, −0.00333] | −0.00156 [−0.00849, 0.00323] |
| Lambda 0.01 | 0.11067 | −0.00169 [−0.00233, −0.00102] | +0.00208 [−0.00509, 0.00712] |
| Lambda 0.04 | 0.11190 | −0.00045 [−0.00063, −0.00027] | +0.00331 [−0.00400, 0.00837] |

The primary penalty meets the improvement criterion against the shared exponent alone. At 64 m, the separate, primary partially pooled and shared flat-call signed errors are −0.50113, −0.00537 and −0.00150, respectively. For the primary full fit the flat, modulated and two-voice exponents are 2.555, 2.995 and 3.386. Their 0.50 radii are 86.15, 143.58 and 170.08 m, and their 0.70 radii are 45.93, 84.17 and 90.89 m. The comparison is follow-up evidence from the same distance targets, and the intervals condition on the available rows and the sampling convention with unknown acquisition groups.
