# Independent verification of supported annulus summaries

**Pass.** I independently implemented the spatial summaries from the specification at `a844b4d` before inspecting or comparing production output. I regenerated the archived acoustic and date-draw inputs, then compared the seven released tables at `05bd6e8`. All keys, rank ranges, boundary statuses, connected intervals, qualifying nodes and attainment counts matched.

| Output | Rows | Largest absolute numeric difference |
|---|---:|---:|
| Integrated scores, losses and ranks | 54 | 4.17 × 10⁻⁹ |
| Paired score gaps | 54 | 1.21 × 10⁻⁹ |
| Pointwise attainment grid | 7,047 | 0 |
| Annulus attainment and radius comparisons | 30 | 3.10 × 10⁻⁷ m for radius |
| Connected intervals | 28 | 9.37 × 10⁻¹⁷ in area fraction, exact endpoints |
| Completion scores | 18 | 2.22 × 10⁻¹⁶ |
| Completion gaps and identification | 6 | 2.08 × 10⁻¹⁶ |

I computed both quadratures with SciPy's trapezoid rule and distinct weight normalization. I reconstructed the physical loss from the fitted noise term, averaged relative losses across calls at 100 m for the matched uniform scenario, and subtracted the specified fraction of positive response excess under coupling. I independently assembled shared-exponent inputs using an arithmetic mean across the three representations. The alternative summation order leads to small optimizer-level differences in those fits. The resulting differences are negligible at the reported precision. All 18 weight-by-scenario point rankings are two-voice, modulated and flat. The clean area score gap for two-voice minus modulated is 0.0546 (95% interval −0.1129 to 0.1778). Six-dB local attenuation with coupling reduces the clean area indices by 53.28%, 42.03% and 34.50% in flat, modulated and two-voice order. [Scores](../results/annulus_scores.csv) · [Gaps](../results/annulus_score_gaps.csv)

I used the original draw-specific isotonic cutoff and split each sequence of qualifying nodes at grid gaps. I checked interval areas by endpoint squares and independently computed the archived last qualifying point radii by scalar linear interpolation. For clean two-voice, the supported interval is 20–138.5 m with area 84.99%. Its single point radius reaches the 150 m support boundary with a filled fraction of 100%. Across the eight noisy scenarios the shared interval is empty for flat, 20–29 m for modulated and 20–20.5 m for two-voice. The corresponding fractions are 0%, 2.00% and 0.09%, versus 0.99%, 3.87% and 2.14% when filling to the smallest scenario radius. [Attainment](../results/annulus_attainment.csv) · [Intervals](../results/annulus_intervals.csv) · [Grid](../results/annulus_attainment_grid.csv)

I completed the raw acoustic arrays at the feasible endpoints and independently rebuilt all isotonic fits with the nonincreasing min-max mean formula. Positive integration weights and nonnegative modeled responses preserve order by acoustic fidelity. Each opposing endpoint combination is permitted across call types under the frozen completion set. Every pair's sharp point gap spans zero in clean and 20% coupled conditions. The clean modulated-minus-two-voice gap ranges from −0.2283 to 0.2291. These are completion ranges with separate date percentile intervals at each endpoint. [Completion scores](../results/annulus_completion_scores.csv) · [Completion gaps](../results/annulus_completion_gaps.csv)

The independent script imports only archived upstream model functions. It uses local temporary scripts and CSVs. I ran both commands from the repository root with the repository on the Python import path.

```powershell
$env:PYTHONPATH = (Get-Location).Path
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-annulus-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-annulus-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-annulus-compare.py" "$env:TEMP/apmcm-annulus-independent" results
```
