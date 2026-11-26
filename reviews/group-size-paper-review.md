# Independent manuscript review of group-size comparisons

## First review

I reviewed manuscript commit `37bea72042e7a7e4d3e36ace40e2de8be4d9002c` and PDF SHA-256 `d44378daf21e6715b775a7fcae046d60d47323ca3f2a8947daaf7e19f6065144`. The review applies the rubric frozen before the group-size analysis. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Dimension | Score | Finding |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The new paired gaps, matched intervals, strict losses, Q4 counts and local trial coverage agree with the result tables. |
| Traceability | 15 / 15 | The group-size claims map to five tables and an independent raw-data recomputation. The existing figures retain CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | All four questions are covered. The new group-size and earlier missing-comparison results need an explicit distinction in their Q4 interpretation. |
| Clarity and structure | 11.25 / 15 | The figures and captions fit. A forced break leaves only seven text lines from the preceding paragraph on page 12. |
| Build and references | 10 / 10 | Clean two-pass compilation reproduces the PDF byte-for-byte. Author metadata and all team headers are blank. The body and references occupy pages 3–13 and the appendices begin on page 14 of 74. |

**88.75/100.** Both presentation changes below require targeted re-review.

## Evidence checks

- Across all pairs, the natural-minus-control gaps by increasing size stratum are 72.2, 50.0 and 30.6 percentage points. The matching analysis uses 26, 9 and 14 same-distance and same-size pairs, with point gaps of 73.1, 33.3 and 21.4 points and the reported date-block intervals. The descriptive language preserves the distinction between a within-pair subtraction and comparisons across the natural size strata. [Paired contrasts](../results/group_size_pair_contrasts.csv)
- The group complementary log-log size offset follows from independent equal per-bird response probability at given covariates. The strict comparison finds log loss/Brier of 0.5530/0.1789, 0.7376/0.2353 and 0.5488/0.1784. Releasing the offset improves both scores over the fixed model. Both paired differences relative to logit include zero, so the frozen rule retains logit. Group outcomes can check the resulting prediction restriction and leave individual rates, dependence and counts unidentified. [Strict comparisons](../results/group_size_strict_scores.csv) · [Numerical review](group-size-verification.md)
- Across the 2-, 8- and 20-bird settings, 7, 4 and 2 call–distance combinations meet the 80% criterion in clean conditions. Under 20% coupling the counts are 4, 2 and 0. For two-voice at 100 m under coupling, attainment is 93.0%, 50.3% and 22.3%, and the count bounds agree after rounding. Local natural trials at the three exact target sizes number 1, 0 and 2 at that call and distance. At 150 m none of the three exact sizes has local natural trials in any call class. The paper confines the reported contrasts to fitted scenarios and retains the support boundary. [Q4 scenarios](../results/group_size_q4.csv) · [Coverage](../results/group_size_q4_coverage.csv)

## Targeted revisions

1. Identify the earlier Q4 missing-propagation comparison as the eight-bird analysis, particularly where it says all 100 and 150 m settings stay below 80% with coupling. The two-bird, two-voice result immediately above attains 93.0% at 100 m under its own comparison. [Q4 results text](../paper/results.tex)
2. Remove the forced break before Limitations and inspect the final body pages, keeping Figure 4 with its caption and references together. [Manuscript](../paper/main.tex)

## Targeted re-review and acceptance

I reviewed revised manuscript commit `21743a0969d4076982635883d0458a7befc24dec` and PDF SHA-256 `ef22ff94b81c5ae06330160f6053e2ff1ecb4eefad57a44caf46113d0aaaf0e3`. The revision explicitly scopes the missing-propagation results to eight birds and retains logit for strict binary prediction. Figure 4 and its caption fit together on page 11. Page 12 contains the conservation conclusion, the complete limitations section and all five references. Appendix A starts on page 13 of 73. A detached checkout rebuilt the PDF byte-for-byte with two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` and `SOURCE_DATE_EPOCH=1795731780`. All 73 team headers and the author field remain blank. [Revised PDF](../paper/main.pdf)

| Frozen dimension | Revised score |
|---|---:|
| Numerical and factual accuracy | 30 / 30 |
| Traceability | 15 / 15 |
| Coverage and reasoning | 30 / 30 |
| Clarity and structure | 15 / 15 |
| Build and references | 10 / 10 |

**Pass, 100/100.** Both targeted revisions are closed.
