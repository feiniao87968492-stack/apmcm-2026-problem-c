# Independent recomputation of playback dependence and design precision

**PASS.** I reconstructed both holdout groupings directly from Data02 and retained complete experiment pairs. Independently built training matrices and a dense-design BFGS fit for the pairwise model reproduced the 120 fold-model rows and six pooled scores within 0.000003. Coverage counts matched exactly. [Fold results](../results/dependence_q3_folds.csv)

I separately refit the full model for 300 draws under each behavior resampling scheme using the frozen seed. Both used the archived Q2 propagation draws. All 36 margin rows agreed, including the 95% endpoints and integer attainment counts. Modulated at 100 m and two-voice at 150 m are the two clean settings that fall below 80% support with date resampling. [Margin results](../results/dependence_q4_margins.csv)

I reconstructed the Bernoulli joint mass subject to the feasible bounds and searched integer counts from five per arm to recover the first count reaching the cell half-width target. All 18 cell requirements and three summaries matched. Aggregate contrast variances used the sum of the independent cell variances divided by 36. [Trial results](../results/dependence_q4_trial_summary.csv)
