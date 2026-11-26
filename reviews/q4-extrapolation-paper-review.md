# Independent manuscript review of Q4 extrapolation drift

I reviewed `014ea891bbe8c0b9c05ea36738b35190e0f1a542` against the frozen paper rubric. I carried forward the previous assessment for Q1–Q3 and the existing Q4 comparisons, then checked the new paragraph against the extrapolation protocol, the result table and the surrounding monitoring guidance. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Protocol](../docs/model-spec.md#q4-extrapolation-drift-freeze) · [Previous review](q4-paired-planning-paper-review.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The 100 and 120 m anchors, 4,002 baseline attainments, three rounded limits, 3,840 boundary attainments, joint odds factor and point probability shifts match the result table. |
| Traceability | 15 / 15 | The claim registry points to the drift CSV, all seven exported PNGs have CSV and metadata companions, and the appendix includes each of the 38 tracked Python modules once. |
| Coverage and reasoning | 30 / 30 | The paragraph names the union fit, adverse directions and fixed fidelity and clean cutoff. It limits the analysis to the 150 m extrapolation and calls for playbacks there. The paper retains the earlier Q1–Q4 comparisons and the field guidance on noise records and randomized validation. |
| Clarity and structure | 11.25 / 15 | The thresholds need an explicit indication that the displayed values are rounded. Page 15 opens with a single line from the preceding Limitations paragraph. |
| Build and references | 10 / 10 | An independent archive build reproduces the delivered PDF. Body and references take 13 pages, and all team fields and the PDF author are blank. |

**Initial score 96.25/100.** In the new paragraph on page 13, label the displayed drift limits approximate. The both-arms boundary is 0.0930456402872551, which rounds to 0.09305. The control-only value also rounds up. Applying the published decimal as an exact threshold would place those two scenarios beyond their passing limits. Keep the short Limitations paragraph together at the page break on pages 14 and 15. [Manuscript](../paper/results.tex) · [Full-precision evidence](../results/q4_extrapolation_drift.csv)

## Archive build

I extracted a separate Git archive and ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` with `SOURCE_DATE_EPOCH=1795731780`. The PDF hashes match at `e860d9bcdce8cc725eb0e7d2a92a0100867a63eaf3b12b5d5c3151ee3fbd9ce6`. Body and references occupy pages 3–15. The appendices start on page 16 and the drift source occupies part of pages 106–108. I rendered pages 13–16 and 106–108 and inspected the drift paragraph, Figure 4, field guidance, appendix transition and complete new listing. I checked all 108 page headers and the PDF author field. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `5daa2e1b0dc1882d4d6af5c22fd2e6700c693469` labels the limits approximate and gives the signed logit changes explicitly. The signs and anchors agree with the frozen protocol. The Limitations section moved intact to page 15, where one line from the preceding planning paragraph remained. Revision `acd5d0beefd2f773215a6f89d2cb5fb94d2658f4` keeps that paragraph together as well. The rendered pages 13–16 show the complete drift paragraph and Figure 4, the full paired-planning paragraph beside Limitations and References, and the clean appendix transition. [Revised manuscript](../paper/results.tex) · [Final PDF](../paper/main.pdf)

The final separate archive build reproduces SHA-256 `0f62df7459d56314519f34e9303e6edc63f208ecfe8dda36c31945372e174804`. The PDF has 108 pages with all team headers and the author blank. Body and references occupy 13 pages, and Listing 38 still starts on page 106. Both review findings are closed. Clarity and structure earns 15/15. **Final score 100/100, pass.**
