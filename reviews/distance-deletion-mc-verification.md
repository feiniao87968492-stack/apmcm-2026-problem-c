# Independent verification of distance-deletion Monte Carlo precision

**Pass.** I applied the specification frozen at `0e2899e`. Before consulting the production script, I generated the 4,800 acoustic and date draws from the frozen seeds and reconstructed deletion by pivoting the trial distances by experiment and arm. I reused the released Q2 resampler, attenuation and Q3 mask fits, then independently evaluated the attenuation formula at 20, 100 and 150 m. For each resample I mixed the positive mask sum across the original full-data context weights. I calculated both fixed-within-draw clean references from the full fit and the isotonic 20 m fidelity. I applied the three target margins directly. [Frozen specification](../docs/model-spec.md#monte-carlo-precision-of-distance-deletion-freeze)

I independently inverted the two binomial tails for each 95% Clopper–Pearson interval. Each 80% point-rule flag and interval-based status matched production exactly, as did the success counts and valid draw counts in all 48 rows. Support shares matched exactly. The largest endpoint discrepancy was 2.23e-16. Every prefix retained all requested draws. The archived rows reproduce the counts in the published distance-deletion table. [Monte Carlo results](../results/distance_deletion_mc.csv) · [Archived counts](../results/distance_deletion_points.csv)

| Target | Full | Drop 125–175 m | Drop above 175 m | Drop both |
|---|---:|---:|---:|---:|
| Clean two-voice own-net at 150 m | 4527 | 4394 | 4177 | 4002 |
| Coupled two-voice own-net at 100 m | 4116 | 3883 | 3788 | 3575 |
| Clean modulated gross at 100 m | 4074 | 3981 | 4147 | 4049 |

Counts are out of 4,800. For clean two-voice at 150 m, the union deletion changes from archived 239/300 with an interval containing 80% to 4,002/4,800, or 83.38% [82.29%, 84.42%]. For coupled two-voice at 100 m, the 4,800-draw intervals straddle 80% after near deletion [79.75%, 82.00%] and far deletion [77.73%, 80.06%]. Its full-fit interval is above 80% and its union-deletion interval is below. All four clean modulated gross intervals at 100 m lie above 80%. These are pointwise intervals for Monte Carlo error under the fixed model and resampling law. [Monte Carlo results](../results/distance_deletion_mc.csv)

## Reproduction

I ran the independent verifier from the repository root, writing its output to the local temporary directory. The script is stored in that directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-distance-mc-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-distance-mc-independent"
```
