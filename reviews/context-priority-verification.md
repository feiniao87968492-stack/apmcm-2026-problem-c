# Independent verification of Q4 context and behavior priorities

**Pass.** I used the specification frozen at `a2e82e9` and wrote the independent calculations before inspecting the production implementation at `094fad4`. The verifier uses the archived Q2 acoustic resampler and shared-exponent fitter. I independently rebuilt the playback design and response masks from Data02, fitted the specified standardized multinomial logit on the full sample and each of 300 date draws, and paired these predictions with the original acoustic draws by index. I evaluated fidelity from the archived formula and integrated using explicit trapezoid nodal weights proportional to distance, with half weights at the 20 and 150 m endpoints.

For the empirical context mix and clean any-response index, the maximum absolute difference from the published annulus point scores, score intervals and pairwise gap intervals was $2.22\times10^{-16}$, below the frozen tolerance of $10^{-12}$. The clean point scores are 0.259431, 0.380569 and 0.435121 in flat, modulated and two-voice order. The clean and 6 dB any-response point order holds for every pure context. At the empirical mix, modulated calls lead for head raising and approach, and two-voice calls lead for vocalizing. All behavior scores sum masks containing the event. [Archived scores](../results/annulus_scores.csv) · [Archived gaps](../results/annulus_score_gaps.csv) · [Priority scores](../results/context_priority_scores.csv)

For each ordered pair I independently subtracted the nine corresponding vertex scores and optimized the endpoints in every paired draw. Products of the two unit-sum weight vectors form convex weights over those nine values. Every extremal vertex is feasible with two pure weight vectors. The two-voice minus modulated range is [−0.077425, 0.094269] in clean conditions and [−0.046544, 0.089153] at 6 dB. Searching and head raising attain its minimum, while resting after feeding and vocalizing attain its maximum in both scenarios. The 95% interval for the minimum is [−0.296776, −0.015440] in clean conditions and [−0.206401, −0.005773] at 6 dB. No direction has a positive lower 95% limit for its minimum gap. [Priority gaps](../results/context_priority_gaps.csv) · [Exact endpoint comparisons](../results/context_priority_bounds.csv)

The empirical mix uses 36/139 resting after feeding, 65/139 commuting and 38/139 searching. I independently tabulated event, trial and date counts over the common support and each local distance window clipped to that support. The 150 m window contains eight natural trials and one approach. It contains no natural trials for flat or modulated calls after feeding, or for two-voice calls while searching. [Coverage](../results/context_priority_coverage.csv)

All four published tables agree with the independent implementation. The maximum absolute differences are $5.55\times10^{-16}$ across 96 score rows, $5.97\times10^{-16}$ across 96 gap rows, and $3.89\times10^{-16}$ across 12 endpoint rows. Ranks, attaining vertices and robustness flags agree exactly. All 36 coverage rows agree exactly.

## Reproduction

The independent verifier and comparison scripts ran from the system temporary directory. I used these PowerShell commands from the repository and the original contest input path.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-priority-independent.py" "$env:TEMP/apmcm-priority-archive" "<attachment directory>/date" "$env:TEMP/apmcm-priority-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-priority-compare.py" "$env:TEMP/apmcm-priority-independent" results
```

The archived verifier inputs are `q2.py`, `q3.py`, `q4.py`, `physical_attenuation.py`, `results/annulus_scores.csv` and `results/annulus_score_gaps.csv` from `a2e82e9`.
