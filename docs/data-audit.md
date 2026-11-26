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
