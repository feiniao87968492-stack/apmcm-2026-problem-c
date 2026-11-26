# Independent verification of the Q4 distance-deletion diagnosis

**Pass.** I independently reproduced the frozen analysis at `ddb3e30` and compared all four exports in the temporary production run and the tracked results. All four pair-overlap rows, 48 training counts and 72 local coverage rows agree exactly. All 144 prediction and score rows agree to within $2.09\times10^{-16}$, with exact draw counts and 80% flags. [Frozen protocol](../docs/model-spec.md#q4-distance-deletion-freeze) · [Decision table](../results/distance_deletion_points.csv)

## Retained pairs and support

I identified the excluded experiment IDs from the raw trial distances, then removed both arms by ID. Every retained experiment had one natural and one control row on the same date. The 125–175 m inclusive band and the greater-than-175 m band each flag 14 pairs. Two pairs belong to both bands, leaving 26 pairs in their union. The full, near-deletion, far-deletion and union-deletion fits retain 139, 125, 125 and 113 pairs respectively. Natural responder counts are 90, 81, 78 and 71, and control responder counts are 18, 17, 15 and 14. The near-deletion fit has no observations in the 150 m local window. The union retains no distance above 120 m, with two-voice natural and control maxima of 100 and 120 m. [Overlap](../results/distance_deletion_overlap.csv) · [Training counts](../results/distance_deletion_training.csv) · [Local coverage](../results/distance_deletion_coverage.csv)

## Predictions and decisions

I reconstructed the masks and full Q3 design from Data02 and refitted the multinomial logistic model using the frozen penalty, solver defaults and training-based scaling. I generated the same 300 original date draws, used fixed empirical natural-context weights at eight birds, and used the archived Q2 bootstrap and shared-exponent fitter to reconstruct fidelity. All 300 draws are valid under every deletion. I independently constructed the point and draw cutoffs from the full-data fit and applied the coupled-response reduction and margin formulas. The 36 full-data rows match the published gross and own-net baseline within $2.23\times10^{-16}$, and all decisions match exactly. [Baseline](../results/control_subtraction_points.csv)

At 150 m, clean two-voice gross attainment is 73.3%, 64.7%, 55.0% and 46.0% in full, near, far and union order. Own-net attainment is 90.7%, 88.7%, 86.3% and 79.7%, with the union attaining the cutoff in 239 of 300 draws, one short of the 80% rule. Under 20% coupled loss, own-net attainment is 49.7%, 38.3%, 35.7% and 30.0%. For the union, the natural and control clean probabilities are 0.504 and 0.045, compared with 0.647 and 0.081 in the full fit. The clean gross and own-net paired margin changes are respectively −0.0776 [−0.1149, 0.0117] and −0.0577 [−0.0891, 0.0219]. The four other decision changes are at 100 m. Near deletion changes the clean modulated gross decision, and all three deletions change the coupled two-voice own-net decision. Each change is from passing to failing, and the results describe sensitivity to the retained training data. [Results](../results/distance_deletion_points.csv)

## Reproduction

The verifier and comparator ran as temporary scripts from the repository root. The verifier imports the archived acoustic resampling and fitting routines. It independently implements the behavior and decision calculations.

```powershell
$env:PYTHONPATH = (Get-Location).Path
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-distance-deletion-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-distance-deletion-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-distance-deletion-compare.py" "<attachment directory>/date" "$env:TEMP/apmcm-distance-deletion-independent" "$env:TEMP/apmcm-distance-production" results
```
