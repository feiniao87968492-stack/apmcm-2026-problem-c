# Independent manuscript review of Q3 playback-order sensitivity

**Pass, 100/100.** I reviewed manuscript source `5b64f55b241f3213f0b1345a9fa258ff5813ef47` and its compiled PDF under the existing frozen rubric. This review covers the first-playback and carryover additions and their effect on the manuscript structure. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Previous Q3 methods review](playback-design-paper-review.md)

The p. 11 first-playback paragraph matches the independent allocation results for 49 distance- and group-size-matched pairs. The nearest-half interval is 9.33 to 92.00 percentage points. The 45–55% and 40–60% lower endpoints are 7.36 and −0.69 points, respectively. Its description conditions the measured first-response contrast on possible order assignments. [Results and witnesses](../results/q3_first_playback_summary.csv) · [Numerical review](q3-first-playback-verification.md)

The carryover paragraph correctly uses both responses per pair at their recorded distances. Keeping the assigned first response fixed and changing only selected second responses, the matched zero-budget difference is 25/49. All six scenarios require at least 25 corrected pairs to reach a nonpositive difference. Both one-direction nearest-half cases reach zero in that sample. For the 139-pair sensitivity, the two one-direction nearest-half cases retain a full-budget lower bound of 2/139, or 1.44 points. Two-sided carryover can erase the observed difference with 72 changes under either order restriction. The paragraph keeps the actual order and carryover unknown. [Numerical summary](../results/q3_carryover_summary.csv) · [Budget bounds and witnesses](../results/q3_carryover_bounds.csv)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The stated sample sizes, intervals, observed difference and minimum budgets agree with the exports and review evidence. |
| Traceability | 15/15 | PDF annotations on p. 11 point to the first-playback and carryover result notes at source commits `80b1e70` and `055e839`. Each of the seven figures has CSV and metadata companions. |
| Coverage and reasoning | 30/30 | The added text distinguishes the observed first-playback contrast from the two-response correction scenario, and bounds each by its stated assumptions. |
| Clarity and structure | 15/15 | The Q3 additions fit at the top of p. 11, following the recorded-response analysis on p. 10. The revised transition to Q4, references and new listings are legible in the rendered PDF. |
| Build and references | 10/10 | Both passes compiled from the Git archive. Body and references occupy pp. 3–19. The appendices start on p. 20 of 160, and all 60 tracked Python modules have exactly one listing each. All team fields and the PDF author field are blank. |

I ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from the `paper/` directory of a fresh Git archive of the reviewed commit with `SOURCE_DATE_EPOCH=1795731780`. The rebuilt PDF SHA-256 is `f7ce6e58d64672ad063703a9e68ad6ad8d8ffafb6dd59c8d451d1af95c13925d`. [Paper PDF](../paper/main.pdf)
