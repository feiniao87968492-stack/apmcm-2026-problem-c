# Independent numerical review of missing propagation comparisons

**Pass.** The review used the specification frozen in `87748d6`. I reconstructed the four outputs from Data02–Data11 before reading the implementation and compared all exported rows for the default 300 draws.

## Q2 completion bounds and quality grid

I materialized the completed arrays with each missing correlation set to −1 or +1. For each of the 63 call–representation–distance cells, the available count and missing count matched exactly, and the three means matched within $1.12\times10^{-16}$. All three representations contain 190 of 300 comparisons for two-voice at 128 m.

I used the min-max interval-mean formula to fit nonincreasing knots and solved threshold crossings in log base 2, including the boundary cases. Across 36 crossing rows, all reported statuses and ranks matched and the largest absolute radius difference was $8.53\times10^{-14}$ m. At threshold 0.50, the available-value radii are 84.72, 144.56 and 169.73 m for flat, modulated and two-voice respectively. The completion bounds are 44.80–130.46, 89.21–167.35 and 73.81–251.20 m. At 0.40 the two-voice upper completion attains the 256 m support boundary. Filling all slots at one endpoint is feasible under the specified correlation range, and the nonincreasing min-max formula preserves coordinate order, so these are sharp marginal bounds for the isotonic estimator under the specified completion set. [Cell counts and means](../results/missing_q2_cells.csv) · [Isotonic radius bounds](../results/missing_q2_radius_bounds.csv)

I also filled the raw arrays at each of the 101 quality levels. For the shared-exponent fit I constructed the residuals independently and used a bracketed root to find each in-range crossing. All 2,424 radius rows matched in support status and rank, with a maximum radius difference of $1.04\times10^{-6}$ m. At thresholds 0.40, 0.50 and 0.60, the first grid values where two-voice leads are 0.22, 0.21 and 0.46 for the isotonic fit and 0.30, 0.39 and 0.56 for the shared-exponent fit. At 0.70, two-voice overtakes flat between 0.35 and 0.36 and overtakes modulated between 0.97 and 0.98 in the isotonic fit. Modulated leads at all 101 values in the shared-exponent fit at that threshold. [Quality grid](../results/missing_q2_quality_grid.csv)

## Q4 common reference and attainment

I reconstructed the original acoustic draws, preserving the draw order including the aligned-draw random-number consumption. I rebuilt the behavioral masks and assigned call types from Data02, verified that pair members shared a date, and refit the standardized multinomial model on 300 resamples of the 12 whole dates. The shared full-data point reference was 0.28759819888730354. Across 54 completion and scenario rows, point and percentile margins matched within $7.01\times10^{-16}$. All attainment shares and 80% flags matched exactly, as did all 18 setting decisions. [Q4 attainment](../results/missing_q4_attainment.csv)

In clean conditions, modulated and two-voice at 50 m pass across completions. Flat at 50 m, modulated at 100 m, and two-voice at 100 and 150 m depend on completion. The three remaining settings fail across completions. Under 20% coupled loss, modulated at 50 m passes across completions, two-voice at 50 m depends on completion, and the other seven fail across completions. At two-voice 50 m under coupled loss, the available-value attainment share is 85.33% and the completion endpoints give shares of 51.00% and 90.33%. These statements describe the conditional scenario criterion on 20–150 m. The completion endpoints and the percentile margins quantify distinct sources of uncertainty. [Q4 attainment](../results/missing_q4_attainment.csv)

## Reproduction commands

I ran the following PowerShell commands in the repository with the independent verifier and comparator stored in the system temporary directory. The independent verifier imports no project modules.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-missing-review.py" "<attachment directory>/date" "$env:TEMP/apmcm-missing-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-missing-compare.py" results "$env:TEMP/apmcm-missing-independent"
```

The published entry point regenerates the compared tables with `python main.py --data "<attachment directory>/date"`. The review leaves no outstanding numerical correction for these four tables.
