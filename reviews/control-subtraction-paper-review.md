# Independent review of Q4 control subtraction

I reviewed manuscript commit `2a6e078494fb3b45a8cf6d0e6f66f2cc54e7492a` under the frozen rubric. A two-pass build from a separate Git archive matched the committed PDF SHA-256 `aada5f77e72470d9a407b9840c31df970f93096f56e26a2c1bd75299379fbb18`. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Dimension | Initial score | Evidence |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The six clean area means, rankings, cutoff values and coupled decision counts agree with the result tables. |
| Traceability | 15 / 15 | The claim registry links the area, radii, point and decision outputs. Figure 4 retains its archived companion data. |
| Coverage and reasoning | 30 / 30 | The paper distinguishes score subtraction at the shared cutoff from the signed score at its recalibrated clean reference. It describes the indices as scenario contrasts. |
| Clarity and structure | 11.25 / 15 | The new paragraph fits on page 13. The nearby Figure 4 caption needs to identify the curves as gross scores. |
| Build and references | 10 / 10 | The archive builds byte-for-byte. Body and references occupy pages 3–14, appendices begin on page 15 and all 75 team fields and author metadata are blank. |

**Initial score 96.25/100.** In Figure 4's caption, identify the gross score and the original common cutoff to distinguish the plotted curves from the net scores discussed in the preceding paragraph. [Manuscript source](../paper/results.tex)

## Evidence checks

For flat, modulated and two-voice calls, the clean gross means are 0.259, 0.381 and 0.435 and the clean net means are 0.210, 0.328 and 0.370 after rounding. Both definitions preserve the same point order across the three loss settings. If `pN-pC>0`, a 20% acoustic-only loss multiplies the clean net score by 0.80. Coupled response changes the excess by the same factor, giving 0.64 overall. This identity uses a fixed control probability. [Area results](../results/control_subtraction_area.csv) · [Frozen definition](../docs/model-spec.md#q4-control-subtraction-freeze)

The common gross reference is 0.287598 and the own net reference is 0.194371. Under coupling, two gross settings, zero net settings with the gross reference and three net settings with their own reference pass the 80% rule. The supplemental results give uncensored crossings and support boundary cases. For example, the net two-voice coupled point score never reaches the common gross reference on the grid, and the same curve reaches the 150 m boundary at its own reference. [Fixed-distance results](../results/control_subtraction_points.csv) · [Bounded radii](../results/control_subtraction_radii.csv)

I built from the archive in two passes with `pdflatex -interaction=nonstopmode -halt-on-error main.tex` and `SOURCE_DATE_EPOCH=1795731780`, rendered pages 12–14 with Poppler and checked all sequential page headers in the extracted text. The new paragraph, figure, caption and references are legible and within the page margins. [Reviewed PDF](../paper/main.pdf)

## Targeted re-review

I independently rebuilt `8f0d9132da0e44e9bd7ff9ea67be52260ce48d47` from a separate Git archive using the same commands. The rebuilt PDF matches SHA-256 `8342503fc4dbdceb445804981c78728527012e2a884d4f91389262c4c93f987a`. On page 13, the revised caption identifies Figure 4 as gross scores with the original common cutoff and fits with the figure. All 75 team fields and author metadata are blank. Body and references occupy pages 3–14, and Appendix A begins on page 15. Clarity and structure is restored to 15/15. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
