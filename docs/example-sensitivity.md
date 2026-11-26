# WAVERYS and propagation example sensitivity

The protocol froze at ea42111 and the computations are at a81e3ec. The WAVERYS nearshore and offshore daily means span 1.005–2.235 and 1.377–3.022 m. [Source snapshot](../sources/false-bay/README.md)

| WAVERYS cell | All 139 pairs, slope [95% interval] | 49 same-distance pairs, slope [95% interval] | Strict log loss | Strict Brier |
|---|---:|---:|---:|---:|
| Nearshore | −4.44 [−30.51, +14.07] | +21.53 [−26.50, +92.10] | 0.5555 | 0.1828 |
| Offshore | −5.44 [−27.38, +7.61] | +12.54 [−21.69, +55.75] | 0.5493 | 0.1806 |

Slopes are percentage points of daily natural-minus-control response per metre. All intervals span zero. Baseline strict log loss and Brier are 0.5530 and 0.1789. Both WAVERYS models miss the joint predictive criterion. ERA5 results appear alongside them in the supporting tables. [Slopes](../results/waverys_slopes.csv) · [Strict validation](../results/waverys_validation.csv)

The original study used three example calls per type at Brandvlei Dam. The nominal 300 comparisons per type and distance come from comparing ten reference repetitions with ten distant repetitions within each example. Consecutive groups of 100 rows represent assumed example membership. Across the 27 deletions, the point ordering is two-voice, modulated, flat throughout 0.40–0.60. At 0.70 modulated leads in 15 fits and two-voice in 12. The 0.50 radius ranges are 80.7–91.9, 127.8–153.3 and 164.6–171.8 m in flat, modulated and two-voice order. These are ranges over deletion fits. [All radii and ranks](../results/example_deletion_radii.csv)

With fixed acoustic curves and the same date behavior draws and common reference, the 80% decision changes only for clean modulated at 100 m. Full-data support is 81.3%, and the deletion range is 73.7–85.3%, with 18 of 27 fits passing. The other 17 settings retain the full-data decision. [Margins and attainment](../results/example_deletion_q4.csv) · [Summary](../results/example_deletion_q4_summary.csv)
