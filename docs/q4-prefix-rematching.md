# Q4 consecutive-radius draw rematching

Each acoustic draw and each date-block draw is used exactly once in any bijection. For every possible pair, we recompute its common reference from the clean full-data response excess and isotonic fidelity at 20 m. A pair counts at a target only if its two-voice signed net score clears that reference on all four curves at every node from 20 m through the target. A bijection's radius is its last passing node on the 0.5 m grid, with at least 3,840 of the same 4,800 pairs required. [Frozen specification](model-spec.md#q4-consecutive-radius-draw-rematching-freeze)

| Behavior fit | Scenario | Original radius (m) | Sharp radius bounds (m) | Minimum count at lower radius / next | Maximum count at upper radius / next |
|---|---|---:|---:|---:|---:|
| Full | Clean | 150 cap | 150–150 cap | 4,451 / — | 4,489 / — |
| Full | 20% loss in each component | 96 | 94.5–98 | 3,843 / 3,827 | 3,844 / 3,832 |
| Union deletion | Clean | 150 cap | 149–150 cap | 3,842 / 3,823 | 3,890 / — |
| Union deletion | 20% loss in each component | 84 | 82.5–85 | 3,866 / 3,838 | 3,850 / 3,827 |

The sharp minimum count at a node establishes whether every bijection passes. The sharp maximum establishes whether any bijection passes. Both counts are nonincreasing along the grid, so binary search locates the boundary. A minimum-count bijection at the first node where some bijection fails attains the lower radius. A maximum-count bijection at the upper radius attains the upper radius. The two cap cases have no next grid node to evaluate. The summary distinguishes the optimal count at each node from the count of the single permutation witnessing the radius. [Boundary counts](../results/q4_prefix_rematching.csv) · [Eight attaining permutations](../results/q4_prefix_rematching_witnesses.csv)

The clean deletion case qualifies in 3,850 original pairs at 150 m. The archived endpoint-minimizing permutation qualifies in 3,818 pairs at that single node and 3,810 through the entire prefix. Original independent pairing remains primary. The bounds describe dependence sensitivity conditional on fixed empirical draws. The 150 m cap is the end of the grid. After deletion, natural and control predictions extrapolate beyond 100 and 120 m, respectively. [Original consecutive analysis](q4-consecutive.md) · [Endpoint rematching](q4-draw-rematching.md) · [Independent verification](../reviews/q4-prefix-rematching-verification.md)

```sh
python main.py --data "<attachment directory>/date" --output generated --q4-prefix-rematching
```
