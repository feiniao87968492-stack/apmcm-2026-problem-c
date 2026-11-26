# Independent verification of Q4 response sensitivity at 6 dB

**Pass.** I reused the independently rebuilt whole-date fits and regenerated the acoustic draws with the released seeds and order. I fitted the isotonic curves by their min–max formula and the parametric curves with an analytic Jacobian. I computed the 6 dB local and matched uniform two-voice attenuation ratios for each draw, then applied the attenuation and positive-response-excess adjustment directly. I evaluated the four-shape endpoint and prefix counts and bisected each upper limit using the signed-score inequality. [Frozen protocol](../docs/model-spec.md#q4-response-sensitivity-at-6-db-freeze) · [Paired-input verification](q4-matched-noise-verification.md)

All eight rows match exactly at the five fixed sensitivity levels and at the boundary and probe, including the archived acoustic-only and coupled prefix counts. The largest absolute difference in the upper limits is 4.67e-7. All boundaries are interior. Each inclusive boundary qualifies in 3,840 of 4,800 draws, and increasing lambda by 1e-7 reduces the count to 3,839. Endpoint-minus-prefix differences agree within 1e-6. [Results](../results/q4_response_sensitivity.csv) · [Archived endpoints](../results/q4_matched_noise_targets.csv)

| Training set | Noise ratio | Endpoint maximum | Prefix maximum | Endpoint minus prefix |
|---|---|---:|---:|---:|
| Full | Local | 0.683627 | 0.683627 | 0.000000 |
| Full | Matched uniform | 0.683627 | 0.667481 | 0.016146 |
| Union deletion | Local | 0.344207 | 0.339062 | 0.005146 |
| Union deletion | Matched uniform | 0.344207 | 0.319405 | 0.024803 |

Local and matched uniform attenuation give identical endpoint counts because the uniform multiplier uses the same draw's local multiplier at 100 m. The prefix additionally tests every shorter node. The limits apply to the hypothetical 6 dB mapping and condition on the fitted scores and the paired-resampling distribution.

I ran the independent solver from the repository root. The script and scratch arrays are in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q4-response.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-consecutive" "$env:TEMP/apmcm-q4-net-loss/loss.npz"
```
