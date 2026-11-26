# Independent manuscript review of Q4 attenuation-shape propagation

I reviewed `3651542e03f0909c1103052e4004b2a469a659f5` against the frozen paper rubric. This review covers the summary, the new Q4 analysis, the neighboring interpretation and the additional source listing. Earlier reviews cover the other analyses. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen specification](../docs/model-spec.md#q4-attenuation-shape-propagation-freeze) · [Numerical review](q4-shape-propagation-verification.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The reported point margins, paired change and interval, counts, percentages and threshold decisions match the production and independent calculations. |
| Traceability | 15 / 15 | The claim registry links the shape comparison table. Each of the 48 tracked Python files has a unique full-file listing. All seven exported figures have CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | The body identifies union deletion and the paired sensitivity design. Name union deletion and the 20% coupled-loss condition in the summary to identify the exact comparison. |
| Clarity and structure | 11.25 / 15 | The new paragraph and Figure 4 render legibly. The previous paragraph's last line is stranded at the top of page 15. |
| Build and references | 10 / 10 | The independent PDF rebuild matches the archive. Body and references occupy 15 pages. Team fields and the PDF author field are blank. |

**Initial score 88.75/100.** The clean two-voice comparison at 150 m meets the draw rule under all four equal-weight score shapes for both behavior fits. Union-deleted playbacks remain extrapolated there. The separate-exponent change at 100 m applies to the coupled own-net margin under union deletion. Use the full scenario name in the summary. Condense the preceding stimulus-only comparison or adjust its pagination so the sentence opens and closes together. [Manuscript](../paper/results.tex) · [Evidence table](../results/q4_shape_propagation.csv)

## Separate archive rebuild

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780` reproduce SHA-256 `bd1e21b5c512a8ecd2783433007f262db95b883f6e8be315038c248f5ef3dbaf`. I inspected the rendered summary, Q4 results and Figure 4, then confirmed Listing 48 starts on page 135 and ends on page 137. Body and references occupy pages 3–17. The appendices start on page 18. All 137 team fields and the PDF author field are blank. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `9300739e7d64adddd6702bbb749dd2c2520f9c38` names union deletion and 20% coupled loss in the summary. Revision `64f59c813109f4bda8fc25d1e11bbc39b5f09262` keeps the stimulus-only model statement with the preceding paragraph. The rendered summary and pages 14–15 show the complete scenario description and a clean paragraph break. The shape results still use a common full-data reference for all four shapes and both behavior fits. [Revised manuscript](../paper/results.tex)

The independent two-pass archive build reproduces final SHA-256 `658ace1af86b54523eee8998f1d88cb5482d23b788ae735bfe476337c07baa15`. All 137 team fields and the PDF author field are blank. Body and references occupy 15 pages, with 48 source listings in appendices starting at page 18. Coverage and reasoning earns 30/30 and clarity and structure earns 15/15. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
