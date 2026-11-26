# Independent manuscript review of the actual-distance tail audit

I reviewed `11d8a59740c9456046edbea450a187ae916df41c` against the frozen paper rubric and carried forward the prior assessment of the earlier sections. I checked the actual-distance paragraph, the scope of the adjacent 150 m claim, the evidence map and the new source listing. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen audit](../docs/model-spec.md#actual-playback-distance-audit-of-tail-validation) · [Previous manuscript review](q4-tail-ablation-paper-review.md)

| Dimension | Score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The 33 long-playback trials and 19 shorter partners, plateau-minus-multinomial score changes and long-trial intervals match the exports. The two natural and one control trial in the stated two-voice window all occur at 150 m. |
| Traceability | 15 / 15 | The claim registry identifies both audit tables and the appendix gives a complete, unique listing for each of the 41 tracked Python files. All seven exported figures have CSV and metadata companions. |
| Coverage and reasoning | 30 / 30 | The audit distinguishes long trials from their shorter partners and presents both improvements as point differences with intervals that span zero. The neighboring text retains the adoption decision and limits the standardized 150 m result to extrapolation for both arms after union deletion. The conservation guidance calls for field measurement and randomized evaluation. |
| Clarity and structure | 15 / 15 | The new paragraph and adjacent interpretation fit together on page 14. The revised body, Figure 4, appendix transition and new source listing render legibly. |
| Build and references | 10 / 10 | The independent archive rebuild reproduces the delivered PDF, with 13 pages of body and references and blank team and author fields. |

**Final score 100/100, pass.** The published rounded long-trial differences are −0.034 for Brier and −0.062 for mask log loss. The shorter partners give +0.015 and +0.236. Both long-trial 95% date intervals include zero. The pooled actual-long result therefore supplies a sensitivity finding for the held-out trials across call types and observed conditions. Only three held-out two-voice trials appear at 150 m, which supports the manuscript's qualification of the standardized prediction and the call for additional playbacks. [Manuscript](../paper/results.tex) · [Scores](../results/q4_tail_distance_scores.csv) · [Coverage](../results/q4_tail_distance_coverage.csv) · [Numerical review](q4-tail-distance-verification.md)

## Independent archive rebuild

I extracted a separate Git archive and ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` with `SOURCE_DATE_EPOCH=1795731780`. The archived and rebuilt PDF both have SHA-256 `8388bf645a54b40d247b3dc90828940bda9cc9f90967b2b338ace966cafb7e3f`. All 117 page headers have an empty team field and the PDF author is blank. Body and references occupy pages 3–15, and the appendices start on page 16. I visually inspected pages 13–16 and 116–117, including all of Listing 41. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)
