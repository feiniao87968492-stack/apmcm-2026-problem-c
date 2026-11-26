# Independent verification of Q4 envelope-weight attainment

**Pass.** I regenerated the released 4,800 acoustic draws from Data03–Data11 with seed 20261130 and the 4,800 whole-date draws from Data02 with seed 20261201. I recovered the union deletion by removing both trials of any experiment with a recorded distance at or above 125 m. I used the released multinomial refitter with the original eight-bird natural-context weights. I evaluated fidelity directly with a vectorized min–max formula for the decreasing isotonic fit, interpolated it in log distance and combined the fixed behavior probabilities with each reference. [Frozen specification](../docs/model-spec.md#q4-envelope-weight-attainment-freeze)

All 60 checkpoint counts match exactly and each uses all 4,800 draws. Point margins and percentile endpoints match within 4.17e-16. The archived margins and counts and their differences also match. At equal weights the isotonic counts for the point cases in the frozen order are 4,593, 4,215 and 3,949 for full training and 4,142, 3,722 and 3,927 after union deletion. The corresponding archived shared-exponent counts are 4,527, 4,116 and 4,074 for full training and 4,002, 3,575 and 4,049 after union deletion. [Checkpoint table](../results/q4_envelope_attainment_points.csv)

I checked the five point roots by a direct bracketed solve and inspected both sides of each one. All weights match within 1.34e-15. I also evaluated the entire path on a grid of 2,049 weights and independently bisected each 80% decision boundary. All 12 interval decisions match the grid and both endpoint counts. The 11 interior boundaries agree within 5.02e-11 in weight when counting direct margins at or above −1e-12. Each interior endpoint qualifies with 3,840 draws and the adjacent failing count is 3,839. The full-training clean two-voice margin at 150 m with a recalculated reference qualifies across the entire path. [Point zeros](../results/q4_envelope_attainment_zeros.csv) · [Attainment intervals](../results/q4_envelope_attainment_intervals.csv)

| Focal margin after union deletion | Upper envelope weight with fixed reference | Upper envelope weight with recalculated reference |
|---|---:|---:|
| Clean two-voice own-net at 150 m | 0.490312 | 0.751721 |
| 20% coupled two-voice own-net at 100 m | 0.293838 | 0.154242 |
| Clean modulated gross at 100 m | 0.372357 | 0.489427 |

Both reference conventions use the full-data behavior fit at 20 m. Their decision differences therefore arise from how the acoustic weight enters the reference as well as the score. The attainment probabilities condition on paired resampling and the released models. The union prediction at 150 m extrapolates beyond retained playback distances.

I ran the two independent scripts from the repository root. The scripts and scratch arrays are in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q4-envelope.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q4-envelope"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q4-envelope.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q4-envelope"
```
