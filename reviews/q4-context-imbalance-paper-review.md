# Independent review of the Q4 bounded context imbalance manuscript update

I reviewed manuscript source `5c39d374d8a49fd5edb4175b1b5be7fa4e610a96` against the evidence at `88bd5a3a86effaf0e89fe10a98fabd98a266a774` and the frozen paper rubric. At a 50% overall noisy-opportunity share and a 30% to 70% bound within each context, the sharp pass-fraction ranges are 80.34% to 83.81% for the full fit and 70.81% to 76.78% after union deletion. Thus every feasible allocation meets 80% for the full fit and every feasible allocation falls below 80% after deletion. The revised sentence identifies the bounds as hypothetical. [Evidence](https://github.com/feiniao87968492-stack/apmcm-2026-problem-c/blob/88bd5a3a86effaf0e89fe10a98fabd98a266a774/docs/q4-context-exposure.md#bounded-context-imbalance-at-50-overall-exposure) · [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The 50% overall share, context bounds and both decisions match the archived evidence. |
| Traceability | 15/15 | The compiled link on page 17 points to the pinned evidence document. Each of the seven archived figures has CSV and metadata companions. |
| Coverage and reasoning | 30/30 | The added sentence states the allocation restriction and its decision consequence for each fit. |
| Clarity and structure | 15/15 | The rendered paragraph and its evidence link fit legibly on page 17. |
| Build and references | 10/10 | The archive built in two passes. The body and references occupy pages 3 to 20 of 176, with the appendices beginning on page 21. All 69 tracked Python modules appear once. Team numbers and the PDF author field are blank. |

**Pass, 100/100.** I ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` in a fresh Git archive with `SOURCE_DATE_EPOCH=1795731780`. The independently rebuilt PDF SHA-256 is `ec7d7a37265c424e7bd5e26a16d9917365e2e4ed9e13d8e1d397c660d0f793d4`. [Anonymous PDF](../paper/main.pdf)
