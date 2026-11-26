# Independent manuscript review of missing propagation comparisons

I reviewed manuscript commit `35b4fd8815a2bd1bb065cc53f3c5a123ef5bece8` and PDF SHA-256 `8bcaaa7249cbdddcc35580789ba10636bc595e805c273478cbb0c2b8c32ad0de`. I extracted that commit into a separate directory, read the local 2026 Problem C and essay-format PDFs, checked the manuscript against the released tables and the independent raw-data recomputation, and rendered and inspected pages 1–13. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Numerical verification](missing-propagation-verification.md)

| Frozen dimension | Score | Evidence |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The new counts, threshold radii, quality-grid crossings and date-based attainment match the released tables. |
| Traceability | 15 / 15 | The new sections identify the field study and nominal replication, and the claim registry points to all four new outputs. All seven figures have CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | Q1–Q4 remain covered. The conservation paragraph gives a concrete study design and candidate interventions. It leaves the placement of monitoring under the new Q4 evidence implicit. |
| Clarity and structure | 11.25 / 15 | Figures and captions fit. A single line from the limitations paragraph starts page 12 directly above the bibliography. |
| Build and references | 10 / 10 | A clean two-pass LaTeX build reproduced the extracted text without undefined references. Body and references occupy pages 3–12, and the appendices begin on page 13 of 73. The team number and PDF author are blank. |

**88.75/100.** No hard failure. Two changes are due for targeted re-review.

## Evidence checks

- Q1 uses grouped classification and preserves the six-feature logistic benchmark after uncertainty is considered. Q3 distinguishes the paired stimulus contrast, adjusted probabilities, grouped predictive comparisons and conditional timing. The onset appendix separates response probability from conditional median onset and marks unavailable control-approach timing. [Manuscript](../paper/main.tex) · [Onset appendix](../paper/latency-table.tex)
- For Q2, each two-voice representation at 128 m has 190 available comparisons. The three isotonic values at 0.50 are 84.7, 144.6 and 169.7 m, with completion bounds of 44.8–130.5, 89.2–167.3 and 73.8–251.2 m. The manuscript confines sharp bounds to the monotone isotonic chain and its support. The isotonic leader at 0.70 is modulated at 0.97 and two-voice at 0.98. Modulated leads across all 101 shared-exponent fits at that threshold. The archived row-bootstrap intervals and completion ranges represent different uncertainties. [Counts](../results/missing_q2_cells.csv) · [Radius bounds](../results/missing_q2_radius_bounds.csv) · [Quality grid](../results/missing_q2_quality_grid.csv)
- For Q4, the common reference uses the original date-based draws. Two of nine clean settings pass across all completions, four depend on completion and three fail throughout. Under 20% coupling, modulated at 50 m passes throughout, two-voice at 50 m is conditional on completion (85.3% from available values and 51.0–90.3% across completions), and seven settings fail throughout. The paper retains 150 m as the shared support boundary. [Q4 attainment](../results/missing_q4_attainment.csv) · [Claim registry](../claims/claim-registry.md)
- The public PDF contains no team number or author metadata. Both `pdflatex -interaction=nonstopmode -halt-on-error` passes succeeded from the archived commit. The published and rebuilt `pdftotext -layout` outputs share SHA-256 `a34c7c7b9b404ac5664294b1622c430bb21883f33c9d53fc6fce6c91a4183662`. The essay-format rules put a 25-page limit on the body and allow longer appendices. [Reviewed PDF](../paper/main.pdf)

## Targeted revisions

1. Tie field monitoring priorities to the completion results, especially two-voice at 50 m under 20% coupled loss and the longer tested distances, with 150 m treated as the support boundary. Retain the measured-noise and acquisition-identification requirements in the proposed field tests. [Conservation section](../paper/main.tex)
2. Shorten or consolidate the last sentence of the limitations section so that page 12 begins cleanly. Rebuild and inspect the affected page transition. [Limitations section](../paper/main.tex)

## Targeted re-review and acceptance

I reviewed revised manuscript commit `99dad78d5d31239d275f066bc322aff3949a7d89` and PDF SHA-256 `0abe1b4f4307790c26454a4b362f3884d108e31c45826862a657542752aba020`. The summary now identifies the completion-dependent 50 m two-voice result under 20% coupled loss. The conservation paragraph ties it to field follow-up, calls for acquisition identifiers and measured noise, and treats 150 m as the support boundary. The complete limitations section now starts page 12 above the five references. I inspected the revised pages and confirmed Figure 4 and its caption remain together on page 11. The appendix begins on page 13 of 73. The published and rebuilt extracted PDF text share SHA-256 `90a76feed3bd633b420d64dce1a8bdd08d9f41a51f0d56d7f343cff9420a31c6`, with blank team and author fields. [Revised PDF](../paper/main.pdf)

| Frozen dimension | Revised score |
|---|---:|
| Numerical and factual accuracy | 30 / 30 |
| Traceability | 15 / 15 |
| Coverage and reasoning | 30 / 30 |
| Clarity and structure | 15 / 15 |
| Build and references | 10 / 10 |

**Pass, 100/100.** Both targeted revisions are closed.
