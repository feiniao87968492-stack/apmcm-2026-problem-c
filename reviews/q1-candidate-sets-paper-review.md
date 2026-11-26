# Independent manuscript review of Q1 candidate sets

I reviewed `d0e833b028f5ba0cb5a45aa918f314431273e40f` against the frozen paper rubric and carried forward the previous assessment of the earlier analyses. This review covers the new candidate-set analysis, its use alongside the retained hard-label benchmark, and the updated appendix. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen candidate-set protocol](../docs/model-spec.md#q1-candidate-sets-for-a-held-out-recording-group) · [Previous review](q4-tail-distance-paper-review.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | Top-1 and top-2 coverage, the three 80% coverage and size estimates, the complete-group improvement and paired interval, and the 90% full-set counts and calibration ranks match the exports. |
| Traceability | 15 / 15 | The claim registry maps the Q1 results to the threshold, fold, summary and paired tables. The appendix covers all 42 tracked Python files, with one full listing per file. All seven exported figures have CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | The coverage and size tradeoff is clear. Name the equal-group target explicitly and tie top-1 and top-2 to the new leave-one-group-out splits. |
| Clarity and structure | 15 / 15 | Both Q1 additions fit on page 4. Figure 1 fits on page 5 and remains readable. The source listing begins on page 118 and ends on page 121. |
| Build and references | 10 / 10 | The independent archive rebuild matches the delivered PDF. Body and references occupy 14 pages. All team fields and the PDF author are blank. |

**Initial score 92.5/100.** The group-maximum 80% rule covers every recording in 14 of 16 held-out groups, up from 3 of 16 for top-2 on the same splits. Its average set size rises from 2 to 2.83, and 93 of 108 sets contain all three labels. To clarify the evaluation unit, introduce the top-1 and top-2 paragraph with “On these leave-one-group-out splits.” These give top-1 two-voice coverage of 1/24, while the retained five-fold benchmark gives hard-label recall of 2/24. Add that equal-group calibration targets coverage for a uniformly chosen recording in a new group and retain the neighboring explanation of the group-maximum target. [Manuscript](../paper/results.tex) · [Summary](../results/q1_candidate_sets_summary.csv) · [Paired comparisons](../results/q1_candidate_sets_paired.csv)

## Independent archive rebuild

I built from an independent Git archive with two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/` and `SOURCE_DATE_EPOCH=1795731780`. The archived and rebuilt PDFs both have SHA-256 `2d78525d89e100f67ae079fbcec65946158d8f89a832ffafd0a47ef313e4e9c0`. Body and references occupy pages 3–16, and the appendices start on page 17. All 121 page headers have blank team fields. I rendered the affected Q1 pages and inspected Figure 1 and the new source listing. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `5e10f952d1787a3db585c1896ad4cd26e0607d1b` distinguishes coverage of a uniformly chosen new-group recording from simultaneous coverage of the group. It explicitly assigns top-1 and top-2 results to the leave-one-group-out splits and retains the five-fold hard-label benchmark. Both passages remain intact on rendered page 4. Figure 1 remains legible on page 5. [Revised manuscript](../paper/results.tex)

The independent two-pass build reproduces final PDF SHA-256 `e27ce96c619f85f2cecdadd46f103e68deeabc35cab0d33c1770216b37633787`. Body and references occupy 14 pages, the appendices start on page 17, and all 121 team headers and the PDF author field are blank. Coverage and reasoning earns 30/30. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
