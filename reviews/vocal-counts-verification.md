# Independent numerical review of vocal counts and contact scenarios

**Pass.** I implemented the three calculations directly from Data02–Data11 under the specification frozen at `4652deb` before reading the production implementation. I checked the six exported tables. [Frozen specification](../docs/model-spec.md#vocal-count-and-contact-indicator-freeze)

## Paired count changes

I keyed the natural and control trial tables by experiment identifier, checked that their dates agree, and applied the exact distance and size filter before testing count completeness. Both count fields are available for all 139 pairs, including all 49 matched pairs. Each subset covers 12 dates. Natural and control mean changes are +1.914 and −0.065 calls per minute across all pairs and +1.776 and +0.102 in the matched subset. Natural-minus-control changes are +1.978 [1.682, 2.351] and +1.673 [1.308, 2.168], respectively, from 300 pair-weighted whole-date resamples. All six estimates and intervals match the export. [Pairwise results](../results/vocal_count_pairs.csv)

Positive after counts occur in 78 natural and seven control trials. Strict count increases occur in 76 and five, exactly matching the recorded `VocalYesNo` flag in every row. Two trials in each arm have positive after counts without a count increase. The count fields record group calls in equal 60-second windows. Summed calls can include repeated vocalizations from the same individual. [Count and flag audit](../results/vocal_count_audit.csv)

## Strict count prediction

I reconstructed each test date and removed any training pair sharing a natural playback track with that date. Training, testing and purging counts match the 12 archived folds. I independently optimized the summed Poisson objective with a unit L2 penalty on standardized nonintercept coefficients, using analytic gradients, analytic Hessians and a trust-region solver. I then separately scored pooled mean Poisson deviance and MAE. Across 36 fold/model rows the maximum absolute difference is $5.86\times10^{-7}$, and across six pooled comparison rows it is $9.54\times10^{-8}$, with identical decisions. [Archived strict folds](../results/strict_q3_coverage.csv) · [Vocal count folds](../results/vocal_count_folds.csv) · [Score comparisons](../results/vocal_count_scores.csv)

Stimulus means, the full Poisson, and the version with pre-playback count give deviance 2.5196, 2.3696 and 2.1938, and MAE 1.2694, 1.1455 and 1.1806. Adding pre-playback count changes deviance by −0.1758 [−0.7088, +0.1974] and MAE by +0.0351 [−0.0670, +0.1321] relative to the full Poisson. Neither Poisson specification meets the frozen joint gain criterion against stimulus means. [Score comparisons](../results/vocal_count_scores.csv)

## Contact scenarios

I recreated the acoustic row draws and the 300 whole-date logistic and multinomial refits, standardized their probabilities at eight birds using the natural-trial context proportions, and applied the threshold conditions directly to each draw. Across 18 settings and both outcomes, all near-distance coverage cells and every attainment count, point flag and 80% decision match exactly. The largest difference in probabilities, intervals or margins is $4.45\times10^{-16}$. Both endpoints attain the 80% rule in six clean settings and four coupled settings, with identical decisions. The modulated call at 50 m under coupling has 100% attainment for any response and 95% for count increase. At modulated 100 m under coupling, attainment is 63.7% and 59.3%, respectively. At the 150 m support boundary, two-voice attains 99.7% in clean conditions and 0% under coupling for both endpoints. Its local coverage is two natural and one control trial within 25 m. [Q4 outcomes and paired differences](../results/vocal_contact_q4.csv) · [Local coverage](../results/vocal_contact_coverage.csv)

## Reproduction

I ran these commands from the repository root with the independent scripts in the local temporary directory. The verifier imports no project modules.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-vocal-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-vocal-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-vocal-compare.py" "$env:TEMP/apmcm-vocal-independent" results results
```
