# Independent verification of Q1 recording-group candidate sets

**Pass.** I read the 108 Data01 recordings, independently indexed the 16 sorted date-by-location groups and repeated the 16 seeded fit/calibration allocations. Each fold used six fitting groups and nine calibration groups, with 38–83 calibration recordings. I fit the six-feature standardized logistic model and aligned the probability columns to the specified call order. I computed the weighted thresholds with exact rational masses and the other thresholds by sorting calibration rows or group maxima. All 96 threshold and split rows and 128 fold count rows match exactly. [Frozen specification](../docs/model-spec.md#q1-candidate-sets-for-a-held-out-recording-group) · [Thresholds](../results/q1_candidate_sets_thresholds.csv) · [Fold counts](../results/q1_candidate_sets_folds.csv)

I used 4,800 shared whole-group draws at seed 20261127 to recalculate each count or ratio, including the singleton-error rate only where a draw contains singletons. All 120 summaries and 195 paired rows match. The largest absolute discrepancies across point scores, interval endpoints and paired contrasts were 2.78e-16. All numerator and denominator checks matched to 1.78e-15, and the valid draw counts match exactly. Top two gives zero singletons and its singleton-error rate is undefined. Both 90% group rules give one misclassified singleton in the point sample and 3,117 valid draws for their singleton-error rate. [Summary](../results/q1_candidate_sets_summary.csv) · [Paired contrasts](../results/q1_candidate_sets_paired.csv)

| Candidate rule | Recordings covered | Equal-group coverage | Groups fully covered | Mean size | Two-voice covered |
|---|---:|---:|---:|---:|---:|
| Top one | 42/108 | 40.59% | 2/16 | 1.000 | 1/24 |
| Top two | 78/108 | 66.44% | 3/16 | 2.000 | 8/24 |
| Pooled row, 80% | 82/108 | 75.78% | 6/16 | 2.204 | 12/24 |
| Pooled row, 90% | 102/108 | 88.27% | 10/16 | 2.685 | 21/24 |
| Equal group, 80% | 100/108 | 86.86% | 9/16 | 2.620 | 20/24 |
| Group maximum, 80% | 106/108 | 97.67% | 14/16 | 2.833 | 24/24 |
| Equal group and group maximum, 90% | 107/108 | 99.75% | 15/16 | 2.944 | 24/24 |

Relative to top two, the 80% equal-group rule gains 0.204 [0.129, 0.297] in recording coverage and adds 0.620 [0.420, 0.754] labels per set. It includes all three labels for 73 recordings. The 90% group rules coincide because all finite calibration scores together carry exactly 0.90 mass, so the lower weighted 90th percentile is the largest calibration score. Both rules return all three labels for 103 recordings. [Summary](../results/q1_candidate_sets_summary.csv) · [Paired contrasts](../results/q1_candidate_sets_paired.csv)

The guarantee for pooled calibration uses exchangeable rows. Under exchangeability of calibration and future recording groups conditional on the fit and label-blind allocation, the equal-group threshold covers a uniformly selected recording within the new group marginally. To see this, give each group one tenth of the probability mass and distribute that mass uniformly over its recordings. Replacing the new group's individual scores by infinity can only raise the complete-sample quantile. Exchangeability gives the random new group the average probability of coverage across the ten groups. Group maxima instead use one score per group and target simultaneous group coverage. The 24 two-voice recordings provide an empirical coverage diagnostic. Repeated dates or sites can affect group exchangeability, and the bootstrap describes the single realized allocation schedule.

I ran the independent script from the repository root and stored the scratch files in the local temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q1-sets.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q1-sets"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q1-sets.py" "$env:TEMP/apmcm-verify-q1-sets"
```
