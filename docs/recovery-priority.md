# Historical correlation recovery priorities

The protocol froze at `b0ae1b4` and ran at `6efac25`. One unit is a call type and distance across three representations. Nine of 21 units have missing scores. Each chosen unit takes a common stipulated value of −1, 0 or +1 across its missing scores, independently of the values assigned to other chosen units. All remaining missing scores are bounded by [−1,1]. The clean two-voice minus modulated area-index gap without recovery is [−0.229075, 0.228278], with width 0.457353. [Unit audit](../results/recovery_units.csv) · [Case enumeration](../results/recovery_cases.csv)

| Budget | Selection rule | Selected units | Missing correlations covered | Smallest width reduction | Largest width reduction |
|---|---|---|---:|---:|---:|
| One | Both rules | Two-voice 128 m | 330 | 41.45% | 55.92% |
| Two | Maximize minimum reduction | Modulated 128 m and two-voice 128 m | 540 | 73.51% | 87.97% |
| Two | Maximize missing count | Two-voice 128 m and 256 m | 600 | 57.63% | 61.37% |

The enumeration covers 45 plans and 351 value assignments. Among the nine assignments for the two-unit minimax plan, seven give a strict point ordering of two-voice and modulated in both clean and 20% coupled conditions. Four favor two-voice and three favor modulated. The corresponding count is five for the largest-missing-count plan. The reported frequencies count stipulated cases. Date-block intervals and direction shares are conditional on each fixed pair of completion curves. [Plan rankings](../results/recovery_plans.csv) · [Pairwise gap bounds and intervals](../results/recovery_gaps.csv)

For example, assigning zero at both 128 m units reduces the two-voice radius bounds at fidelity 0.50 from 73.8–251.2 m to 95.5–114.1 m and at 0.60 from 65.4–190.7 m to 67.9–89.0 m. The modulated bounds collapse to 109.3 m and 88.8 m in that case. All radius endpoints retain the archived acoustic support status. [Selected-plan radius bounds](../results/recovery_radii.csv)

The priority is conditional on the clean target gap, equal unit costs and the three stipulated values. It describes hypothetical retrieval of historical measurements.

## Continuous recovery certificate

The continuous protocol was frozen at `cff2038` and evaluated at `49c0545`. The endpoints and every equality between adjacent contiguous-block means partition the recovered knot interval into segments on which both isotonic fits are affine. Log-distance interpolation and the area-weighted index preserve this affine dependence. The gap width adds the two call widths, so the two-call plan can maximize the widths individually.

| Loss | Budget | Baseline width | Worst residual width | Minimum shrinkage | Minimum fraction | Three-value minus continuous |
|---|---:|---:|---:|---:|---:|---:|
| Clean | 1 | 0.457353 | 0.267795 | 0.189558 | 41.45% | 0 |
| Clean | 2 | 0.457353 | 0.121173 | 0.336179 | 73.51% | 0 |
| 20% coupled | 1 | 0.302256 | 0.176873 | 0.125383 | 41.48% | 0 |
| 20% coupled | 2 | 0.302256 | 0.080302 | 0.221954 | 73.43% | 0 |

Under both losses, the lower clipped knot 0.04744 for two-voice at 128 m attains the worst case. In the two-unit plan, any modulated knot in [0.190761, 0.657428] attains the same residual width because recovering modulated at 128 m resolves all of its missing correlations. The highest remaining three-value bounds are 0.146622 at budget one and 0.263556 at budget two. The continuous winners exceed them by 0.042936 and 0.072623 in clean conditions, excluding all 8 and 35 competing plans respectively. The 20% coupled rows evaluate those same plans. [Certificate](../results/recovery_continuous.csv) ? [Breakpoints](../results/recovery_breakpoints.csv)
