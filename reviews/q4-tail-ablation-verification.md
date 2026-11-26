# Independent numerical verification of the five-model Q4 tail ablation

**Pass.** The independent computation reproduces all 30 Q4 attainment counts, all 15 adverse-drift boundary and feasibility results, and adoption of A. Maximum absolute differences were 2.34e-11 for margin statistics, 8.83e-13 for anchor-to-150 m changes and their intervals, and 7.47e-10 for drift limits, odds multipliers and point shifts.

I reproduced the two validation exercises and the 4,800 paired Q4 draws with acoustic seed 20261130 and date seed 20261201. [Frozen specification](../docs/model-spec.md#q4-monotone-and-bounded-extrapolation-ablation-freeze) I built the intact pair and natural-track filters separately, reused the released design and multinomial, and implemented the constrained hurdle objective, mask composition and clipping outside the production code. I compared the hurdle solutions against SLSQP on each nonempty validation fit, both Q4 point fits and the first three date draws per Q4 fit. The objectives agreed within 1e-8 and the tested probabilities within 2e-5. I solved the four-state joint table algebraically from the odds-ratio equation and computed the losses from its cell probabilities.

## Strict playback validation

The ordinary assessment scored 139 pairs on 12 dates. The tail assessment scored 26 pairs on eight dates, leaving four empty test dates. Both exercises purged every natural track observed on the held-out date. I obtained 4,800 valid score resamples per assessment. All 100 populated model-fold rows matched production to 1.33e-8 on the losses, and the ten pooled summaries and paired intervals matched to 4.17e-9. The fold comparisons matched training and test counts exactly. Both training/holdout overlap columns and all fit-failure flags were zero. [Fold evidence](../results/q4_tail_ablation_folds.csv) · [Pooled validation](../results/q4_tail_ablation_validation.csv)

| Model | Ordinary mask loss | Ordinary Brier | Ordinary joint loss | Tail mask loss | Tail Brier | Tail joint loss |
|---|---:|---:|---:|---:|---:|---:|
| A | 1.29934 | 0.16978 | 1.05868 | 1.14866 | 0.21475 | 1.33270 |
| B | 1.14080 | 0.17891 | 1.10547 | 1.29355 | 0.22988 | 1.40674 |
| C | 1.15643 | 0.18373 | 1.13671 | 1.29347 | 0.23285 | 1.40656 |
| D | 1.29934 | 0.16978 | 1.04314 | 1.14866 | 0.21475 | 1.30268 |
| E | 1.14702 | 0.17391 | 1.09034 | 1.19512 | 0.19847 | 1.21434 |

B, C and E lower ordinary mask loss with paired interval upper endpoints below zero, while all three have a higher ordinary Brier point than A. E improves the tail Brier point by −0.01628 and has a higher tail mask loss by +0.04646. D's ordinary and tail joint differences are −0.01554 and −0.03003 with paired 95% intervals [−0.03434, +0.00364] and [−0.04725, +0.00497]. D shares A's marginal scores. The frozen adoption rule retains A. [Adoption table](../results/q4_tail_ablation_adoption.csv)

## Q4 margins and extrapolation

I independently combined released shared-exponent fidelity with standardized eight-bird arm probabilities and fixed each draw's reference using the equal-call mean of A's full-data isotonic 20 m scores divided by two. All acoustic and date draws were valid in both fits. For D's Q4 arithmetic I reused A's marginal predictions as required by the shared-odds construction. The independently fitted pair log odds ratios agreed within 1.63e-7 in the two point fits and five draws per training fit. Their marginal probabilities exactly matched A. [Q4 margins](../results/q4_tail_ablation_margins.csv)

| Training | Target | A | B | C | D | E |
|---|---|---:|---:|---:|---:|---:|
| Full | Clean two-voice net at 150 m | 4,527 | 4,148 | 4,655 | 4,527 | 4,764 |
| Full | Coupled two-voice net at 100 m | 4,116 | 3,936 | 4,313 | 4,116 | 4,336 |
| Full | Clean modulated gross at 100 m | 4,074 | 4,109 | 3,499 | 4,074 | 4,550 |
| Union deletion | Clean two-voice net at 150 m | 4,002 | 3,356 | 4,200 | 4,002 | 4,764 |
| Union deletion | Coupled two-voice net at 100 m | 3,575 | 3,276 | 3,873 | 3,575 | 4,336 |
| Union deletion | Clean modulated gross at 100 m | 4,049 | 4,009 | 3,830 | 4,049 | 4,550 |

The counts are out of 4,800. Under union deletion, the 80% decision switches from pass to fail for B's clean two-voice net margin at 150 m and C's clean modulated gross margin at 100 m. It switches from fail to pass for C and E's coupled two-voice net margin at 100 m. C's clean modulated 100 m decision also switches from pass to fail on full training. E's full and union results coincide because E's training restriction already removes every tail pair. Across all constrained hurdle refits the largest distance coefficient was zero. For E, the standardized probabilities are identical at each retained anchor and 150 m for all draws in both arms. A's point responses decline by 7.43 and 0.96 percentage points for natural and control, respectively, and both draw intervals include zero. [Anchor-to-150 m results](../results/q4_tail_ablation_tail.csv)

I directly bisected the count of attainable draws in odds space and independently used a scalar root solve for the point margin. For drift in both arms, the joint maxima are 0.093046 (A and D), 0.252397 (C), and 0.960482 (E). B has a point limit of 0.369117 and 3,356 qualifying draws at zero drift, so it has no jointly feasible adverse drift. For all feasible scenarios the draw condition binds and the inclusive count goes from 3,840 at the boundary to 3,839 just above it. E's higher limit accompanies its assumed plateau and its higher baseline margin. [Drift table](../results/q4_tail_ablation_drift.csv)

## Reproduction

I ran the independent script from the repository root. The script and its outputs are stored in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-tail.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-tail"
```
