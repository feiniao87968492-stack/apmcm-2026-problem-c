# Independent verification of Q4 consecutive-distance attainment

**Pass.** I rebuilt the 4,800 whole-date refits from Data02 at seed 20261201. I assigned controls their paired natural call, deleted both trials when either distance was at least 125 m, and standardized predictions at eight birds with the original natural context weights. Independently regenerated predictions at 20, 100 and 150 m match the previous fixed-distance verification. I regenerated the acoustic means from Data03–Data11 at seed 20261130 and fitted the four curves using the min–max formula for isotonic fits and an analytic Jacobian for least squares. [Frozen protocol](../docs/model-spec.md#q4-consecutive-distance-attainment-freeze) · [Previous marginal verification](q4-net-loss-verification.md)

I used a cumulative logical AND on the nonnegative indicators for each draw. For the four-shape rule, I first required all four shapes to qualify at each node. All 5,220 rows match on marginal counts, prefix counts and observed-range flags. The largest point margin difference was 3.68e-9. I also verified all 20 radii and their recorded counts, the 40 pairwise radius differences and the four observed ranges. All 20 archived marginal counts at 100 m under 20% losses and at 150 m under clean conditions match exactly, including the four-shape counts. [Node evidence](../results/q4_consecutive_counts.csv) · [Grid radii](../results/q4_consecutive_radii.csv) · [Radius differences](../results/q4_consecutive_differences.csv)

| Training | Scenario | Shared point last | Shared marginal last | Shared marginal prefix | Shared same-draw prefix | Four-shape same-draw prefix |
|---|---|---:|---:|---:|---:|---:|
| Full | Clean | 150 | 150 | 150 | 150 | 150 |
| Union deletion | Clean | 150 | 150 | 150 | 150 | 150 |
| Full | 20% loss in each component | 150 | 110 | 110 | 109.5 | 96 |
| Union deletion | 20% loss in each component | 119.5 | 94.5 | 94.5 | 92.5 | 84 |

Radii are metres on the 0.5 m grid. Values of 150 m are grid caps. At clean 150 m after union deletion, the shared count changes from 4,002 marginally to 3,994 when the same draws must also pass at every shorter node. Across all four shapes, the corresponding counts are 3,858 and 3,850, leaving ten draws above the decision threshold. The full-data natural and control ranges are 20–200 m and 5–200 m with 58 trials each. After union deletion the ranges are 20–100 m and 5–120 m with 49 trials each, placing the 150 m prediction beyond both ranges. [Observed ranges](../results/q4_consecutive_ranges.csv)

I ran the independent scripts from the repository root. The scripts and scratch arrays are in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q4-consecutive.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-consecutive" "$env:TEMP/apmcm-q4-net-loss/loss.npz"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q4-consecutive.py" "$env:TEMP/apmcm-q4-consecutive" "<attachment directory>/date"
```
