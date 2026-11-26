# Independent verification of Q4 two-loss net boundaries

**Pass.** I regenerated the 4,800 acoustic draw means at seed 20261130 and used the previously independently rebuilt whole-date refits at seed 20261201. I fitted the four curves separately using the isotonic min–max formula and an analytic Jacobian for least squares. I used fixed natural-context weights and the full-data clean 20 m isotonic own-net cutoff. The cutoff was 0.194371 at the point fit and ranged from 0.076086 to 0.309759 across draws. Every cutoff was positive. [Frozen specification](../docs/model-spec.md#q4-two-loss-net-boundary-freeze) · [Date refit verification](q4-envelope-attainment-verification.md)

For each shape I computed the 3,840th smallest requirement independently. For the joint criterion I also evaluated the minimum signed score over the four shapes within each draw. Fixed exponent gives the largest requirement in all finite draws and binds all four joint limits. All 20 requirements, shape labels and summary counts matched, with maximum requirement error 8.64e-9. All 180 direct checkpoint counts and all 16 overlapping archived counts matched exactly. [Requirements](../results/q4_net_loss_requirements.csv) · [Checkpoint counts](../results/q4_net_loss_counts.csv) · [Archived counts](../results/q4_shape_propagation.csv)

I recomputed each of the 120 boundary rows. The 54 solved boundaries, 48 capped values and 18 infeasible slices matched their labels, and feasible limits differed by at most 9.60e-9. At each independently solved boundary I found 3,840 qualifying draws with the frozen relative equality tolerance and 3,839 after the specified 1e-8 increment along the boundary's coordinate. Absolute boundary positions differ slightly between the analytic and numerical Jacobian fits, so each exact count check uses its own fitted equality. Capped counts and rejected zero-allowance counts matched the published table. [Boundary table](../results/q4_net_loss_boundaries.csv)

| Training | Distance (m) | Joint requirement | Maximum equal loss in both components | Clean joint count out of 4,800 |
|---|---:|---:|---:|---:|
| Full | 100 | 0.647066 | 0.195596 | 4,777 |
| Full | 150 | 0.813826 | 0.097877 | 4,468 |
| Union deletion | 100 | 0.706113 | 0.159695 | 4,762 |
| Union deletion | 150 | 0.995704 | 0.002150 | 3,858 |

After union deletion at 150 m, the largest loss allowed in either component alone is 0.004296. The limits describe the specified hypothetical acoustic and response losses under the fitted curves and paired resampling. The union-deleted 150 m behavior estimate extrapolates beyond the retained playback distances.

I ran the independent computation and comparison from the repository root. The scripts and scratch data are stored in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q4-net-loss.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-net-loss" "$env:TEMP/apmcm-verify-q4-envelope/behavior.npy"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q4-net-loss.py" "$env:TEMP/apmcm-q4-net-loss"
```
