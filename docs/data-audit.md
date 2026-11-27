# Data audit

- Data01 contains 108 recordings in 16 date-by-location groups. There are 44 flat, 40 modulated, and 24 two-voice calls. The second fundamental is missing in 84 recordings. The primary classifier uses the six complete numeric predictors. The source study measured pulse rate only when the recording displayed amplitude modulation. Pulse rate is absent in all 44 flat calls, 6 of 40 modulated calls, and 4 of 24 two-voice calls.
- Data02 contains 278 stimuli in 139 experiment pairs. The natural stimuli comprise 48 flat, 33 modulated, and 58 two-voice calls. Any response is recorded for 90 natural stimuli and 18 controls. Observed playback distances span 5–200 m and median group size is 8.
- Data03–Data11 each contain 300 rows and seven columns for distances from 4 to 256 m. The source study measured propagation at Brandvlei Dam under calm conditions. Each call type used three examples and up to 10 by 10 reference?distance comparisons per example. The CSVs omit example identifiers. The consecutive 100-row groups are a sensitivity assumption. Missingness varies with distance and call type, so retain available-case counts beside distance summaries.
- The reported behavior is at the observed-group level. The supplied intensity variables and the latency variables represent different measurements.
- The analyses use the original contest CSV files as inputs. [Archive and supplementary material](https://zenodo.org/records/21376649).

Natural and control stimuli differ within 90 pairs in distance and within two pairs in observed group size. Date and context agree within every pair. Raw paired differences are descriptive and modeled comparisons use identical covariate grids.


## Public archive coverage

The field paper lists the Zenodo concept DOI 10.5281/zenodo.21376648 for underlying data and record DOI 10.5281/zenodo.21376649 for extended data. Both resolve to the same deposit, which had one public version on 2026-11-27. All 20 files match the contest attachments by the deposit's MD5 checksums, allowing for the filename change in Supplementary 4. The deposit contains 11 CSVs, two R scripts, three PDFs, one example playback video and three example call WAVs. [Field paper](https://doi.org/10.12688/openreseurope.24618.1) · [Archive metadata](https://zenodo.org/api/records/21376649) · [Versions](https://zenodo.org/api/records/21376649/versions)

The field paper reports broadcast levels of 82–86 dB SPL at 1 m for the marine playback trials and 84 dB SPL at 1 m for the dam propagation experiment. Data02 records the trial identifiers, playback tracks, distances and responses. The deposit lacks background sound levels linked to those trials and lacks a calibrated recording series from which to reconstruct them. [Field methods](https://doi.org/10.12688/openreseurope.24618.1) · [Data02 and example media](https://zenodo.org/records/21376649)

Recovering the missing 128 m propagation correlations would require the original 1 m and 128 m recordings or the omitted correlation values, with the calls and repetitions identified. The deposit supplies the processed correlation tables. The prioritization analysis measures the conditional benefit if those observations become available. [Recovery analysis](recovery-priority.md)

## Supplementary 2 background audio

The example playback MP4 (SHA-256 `77a3450fa8070503035f50002913716270526de7c309bb4b486c166609192586`) contains 44.928 s of continuous decoded stereo AAC at 48 kHz. Times below are relative to the start of the file. Channel levels are dBFS, relative to the digital recording's full scale.

| Time (s) | Observation | Use as background |
|---|---|---|
| 1.10–2.45 | Low-level pre-playback candidate between low-frequency transients near 0.8 and 2.6 s. Left/right RMS is −41.06/−39.76 dBFS. The independent reviewer identified a similar interval (1.25–2.45 s). | Source uncertain. The 1.35 s duration can fit the longest Supplementary 5 example (1.21125 s). |
| 3.90–4.50 | Low-level pre-playback candidate at −41.57/−40.10 dBFS. The first sampled playback caption appears at 5.0 s. | Source uncertain and too short for the longest example. |
| 5.60–6.00, 8.05–8.45, 10.75–11.15 | Strong harmonic bursts align with the playback phases. Left-channel RMS is −13.58, −13.60 and −14.26 dBFS, respectively. | Playback contamination. |
| 8.70–10.00 | A short harmonic event occurs near 8.8–9.1 s and the sampled frames at 9.0–10.0 s display RESPONSE. | Response phase with unassigned acoustic sources. |
| 12.00–44.90 | Trial footage continues and includes intermittent peaks near 14.4, 23.3 and 34.2 s. | Source uncertain. |

The main and independent audits used frames, stereo waveforms and spectra. Direct listening was unavailable. An exploratory voice-activity detector also flagged the first candidate. Such flags can arise from broadband noise and leave the presence of speech unresolved. The soundtrack has no source-isolated background channel or clean-interval annotation. Neither audit could establish a continuous segment free of playback, speech and music. The evidence supports retaining the [Supplementary 5 synthetic-noise comparison](appendix5-noise.md) as a waveform sensitivity analysis. The three-way comparison with an original background clip lacked an eligible input. [Independent audit](../reviews/appendix2-background-verification.md)

Calibrating acoustic loss for Q4 requires receiver-position recordings with calibrated levels and enough annotated background-only intervals across locations or trials to estimate spectra and SNR. Calibrating the response loss separately requires natural and control playback outcomes linked to the measured noise exposure, accounting for distance, context and group size. A single example soundtrack supplies neither calibration.

### Reproduce the audio-window checks

With PyAV 13.1.0 and NumPy installed, set `$attachmentCsvDir` to the local `date` directory and run this from PowerShell. The 0.5 s pre-playback and playback frames and 2 s frames across the full clip can be checked in a local video player.

```powershell
$video = Get-ChildItem -LiteralPath $attachmentCsvDir -Filter 'Supplementary2*.mp4' |
    Select-Object -First 1
@'
import sys
from hashlib import sha256
from pathlib import Path

import av
import numpy as np

path = Path(sys.argv[1])
print(sha256(path.read_bytes()).hexdigest())
with av.open(str(path)) as container:
    audio = list(container.decode(audio=0))

rate = audio[0].sample_rate
wave = np.concatenate([frame.to_ndarray() for frame in audio], axis=1)
sample_starts = np.cumsum([0] + [frame.samples for frame in audio[:-1]])
timestamps = np.array([frame.time for frame in audio])
np.testing.assert_allclose(timestamps * rate, sample_starts, rtol=0, atol=1e-5)
print(rate, wave.shape, wave.shape[1] / rate)

windows = [(1.10, 2.45), (1.25, 2.45), (3.90, 4.50),
           (5.60, 6.00), (8.05, 8.45), (10.75, 11.15)]
for left, right in windows:
    segment = wave[:, round(left * rate):round(right * rate)]
    dbfs = 10 * np.log10(np.mean(segment ** 2, axis=1))
    print(left, right, np.round(dbfs, 2))
'@ | python - $video.FullName
```

## Playback design and order recoverability

This read-only audit was frozen against manuscript baseline 7b6bd67. The version 1 field paper, Methods, “Playback experiments” (pp. 4–5), describes testing the same observed group once with a natural call track and once with a sea-wave recording. The researchers randomly switched which stimulus came first between experiments and randomly drew the natural playback track without replacement within each behavioral context. They included only groups tested with both stimuli. The sea-wave control was broadcast as a stimulus. Each row describes a group response to one playback, and the two rows for an experiment form a group-level pair. [Field paper v1](https://doi.org/10.12688/openreseurope.24618.1)

For successive same-day experiments, the researchers sought to keep each new group more than 300 m away during the preceding playback. At the same boat position the protocol also required at least five minutes between experiments. The alternative was to move the boat more than 1 km in a direction different from the previous group's route. [Field paper v1](https://doi.org/10.12688/openreseurope.24618.1)

Data02 (MD5 f936555cb0af178dcb749ec9b51adab5) has 40 columns and 278 rows. Each of the 139 `expID` values joins one `call` and one `control` row with matching `Date` and `Context`. `PlaybackTrack` records the assigned natural track and uses the common label `control` for the sea-wave stimulus. The records support auditing realized track use by context. They lack the randomization log, draw sequence and available track pool for each draw. `Distance` describes boat-to-bird playback distance. The data lack timestamps and coordinates for checking separation or elapsed time between groups. [Versioned data deposit](https://zenodo.org/records/21376649)

Data02 has no presentation-order field or per-stimulus timestamp. All pairs occupy adjacent rows in the file, with 81 stored call first and 58 stored control first. The field methods and accompanying analysis materials do not document this file order as chronological. The response latency fields measure elapsed time from an individual playback's onset and cannot identify which stimulus came first. The Q3 models pair the stimuli and adjust for recorded covariates. Presentation order and carryover are unestimated. [Data02, Code1 and Supplementary 3](https://zenodo.org/records/21376649)
