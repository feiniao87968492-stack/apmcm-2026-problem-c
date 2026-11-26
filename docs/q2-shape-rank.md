# Q2 attenuation shape and representation weights

With equal representation weights, fitting a separate exponent for each call reduces pooled interior-distance RMSE from 0.055257 to 0.046770, a 15.36% gain. The flat, modulated and two-voice RMSEs fall from 0.047549, 0.047352 and 0.068242 to 0.032126, 0.047334 and 0.057355. This meets the frozen rule to prefer separate exponents in the equal-weight Q2 comparison. Q4 uses its published shared-exponent inputs. [Frozen specification](model-spec.md#q2-attenuation-shape-by-common-representation-weight) · [All RMSEs](../results/q2_shape_rank_rmse.csv) · [Holdout predictions](../results/q2_shape_rank_holdouts.csv) · [Adoption rule](../results/q2_shape_rank_decision.csv)

| Model | Equal-weight pooled RMSE | 0.70 modulated minus two-voice radius (m) | 95% paired draw interval (m) | Draws favoring modulated / two-voice |
|---|---:|---:|---:|---:|
| Isotonic | 0.068156 | −1.567 | [−3.435, 0.567] | 28 / 272 |
| Fixed exponent 2 | 0.060345 | +3.103 | [1.521, 4.874] | 300 / 0 |
| Shared exponent | 0.055257 | +0.683 | [−0.998, 2.493] | 232 / 68 |
| Separate exponents | 0.046770 | −21.804 | [−23.983, −18.934] | 0 / 300 |

At fidelity 0.50 all four equal-weight methods put two-voice ahead of modulated and flat in all 300 draws. No equal-weight draw ties at either threshold. At 0.70 the point fits all favor two-voice at envelope weights 0 and 0.10 and all favor modulated at 0.50. At envelope weight 1 the three parametric fits report 4 m lower support bounds for all calls. The isotonic estimate ranks modulated above the two lower bounds. The equal-weight intervals and rank frequencies condition on the same wide-row draws with unknown acquisition units. [Supported radii at all five weights](../results/q2_shape_rank_radii.csv) · [Paired draws](../results/q2_shape_rank_draws.csv) · [Signed gaps](../results/q2_shape_rank_gaps.csv) · [Complete rank counts](../results/q2_shape_rank_ranks.csv)

Run `python main.py --data "<attachment directory>/date"` to regenerate the tables.
