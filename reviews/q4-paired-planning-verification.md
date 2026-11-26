# Independent verification of Q4 paired planning

I used the specification frozen at `2bdbc6f` and compared the results with `b47db32`. My independent script rebuilds the released Q3 design and multinomial fit from Data02. It uses coefficients relative to the zero mask and transforms the standardized slope penalty to that parameterization. I used a five-point numerical derivative of each margin, including its clean cutoff. The three margin values match the archived estimates to absolute tolerance \(10^{-12}\). [Frozen protocol](../docs/model-spec.md#paired-dependence-allocation-sensitivity-freeze) · [Archived margins](../results/control_subtraction_points.csv)

For each historical or prospective pair, I solved the binary joint-table equation on its Fréchet interval using Brent's method. I explicitly enumerated all supported mask pairs and checked that the joint distribution preserves both marginal mask distributions and the requested binary odds ratio. I calculated the meat by summing outer products of the two unpenalized scores combined, weighted by their joint probabilities. Current pairs use recorded covariates. Proposed pairs use the original context weights. At independence the expected meat matches the marginal information without ridge, both for the current sample and each of the 12 proposed cells, to absolute tolerance \(10^{-12}\). [Strict fold inputs](../results/strict_q3_pair_folds.csv)

| Plan | Independence | Fold minimum | Fold midpoint | Fold maximum | Pairs at 20 m | Pairs at 150 m | Independence cost vs Fisher |
|---|---:|---:|---:|---:|---:|---:|---:|
| Uniform | 0.513439 | 0.509654 | 0.505874 | 0.503162 | 30 | 30 | 0.081460 |
| Constrained Fisher | 0.431979 | 0.427069 | 0.427727 | 0.428582 | 66 | 22 | 0 |
| Midpoint greedy | 0.433592 | 0.428707 | 0.423741 | 0.422293 | 66 | 23 | 0.001614 |
| All-scenario greedy | 0.441178 | 0.437604 | 0.436638 | 0.437212 | 71 | 18 | 0.009199 |

The entries for each scenario are maximum variance ratios across the three margins relative to current data in that scenario. Independence supplies the largest ratio across scenarios for all four plans. The released constrained Fisher allocation gives the smallest such ratio among the compared plans. The midpoint greedy plan improves its targeted scenario relative to Fisher and incurs an independent-scenario cost of 0.001614. The all-scenario greedy result is a stepwise allocation and its final objective is 0.441178. [Production summary](../results/q4_paired_planning_summary.csv)

All 48 allocation rows and the 20 and 150 m totals agree exactly. The 48 precision rows and four summary rows agree within \(1.18\times10^{-13}\) across the compared numerical fields. All four allocations sum to 120 and assign at least ten pairs to each of the three focal cells. [Allocations](../results/q4_paired_planning_allocations.csv) · [Precision](../results/q4_paired_planning_precision.csv)

## Reproduction

I ran the following commands from the repository root with the independent scripts in the system temporary directory. The verifier imports no project modules.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-paired-independent.py" "<attachment directory>/date" results "$env:TEMP/apmcm-paired-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-paired-compare.py" results "$env:TEMP/apmcm-paired-independent"
```
