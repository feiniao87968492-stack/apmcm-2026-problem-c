# Independent manuscript review of Q2 attenuation shape and ranks

I reviewed `93427e2a383e15678170d92d1ebcae3e4e01ca7f` against the frozen rubric. I checked the new model preference, weight-dependent radii and ranks, the summary, the Q4 method wording and the additional source listing. Earlier reviews cover the other analyses. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen specification](../docs/model-spec.md#q2-attenuation-shape-by-common-representation-weight) · [Numerical review](q2-shape-rank-verification.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | Equal-weight RMSE, the figure in the summary, 0.70 signed gaps and conditional rank frequencies reconcile with the exports. |
| Traceability | 15 / 15 | The claim registry maps the seven Q2 shape tables. The appendix lists all 47 tracked Python files once each. All seven exported figures have CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | The preference rule is supported, but the point rank discussion needs the 0.70 threshold stated again. The Q4 methods and summary should name the published attenuation shapes to make the scope of the scenario claims explicit. |
| Clarity and structure | 15 / 15 | The Q2 text and Figure 2 fit across pages 6–7, and Listing 47 is legible. |
| Build and references | 10 / 10 | A separate archive rebuild matches the PDF, body and references occupy 15 pages, and all 135 team headers and the PDF author are blank. |

**Initial score 92.5/100.** At envelope weight 0.50 all four shapes favor modulated at fidelity 0.70 and favor two-voice at fidelity 0.50. Attach the reported weight ordering and the envelope-only bound to the 0.70 threshold. Describe the bound as below the 4 m support limit. Name the isotonic and shared-exponent shapes in the summary's noise-agreement statement, and name the published shared-exponent curve in the Q4 methods. The separate exponents meet the preference rule in the new equal-weight Q2 comparison. The noise-agreement result was calculated with the two published shapes. [Manuscript](../paper/results.tex) · [Decision](../results/q2_shape_rank_decision.csv) · [Radii](../results/q2_shape_rank_radii.csv) · [Gaps](../results/q2_shape_rank_gaps.csv)

## Independent archive rebuild

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780` produce SHA-256 `848e4230be291c63b870a82b8f8321487fdf27ea5050e14a723420c3b350717f`. I rendered and inspected the affected Q2 pages and Listing 47, which starts on page 133 and ends on page 135. Body and references occupy pages 3–17. The appendices start on page 18. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `6ce2726eb58bdacef546c0630200166c409fb77d` names the published isotonic and shared-exponent scenarios in the summary, names the shared-exponent curve in the Q4 methods, and states fidelity 0.70 again before the point rank results. The below-support language agrees with the envelope-only status. The published Figure 2 caption identifies the shared-exponent line. The rendered summary and Q2 pages show the complete revised text and figure. [Revised manuscript](../paper/results.tex) · [Q4 methods](../paper/main.tex)

The independent two-pass archive build reproduces final SHA-256 `67bfe8096b7708769636f7e7200da2450e4d3b2ef1221f5ac2e8bd8b0865e3cf`. The 135 team fields and the PDF author are blank. Body and references occupy 15 pages, with 47 source listings in the appendices from page 18. Coverage and reasoning earns 30/30. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
