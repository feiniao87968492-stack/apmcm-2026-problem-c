# Q1-to-Q4 monitoring without acoustic features

The two fixed Q4 passing sets and 105 FalseBay holdouts come from the archived cost comparison. Each fold's prevalence is the observed passing fraction of its full training complement. A probability equal to or above the fixed cost cutoff triggers passage. Always-pass and always-nonpass are fixed action references. [Frozen specification](model-spec.md#q1-to-q4-monitoring-without-acoustic-features-freeze)

| Rule | Primary equal-cost false passes | Missed passes | Mean cost per recording |
|---|---:|---:|---:|
| Always pass | 84 | 0 | 0.8000 |
| Always nonpass | 0 | 21 | 0.2000 |
| Training prevalence | 0 | 21 | 0.2000 |
| Hard logistic | 6 | 19 | 0.2381 |
| Hard XGBoost | 10 | 18 | 0.2667 |
| Multinomial probability | 4 | 21 | 0.2381 |
| Binary logistic probability | 5 | 21 | 0.2476 |
| Proportional-odds probability | 5 | 20 | 0.2381 |

Primary training prevalences range from 0.2128 to 0.2299, below all three decision cutoffs. For the broader set they range from 0.5316 to 0.6207, giving always pass at cutoffs 0.25 and 0.50 and always nonpass at 0.75. The primary equal-cost criterion requires an upper paired 95% cost-difference limit below zero against fold prevalence. All five upper limits are positive. The multinomial excess cost is 0.0381 per recording (95% paired interval 0.0106 to 0.0731). No rule demonstrates lower cost against prevalence in any tested setting. In particular, the broader-set 1:3 gains previously seen against the hard classifiers disappear against prevalence, which incurs 44 false passes and zero misses at mean cost 0.4190, versus 0.5238 for the multinomial and binary rules. [Training fold counts](../results/q1_q4_prevalence_folds.csv) ? [All decisions](../results/q1_q4_prevalence_decisions.csv) ? [All paired contrasts](../results/q1_q4_prevalence_contrasts.csv)

| Probability model | Two-voice Brier / log loss | Broader set Brier / log loss |
|---|---:|---:|
| Training prevalence | 0.16125 / 0.50406 | 0.25285 / 0.69926 |
| Multinomial | 0.16981 / 0.51638 | 0.28877 / 0.82684 |
| Binary logistic | 0.17028 / 0.51641 | 0.28243 / 0.80430 |
| Proportional odds | 0.17779 / 0.54608 | 0.28199 / 0.80854 |

The score comparison is descriptive. The low primary cost under prevalence comes with zero sensitivity. The costs and prevalence benchmark describe the specified scenarios and held-out sample. Field decisions require separate validation. [Scores and differences](../results/q1_q4_prevalence_scores.csv)

Run the comparison from the repository root using committed prediction tables.

\`\`\`sh
python main.py --data . --output generated --q1-q4-prevalence
\`\`\`

[Independent verification](../reviews/q1-q4-prevalence-verification.md)
