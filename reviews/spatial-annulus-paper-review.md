# Independent review of the supported annulus manuscript

I reviewed manuscript commit `5e15489c083db3cd538ffaea61cbe0709477f165` under the frozen independent paper rubric. An archived-source build reproduced PDF SHA-256 `8dd73c1c3acde944b32a7c6bd7d61bfdd5b0c63b47bbf2c118c53b5aef4a6678` byte-for-byte. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Dimension | Score | Finding |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | Both normalized averages, paired ranking interval, losses, attainment fractions and completion bounds agree with the released tables. |
| Traceability | 15 / 15 | The claim registry maps the three analyses to the seven released tables. |
| Coverage and reasoning | 30 / 30 | Q1–Q4 remain covered. The annulus analysis separates integrated index, pointwise attainment and incomplete-data ranking, and states the radial assumption and support boundary. |
| Clarity and structure | 11.25 / 15 | The added text and Figure 4 fit on page 12. An inherited forced break leaves a short continuation of conservation alone on page 13. |
| Build and references | 10 / 10 | The archived build reproduces the PDF, all 75 team fields and the author field are blank, and the body and references occupy pages 3–14. |

**Initial score 96.25/100.** Remove the forced break before Limitations to place the conservation continuation and references together. [Manuscript source](../paper/main.tex)

## Evidence checks

- The clean distance averages are 0.312, 0.426 and 0.464 for flat, modulated and two-voice calls. The corresponding area averages are 0.259, 0.381 and 0.435. The point order holds under both weights throughout the scenarios. The clean two-voice minus modulated area gap has paired limits of −0.113 and 0.178. The reported 6 dB coupled losses agree for both attenuation shapes. [Scores](../results/annulus_scores.csv) · [Gaps](../results/annulus_score_gaps.csv)
- The 80% rule qualifies clean two-voice over 20–138.5 m, covering 85.0% of the supported annulus. The clean point radius reaches the 150 m boundary. The eight-scenario intersection is empty for flat, 20–29 m for modulated and 20–20.5 m for two-voice. The stated 0%, 2.00% and 0.09% fractions and the point-radius comparisons agree with the results. The manuscript limits these comparisons to the radial scenarios. [Attainment](../results/annulus_attainment.csv) · [Intervals](../results/annulus_intervals.csv)
- The isotonic completion endpoints match the three clean ranges in the paper. All six pairwise point-gap ranges contain both positive and negative values. The ranking therefore depends on allowed completions in both clean and 20% coupled conditions. [Completion scores](../results/annulus_completion_scores.csv) · [Completion gaps](../results/annulus_completion_gaps.csv)

## Targeted re-review

I rebuilt `1018047` from a separate Git archive with two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` and `SOURCE_DATE_EPOCH=1795731780`. The rebuilt PDF matches SHA-256 `125f0236c896377d214a616beeb849d84ff9a85b075b337cbf3e2044561eed2b`. The rendered page 13 now contains the conservation continuation, complete Limitations and all five references. Figure 4 and its caption remain together on page 12. The body and references occupy pages 3–13, and Appendix A begins on page 14 of 74. All team fields and author metadata are blank. Clarity and structure is restored to 15/15. **Final score 100/100, pass.** [Reviewed PDF](../paper/main.pdf)
