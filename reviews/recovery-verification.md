# Independent verification of historical correlation recovery

**Pass.** I independently reconstructed the frozen comparison at `b0ae1b4` and checked the five published tables from `6efac25`. The calculation uses the archived Q3 mask fits and date predictions. I read Data03–Data11 directly, filled each missing correlation slot in the raw arrays, calculated the equal-weight completed means and implemented nonincreasing least-squares regression with the interval-mean min–max formula. I then interpolated on the log-distance grid and calculated area means using explicit trapezoid weights proportional to distance, with half weights at the endpoints.

All 63 representation-specific counts match the archived missing-data audit. Nine of the 21 call-by-distance units have missing entries. The largest counts across the three representations are 330 for two-voice at 128 m, 270 for two-voice at 256 m, and 210 each for flat and modulated at 128 m. The no-recovery profile reproduces the 12 Q2 radius endpoints and their boundary statuses at thresholds 0.50 and 0.60. It also reproduces all six clean and coupled Q4 gap rows, endpoint intervals and direction frequencies within the frozen absolute tolerance of $10^{-12}$. The clean two-voice minus modulated gap spans [−0.229075, 0.228278], with width 0.457353. [Unit audit](../results/recovery_units.csv) · [Archived radii](../results/missing_q2_radius_bounds.csv) · [Archived gaps](../results/annulus_completion_gaps.csv)

I enumerated nine one-unit and 36 two-unit plans with all 351 stipulated outcomes. Both criteria choose two-voice at 128 m at budget one and reduce the width by at least 0.189558 (41.45%) in the stipulated cases. At budget two, the minimax plan adds modulated at 128 m and guarantees a reduction of 0.336179 (73.51%) over those cases. The count plan adds two-voice at 256 m and guarantees 0.263556 (57.63%). Its 600 missing entries exceed the 540 in the minimax plan. All per-case widths and the selected-plan flags match the published results. [Plans](../results/recovery_plans.csv) · [Cases](../results/recovery_cases.csv)

I independently recomputed the selected cases at Q2 thresholds 0.50 and 0.60, including the support flags. I also applied the clean and 20% coupling formulas to the original date draws with the stipulated acoustic endpoints fixed. The target pair's Q4 direction is determined in seven of nine two-unit minimax cases within each condition, four favoring two-voice and three favoring modulated. The two-unit count plan determines that direction in five of nine cases, three favoring two-voice and two favoring modulated. The cases correspond to stipulated historical recoveries. Their frequencies describe the enumeration. [Radius sensitivity](../results/recovery_radii.csv) · [Gap sensitivity](../results/recovery_gaps.csv)

The verification matched all 21 unit rows exactly. The maximum absolute difference in the 351 cases and 45 plan summaries was $1.23\times10^{-15}$. The 132 radius rows agreed within $2.56\times10^{-13}$ m, with exact radius statuses, and the 132 Q4 gap rows agreed within $7.01\times10^{-16}$, with exact direction flags.

The independently written scripts ran from the local temporary directory with the pinned project environment. The verifier uses `q3.py` and `playback_dependence.py` for the existing behavior fits.

```powershell
$env:PYTHONPATH=(Get-Location).Path
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-recovery-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-recovery-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-recovery-compare.py" "$env:TEMP/apmcm-recovery-independent" results
```
