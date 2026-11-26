# Independent verification of Q2 attenuation shape and weight

**Pass.** I regenerated the clipped available-value means for all five envelope weights. I used the min–max formula for decreasing isotonic fits and an independently coded physical model with an analytic Jacobian in least squares. The starting points, bounds and tolerances followed the frozen protocol. Radius roots came from a bracketed solve in log distance after checking the 4 and 256 m bounds. I left out each of the five distances simultaneously for all calls. [Frozen protocol](../docs/model-spec.md#q2-attenuation-shape-by-common-representation-weight)

All 300 holdout predictions matched within 5.01e-7 and all 80 RMSEs within 7.13e-8. Across 40 model, weight and threshold combinations, all bound statuses and rank labels match. The largest absolute gap difference was 3.83e-5 m. At equal weights, the production results match the archived 45 holdouts to 1.84e-9 and 12 RMSEs to 4.68e-10. All 12 overlapping archived radius statuses match. Their largest differences were 3.41e-7 m for the shared-exponent curve and 5.69e-14 m for isotonic. These numerical comparisons include the sensitivity of the least-squares solver to small target differences and the independent analytic Jacobian. [Holdouts](../results/q2_shape_rank_holdouts.csv) · [RMSEs](../results/q2_shape_rank_rmse.csv) · [Radii](../results/q2_shape_rank_radii.csv)

At equal weights, the shared and separate exponent fits have pooled RMSEs of 0.055257 and 0.046770. The 15.36% reduction meets the prespecified 5% cutoff, and all three call RMSEs improve, including modulated from 0.047352 to 0.047334. My analytic-Jacobian calculation gives a relative improvement of 0.153593383, compared with 0.153593416 in production. The separate-exponent curve meets the adoption rule for this Q2 comparison. The integrated Q4 analyses use their published inputs. [Decision](../results/q2_shape_rank_decision.csv)

I regenerated the 300 equal-weight acoustic draws with seed 20261127, including the intervening aligned stream used by Q2. Across all 2,400 draw rows, radius and gap discrepancies were at most 7.17e-5 m, support and rank labels matched exactly, and all sign and rank frequencies matched exactly. The largest discrepancy across conditional gap percentiles was 1.63e-6 m. [Draws](../results/q2_shape_rank_draws.csv) · [Gap summary](../results/q2_shape_rank_gaps.csv) · [Rank summary](../results/q2_shape_rank_ranks.csv)

| Shape | Equal-weight 0.70 modulated minus two-voice point radius (m) | Draws with modulated leading |
|---|---:|---:|
| Isotonic | −1.567 | 28/300 |
| Fixed exponent | +3.103 | 300/300 |
| Shared exponent | +0.683 | 232/300 |
| Separate exponents | −21.804 | 0/300 |

At 0.50 and equal weights all four models rank two-voice above modulated above flat in every draw. The 0.70 draw comparison conditions on the representation-wise wide-row resampling scheme. Acquisition-unit identifiers are unavailable.

I ran the independent fitting and comparison scripts from the repository root. The scripts and scratch tables are in the local temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q2-shape.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q2-shape"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q2-shape.py" "$env:TEMP/apmcm-verify-q2-shape"
```
