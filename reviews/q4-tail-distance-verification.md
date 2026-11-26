# Independent verification of tail scores by recorded playback distance

**Pass.** I rebuilt the 12 date-and-track-purged tail folds using an expID-by-stimulus distance table and metadata from each natural trial. I refitted A, B, C and E with the frozen implementation and used A's marginal predictions for D. I computed trial losses directly and summed scores and trial counts by the date of the natural member of each pair before applying the 4,800 date resamples at seed 20261201. [Frozen specification](../docs/model-spec.md#actual-playback-distance-audit-of-tail-validation)

The 26 held-out pairs contain 33 trials at 125 m or above on eight dates and 19 shorter partners on seven dates. Both bands had 4,800 valid resamples. All 12 published aggregate rows, including the pooled rows, matched. The maximum absolute difference was 4.45e-16 across absolute scores, differences and interval endpoints. Trial-weighted recombination of the two bands matched the archived pooled deltas within 1.15e-16. [Score table](../results/q4_tail_distance_scores.csv) · [Archived validation](../results/q4_tail_ablation_validation.csv)

| Band | E minus A mask log loss [95% interval] | E minus A any-response Brier [95% interval] |
|---|---:|---:|
| At least 125 m | −0.06243 [−0.28364, 0.20914] | −0.03427 [−0.06729, 0.00871] |
| Below 125 m | +0.23558 [0.05785, 0.36194] | +0.01497 [−0.00698, 0.04078] |

Both actual-long E intervals include zero. B and C have higher point losses than A on both long-trial scores, with intervals spanning zero. The frozen adoption rule retains A.

The two-voice coverage counts match the production table exactly. In the inclusive 125–175 m band, natural playbacks have two trials on two dates and two responses. Control has one trial on one date and zero responses. All three trials were played at exactly 150 m. [Coverage table](../results/q4_tail_distance_coverage.csv)

I ran the independent aggregation from the repository root. The script and scratch outputs are stored in the local temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-tail-distance.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-tail-distance"
```
