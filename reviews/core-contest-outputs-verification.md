# Independent review of restored contest outputs

The reporting plan froze at `7892ae8`. I replayed the existing 300 wide-row inputs at seed 20261127, fit the selected 0.0025-penalty pooled model and independently inverted its attenuation formula analytically. For ceiling `A`, scale `D`, exponent `g` and threshold `t`, the unconstrained radius is `D * ((A/t)^2 - 1)^(1/g)` for `t < A`. I bounded the radii to the measured 4–256 m support and took the 2.5th and 97.5th percentiles across the 300 draws. [Frozen design](../docs/model-spec.md#core-contest-reporting-thresholds-and-respondent-timing-freeze)

| Threshold | Flat radius and interval (m) | Modulated radius and interval (m) | Two-voice radius and interval (m) |
|---|---:|---:|---:|
| 0.40 potential | 111.51 [110.33, 112.75] | 178.09 [176.33, 180.31] | 207.25 [205.70, 208.65] |
| 0.50 standard | 84.52 [83.49, 85.80] | 143.85 [141.96, 146.08] | 173.24 [172.18, 174.39] |
| 0.60 reliable | 63.13 [61.98, 64.52] | 114.73 [112.93, 116.94] | 141.06 [140.08, 142.04] |
| 0.70 sensitivity | 43.16 [41.94, 44.67] | 85.02 [83.25, 87.08] | 99.42 [98.05, 100.78] |

The analytic inversion matches all 12 selected radius and interval rows in the clean default entry output within 3.3 × 10⁻¹³ m. Every point and draw crossing lies within the measured range, and all support-bound counts are zero. I also compared the original six fields of every archived 0.50 and 0.70 row against `25062e9`. All prior point values and crossing statuses match exactly. [Radius table](../results/core_q2_radii.csv)

I parsed Data02 directly and computed empirical medians for each stimulus from observed, flagged latencies, retaining zeros and using the earliest flagged onset for the any-event endpoint. The 24 representative rows agree with that replay, with eight birds and the same by-stimulus values at each distance. Counts below are pooled over calls and distances. [Latency table](../results/core_q3_representative_latency.csv)

| Endpoint | Natural median (s) and count | Control median (s) and count |
|---|---:|---:|
| Earliest response | 2.05 (90) | 2.00 (18) |
| Head raising | 2.00 (55) | 1.00 (13) |
| Vocalizing | 2.90 (76) | 4.80 (5) |
| Approach | 8.00 (23) | Unestimable (0) |


## Anonymous manuscript review

I independently extracted a clean archive of `fc77543` and ran two passes of `pdflatex -halt-on-error -interaction=nonstopmode main.tex` with `SOURCE_DATE_EPOCH=1795731780`. I rendered pages 4, 5 and 8 with Poppler. Table 2 gives the 12 selected estimates and intervals at the reported precision, and Figure 2 labels the three contest thresholds and distinguishes the 0.70 sensitivity. Table 4 matches the per-stimulus raw-data calculations and labels the pooling across calls and distances, eight birds, all three representative distances and unestimable control approach. The tables and figure are legible within the margins. [Manuscript tables and captions](../paper/results.tex)

The PDF contains 188 pages with references on page 10 and appendices starting on page 11. The cover and all running headers leave the team number blank. The PDF author metadata is blank, and listing captions run from 1 through 77. The 77 LaTeX listing paths each match one Git-tracked Python source. The independent PDF SHA-256 is `a7feec51f0eb5c8f28d0a509a72b09d21824dfdf9a9347bbd08d69d4a739e930`. **Pass.** [Anonymous PDF](../paper/main.pdf)
