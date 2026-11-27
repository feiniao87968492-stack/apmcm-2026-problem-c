# Independent manuscript review of Q4 draw rematching

**Pass, 100/100.** I reviewed source commit e51a0a1c60352d6ad448099ed71474cd083d4194 under the frozen paper rubric. The review covers the new endpoint paragraph, its relationship to the consecutive-distance result, and the source listing. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

For the clean 150 m endpoint under union deletion, the original count is 3,858/4,800 (80.38%), and the equally weighted cross-product gives 18,524,228/23,040,000 (80.40%). One-to-one assignments attain 3,818/4,800 and 3,898/4,800 (79.54% and 81.21%). This is the sole setting whose bounds span the decision threshold of 3,840/4,800. The manuscript places the result beside the existing 150 m endpoint and keeps it distinct from the next paragraph's consecutive-grid criterion. The natural and control arms extrapolate beyond their respective retained maxima of 100 m and 120 m. [Summary at 273de5c](https://github.com/feiniao87968492-stack/apmcm-2026-problem-c/blob/273de5cbe1bfe3056ee5292aab103a17d99ce441/docs/q4-draw-rematching.md) · [Independent numeric verification](q4-draw-rematching-verification.md)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The reported shares, unique possible decision flip, four-shape criterion and retained ranges agree with the verified results. |
| Traceability | 15/15 | The PDF annotation points to the results and attaining permutations pinned at 273de5c. All seven figures have CSV and metadata companions. |
| Coverage and reasoning | 30/30 | The explanation holds both sets of draws fixed, recomputes the 20 m reference for each combination and retains independent pairing as primary. It states which predictions extrapolate. |
| Clarity and structure | 15/15 | The rematching paragraph flows across pages 15–16 alongside the published endpoint and prefix results. Listing 54 is legible across pages 148–150. |
| Build and references | 10/10 | The Git archive builds cleanly. Body and references occupy pages 3–19. The appendices start on page 20 of 162, with one listing for each of the 61 tracked Python modules. The team and author fields are blank. |

I ran two passes of pdflatex -interaction=nonstopmode -halt-on-error main.tex from the paper directory of a fresh Git archive with SOURCE_DATE_EPOCH=1795731780. The independently rebuilt PDF SHA-256 is 30847d7e7eb227a02ed95734553e33a5dde23790a729be57586610d22b55a221. [Paper PDF](../paper/main.pdf)
