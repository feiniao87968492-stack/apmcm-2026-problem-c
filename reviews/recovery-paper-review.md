# Historical correlation recovery manuscript review

I reviewed commit `28f2f75b858b4e111472b959be7b035625320bcf` against the frozen paper rubric. In a separate Git archive, two runs of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` with `SOURCE_DATE_EPOCH=1795731780` reproduced the submitted PDF byte-for-byte. SHA-256 is `00da7f8ece08ba9f949cac0915a90a844849be5e3493e76b633ec93c17c50a9d`. The author field and the team field on each of the 74 pages are blank. The body and references occupy pages 3–13, and Appendix A begins on page 14. [Frozen rubric and specification](../docs/model-spec.md) · [Reviewed PDF](../paper/main.pdf)

| Dimension | Score | Finding |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The starting gap width, selected units, minimum reductions and counts of identified directions agree with the released results. |
| Traceability | 15 / 15 | The claim registry points to the unit audit, plan selection, case data, radius bounds and gap sensitivities. |
| Coverage and reasoning | 30 / 30 | The manuscript covers Q1–Q4 and states the equal-cost unit definition and the stipulated recovery values. The radial scenarios and conservation guidance retain their existing scope. |
| Clarity and structure | 15 / 15 | The recovery paragraph reads across pages 12–13. Figure 4 and its caption, the limitations section and the references fit on page 13. |
| Build and references | 10 / 10 | The independent archive rebuild is byte-identical, the anonymous fields are blank, and the paper meets the page limit. |

**Pass, 100/100.** No outstanding material issues.

## Evidence checks

- The clean two-voice minus modulated point gap without recovery is approximately [−0.229075, 0.228278], with width 0.457353. Both selection rules recover two-voice at 128 m on the one-unit budget, reducing width by at least 41.45% across the stipulated cases. The two-unit minimax plan recovers modulated and two-voice at 128 m with a 73.51% minimum reduction. Selecting by missing count recovers two-voice at 128 m and 256 m with a 57.63% minimum reduction. [Plan comparisons](../results/recovery_plans.csv) · [Case enumeration](../results/recovery_cases.csv)
- Seven of the nine cases for the minimax plan identify the target point ordering in both clean and 20% coupled conditions. Four favor two-voice and three favor modulated. The text ties these counts to the specified hypothetical assignments. The supporting tables report conditional date intervals and Q2 radius sensitivities with the acoustic support flags. [Gap results](../results/recovery_gaps.csv) · [Radius results](../results/recovery_radii.csv) · [Independent recomputation](recovery-verification.md)
