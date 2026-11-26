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

| Noise scenario finding | Supporting artifact | Scope |
|---|---|---|
| Matched uniform and local attenuation | results/noise_q4_losses.csv, results/noise_q4_points.csv, results/noise_q4_radii.csv | Hypothetical variance changes, fixed isotonic reference |
| Expected count bounds and assumptions | results/noise_q4_responders.csv | Eight-bird standardized predictions |

| Final release finding | Supporting artifact | Scope |
|---|---|---|
| Figure 2 adopted curve and threshold crossings | results/physical_q2_curves.csv, results/physical_q2_curves.meta.json, results/physical_q2_radii.csv | Physical fit, archived isotonic comparison and conditional acoustic intervals |
| Q4 agreement across modeled variants | results/noise_q4_agreement.csv, results/noise_q4_agreement_by_factor.csv, results/noise_q4_points.csv | 80% attainment within each variant and conditional protection implications |

| Strict playback finding | Supporting artifacts | Scope |
|---|---|---|
| Date holdout with a natural-track purge | results/strict_q3_coverage.csv, results/strict_q3_scores.csv | All 139 pairs held out once |
| Joint binary outcomes with fixed margins | results/strict_q3_pair_folds.csv, results/strict_q3_pair_contrast.csv | Fold-specific estimates of a shared association |
| Crossed playback resampling and fixed-reference Q4 | results/strict_q4_crossed_coverage.csv, results/strict_q4_margins.csv | Conditional on sampled dates and natural tracks |

| Sea-state finding | Supporting artifacts | Scope |
|---|---|---|
| Observed date-level slopes and strict prediction comparisons | results/sea_state_daily.csv, results/sea_state_slopes.csv, results/sea_state_validation.csv | Exploratory comparison across 12 observed dates |
| Standardized weather contrasts | results/sea_state_standardized.csv, sources/false-bay/README.md | Reanalysis proxies and date-block intervals |

| WAVERYS and propagation finding | Evidence |
|---|---|
| WAVERYS daily slopes and strict validation | results/waverys_slopes.csv, results/waverys_validation.csv |
| Example deletion radii and attainment | results/example_deletion_radii.csv, results/example_deletion_q4_summary.csv |

| Missing propagation finding | Evidence |
|---|---|
| 190 of 300 comparisons per representation for two-voice at 128 m | results/missing_q2_cells.csv |
| Sharp isotonic radius bounds and grid-based quality reversals | results/missing_q2_radius_bounds.csv, results/missing_q2_quality_grid.csv |
| Q4 completion-dependent decisions with the original date reference | results/missing_q4_attainment.csv |

| Group size finding | Evidence |
|---|---|
| Size-stratified contrasts across all pairs and pairs matched on distance and size | results/group_size_pair_contrasts.csv |
| Out-of-date and track-purged prediction with fixed and estimated size coefficients | results/group_size_strict_folds.csv, results/group_size_strict_scores.csv |
| Fixed-distance Q4 attainment, responder bounds and local support at 2, 8 and 20 birds | results/group_size_q4.csv, results/group_size_q4_coverage.csv |

| Vocal-count finding | Evidence |
|---|---|
| Paired changes and count/flag concordance | results/vocal_count_pairs.csv, results/vocal_count_audit.csv |
| Strict holdout comparison of count models | results/vocal_count_folds.csv, results/vocal_count_scores.csv |
| Contact and any-response decisions under the same thresholds | results/vocal_contact_q4.csv, results/vocal_contact_coverage.csv |

| First reply and event order finding | Evidence |
|---|---|
| First reply by stimulus and context, conditional and all-trial denominators | results/first_reply_matrix.csv |
| Directed reply counts and natural played-call-by-context detail | results/first_reply_by_played_call.csv |
| Strict reply prediction and same-type matching within dates and contexts | results/first_reply_folds.csv, results/first_reply_scores.csv, results/first_reply_matching.csv |
| Group vocal and approach onset order and lag | results/first_reply_event_order.csv |

| Supported annulus finding | Evidence |
|---|---|
| Distance and area averages, losses and rankings | results/annulus_scores.csv, results/annulus_score_gaps.csv |
| Connected intervals and point-radius area comparison | results/annulus_attainment_grid.csv, results/annulus_intervals.csv, results/annulus_attainment.csv |
| Sharp area-index completion bounds and ranking | results/annulus_completion_scores.csv, results/annulus_completion_gaps.csv |

| Context and behavior priority finding | Evidence |
|---|---|
| Context-specific and empirical area averages, ranks and paired gaps | results/context_priority_scores.csv, results/context_priority_gaps.csv |
| Exact pairwise gap endpoints, vertices and directional robustness | results/context_priority_bounds.csv |
| Natural trial, date and event coverage | results/context_priority_coverage.csv |

| Historical recovery finding | Evidence |
|---|---|
| Missing counts and one- and two-unit recovery comparisons | results/recovery_units.csv, results/recovery_plans.csv, results/recovery_cases.csv |
| Selected-plan radius and ranking sensitivities | results/recovery_radii.csv, results/recovery_gaps.csv |
| Continuous worst-case shrinkage and clean optimality certificate | results/recovery_continuous.csv, results/recovery_breakpoints.csv |

| Q3 response-gap finding | Evidence |
|---|---|
| Response frequency and responder composition in all and matched pairs | results/behavior_gap_raw.csv |
| Standardized decomposition and local support by call and distance | results/behavior_gap_standardized.csv |

| Q4 control subtraction finding | Evidence |
|---|---|
| Gross and net area means and paired rankings | results/control_subtraction_area.csv, results/control_subtraction_area_gaps.csv |
| Gross and net bounded radii and cutoff decisions | results/control_subtraction_radii.csv, results/control_subtraction_points.csv, results/control_subtraction_decisions.csv |

| Q4 behavior model finding | Evidence |
|---|---|
| Area means, pairwise contrasts and shared or model-specific cutoff decisions | results/behavior_ablation_area.csv, results/behavior_ablation_area_gaps.csv, results/behavior_ablation_points.csv |
| Sparse local sample coverage | results/behavior_ablation_coverage.csv |

| Q4 distance deletion finding | Evidence |
|---|---|
| Pair overlap, arm counts and retained distance support | results/distance_deletion_overlap.csv, results/distance_deletion_training.csv, results/distance_deletion_coverage.csv |
| Fixed-cutoff predictions, paired margin differences and decisions | results/distance_deletion_points.csv |
| Monte Carlo precision at the 80\% cutoff | results/distance_deletion_mc.csv |
| Adverse extrapolation drift at 150 m, probability shifts and the binding draw criterion | results/q4_extrapolation_drift.csv |

| Fisher planning for the three Q4 margins | Evidence |
|---|---|
| 120-pair allocations | results/q4_fisher_allocations.csv |
| Delta-method standard errors and gains versus uniform | results/q4_fisher_precision.csv |
| Allocation sensitivity to paired dependence | results/q4_paired_planning_allocations.csv, results/q4_paired_planning_precision.csv, results/q4_paired_planning_summary.csv |
