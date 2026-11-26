# Q4 behavior model sensitivity

The analysis froze at `aa170ea` and ran at `4adb6e7`. In strict date and track holdout, the full multinomial (A), pairwise mask model (B) and half-count stimulus frequencies (C) have mask log losses 1.299, 1.142 and 1.125 and any-response Brier scores 0.1698, 0.1681 and 0.1778. The same acoustic and whole-date draws are used for all three. Gross and shared-threshold net scores use A's clean common reference. The own-threshold net score uses its model's clean reference. [Strict scores](../results/strict_q3_scores.csv)

| Model | Clean gross / shared net / own net | Coupled gross / shared net / own net | Decisions changed versus A, out of 54 |
|---|---|---|---:|
| A | 5 / 3 / 6 | 2 / 0 / 3 | 0 |
| B | 6 / 4 / 6 | 2 / 0 / 3 | 2 |
| C | 6 / 4 / 8 | 1 / 0 / 5 | 7 |

Each count is out of nine fixed-distance settings and requires at least 80% of paired draws to meet the cutoff. For clean gross two-voice at 150 m, support is 73.3%, 80.7% and 89.7% for A, B and C. Under 20% coupling, both alternatives have zero passing settings with the shared net cutoff. [Point margins and decisions](../results/behavior_ablation_points.csv)

All area point rankings are two-voice, modulated, flat. Under coupling, the net two-voice minus modulated area gap is 0.0272 for A, 0.0130 for B and 0.00665 for C. Their paired 95% intervals are [−0.1124, 0.1009], [−0.1059, 0.0875] and [0.00487, 0.00843]. For C the behavior contrast is common across calls and distances, so propagation accounts for the call differences. Twelve of 18 local cells are sparse, including all six at 150 m. A remains primary. [Area means](../results/behavior_ablation_area.csv) · [Paired gaps](../results/behavior_ablation_area_gaps.csv) · [Local coverage](../results/behavior_ablation_coverage.csv)
