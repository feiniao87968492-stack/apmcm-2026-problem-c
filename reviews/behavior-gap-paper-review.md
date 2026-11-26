# Independent manuscript review for the Q3 behavior-gap decomposition

I reviewed manuscript commit `21d29654e19aa693d1aa6daf050b5645ad69dc11` under the frozen independent paper rubric. A two-pass build from a Git archive reproduced the committed PDF SHA-256 `3ddabc4059922b61276c4b7c9cb2d641b9063604f007e61df879f63869bd7840`. The first build scored 96.25/100 because the final Limitations line appeared alone above the references at the start of page 14. The targeted page break at `1c0b92e10d51b767bcbd21f4f549b3304b4cf1a9` closes that issue.

| Dimension | Final score | Evidence |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The reported gap, decomposition terms, date intervals and local trial counts match the released estimates. |
| Traceability | 15 / 15 | The claim registry maps the raw and standardized estimates to their result tables. Both include responder or local-support counts. |
| Coverage and reasoning | 30 / 30 | Q1–Q4 retain coverage. The new Q3 results distinguish response frequency from composition among responders and state the descriptive scope and the order of standardization and conditioning. |
| Clarity and structure | 15 / 15 | The new paragraph fits on page 7. Figures 3 and 4 remain with their captions. The complete Limitations section and references share page 14. |
| Build and references | 10 / 10 | The anonymous PDF builds byte-for-byte. The body and references occupy pages 3–14. The appendices start on page 15. |

**Final score 100/100, pass.**

## Evidence checks

In all 139 pairs, the vocalizing gap is 51.1 percentage points, with 29.1 points for frequency and 22.0 points for composition. The 95% date-block composition interval is [14.5, 30.8] points. For the 49 same-distance, same-size pairs, the composition estimate is 26.3 [11.6, 40.0] points. Approach composition is positive in both samples. Both head-raising composition intervals include zero. The two raw cohorts have 90 and 18 or 33 and 8 natural and control responders, respectively. Every raw decomposition has all 300 date draws available. [Raw estimates](../results/behavior_gap_raw.csv)

At eight birds, the standardization mixes mask probabilities across empirical contexts before conditioning. Head-raising composition point estimates are negative in all nine settings. Vocalizing and approach composition point estimates are positive in all nine. For two-voice calls near 150 m, the support table gives two natural trials and one control within 25 m. Both natural trials responded and the local control trial had no recorded response. The manuscript describes both terms descriptively. [Standardized estimates](../results/behavior_gap_standardized.csv) · [Claim registry](../claims/claim-registry.md)

Across both tables, I checked all 110 point identities and confirmed agreement of 63 standardized positive-mask gaps with the archived Q3 contrast file to absolute tolerance `1e-12`. The independent numerical review covers the resampled estimates and supporting counts. [Archived mask contrasts](../results/q3_predicted_mask_contrasts.csv) · [Numerical review](behavior-gap-verification.md)

## Final archived build

I ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from a separate Git archive of `1c0b92e` with `SOURCE_DATE_EPOCH=1795731780`. The resulting PDF matched the committed SHA-256 `7bc15d45c2785eba781128a5b204ab0e0e87bd599a531a2c8a1415dc6cd2b3ac`. I checked all 75 sequential page headers, blank team fields and blank author metadata. I rendered pages 7–9 and 12–14 to inspect the decomposition, figures and revised pagination. [Final PDF](../paper/main.pdf)
