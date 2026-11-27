# Independent verification of Q4 draw rematching

**Pass.** I regenerated the frozen 4,800 acoustic and 4,800 date-block draws using the published generators and reconstructed each crossed pass matrix independently. I computed the cutoff matrix from the product of the three clean isotonic fidelities at 20 m and the three full-data response differences at 20 m, divided by six. For 100 m I multiplied nonnegative response excess by 0.64 and negative excess by 0.80 before applying each shape's fidelity. For 150 m I applied each shape's fidelity to the unaltered excess. I used the inclusive cutoff comparison separately for each shape and required all four to pass. The common crossed cutoff ranges from 0.07560885 to 0.31224772. [Frozen protocol](../docs/model-spec.md#q4-acoustic-and-behavior-draw-rematching-freeze)

I used SciPy's dense linear sum assignment to minimize and maximize the total binary pass cost over complete bijections. The four counts below agree with production commit `d834afa`. All four diagonal counts also agree with the archived two-loss analysis. The crossed denominator is 23,040,000 and the other denominators are 4,800. [Archived results](../results/q4_net_loss_counts.csv) · [Production summary](../results/q4_draw_rematching.csv)

| Behavior fit | Distance (m) | Original count | Crossed count | Minimum count | Maximum count | 80% decision can reverse |
|---|---:|---:|---:|---:|---:|---|
| Full | 100 | 3,773 | 18,104,899 | 3,721 | 3,825 | No |
| Full | 150 | 4,468 | 21,443,127 | 4,451 | 4,489 | No |
| Union deletion | 100 | 3,039 | 14,579,738 | 2,977 | 3,107 | No |
| Union deletion | 150 | 3,858 | 18,524,228 | 3,818 | 3,898 | Yes |

For each of the eight published extremizing permutations I checked that every acoustic draw and behavior draw occurs once. All 38,400 witness rows agree with the reconstructed pass matrices, and each permutation reaches its independently optimized count. Only union deletion at 150 m can fall below 3,840 passes under rematching. The retained natural and control distances end at 100 and 120 m, respectively, so this result still extrapolates for both arms. The crossed comparison represents empirical independence. The permutation endpoints vary draw dependence conditional on the fixed empirical marginals. [Witness assignments](../results/q4_draw_rematching_witnesses.csv) · [Retained distances](../results/q4_consecutive_ranges.csv)
