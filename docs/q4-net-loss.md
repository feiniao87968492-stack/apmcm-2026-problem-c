# Q4 two-loss tradeoffs

Let a be acoustic loss and b the loss of the positive natural-minus-control response excess. In each paired draw the clean 20 m net reference K is the same for all four attenuation shapes and both behavior fits. K is positive throughout, with point value 0.194371 and draw range 0.076086–0.309759.

When F and the response excess are positive, a draw requires retention of at least K divided by their product. Otherwise the draw is infeasible. For all-four attainment the draw requirement is the maximum across shapes. The 3,840th smallest requirement R gives the closed feasible region (1−a)(1−b) ≥ R on the square [0,0.20]². The CSV records the acoustic extent at b=0 and the endpoint of any b=0.20 plateau. [Frozen protocol](model-spec.md#q4-two-loss-net-boundary-freeze) · [Requirements](../results/q4_net_loss_requirements.csv)

| Behavior fit | Distance | Joint R | Maximum b at a=0 | At a=10% | At a=20% | Maximum equal losses |
|---|---:|---:|---:|---:|---:|---:|
| Full | 100 m | 0.647066 | 20% cap | 20% cap | 19.117% | 19.560% |
| Full | 150 m | 0.813826 | 18.617% | 9.575% | Infeasible | 9.788% |
| Union deletion | 100 m | 0.706113 | 20% cap | 20% cap | 11.736% | 15.969% |
| Union deletion | 150 m | 0.995704 | 0.430% | Infeasible | Infeasible | 0.215% |

The fixed exponent g=2 binds the joint boundary in all four cases and has the largest requirement in every finite draw. Separate exponents pass at 20% loss in both components for union-deleted 100 m, with 4,034 qualifying draws. Requiring all four shapes jointly leaves 3,039. At 150 m after union deletion, all four qualify together in 3,858 clean draws, just 18 above the decision cutoff. The small allowances near that corner are conditional on the fitted scores and resampling. The losses are hypothetical and union-deleted 150 m behavior still extrapolates. [Boundary allowances and direct counts](../results/q4_net_loss_boundaries.csv) · [Checkpoints](../results/q4_net_loss_counts.csv)

```sh
python main.py --data "<attachment directory>/date" --q4-net-loss
```
