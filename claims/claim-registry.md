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
