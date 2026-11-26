# Independent verification of Q4 losses at target radii

**Pass.** I reused the independently reconstructed date refits from the consecutive-distance analysis and regenerated the acoustic draws at the frozen seed. I fitted decreasing isotonic curves by the min–max formula and fitted the three parametric curves with an analytic Jacobian. I took the minimum clean score within each specified draw, shape and distance set and directly bisected the common retention multiplier at which the signed scores attain the fixed cutoff in 3,840 draws. Because the cutoff is positive, scores with nonpositive excess always fail. [Frozen specification](../docs/model-spec.md#q4-loss-boundaries-at-target-radii-freeze) · [Consecutive-grid verification](q4-consecutive-verification.md)

All 1,566 grid rows matched both the clean and 20/20 counts and every retained-range flag. The maximum absolute difference in required retention was 2.15e-7 across the grid. All 108 loss limits matched their capped, boundary or infeasible status. Feasible limits at 50, 100 and 150 m agreed to 3.13e-9. Counts matched at the independently fitted limits, after the specified 1e-8 probes and for the infeasible slices at zero allowance. All 12 radii, radius counts and status flags matched exactly. [Grid](../results/q4_target_loss_grid.csv) · [Boundaries](../results/q4_target_loss_boundaries.csv) · [Radii](../results/q4_target_loss_radii.csv)

| Training | Four shapes at target, 20/20 radius (m) | Shared exponent on prefix, 20/20 radius (m) | Four shapes on prefix, 20/20 radius (m) |
|---|---:|---:|---:|
| Full | 97 | 109.5 | 96 |
| Union deletion | 85.5 | 92.5 | 84 |

For the four-shape prefix after union deletion, the required retention is 0.532176, 0.710721 and 0.997737 at 50, 100 and 150 m. The maximum equal losses in each component are 20% at the scenario cap, 15.6957%, and 0.1132%, respectively. At clean 150 m the four-shape prefix count is 3,850/4,800, with a separate exact 95% Monte Carlo interval of [79.05%, 81.33%]. The interval contains 80%, while the fixed-ensemble decision meets 3,840 draws. It describes simulation precision conditional on the model and resampling scheme. The union-deleted 150 m prediction extrapolates beyond the retained ranges of both playback arms. [Boundary counts](../results/q4_target_loss_boundaries.csv) · [Range evidence](../results/q4_consecutive_ranges.csv)

I ran the independent computation and comparison from the repository root. The scripts and scratch inputs are stored in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q4-target.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-consecutive" "$env:TEMP/apmcm-q4-net-loss/loss.npz"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q4-target.py" "$env:TEMP/apmcm-q4-consecutive"
```
