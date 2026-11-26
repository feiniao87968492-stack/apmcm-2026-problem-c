# Independent manuscript review of Q4 two-loss boundaries

I reviewed `36280389948fe1c2aebcbc29918f9827a9e162da` against the frozen rubric. The review covers the added two-loss comparison, the surrounding Q4 interpretation and the additional source listing. Earlier reviews cover the other analyses. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen specification](../docs/model-spec.md#q4-two-loss-net-boundary-freeze) · [Numerical review](q4-net-loss-verification.md)

| Dimension | Score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The retention formula, joint order statistic, binding shape, rounded loss limits and 3,858 clean draws reconcile with the frozen calculation and all three result tables. |
| Traceability | 15 / 15 | The claim registry links requirements, boundaries and counts. All 49 tracked Python files have a unique full-file listing. All seven exported figures have CSV and metadata companions. |
| Coverage and reasoning | 30 / 30 | The paragraph takes the maximum across the four requirements within each draw before applying the draw threshold. It identifies the losses as hypothetical and keeps the 150 m prediction after union deletion within its extrapolation scope. |
| Clarity and structure | 15 / 15 | The new paragraph fits on page 15. The page breaks before the model comparison and Fisher planning paragraphs are clean, and Figure 4 remains legible. |
| Build and references | 10 / 10 | A separate archive rebuild matches the PDF. Body and references occupy 15 pages. All 139 team fields and the PDF author field are blank. |

**Final score 100/100, pass.** For a positive clean net score the loss factors multiply. A nonpositive clean net score cannot attain the positive cutoff. For joint attainment each draw must satisfy all four shapes, and the paper follows this within-draw ordering. The fixed exponent binds all four limits. The maximum equal losses are 19.56% and 15.97% at 100 m, and 9.79% and 0.215% at 150 m, for the full and union-deleted fits respectively. After union deletion at 150 m the clean count is 3,858 and the single-component allowance is 0.430%. The protection discussion continues to call for field measurement and randomized validation. [Manuscript](../paper/results.tex) · [Requirements](../results/q4_net_loss_requirements.csv) · [Boundaries](../results/q4_net_loss_boundaries.csv) · [Counts](../results/q4_net_loss_counts.csv)

## Independent archive rebuild

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780` reproduce SHA-256 `5aa85c3446a636cbb30b7a5cefe2c1d4169317d96dae85bcf54f9fce48f3639e`. Body and references occupy pages 3–17, and the appendices start on page 18. I inspected the rendered Q4 pages 15–17 and the complete new Listing 49 on pages 137–139. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)
