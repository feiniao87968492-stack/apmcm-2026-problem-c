# Independent manuscript review of the Q4 noise evidence

I reviewed source commit `da208730ab543ffdfa7b6cbde0b2a1a86a34e088` under the frozen paper rubric and reviewed the revised source at `b091890b03be1cb4fbfb3eae78b0a81a36e2f5a2`. The evidence baseline was `41f7153643d6098940507a8682c2bcbb4d64f97f`. Earlier reviews cover the unchanged Q1–Q3 results and other Q4 analyses. The manuscript changes draw from the existing sources and derived tables. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Claim registry](../claims/claim-registry.md)

| Dimension | Initial | Final | Evidence |
|---|---:|---:|---|
| Numerical and factual accuracy | 30/30 | 30/30 | The +6 dB counts, the exponent limits, the 150 m loss boundaries and the composite differences agree with the archived tables. |
| Traceability | 15/15 | 15/15 | The six repository links resolve to paths present in the pinned evidence commit, including the video audit section. The 54 tracked Python files each have one listing. The seven figures have matching CSV and metadata files. |
| Coverage and reasoning | 30/30 | 30/30 | The gross radius and the signed net score differ in score, reference and distance rule. The 100 m simulation motivates verification of response coupling. The borderline 150 m result motivates sampling both arms near the support limit. The laboratory waveform comparison and the video audit lead to distinct field measurements. |
| Clarity and structure | 11.25/15 | 15/15 | The revised summary names the full behavior fit and all four shapes. The revised prose names both frequency bands and states the eligibility issue in the example video. |
| Build and references | 10/10 | 10/10 | The archive builds succeeded. The revised PDF is anonymous and the body and references occupy 16 pages. |

**Initial score 96.25/100. Final score 100/100, pass.** The revision closes the wording findings. I requested that the abstract identify the fit and the four acoustic shapes, and that the waveform paragraph state the upper band in ordinary prose. The revision also makes explicit that the time-stamped video audit could not verify the absence of playback, speech and music in the candidate window. [Summary and Q4 results](../paper/results.tex) · [Noise simulation and monitoring text](../paper/main.tex)

## Evidence checks

- At 100 m under +6 dB local loss, the full fit gives 4,538/4,800 (94.5%) with acoustic loss alone and 3,230/4,800 (67.3%) with equal response coupling. After union deletion the corresponding counts are 4,288 and 2,430. The full and deleted fits give local/matched-uniform exponent limits of 0.683627/0.667481 and 0.339062/0.319405, respectively. Each limiting exponent yields 3,840 qualifying draws. Equal retention at 100 m explains the shared endpoint result. The prefix requires passage at each evaluated 0.5 m node from 20 m in the same draw across all four acoustic shapes. The earlier 95.6 and 29.5 m radii are gross scores under the prior equal-call matching convention. [Response sensitivity](../results/q4_response_sensitivity.csv) · [Matched net scenarios](../docs/q4-matched-noise.md) · [Gross scenarios](../docs/noise-scenarios.md)
- At 150 m after union deletion, equal hypothetical losses of 0.215% each at the endpoint and 0.113% each along the full four-shape prefix match the diagonal export. The 3,850 clean prefix draws leave ten above 3,840. Independently applying an exact binomial interval gives 79.05255%–81.32726% for Monte Carlo precision. Natural and control training ranges end at 100 m and 120 m, respectively. [Target loss boundaries](../results/q4_target_loss_boundaries.csv) · [Retained ranges](../results/q4_consecutive_ranges.csv)
- At 0 dB input SNR the upper-band composite declines by about 0.05228, 0.04127 and 0.05047 over the three recordings. For that band the excess envelope losses are each below 0.001, consistent with the spectral interpretation. The 200 paired realizations per condition and equal RMS support a within-clip comparison. The study's 1.10–2.45 s video candidate remains unverified. The text calls separately for annotated, calibrated receiver recordings and for exposure measurements linked to paired playback outcomes. [Waveform results](../docs/appendix5-noise.md) · [Timestamped video audit](../docs/data-audit.md#supplementary-2-background-audio) · [Independent video review](appendix2-background-verification.md)

## Archive build

I extracted each reviewed commit with `git archive` and ran the following sequence from its archived `paper/` directory.

```powershell
$env:SOURCE_DATE_EPOCH = '1795731780'
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Get-FileHash main.pdf
```

The first PDF SHA-256 was `59460d35535258560b0d52d16cc67e691597fefe2e52ce63902c3c797036b40c`. The revised PDF SHA-256 is `08b39c0540952ea5a5ac7181c2094f2017fd715acd0002a7c8067cfc409444d6`. The summary and contents occupy pages 1–2. Body and references occupy pages 3–18. The appendices begin on page 19 of 149. Each page has a blank team identifier and the PDF author field is blank. I checked the changed pages as raster images and the six evidence URLs as PDF annotations, including the video audit anchor. Figure 4 and the four added source listings are legible. [PDF](../paper/main.pdf)
