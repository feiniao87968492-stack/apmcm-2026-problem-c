# Independent verification of Q4 local and matched uniform noise

**Pass.** I reused the independently generated full and union-deleted date refits, regenerated the 4,800 acoustic draws and evaluated equal-weight fidelity using the isotonic min–max formula and parametric least squares with an analytic Jacobian. I calculated the two-voice retention as the square root of the clean-to-noisy variance ratio, keeping the common clean 20 m isotonic net cutoff fixed. The local attenuation uses the ratio at each node. The matched uniform attenuation applies the same draw's ratio at 100 m throughout. I applied each retained acoustic ratio to the signed positive-excess score formula and checked four-shape prefix attainment by logical accumulation. All 522 clean prefix counts match the independently reconstructed archived grid. [Frozen protocol](../docs/model-spec.md#q4-local-versus-matched-uniform-noise-freeze) · [Consecutive-grid verification](q4-consecutive-verification.md)

All 16 target rows match exactly at 0, 3 and 6 dB, including statuses and aggregate boundaries. I directly bisected the count as a function of increased noise in dB. The largest absolute discrepancy between the independent and production dB limits was 5.93e-7. Each of the four interior limits has 3,840 passes in the independent solve and 3,839 after an increase of 1e-7 dB. The other 12 limits are capped at 6 dB. Target prefixes at 50 and 100 m are inside both retained arm ranges in the two analysis samples. [Targets](../results/q4_matched_noise_targets.csv)

| Fit | Coupled relation | 100 m count at 6 dB | Maximum noise increase at 100 m (dB) | Prefix radius at 6 dB (m) |
|---|---|---:|---:|---:|
| Full | Local | 3,230 | 5.316405 | 93.5 |
| Full | Matched uniform | 3,168 | 5.279167 | 79.0 |
| Union deletion | Local | 2,430 | 4.502439 | 89.0 |
| Union deletion | Matched uniform | 2,330 | 4.456254 | 72.5 |

All 16 radii, counts at 20 m, counts at the last passing node, next-node counts, grid cap labels and retained-range flags match exactly. The 6 dB coupled radii are based on the net prefix criterion across all four shapes and the same 4,800 pairs of acoustic and date draws. Range flags refer to the playback data retained in each fit. These hypothetical noise mappings use a matched ratio at 100 m independently within each acoustic draw. [Radii](../results/q4_matched_noise_radii.csv)

I ran the independent script from the repository root. The script and reconstructed inputs are in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q4-matched-noise.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-consecutive" "$env:TEMP/apmcm-q4-net-loss/loss.npz"
```
