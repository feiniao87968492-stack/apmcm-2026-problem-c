# Q3 response direction in discordant playback pairs

The initial freeze was ba7fc52. The user clarified equal-size eligibility, both Firth designs and the role of the two intercepts before the first formal run. The completed pre-run specification is 9212008. The date holdout purges tracks across all pairs on the held date before applying the equal-size filter. [Frozen specification](model-spec.md#q3-discordant-pair-direction-freeze)

Of 137 equal-size pairs, 74 were natural-only and two were control-only. The two control-only pairs had equal distances and used modulated and two-voice calls. The matched-distance subset has 49 pairs, with 27 natural-only, two control-only, six both and 14 neither. These are observed counts. [Counts by sample and call](../results/q3_direction_counts.csv)

| Candidate | Log loss | Brier |
|---|---:|---:|
| Half-count direction frequency | 0.142178 | 0.026499 |
| Multinomial, independent arms | 0.133113 | 0.027272 |
| Multinomial, shared odds ratio | 0.131451 | 0.026596 |
| Firth, distance ratio | 0.147271 | 0.026951 |
| Firth, distance ratio and call | 0.163487 | 0.029439 |

The 76 held-out discordant pairs span 12 dates. Adding the distance ratio to the half-count comparator raises log loss by 0.005093 (paired 95% interval 0.001684 to 0.008439) and Brier by 0.000452 (0.000191 to 0.000732). Adding call indicators to the Firth distance model raises log loss by 0.016216 (0.007039 to 0.026381) and Brier by 0.002488 (0.000947 to 0.004387). Both Firth rules use the frozen half-count fallback in the fold with 58 natural-only and zero control-only training events. The shared-odds-ratio model reduces log loss in point estimate versus independence and the half-count rule, with paired intervals spanning zero. Retain the half-count comparator for direction and the published multinomial for Q4 absolute probabilities. [Scores](../results/q3_direction_scores.csv) · [Paired contrasts](../results/q3_direction_contrasts.csv) · [Fold counts](../results/q3_direction_folds.csv)

Under the paired logistic formulation, conditional direction depends on the difference between the arm logits, so the shared pair-response intercept cancels. A fitted direction intercept captures the natural-control log-odds contrast at the predictor reference. The Jeffreys penalty uses the full information matrix including the direction intercept. Standardized equal-distance predictions set both arms at 50, 100 or 150 m and eight birds. They average joint cells across the empirical natural-context weights before conditioning for the multinomial-based models. The predictions describe which arm responds among discordant pairs. [Standardized conditional probabilities](../results/q3_direction_standardized.csv)

Run `python main.py --data "<attachment directory>/date"` to regenerate the five direction tables.
