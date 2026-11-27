# Independent verification of the Appendix 5 noise simulation

**Pass.** I independently decoded the three mono PCM WAVs with the Python wave module. Their lengths were 14,535, 12,000 and 12,000 samples at 12 kHz, and their centered RMS values were 0.020208, 0.025663 and 0.034721 for flat, modulated and two-voice. I generated the paired Gaussian vectors at seed 20261202, projected each prefix with a two-sided FFT and rescaled by its Euclidean norm. I recomputed the spectrogram with explicit periodic Hann windows, the magnitude spectrum from positive-frequency bins, and the envelope from the inverse transform of the analytic spectrum. The noiseless correlations and composites equal one to rounding accuracy. [Frozen protocol](../docs/model-spec.md#appendix-5-noise-injection-simulation-freeze) · [Noiseless checks](../results/appendix5_noise_zero.csv)

I checked the realized noise by subtracting the original waveform from each mixed signal. Its SNR differs from the target by at most 8.89e-15 dB across all 10,800 mixtures. All 216 metric summaries and 144 band-minus-broadband paired contrasts match within 5.00e-13 for the reported means and percentile endpoints. All 63 rank rows and their counts match exactly. [Summaries](../results/appendix5_noise_summary.csv) · [Paired contrasts](../results/appendix5_noise_contrasts.csv) · [Ranks](../results/appendix5_noise_ranks.csv)

At −10 dB, flat leads by mean composite in broadband and in the 100–500 Hz band. Modulated leads for the above-500–3,000 Hz band. At 10 dB, the broadband mean order is flat, two-voice, modulated. These are simulation comparisons conditional on the three example clips, with added noise power matched per clip and input SNR.

The independent script was run from the repository root. Its script and outputs are in the local temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-appendix5.py" "<attachment directory>/date" "$env:TEMP/apmcm-appendix5-verify"
```
