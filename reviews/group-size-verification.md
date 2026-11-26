# Independent numerical review of group-size comparisons

**Pass.** I used the specification frozen at `45165bd` and reconstructed all five result tables from Data02–Data11 before reading the production implementation.

## Paired response and sample coverage

I joined the natural and control trials by experiment ID, checked that their dates agreed, and formed the three strata from natural-trial group size. I recomputed the response indicators, within-pair differences, discordance and date bootstrap intervals for all six strata/subsets. The full sample has 54, 36 and 49 pairs, with response differences of 72.2, 50.0 and 30.6 percentage points. The equal-distance, equal-size subset has 26, 9 and 14 pairs, giving 73.1 [59.3, 88.0], 33.3 [0.0, 66.7] and 21.4 [−10.9, 56.4] percentage points. All counts and intervals matched, and all 300 resamples provided support in every cell. These are descriptive contrasts within observed pairs. [Pair contrasts](../results/group_size_pair_contrasts.csv)

## Strict held-out predictions

I reconstructed the 12 date folds with set operations and checked all coverage counts against the archived strict folds. I used an independently programmed Bernoulli hazard objective and analytic gradient and Hessian with a trust-region solver for both cloglog models. All 36 fold rows and six comparison rows matched to within `8.18e-7` and `1.05e-7`, respectively, across scores, contrasts and raw size coefficients.

The binary logit, cloglog with the fixed log-size offset, and cloglog with a free size coefficient gave pooled log loss/Brier of 0.5530/0.1789, 0.7376/0.2353 and 0.5488/0.1784. The free cloglog model improved both scores relative to the offset model. Relative to the logit its paired 95% intervals for the score changes were [−0.0189, 0.0103] and [−0.00320, 0.00196], so both spanned zero. The free coefficient of log group size ranged from −0.533 to −0.298 across folds. The offset comparison evaluates the combined assumptions that individual responses are independent, have the same probability within each trial, and have a specified per-bird response model with no size term. The observed group indicators leave individual probabilities and dependencies unidentified. [Fold scores and coefficients](../results/group_size_strict_folds.csv) · [Pooled scores and paired intervals](../results/group_size_strict_scores.csv)

## Q4 group-size scenarios

I reconstructed the clipped, equally weighted isotonic acoustic curves and paired independent-row acoustic draws from the CSVs, preserving the RNG consumption of the archived aligned sensitivity. I assembled the behavioral mask from its three binary indicators, independently fit the full standardized multinomial model across the original date resamples and applied the same empirical context weights to all group sizes. The common eight-bird point cutoff was 0.28759819888730354. I checked all 54 scenario rows and 108 coverage rows. The largest Q4 numerical discrepancy was `1.78e-15`, with exact agreement on the attainment counts and decisions. All local exact-size and size-stratum trial counts, responses and date counts matched.

In the 2-, 8- and 20-bird scenarios, 7, 4 and 2 of nine call–distance settings reach 80% attainment in clean conditions. Under 20% coupled loss, the corresponding counts are 4, 2 and 0. At 100 m, two-voice coupled attainment is 93.0%, 50.3% and 22.3%, with sharp conditional expected count bounds of [0.681, 1.362], [0.548, 4.384] and [0.432, 8.635]. The local natural-stimulus trial counts at those exact sizes are 1, 0 and 2. Within 25 m of the 150 m support boundary, there are no natural-stimulus trials at any exact target size. The reported Q4 differences use standardized group predictions, while the count bounds use the group indicator's logical restrictions. [Scenario table](../results/group_size_q4.csv) · [Local sample coverage](../results/group_size_q4_coverage.csv)

## Reproduction commands

The independent scripts use the raw attachments and third-party libraries, with no project-module imports. I ran them from the repository with the scripts in the system temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-size-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-size-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-size-compare.py" results "$env:TEMP/apmcm-size-independent"
```

The review found no numerical corrections necessary for the released tables.
