# Independent verification of Q4 consecutive-radius rematching

I regenerated the frozen acoustic and date-block draws using the published generators. I built the crossed 20 m cutoff with three separate call-wise outer products, summing them and dividing by six. The cutoff was positive for every pair of draws. I used the minimum fidelity across four shapes with positive response excess and took the running minimum of the resulting score across grid nodes. With nonnegative fidelities and positive cutoffs, a nonpositive excess always fails. Applying the simultaneous losses is equivalent to dividing the positive cutoff by 0.64 for this comparison. This reconstructs the crossed prefix mask independently of the production implementation. [Frozen specification](../docs/model-spec.md#q4-consecutive-radius-draw-rematching-freeze)

All 1,044 diagonal prefix counts agree with the archived consecutive-distance analysis. I applied dense linear sum assignment to the binary prefix masks to minimize and maximize the qualifying count on the tested nodes. The masks are nested, so a passing bound followed by a failing bound certifies the corresponding grid crossing. At 150 m I evaluated the bound at the grid cap. [Archived prefix counts](../results/q4_consecutive_counts.csv)

| Behavior fit | Loss | Bound | Radius (m) | Bound count at radius | Bound count at next node |
|---|---|---|---:|---:|---:|
| Full | Clean | Minimum | 150 cap | 4,451 | |
| Full | Clean | Maximum | 150 cap | 4,489 | |
| Full | 20% each | Minimum | 94.5 | 3,843 | 3,827 |
| Full | 20% each | Maximum | 98.0 | 3,844 | 3,832 |
| Union deletion | Clean | Minimum | 149.0 | 3,842 | 3,823 |
| Union deletion | Clean | Maximum | 150 cap | 3,890 | |
| Union deletion | 20% each | Minimum | 82.5 | 3,866 | 3,838 |
| Union deletion | 20% each | Maximum | 85.0 | 3,850 | 3,827 |

The archived endpoint-minimizing permutation for the clean union deletion has 3,860 prefix passes at 149.5 m and 3,810 at 150 m, so its grid radius is 149.5 m. Optimizing the consecutive radius itself attains 149 m. Both clean union-deletion extremes extrapolate beyond the observed natural and control maxima of 100 and 120 m. [Archived endpoint permutation](../results/q4_draw_rematching_witnesses.csv) · [Observed ranges](../results/q4_consecutive_ranges.csv)

I independently scored all 38,400 rows across the eight exported permutations. Each uses every acoustic and behavior draw once. Each first-failed grid distance and witness count at the radius and next node agrees with the reconstructed masks. At an interior minimum the witness minimizes the count at the first failing node. At an interior maximum it maximizes the count at the last passing node. [Boundary counts](../results/q4_prefix_rematching.csv) · [Attaining permutations](../results/q4_prefix_rematching_witnesses.csv)
