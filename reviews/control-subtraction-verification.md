# Independent verification of Q4 control subtraction

I used the protocol frozen in `f2d71da`. I reconstructed the adopted shared-exponent fidelity from its fitted parameters and reused the archived Q2 acoustic and Q3 playback estimators at 300 draws. I computed the gross and signed net curves directly, integrated using explicit trapezoid weights proportional to distance with half weights at the endpoints, and solved the last qualifying threshold crossing by linear interpolation. The gross and net clean common cutoffs were 0.28759819888730354 and 0.19437071430107955. Each draw uses its own paired 20 m isotonic reference.

The clean gross area means, area-score intervals, pairwise gap intervals, rank intervals, and bounded radius estimates agree with the released annulus and noise summaries within the frozen tolerance of $10^{-12}$. For each of the 27 call, loss-link and distance combinations, the gross point margins and experiment-pair margin intervals, support shares and flags agree with the archived physical sensitivity at the same tolerance. The new inference uses whole-date draws. [Annulus area scores](../results/annulus_scores.csv) · [Annulus pairwise gaps](../results/annulus_score_gaps.csv) · [Archived clean radius intervals](../results/noise_q4_radii.csv) · [Physical sensitivity](../results/physical_q4_margins.csv)

At every point and draw, the difference between gross and net scores equaled acoustic fidelity after loss multiplied by the unchanged control probability. With 20% coupling, positive net scores are 0.64 times the clean value. Negative net scores scale by 0.80 because the coupling term clips the positive probability excess. The identities passed at absolute tolerance $10^{-12}$.

| Clean area means | Flat | Modulated | Two-voice |
|---|---:|---:|---:|
| Gross | 0.259431 | 0.380569 | 0.435121 |
| Net | 0.209519 | 0.327504 | 0.369938 |

The point area order is two-voice, modulated, flat for both scores in every scenario. Under 20% coupling, the gross point radii are 50.39, 79.72 and 102.78 m. Subtraction at the gross cutoff gives a 32.60 m modulated radius and no crossing within support for flat or two-voice, whose curves remain below the cutoff. The own net cutoff yields 58.32, 113.37 and at least 150 m respectively. The 150 m figure is the upper support boundary. [Area means](../results/control_subtraction_area.csv) · [Area gaps](../results/control_subtraction_area_gaps.csv) · [Bounded radii](../results/control_subtraction_radii.csv)

| Number of nine settings meeting 80% support | Clean | 20% acoustic-only | 20% coupled |
|---|---:|---:|---:|
| Gross | 5 | 2 | 2 |
| Net, gross cutoff | 3 | 2 | 0 |
| Net, own cutoff | 6 | 5 | 3 |

Changing gross to net at the same cutoff removes two passing decisions under clean conditions and two under coupling. The own net cutoff adds five passing decisions relative to gross across the three scenarios. Changing only the net cutoff adds three passing decisions per scenario. At two-voice and 100 m under coupling, support is 47.7% gross, 17.0% net at the gross cutoff and 81.7% net at its own cutoff. [Fixed-distance support](../results/control_subtraction_points.csv) · [Decision changes](../results/control_subtraction_decisions.csv)

I compared all exported rows with independent results at absolute tolerance $10^{-12}$. The largest absolute differences were $2.22\times10^{-16}$ across 18 area rows, $2.08\times10^{-16}$ across 18 area-gap rows, $4.27\times10^{-14}$ m across 27 radius rows, $1.11\times10^{-16}$ across 81 point rows and $2.22\times10^{-16}$ across 81 decision rows. Ranks, boundary statuses, counts and decision flags matched exactly.

## Reproduction

The independent calculation and comparison scripts are in the local temporary directory. Run from the repository using the archived data and the original default seeds.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-net-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-net-independent" "."
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-net-compare.py" "$env:TEMP/apmcm-net-independent" results "."
```
