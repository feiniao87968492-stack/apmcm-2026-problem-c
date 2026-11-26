# Independent verification of Q4 attenuation-shape propagation

**Pass.** I regenerated the 4,800 acoustic draws at seed 20261130 and reused the independent 4,800 date refits from the envelope-weight verification at seed 20261201. The date refits remove both trials of each pair with either distance at or above 125 m for union deletion. I evaluated isotonic fidelity through the min–max formula and fitted the three parametric curves with an analytic Jacobian. I combined the four equal-weight fidelities with the same eight-bird context-standardized behavior estimates and recomputed the full-data 20 m isotonic cutoff. [Frozen specification](../docs/model-spec.md#q4-attenuation-shape-propagation-freeze) · [Independent date refits](q4-envelope-attainment-verification.md)

I independently recomputed all 24 configurations. Every attainment count, gain, loss and decision flag matches exactly. Maximum absolute differences were 6.49e-9 for point fidelity, 3.67e-9 for point margin and 1.79e-8 across the reported paired percentile endpoints. All counts use 4,800 valid draws. The six isotonic and six shared-exponent point margins also match their archived values to 1.05e-16, with identical attainment counts. [Comparison table](../results/q4_shape_propagation.csv) · [Isotonic archive](../results/q4_envelope_attainment_points.csv) · [Shared-exponent archive](../results/distance_deletion_mc.csv)

| Training | Focal margin | Isotonic | Fixed exponent | Shared exponent | Separate exponents |
|---|---|---:|---:|---:|---:|
| Full | Clean two-voice own-net, 150 m | 4,593 | 4,468 | 4,527 | 4,638 |
| Full | Coupled two-voice own-net, 100 m | 4,215 | 3,773 | 4,116 | 4,381 |
| Full | Clean modulated gross, 100 m | 3,949 | 3,747 | 4,074 | 4,129 |
| Union deletion | Clean two-voice own-net, 150 m | 4,142 | 3,858 | 4,002 | 4,261 |
| Union deletion | Coupled two-voice own-net, 100 m | 3,722 | 3,039 | 3,575 | 4,034 |
| Union deletion | Clean modulated gross, 100 m | 3,927 | 3,708 | 4,049 | 4,119 |

All shapes meet the 3,840-draw rule for the clean two-voice margin at 150 m, including 3,858 draws for fixed exponent under union deletion. Relative to shared exponent, separate exponents change one decision, the coupled two-voice margin at 100 m after union deletion. They raise that point margin from 0.024219 to 0.039766, a paired difference of +0.015547 [0.011109, 0.020318], with 459 gaining draws and zero losing draws. Fixed exponent changes three passing decisions to failing. The decision comparisons condition on the common reference and the fixed behavior fits. The 150 m prediction after union deletion remains extrapolated.

I ran the independent fitting and comparison scripts from the repository root. The scripts, scratch results and previously reconstructed date fits are in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q4-shape.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-shape" "$env:TEMP/apmcm-verify-q4-envelope/behavior.npy"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q4-shape.py" "$env:TEMP/apmcm-q4-shape"
```
