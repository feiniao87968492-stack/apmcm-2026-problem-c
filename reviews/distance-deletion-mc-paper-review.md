# Independent manuscript review of the Q4 Monte Carlo audit

I reviewed `e04177fc8b77ec561262215865c6798199898090` using the frozen manuscript rubric. A fresh Git archive rebuilt the submitted PDF byte-for-byte with SHA-256 `f9a026b48b7e76d902415c9542abc8cc0dc3370831536d948dcc1c0df63a994b`. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | All archived support shares, fresh counts, interval claims and statements about retained observations agree with the evidence. |
| Traceability | 15 / 15 | The claim registry links the Monte Carlo table. All 35 tracked Python files each have one complete listing. |
| Coverage and reasoning | 30 / 30 | The paper covers the four questions and describes the new intervals as conditional simulation precision. The union fit still extrapolates to 150 m. |
| Clarity and structure | 11.25 / 15 | The added paragraph and Figure 4 fit on page 13. A forced page break leaves a four-line continuation of the conservation paragraph alone on page 14. |
| Build and references | 10 / 10 | The archive build reproduces the PDF. All 102 team headers and the author field are blank. The body and references occupy 13 pages. |

**Initial score 96.25/100, pass.** Remove the forced break preceding Limitations so the conservation continuation can share its page with the limitations and references. [Manuscript source](../paper/main.tex)

## Evidence checks

The two bands each select 14 pairs, with two shared and 113 retained under union deletion. The maximum union training distance is 120 m. For clean two-voice own-net at 150 m, archived counts for the full, near, far and union fits are 272, 266, 259 and 239 of 300. The archived union interval contains 80%. The fresh union count 4,002 of 4,800 gives 83.38% with an exact 95% interval of 82.29–84.42%. All four fresh clean 150 m two-voice own-net and clean 100 m modulated gross intervals exceed 80%. For coupled two-voice own-net at 100 m, the full and union intervals are respectively above and below 80%, with both single-band intervals containing the cutoff. The wording preserves the distinction between resampling computation and field support. [Overlap](../results/distance_deletion_overlap.csv) · [Training support](../results/distance_deletion_training.csv) · [Monte Carlo results](../results/distance_deletion_mc.csv)

I ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780`. I checked all sequential headers and rendered the affected body and listing pages using Poppler. A set-and-count comparison of the listing paths against Git confirms complete coverage. Listing 35 starts on page 100 and ends on page 102. [Manuscript source](../paper/main.tex)

## Targeted re-review

I independently rebuilt `c48f091` from a separate Git archive with the same two-pass command. The PDF matches SHA-256 `69f156697e7ea7f1ceadb6083cd5b297f14c7db0dac8796ff367d19ea19416d5`. The rendered page 13 identifies the 300-draw support estimates as archived and keeps Figure 4 with its caption. The rendered page 14 contains the conservation continuation, Limitations and all five references. Body and references occupy pages 3–14, and appendices begin on page 15 of 101. The 35 tracked Python files each have one full listing. Listing 35 spans pages 99–101. All 101 team fields and the PDF author field are blank. Clarity and structure earns 15/15 after the revision. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
