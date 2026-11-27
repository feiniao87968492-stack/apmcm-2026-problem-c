# Independent manuscript review of Q4 consecutive-radius rematching

**Pass, 100/100.** I reviewed source commit `fed699317a169af761817fb0dd67262733d1c5ad` under the frozen paper rubric. The review covers the added consecutive-radius paragraph, its relation to the neighboring endpoint and grid analyses, and the source listing. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

The manuscript reports the sharp grid-radius bounds with the reference recomputed for each pairing and the independent pairing retained as primary. For clean full and deleted fits the ranges are 150–150 m and 149–150 m. With 20% loss in each component the ranges are 94.5–98 m and 82.5–85 m, and the original values are 96 and 84 m. For the clean deleted fit at 150 m, the original permutation retains 3,850 passing pairs through the grid prefix and the archived endpoint-minimizing permutation retains 3,810. The material radius results agree with the frozen evidence. The 150 m grid cap and the natural and control retained maxima of 100 and 120 m are explicit. [Pinned results and attaining permutations](https://github.com/feiniao87968492-stack/apmcm-2026-problem-c/blob/c4dc8fec4cb7024d1a46d0584809639fd9d137c7/docs/q4-prefix-rematching.md) · [Boundary counts](../results/q4_prefix_rematching.csv)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | All four radii, both 20% losses, the 3,840-pair rule and both 150 m prefix counts agree with the archived results. |
| Traceability | 15/15 | The PDF link resolves to the pinned results path at `c4dc8fe`. All seven figures have their CSV and metadata companions. |
| Coverage and reasoning | 30/30 | The text describes fixed empirical marginals, the pair-specific 20 m threshold, simultaneous four-curve passage through a grid prefix, the grid cap and extrapolation after deletion. |
| Clarity and structure | 15/15 | The full new paragraph is legible on p. 16 beside the preceding grid analysis. The page turns and listing 55 on pp. 150–152 are legible. |
| Build and references | 10/10 | The clean archive compiled in two passes. Body and references occupy pp. 3–19 and the appendices begin on p. 20 of 164. All 62 tracked Python modules have exactly one listing. Team and author fields are blank. |

I ran two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the `paper/` directory of a fresh Git archive with `SOURCE_DATE_EPOCH=1795731780`. The independently rebuilt PDF SHA-256 is `b54d16b74f5ab5cdeab8544a962b87b0bd91a3b1417bc50c24e5a81379326c28`. [Paper PDF](../paper/main.pdf)
