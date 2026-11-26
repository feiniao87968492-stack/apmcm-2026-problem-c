# Independent manuscript review of Q2 envelope-weight ranks

I reviewed `70156fc64449e8761b06bef6e39ab7b7f5d6dfdf` against the frozen paper rubric. The previous review covers earlier analyses. I checked the weight-path paragraphs, their transition from the adopted shared-exponent model, Figure 2 and Listing 43. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen Q2 sensitivity](../docs/model-spec.md#q2-rank-changes-along-a-common-envelope-weight-path) · [Previous review](q1-candidate-sets-paper-review.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The reversal weights, reported support tie, 28 draws already reversed, and range for the other 272 draws match the evidence tables. |
| Traceability | 15 / 15 | The claim registry links the four Q2 exports. All 43 tracked Python files have a unique full-file listing, and all seven figures have their CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | Explicitly name the available-value isotonic fit for the weight path and state why the flat–two-voice reversal is a jump. |
| Clarity and structure | 15 / 15 | Both new paragraphs and Figure 2 are legible on page 6. Listing 43 spans pages 121–124. |
| Build and references | 10 / 10 | The separate archive rebuild matches the delivered PDF. Body and references occupy 14 pages. Every team field and the author are blank. |

**Initial score 92.5/100.** The preceding text discusses the adopted shared-exponent fit, so name the available-value isotonic fit when introducing the new path. At the flat–two-voice switches for thresholds 0.60 and 0.70, the two-voice 32–64 m plateau exactly meets the threshold. The last-qualifying convention gives 64 m at the event, where two-voice still leads. The flat lead starts immediately above each event. The 0.70 tie from about 0.8121 onward is a tie of reported 4 m support-limited radii. The draw range is conditional on reversal above equal weights in the independent-metric wide-row scheme. [Manuscript](../paper/results.tex) · [Events](../results/q2_envelope_rank_events.csv) · [Draw summary](../results/q2_envelope_rank_bootstrap.csv)

## Independent archive rebuild

I extracted a separate Git archive and ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` with `SOURCE_DATE_EPOCH=1795731780`. The archived and rebuilt PDFs both have SHA-256 `785ff1255c2fd5e852cd7705caffe34a29fbc4c408b38384a6cb9a4774739919`. Body and references occupy pages 3–16, and the appendices begin on page 17. All 124 team fields and the PDF author are blank. I rendered the affected Q2 pages, Figure 2 and the new listing. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `f30e7e84b7c1d8a572a8e59cb414f6533f3ed34e` identifies the available-value isotonic path, explains the 64 m plateau endpoint at the flat–two-voice switches and states that zero draws are right-censored. Revision `6d3453b7ed888eaa7f16631d10b7355fc3fb4e69` corrects the punctuation at the plateau explanation. The revised text and Figure 2 fit on rendered page 6, followed by the playback section. Both substantive findings are closed. [Revised manuscript](../paper/results.tex)

The final two-pass archive build reproduces SHA-256 `ad21a8fa253ea275213d05e7c58be510c0f58079e3f68042ddecfcb9579ddd34`. Body and references still occupy 14 pages. The 124 team fields and the PDF author field are blank, and the appendix covers 43 source files. Coverage and reasoning earns 30/30. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
