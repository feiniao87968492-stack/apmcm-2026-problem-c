# Independent verification of Q4 bounded context imbalance

**Pass.** I evaluated the linear opportunity pass fraction using exact rational arithmetic and the published clean and +6 dB pass counts. For each displacement, I independently enumerated the vertices by fixing two context shares at their lower or upper limits and solving for the third using the weighted overall share constraint. I retained intersections inside all three intervals and evaluated the objective at each. An optimum occurs at one of these intersections because the feasible set is the intersection of a box and a plane and the score is linear. [Frozen specification](../docs/model-spec.md#q4-bounded-context-imbalance-at-half-exposure-freeze) | [Archived context counts](../results/q4_context_exposure_counts.csv)

At zero displacement the bounds reproduce the archived uniform-exposure row in both fits. At 50 percentage points, both values and allocations reproduce the respective archived minimum and maximum at half overall exposure. The check below gives the sharp pass fractions in percent. [Archived comparisons](../results/q4_context_exposure_checks.csv)

| Displacement (pp) | Full minimum | Full maximum | Union deletion minimum | Union deletion maximum |
|---:|---:|---:|---:|---:|
| 0 | 82.077188 | 82.077188 | 73.792491 | 73.792491 |
| 10 | 81.210567 | 82.943810 | 72.299176 | 75.285806 |
| 20 | 80.343945 | 83.810432 | 70.805860 | 76.779122 |
| 30 | 79.477323 | 84.677053 | 69.312545 | 78.272437 |
| 40 | 78.610701 | 85.543675 | 67.819230 | 79.765752 |
| 50 | 77.744080 | 86.410297 | 66.325914 | 81.259068 |

I solved the relevant linear bound for equality at 4/5 and enumerated vertices again at each exact crossing. The two allocations below are ordered after feeding, commuting, and searching. Each gives an exact weighted exposure of 1/2 and pass share of 4/5.

| Fit and bound | Exact displacement | Displacement (pp) | Attaining shares |
|---|---:|---:|---|
| Full minimum | 13859/57821 | 23.968800263 | (74065/231284, 85539/115642, 30103/115642) |
| Union-deletion maximum | 82833/199268 | 41.568641227 | (16801/199268, 1577636/3238105, 182467/199268) |

The full-fit minimum meets the inclusive rule at the crossing. Strictly larger displacement permits failure. For union deletion, the maximum first meets the rule at its crossing. With the illustrative 30%-70% exposure interval, every full-fit allocation passes while every union-deletion allocation fails. The scenario counts suffice to determine these results. The displacements describe hypothetical exposure imbalance.
