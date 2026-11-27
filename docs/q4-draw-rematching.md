# Q4 dependence sensitivity under draw rematching

For each rematched acoustic and playback draw, the clean 20 m threshold is half the equal-call mean of the acoustic draw's isotonic fidelity multiplied by the playback draw's full-data natural-minus-control response. Both behavior fits use that threshold. A pair passes only if the two-voice net score meets it on all four acoustic curves at the target distance. [Frozen specification](model-spec.md#q4-acoustic-and-behavior-draw-rematching-freeze)

| Playback fit | Endpoint | Original | All crossed pairs | Minimum–maximum over bijections | 80% decision can flip |
|---|---|---:|---:|---:|---|
| Full | 100 m, 20% loss in each component | 78.60% | 78.58% | 77.52%–79.69% | No |
| Full | 150 m, clean | 93.08% | 93.07% | 92.73%–93.52% | No |
| Union deletion | 100 m, 20% loss in each component | 63.31% | 63.28% | 62.02%–64.73% | No |
| Union deletion | 150 m, clean | 80.38% | 80.40% | 79.54%–81.21% | Yes |

The crossed comparison weights all 23,040,000 combinations equally. Each bijection uses all 4,800 draws on each side exactly once. A maximum matching on passing edges attains the largest possible pass count after extension to a bijection. A maximum matching on failing edges analogously gives the smallest pass count. The published witnesses give eight complete permutations. The clean union-deletion case can fall to 3,818 passes or rise to 3,898, relative to the inclusive threshold of 3,840. [Exact counts](../results/q4_draw_rematching.csv) · [Attaining permutations](../results/q4_draw_rematching_witnesses.csv)

The independent pairing remains the primary analysis. The extremes describe sensitivity to draw dependence at fixed empirical marginals. In the clean 150 m union-deletion case, the natural and control predictions extrapolate beyond their retained maxima of 100 and 120 m, respectively. [Retained ranges](../results/q4_consecutive_ranges.csv)

```sh
python main.py --data "<attachment directory>/date" --output generated --q4-draw-rematching
```

[Independent verification](../reviews/q4-draw-rematching-verification.md)
