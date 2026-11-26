# Independent manuscript review of Q4 envelope-weight attainment

I reviewed `cfe8e1324f904c43e5a3a2d52ae78029557ee497` against the frozen rubric and carried forward the earlier assessment of unchanged analyses. I verified the new Q4 paragraph, its placement before the drift and model comparisons, and the new source listing. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen Q4 specification](../docs/model-spec.md#q4-envelope-weight-attainment-freeze)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The 4,002 and 4,142 equal-weight counts, 3,813 and 4,048 counts at weight 0.50, and four rounded interval limits match the numerical review and exports. |
| Traceability | 15 / 15 | The claim registry identifies the checkpoint, point-zero and attainment tables. All 45 tracked Python files have a unique full-file listing. The seven figures have their CSV and metadata companions. |
| Coverage and reasoning | 30 / 30 | The text distinguishes the fixed and weight-specific clean references, keeps behavior fixed along the path, describes attainment as conditional on the fitted scenarios and preserves the extrapolation caveat for both arms at 150 m. |
| Clarity and structure | 11.25 / 15 | The new paragraph fits on page 14. The following hurdle comparison starts with a single line at the foot of that page. |
| Build and references | 10 / 10 | An independent archive build reproduces the delivered PDF. All 129 team fields and the author field are blank. Body and references occupy 14 pages. |

**Initial score 96.25/100.** Prevent a page break after the first line of the hurdle comparison paragraph on page 14, for example by applying a local club penalty. No numeric correction is needed. The clean 150 m margin remains positive at weight 0.50 under both reference rules. The two draw counts fall on opposite sides of the 3,840-draw criterion, and the full-precision interval exports confirm the reported inclusive limits. [Manuscript](../paper/results.tex) · [Checkpoints](../results/q4_envelope_attainment_points.csv) · [Point zeros](../results/q4_envelope_attainment_zeros.csv) · [Attainment intervals](../results/q4_envelope_attainment_intervals.csv) · [Numerical review](q4-envelope-attainment-verification.md)

## Separate archive rebuild

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780` reproduce SHA-256 `37f80fc8dad1b408a70f35503628403247aa529f0d211c2cc2c97eb22db78ae8`. I inspected the rendered Q4 results, Figure 4, limitations and Listing 45 on pages 126–129. Body and references occupy pages 3–16, and the appendices begin on page 17. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `084a3d9f1c6270d09e22196c194c21871853de49` moves the full hurdle comparison to page 15. That revision leaves the first line of the Fisher planning paragraph at the foot of page 15. Revision `32bf8b425a8328f19052aa4d2d50bc92940ae744` keeps the full Fisher paragraph on page 16. I inspected both pages after rebuilding and confirmed that the paragraphs and Figure 4 render legibly. [Revised manuscript](../paper/results.tex) · [Final PDF](../paper/main.pdf)

The independent two-pass archive build reproduces final SHA-256 `3f776e363dc0c3f72c22b35ba8df1e1851cc838d30518c22769d0364dd5d7b57`. All 129 team fields and the PDF author field are blank. Body and references occupy 14 pages, and the 45 source listings remain in the appendices from page 17. Both layout findings are closed. Clarity and structure earns 15/15. **Final score 100/100, pass.**
