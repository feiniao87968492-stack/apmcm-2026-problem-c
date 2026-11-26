# Manuscript evidence

| Claim | Supporting artifact | Scope |
|---|---|---|
| Acoustic feature availability and recording counts | docs/data-audit.md, results/q1_feature_summary.csv | Descriptive |
| Q1 adjusted tests, grouped macro F1, and feature importance | results/q1_rank_tests.csv, results/q1_metrics.csv, results/q1_feature_importance.csv | Sample-level ranks and grouped prediction |
| Q2 ranges, conditional intervals, and high-threshold weight sensitivity | results/q2_radii.csv, results/q2_fit_checks.csv | Acoustic similarity under fixed thresholds |
| Q3 paired response and grouped validation | results/q3_paired_response.csv, results/q3_grouped_validation.csv | Observed paired difference and held-out prediction |
| Q3 behavior combinations, conditional latency, and intensity | results/q3_predicted_mask_contrasts.csv, results/q3_representative_latency.csv, results/q3_observed_intensity.csv | Group-level estimates |
| Q4 clean and scenario radii and component comparison | results/q4_radii.csv, results/q4_model_comparison.csv | Clean-reference operational ranges and support bounds |
| Q4 modeled response and expected responders | results/q4_environment_curves.csv, results/q4_expected_responders.csv | Scenario assumptions |
| Mathematical formulas, thresholds, and assumptions | docs/model-spec.md, the methods sections of paper/main.tex | Fixed before production run |
| All figures | figures/figure-index.md | Plotted data and metadata |
| Q3 context and group size examples | results/q3_adjusted_conditions.csv | Matched model contrasts |
| Q1 forest comparison, paired macro F1 and recalls | results/q1_model_comparison.csv, results/q1_fold_counts.csv, results/q1_oof_predictions.csv | Same fixed date-by-location folds. The historical estimate uses other group assignments. |
| Q3 incremental validation and representative coverage | results/q3_grouped_validation.csv, results/q3_validation_oof_scores.csv, results/q3_representative_response_support.csv, results/q3_representative_latency.csv | Predictive metric tradeoff, descriptive distance-window support and pooled conditional onset estimates |
| Q4 common cutoff and alternate noise link | results/q4_comparison_radii.csv, results/q4_comparison_curves.csv, results/q4_clean_index_differences.csv | Conditional scenario results and support bounds |

| Follow-up claim | Supporting artifact | Scope |
|---|---|---|
| Boosting, group deletion and two-voice recall | results/round2_q1_comparison.csv, results/final_q1_group_influence.csv | Frozen grouped predictions and deterministic deletions |
| Leave-one-representation propagation radii | results/round2_q2_radii.csv | Threshold-sensitive scenario with conditional whole-row intervals |
| Nested playback predictors and two-stage factorization | results/round2_q3_comparison.csv, results/final_q3_comparison.csv | Fixed grouped held-out predictions |
| Fidelity augmentation and curve simplification | results/round2_q4_comparison.csv, results/round2_q4_collinearity.csv, results/final_q4_comparison.csv, results/final_q4_radii.csv, results/final_q4_cutoff_attainment.csv | Predictive comparisons and operational thresholds over 20?150 m |

| Creative result | Supporting artifact | Scope |
|---|---|---|
| Blocked Fpeak rank and paired differences | results/creative_q1_fpeak_tests.csv, results/creative_q1_fpeak_groups.csv | Exploratory within-recording-group association |
| Pairwise behavior likelihood and ablation | results/creative_q3_comparison.csv, results/creative_q3_interactions.csv | Paired grouped predictive scores and conditional associations |
| Fixed fidelity gate | results/creative_gate_vs_binary_comparison.csv, results/creative_gate_vs_ungated_comparison.csv, results/creative_gate_representative.csv | Fixed scenario and same-fold prediction within 20–150 m |
| Inverse loss limits and fixed-distance margins | results/creative_q4_inverse_loss.csv | Operational common-cutoff scenarios with censored loss search |

| Post hoc finding | Supporting artifact | Scope |
|---|---|---|
| Sparse mask contribution and smoothed stimulus comparison | results/posthoc_q3_smoothed_comparison.csv, results/posthoc_q3_focal_contribution.csv | Full-sample grouped prediction and additive score decomposition |
| Inverse limits by support criterion and behavior model | results/posthoc_q4_inverse_sensitivity.csv | Post hoc sensitivity under a fixed common cutoff |

| Q4 decision finding | Supporting artifact | Scope |
|---|---|---|
| Dual and product cutoff decisions | results/decision_q4_dual.csv | Exploratory fixed-distance thresholds and conditional support |
| Acoustic and behavioral variance shares | results/decision_q4_variance.csv | Independent crossed bootstrap draws and recomputed common reference |
| Matched-playback allocations and precision | results/decision_q4_trial.csv | Illustrative design under clean marginals and covariance sensitivity |

| Playback dependence finding | Supporting artifact | Scope |
|---|---|---|
| Date and natural-track holdout | results/dependence_q3_pooled.csv, results/dependence_q3_folds.csv | Separate holdouts with shared control stimulus |
| Date-block scenario support | results/dependence_q4_margins.csv | Conditional on 12 sampled dates and reused tracks |
| Average and cell-specific design precision | results/dependence_q4_trial_summary.csv, results/dependence_q4_trial_cells.csv | Planning under independent cells and working pair covariance |

| Matched sensitivity finding | Supporting artifact | Scope |
|---|---|---|
| Observed paired response differences by relative distance | results/matching_q3_strata.csv | Descriptive date-block intervals |
| Loss limits requiring support under both resampling schemes | results/matching_q4_loss_limits.csv | Conditional scenario on the bounded 0–20% grid |
| Weighted behavior scores, attainment and radii | results/matching_q4_weighted_points.csv, results/matching_q4_weighted_radii.csv | Illustrative ecological weights and index-specific clean cutoff |

| Attenuation finding | Supporting artifact | Scope |
|---|---|---|
| Shared-exponent fit and adopted Q2 ranges | results/physical_q2_validation.csv, results/physical_q2_parameters.csv, results/physical_q2_radii.csv | Descriptive curve and interior-distance holdout |
| Ten-row batch intervals and ordering | results/physical_q2_blocks.csv | Hypothetical batch dependence |
| Q4 propagation-model sensitivity | results/physical_q4_margins.csv | Shared behavior and isotonic common reference, within 20?150 m |

| Acoustic and timing finding | Supporting artifacts | Scope |
|---|---|---|
| Same-fold acoustic transformations | results/onset_q1_acoustic.csv | Fixed recording-group validation |
| Conditional latency and first recorded onset | results/onset_q3_latency.csv, results/onset_q3_timing_scores.csv, results/onset_q3_cumulative.csv | Observed onsets and date-block intervals |
