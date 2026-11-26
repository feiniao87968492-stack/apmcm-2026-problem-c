# Independent verification of Q3 discordant-pair direction

**Pass.** I rebuilt intact pairs using an experiment-by-arm table and used the natural trial to assign date, track and call. Training and scoring use the 137 equal-size pairs. Within each of the 12 held dates, I determined the prohibited tracks before filtering for size. I refitted the released multinomial, solved the four-cell joint probabilities algebraically and used a separate Powell optimizer for the Firth likelihood with the full information determinant. I checked its objective against a second optimizer. [Frozen protocol](../docs/model-spec.md#q3-discordant-pair-direction-freeze)

The 49 equal-distance, equal-size pairs contain 14 neither, six both, 27 natural-only and two control-only responses. The control-only observations comprise one modulated and one two-voice playback. Among all equal-size pairs, 74 of 76 discordances favor natural, along with 16 both and 45 neither. All eight count rows and all fold count and overlap columns matched exactly. Fold 7 has 58 natural-only and zero control-only observations in the eligible discordant training sample. Both Firth models therefore use the stipulated half-count fallback in that fold. [Raw counts](../results/q3_direction_counts.csv) · [Fold evidence](../results/q3_direction_folds.csv)

| Model | Log loss | Brier |
|---|---:|---:|
| Half-count | 0.142178 | 0.026499 |
| Independent margins | 0.133113 | 0.027272 |
| Shared odds ratio | 0.131451 | 0.026596 |
| Firth distance | 0.147271 | 0.026951 |
| Firth distance and call | 0.163487 | 0.029439 |

I recomputed absolute score intervals and paired contrasts on 4,800 shared whole-date draws. All draws were valid. The independent and shared-odds models lowered the log-loss point and increased the Brier point relative to half-count. Firth distance increased both errors, and adding call indicators increased both errors relative to Firth distance. The shared odds ratio lowered both error points relative to independence, with both intervals spanning zero. The registered decision retains half-count for discordance direction. [Scores](../results/q3_direction_scores.csv) · [Contrasts](../results/q3_direction_contrasts.csv)

The maximum absolute difference was 1.67e-8 across 60 fold scores, 1.81e-9 across the ten pooled scores and interval endpoints, and 1.48e-9 across the 12 paired contrast rows. I independently evaluated the 45 full-fit standardized predictions at equal distances of 50, 100 and 150 m and eight birds. For the two joint-probability models, I mixed the four cells over the original natural context distribution before calculating the conditional direction. The maximum standardized probability difference was 4.11e-9. The predictions describe the direction among discordant pairs. [Standardized results](../results/q3_direction_standardized.csv)

I ran the independent script from the repository root. The script and scratch tables are stored in the local temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q3-direction.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q3-direction"
```
