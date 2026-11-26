# Independent verification of continuous recovery

I applied the specification frozen at `cff2038`. The independent calculation reads the archived representation-specific completion means, the 261-point standardized playback probability grid, and the released three-value plan minima. It uses exact rational arithmetic on the exported decimal knots to solve adjacent-block equalities. It projects the knots with the nonincreasing min-max formula, interpolates on the log-distance grid and applies explicit trapezoid node weights proportional to distance. The script imports no project modules. The independently computed no-recovery widths agree with the released annulus within $10^{-12}$. [Completion means](../results/missing_q2_cells.csv) · [Response curve](../results/q3_response_curve.csv) · [Archived no-recovery gaps](../results/annulus_completion_gaps.csv)

In the target gap, the two call widths add. Recovering both 128 m knots allows their residual widths to be maximized independently. I examined 25 candidate knots for two-voice, counting the union of the interval endpoints and the adjacent-block equality roots from both fits. The lower endpoint 0.04744 attains its largest residual width under both losses. The modulated call has three candidate knots. Its lower and upper fits coincide for every recovered value in [0.1907611111, 0.6574277778], because 128 m is its only incomplete knot. Every value in that interval therefore attains its maximum residual width of zero.

| Loss | Plan | No-recovery width | Largest residual width | Worst shrinkage | Relative shrinkage | Three-value minus continuous |
|---:|---|---:|---:|---:|---:|---:|
| Clean | Two-voice 128 m | 0.457352682 | 0.267795163 | 0.189557519 | 41.4467% | 0 |
| Clean | Modulated and two-voice 128 m | 0.457352682 | 0.121173312 | 0.336179370 | 73.5055% | 0 |
| 20% coupled | Two-voice 128 m | 0.302256206 | 0.176872984 | 0.125383223 | 41.4824% | 0 |
| 20% coupled | Modulated and two-voice 128 m | 0.302256206 | 0.080301899 | 0.221954308 | 73.4325% | 0 |

At each clean budget the largest competing three-value minimum bounds every competing continuous minimum from above. It is 0.146621850 for modulated 128 m at budget one, and 0.263556101 for two-voice at 128 and 256 m at budget two. The certified margins are 0.042935669 and 0.072623268. Both exceed the frozen tolerance, closing both comparisons with the archived competing bounds. The coupled results evaluate the clean winners. [Archived plan minima](../results/recovery_plans.csv)

**Pass.** All four published summary rows and all 106 breakpoint rows agree with the independent calculations. The largest absolute discrepancies are $3.89\times10^{-16}$ in the summary and $4.44\times10^{-16}$ in the breakpoint table. The comparison also checks the attaining knots and the exclusion of eight one-unit and 35 two-unit competing plans. [Continuous certificate](../results/recovery_continuous.csv) · [Breakpoints](../results/recovery_breakpoints.csv)

## Reproduction

The independent script ran from the system temporary directory with the repository as working directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-continuous-independent.py"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-continuous-compare.py"
```
