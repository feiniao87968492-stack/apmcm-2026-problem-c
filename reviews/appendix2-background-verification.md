# Independent audit of the Supplementary 2 audio

I decoded the approximately 44.928 s H.264 video and AAC audio locally with PyAV 13.1.0. The audio has two channels at 48 kHz and 2,156,544 decoded samples per channel. Audio-frame timestamps advance by 21.333 ms, consistent with 1,024 samples per frame. I examined video frames at 2 s spacing across the clip and at 0.5 s spacing through 11.5 s. I also examined separate channel spectra from 0 to 6 kHz with 1,024-sample windows and 256-sample hops, and calculated RMS and peak amplitudes from both channels.

| Time (s) | Evidence | Confidence |
|---|---|---|
| 1.25–2.45 | Precedes the first sampled playback caption. A furry microphone windscreen is visible near the camera. Channel RMS is −41.08 and −39.79 dBFS. The spectrum has a low-level bed without the strong stacked harmonics seen during playback. | Plausible pre-playback background for this recording. Sound-source attribution is uncertain. |
| 3.90–4.50 | The same scene and low-level audio bed precede the playback caption, which first appears in my 5.0 s sample. The longer 3.90–5.30 s audio window has channel RMS of −41.36 and −40.12 dBFS. | Plausible low-level background. The longer audio window overlaps the caption and gives no independently documented clean interval. |
| 5.6–6.0 and 8.05–8.45 | Strong harmonic bursts in both channels coincide with the first captioned playback phase. First-channel RMS is approximately −13.6 dBFS in each window. | High confidence in stimulus contamination. |
| 8.7–10.0 | A shorter harmonic event occurs near 8.8–9.1 s. The video displays RESPONSE in the 9.0, 9.5 and 10.0 s frames. | High confidence that this is an annotated response phase. The audio source is not separately labeled. |
| 10.75–11.15 | A third strong harmonic burst overlaps the second playback caption, visible at 11.0 and 11.5 s. First-channel RMS is −14.26 dBFS. | High confidence in stimulus contamination. |
| 12–44.9 | The video continues the same trial. The group becomes increasingly visible from about 24 s through 38 s. Both channels contain intermittent peaks in this phase, including events near 14.4, 23.3 and 34.2 s. | High confidence that this is continuing trial footage. Sources of individual events are uncertain. |

The low-level windows bound the best pre-playback background candidates in this file. The frames and both channel spectra establish their timing and relative level. The AAC soundtrack lacks source-isolated channels, a background annotation and metadata identifying a clean interval. Consequently, no continuous ambient-only segment can be verified from the attachment. This audit used video, waveforms and spectra. The review interface could not audition the audio directly.

I ran the local PyAV and audio inspection scripts from the repository root. The scripts and scratch plots are in the local temporary directory.

```powershell
py -3.10 "$env:TEMP/apmcm-appendix2-audit.py" "<attachment directory>/date" "$env:TEMP/apmcm-appendix2-independent"
py -3.10 "$env:TEMP/apmcm-appendix2-audio.py" "$env:TEMP/apmcm-appendix2-independent"
py -3.10 "$env:TEMP/apmcm-appendix2-dense.py" "<attachment directory>/date" "$env:TEMP/apmcm-appendix2-independent"
```
