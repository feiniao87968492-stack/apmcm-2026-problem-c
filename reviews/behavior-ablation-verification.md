# Independent verification of the Q4 behavior-model ablation

I used the specification frozen at `aa170ea` and verified the computed results at `4adb6e7`. I rebuilt the acoustic inputs from the raw tables using the released resampler, isotonic projections and shared-exponent fitter. I used the released full multinomial and pairwise mask fit functions on the raw trials, first on the full sample and then on each of the 300 date draws. I reconstructed the draws at seed 20261128 by concatenating complete date blocks. For stimulus frequencies I computed the eight mask counts with 0.5 per mask independently in each arm. I standardized the fitted probabilities with the original natural-context proportions and independently evaluated the cutoff expressions and normalized trapezoid weights on the 261-point grid.

The model A comparison against the archived control subtraction has 12 area rows, 12 pairwise-gap rows and 54 fixed-distance rows. All scores, cutoffs, point margins and interval endpoints match within the frozen tolerance of 1e-12. Exact rank, support count and 80% decision checks also pass. For every model, point estimate, date draw and grid point, gross minus signed net equals attenuated fidelity times the fixed control probability to within 1e-15. [Archived area means](../results/control_subtraction_area.csv) · [Archived area gaps](../results/control_subtraction_area_gaps.csv) · [Archived point decisions](../results/control_subtraction_points.csv)

| Released ablation table | Rows | Largest absolute difference |
|---|---:|---:|
| Area means, ranks, and paired contrasts against A | 36 | 1.12e-16 |
| Within-model area gaps and paired contrasts against A | 36 | 2.02e-16 |
| Fixed-distance margins, support and changes versus A | 162 | 2.02e-16 |
| Call, stimulus and distance support | 18 | 0 |

The comparisons use the recorded keys and check every field. Rank, trial count, responder count, date count, support count, sparse flag and all decision flags match exactly in both the temporary run and committed results. [Area means](../results/behavior_ablation_area.csv) · [Area gaps](../results/behavior_ablation_area_gaps.csv) · [Fixed-distance results](../results/behavior_ablation_points.csv) · [Coverage](../results/behavior_ablation_coverage.csv)

All model, loss and score combinations have the same point-estimate ranking, two-voice above modulated above flat. In clean conditions, the gross, shared-cutoff net and own-cutoff net pass counts are 5/3/6 for A, 6/4/6 for B and 6/4/8 for C. Under 20% coupling they are 2/0/3 for A, 2/0/3 for B and 1/0/5 for C. The pairwise model changes two of 54 decisions versus A, both clean. Stimulus-specific frequencies change seven. One example is the coupled own-cutoff net decision for modulated calls at 100 m, with support of 59.3%, 65.0% and 100.0% for A, B and C. The C behavioral probability is constant across calls and distances within each arm. Its added support is a model sensitivity on a fixed acoustic grid.

All six arm-by-call cells near 150 m are sparse. Trial counts for natural/control are 3/6 for flat, 3/1 for modulated and 2/1 for two-voice. Responder counts are 2/1, 2/0 and 2/0 respectively. Across the three distances, 12 of 18 cells fail the five-trial or five-responder screen. The strict holdout favors smoothed frequencies on log loss (1.125 versus 1.299 for A) and the pairwise model on Brier (0.1681 versus 0.1698 for A). Those rankings concern held-out behavior prediction. The ablation retains A for the primary Q4 analysis. [Strict holdout scores](../results/strict_q3_scores.csv)

I ran the independent calculation and comparator from the repository root with temporary scripts.

```powershell
$env:PYTHONPATH = (Get-Location).Path
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-ablation-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-ablation-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-ablation-compare.py" "$env:TEMP/apmcm-ablation-independent" results
```
