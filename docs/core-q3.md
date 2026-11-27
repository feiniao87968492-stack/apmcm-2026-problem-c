# Core Q3 playback models

The 12 held dates contain all 139 experiment pairs and 278 trials. Training folds purge pairs whose natural track appears on the held date. Both arms share each pair's assignment. Scores weight trials equally, and paired percentile intervals use 10,000 whole-date resamples with seed 20261209. [Frozen design](model-spec.md#antigravity-3-q3-freeze)

## Response combinations

| Mask model | Log loss | Any-response Brier |
|---|---:|---:|
| Stimulus half-count frequencies | 1.12504 | 0.17778 |
| Released full multinomial | 1.29934 | 0.16978 |
| Structured pairwise mask | 1.14169 | 0.16809 |
| Shrunk hurdle | 1.11170 | 0.16670 |
| Rank-one tilt | 1.10210 | 0.16383 |
| Nested frequency and hurdle pool | 1.11237 | 0.17002 |
| Rank-one tilt with stronger distance penalty | **1.10096** | **0.16356** |
| Call-aware hurdle | 1.14215 | 0.17759 |

The adopted tilt reweights each stimulus's half-count mask frequencies by an exponential term. The exponent is the number of active behaviors times a linear predictor of stimulus, log(1 + distance), log(1 + group size) and context. The standardized distance coefficient receives eight times the L2 penalty of the other coefficients. At fixed stimulus, distance, size and context, the model gives the same prediction across call types.

Against the full multinomial, the paired log-loss difference is −0.19838 [−0.37351, −0.06891] and the Brier difference is −0.00622 [−0.01907, +0.00353]. This meets the frozen improvement and +0.01 Brier noninferiority criteria. Against stimulus frequencies, the differences are −0.02408 [−0.07774, +0.03827] and −0.01423 [−0.03183, +0.00490]. The nested pool misses Brier noninferiority, and the call-aware hurdle misses both Brier noninferiority and the tail log-loss limit. [Pooled scores](../results/core_q3_mask_scores.csv) · [Paired intervals](../results/core_q3_mask_deltas.csv) · [Adoption checks](../results/core_q3_mask_decision.csv)

The tail test excludes all training pairs with an arm at least 125 m away. It scores 52 trials on eight dates, including 33 arms actually at or beyond 125 m. For the selected tilt, log-loss and Brier point differences from the incumbent are +0.02889 and −0.02416 across the tail pairs, and −0.01174 and −0.01112 across the long arms. Both meet the frozen tail limits. Two-voice support within 25 m of 150 m consists of two natural trials with two events and one control with zero events. The median-size predictions use eight birds and weight contexts by the natural-arm empirical proportions. [Fold coverage](../results/core_q3_coverage.csv) · [Representative eight-mask distributions](../results/core_q3_representative_masks.csv) · [Local support](../results/core_q3_support.csv)

## Observable event time through 60 s

The likelihood records a zero-time event, a positive onset in (0,5], (5,15], (15,30] or (30,60], or no event by 60 s. Integrated Brier averages the four later cumulative-risk errors with weights 5/60, 10/60, 15/60 and 30/60. The earliest-event Weibull AFT fits a separate half-count zero probability per stimulus. Its positive waiting time uses a common shape and a scale linked to standardized stimulus and log distance. The nonnegative distance coefficient allows waiting time to increase with distance. The fit uses exact event times and right-censors at 60 s. The estimand is an observable response during playback observation.

| Earliest-event model | Binned log loss | Integrated Brier | Conditional median MAE (s) |
|---|---:|---:|---:|
| Stimulus timing distribution | 0.85567 | 0.17649 | 2.188 |
| Discrete hazard | 0.85772 | 0.17525 | 2.177 |
| Finite-window two-part | 0.86224 | 0.17677 | 2.177 |
| Weibull AFT with zero atom | 1.01950 | 0.18603 | 3.464 |
| Factorized planning comparison | 1.13116 | 0.16334 | 2.188 |

The Weibull log-loss difference is +0.16383 [0.10113, 0.23813] against stimulus timing. The other covariate timing candidates also miss the adoption rule. Stimulus timing remains the validation-selected model for earliest response, head raising, vocalizing and approach. The representative respondent medians use the empirical stimulus-specific training rule. [Timing scores](../results/core_q3_timing_scores.csv) · [Paired timing intervals](../results/core_q3_timing_deltas.csv)

For each arm, the Q4 planning fallback multiplies the selected mask's 60 s any-response probability by the observed conditional probability that a response had occurred by the desired time among that stimulus's responders. By 15 s those conditional shares are 89/90 for natural playback and 17/18 for controls. By 30 s they are 90/90 and 17/18. The comparison uses training-only probabilities within each held-date fold and follows the whole-sample selection of the mask model. Four held events occupy an onset bin with zero training mass in their arm. The existing log-loss scorer clips these probabilities at 10⁻¹². The factorization gives a planning scenario with distance dependence inherited from the selected 60 s mask. At 50, 100 and 150 m, the natural 30 s probabilities are 0.6585, 0.5772 and 0.5293, and the control probabilities are 0.1108, 0.0907 and 0.0806. The comparable stimulus-only 30 s probabilities are 0.6479 and 0.1338. [Conditional rates](../results/core_q3_conditional_rates.csv) · [Prediction grid](../results/core_q3_predictions.csv)

## Representative respondent latency

The stimulus-specific empirical medians at eight birds are the same at 50, 100 and 150 m because the model pools calls and distances within each stimulus. Each value describes responders and retains flagged zero latencies.

| Endpoint | Natural median (s) | Control median (s) |
|---|---:|---:|
| First response | 2.05 | 2.00 |
| Head raising | 2.00 | 1.00 |
| Vocalizing | 2.90 | 4.80 |
| Approach | 8.00 | Unestimable |

The control arm has zero observed approach events. [Representative timing table and counts](../results/core_q3_representative_latency.csv)

## Reproduction and Q4 interface

    python core_q3.py --data "<attachment directory>/date" --output generated

In the prediction table, select `family=timing`, `endpoint=Any`, `selected=True` and the required `window_s` for the Q4 planning route. The `validated_selection` column marks the independently scored timing model selected by the frozen criterion. In the mask family, `selected=True` gives the adopted 60 s risk and `model=full_multinomial` gives the archive comparison. The conditional rate table permits the same timing factorization with either mask model. `predict_mask(frame, evaluation, model, contexts)` returns the eight mask probabilities. `predict_timing(frame, evaluation, model, contexts, endpoint)` returns the five observed event cells and the no-event cell. Pass `mask_model` for factorized timing.
