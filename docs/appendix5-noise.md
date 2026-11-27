# Appendix 5 matched-power noise simulation

The experiment uses the three complete 12 kHz mono recordings, one per call type. For each of 200 paired noise draws, the same Gaussian samples supply all three spectra and six input SNRs from −10 to 20 dB. Within a clip and SNR, the three added noises have identical RMS. Pearson correlations compare aligned magnitude spectrograms, whole-clip magnitude spectra and Hilbert envelopes. The composite clips the equal-weight mean correlation to [0,1]. [Frozen protocol](model-spec.md#appendix-5-noise-injection-simulation-freeze)

| Clip at 0 dB input SNR | Broadband composite | 100–500 Hz composite | Above 500–3,000 Hz composite |
|---|---:|---:|---:|
| Flat | 0.77453 | 0.74567 | 0.72226 |
| Modulated | 0.76452 | 0.73642 | 0.72326 |
| Two-voice | 0.75751 | 0.72141 | 0.70704 |

At 0 dB, the middle-frequency band reduces the mean composite relative to broadband by 0.05228, 0.04127 and 0.05047 in call order. The paired central 95% ranges are [−0.05797, −0.04598], [−0.04750, −0.03465] and [−0.05726, −0.04486]. Spectrogram and magnitude-spectrum losses account for most of these changes. The mean envelope loss changes by less than 0.001 for each clip at this SNR. [Representation losses and composites](../results/appendix5_noise_summary.csv) · [Paired band-minus-broadband differences](../results/appendix5_noise_contrasts.csv)

At 0 dB, flat leads in the mean composite under broadband and 100–500 Hz noise. Modulated leads by 0.00100 over flat in the above-500–3,000 Hz band, and outranks flat in 104 of 200 realizations there. The mean leader also switches between broadband and this band at −10 and −5 dB. At 10 and 20 dB, the mean leader is flat in all three bands, with differences in the ordering of the other two examples. The noiseless comparison returns a composite of one for every clip, with representation losses within 1.23e-15 of zero. The reported percentiles describe noise realizations on these three recordings. The field Q4 loss mapping requires separate evidence on propagation and playback behavior. [Rank frequencies](../results/appendix5_noise_ranks.csv) · [Noiseless checks](../results/appendix5_noise_zero.csv)

Run `python main.py --data "<attachment directory>/date" --appendix5-noise` to regenerate the four CSVs. The same analysis is available through `python appendix5_noise.py --data "<attachment directory>/date"`.
