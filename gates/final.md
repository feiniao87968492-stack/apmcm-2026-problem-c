# Final evidence and reproduction

The results reproduced byte-for-byte from a clean public checkout with the original C attachments. Independent reviews cover model design, implementation readiness, numeric results, figures, and paper claims.

The propagation intervals are conditional on row resampling. The Q3 matched-covariate predictions are group-level model estimates. The two-voice clean integrated radius reaches the upper end of the 20–150 m shared domain. Environmental probabilities and radii quantify the specified scenarios.

Use the [claim registry](../claims/claim-registry.md) for sources and the [figure index](../figures/figure-index.md) for plotted data.

## Round 1 evidence and reproduction

The frozen comparisons and paper rubric are at 3a7b195, with models and derived outputs at 5e7c49d. The final manuscript source and PDF reviewed after revision are at 22529a9. See the [comparison and decision table](../docs/round1-results.md), [independent numeric review](../reviews/round1-numeric-review.md) and [independent paper review with follow-up](../reviews/round1-paper-review.md).

A clean clone of 22529a9 ran the default 300-draw analysis with Python 3.10.11 in an isolated environment created from requirements.txt. Dependency checks passed. The reproduction command was:

```sh
python main.py --data "/path/to/C-attachments/date" --output regenerated
```

The regenerated directory contained the same 46 files as results/. The 40 CSV and JSON files matched byte-for-byte. All six PNGs matched by decoded pixels. With the original production environment the entire result directory also matched byte-for-byte.

Two passes of pdflatex from paper/ in the clean checkout reproduced the released PDF's extracted text and all 28 rendered pages. Page 1 is the summary, page 2 the contents, pages 3–8 the body and references, and appendices start on page 9. The public build left the team number blank. The released PDF SHA-256 is a1ec58529561ae98f6b4ab7f9e091d650e1e88da06c4549ee7ecd659b245483b.

The recording-group comparison, the incremental playback validation and the operational scenario checks support the stated adoption decisions. Acquisition identifiers, local playback events at the far end of the range and measured ambient-noise effects remain evidence limits.

## Final follow-up evidence and reproduction

The experimental specification was frozen at 634bd20. A clean clone of 13c5be8 reproduced all 62 result files using the original attachments and the isolated Python 3.10.11 environment installed from requirements.txt. All 56 CSV/JSON files matched byte-for-byte and all six PNGs matched by decoded pixels. The default 300-draw entry point is `python main.py --data <attachment-dir>`.

The [independent numerical review](../reviews/final-followup-numeric-review.md) verifies the recording-group deletion impacts, grouped behavior scores, paired intervals and all radius and cutoff comparisons. The [independent manuscript review](../reviews/final-followup-paper-review.md) verifies the manuscript claims, figures and format against the frozen rubric.

A two-pass clean-checkout pdflatex build of the revised manuscript reproduced the published PDF's extracted text and all 37 rendered pages. The summary and contents occupy pages 1–2, the body and references occupy pages 3–9, and the appendices begin on page 10. The public team fields are blank.

## Creative modeling evidence

The [frozen specification](../docs/model-spec.md#creative-modeling-freeze) is at b47de34 and the results at 5a00f56. A clean checkout reproduced 68 CSV/JSON files byte-for-byte and six PNGs by decoded pixels. The anonymous manuscript is 45 pages including appendices, with body and references on pages 3–10. See the [numeric review](../reviews/creative-numeric-review.md) and [paper review](../reviews/creative-paper-review.md).

## Post hoc verification

The post hoc checks froze at 43c39e6 and ran at 1ac4bbd. A clean checkout of the revised manuscript and source at c873d45 reproduced 74 CSV/JSON files byte-for-byte and six PNGs by decoded pixels. Two pdflatex passes reproduced the released extracted text and all 47 rendered pages. The team field is blank and the body and references occupy pages 3–10. [Results](../docs/posthoc-results.md) · [Independent numerical verification](../reviews/posthoc-numeric-review.md)

## Q4 decision verification

The decision analyses were frozen at d18ff9a and computed at c1e1ee8. Independent calculations reproduced the decision counts, crossed variance shares and exact integer optimum. A clean checkout of 2e8fe9b reproduced 77 CSV/JSON files byte-for-byte, six PNGs by decoded pixels, and the English PDF's text and all 50 rendered pages. The public team fields are blank. Body and references occupy pages 3–11. [Decision results](../docs/q4-decision-results.md) · [Independent recomputation](../reviews/q4-decision-verification.md)

## Playback dependence verification

The analysis was frozen at fa1b026 and computed at 4c1b3a3. Independent refits verified both holdout schemes, 36 margin rows and the trial precision results. A clean checkout of 1b20cd6 reproduced 82 CSV/JSON files byte-for-byte, six PNGs by decoded pixels and all 51 rendered PDF pages. The public team fields are blank. Body and references occupy pages 3–10, one page shorter than the previous release. [Results](../docs/playback-dependence.md) · [Independent recomputation](../reviews/playback-dependence-verification.md)

## Matched distance and weighted behavior verification

The analyses were frozen at c4bf42f and computed at f6e5984. Independent calculations reproduced the stratified intervals, loss limits and weighted comparisons. A clean checkout of 28437c5 reproduced 86 CSV/JSON files byte-for-byte, six PNGs by decoded pixels and all 53 rendered PDF pages. The public team fields are blank. Body and references occupy pages 3–10. [Results](../docs/matched-sensitivity.md) · [Independent recomputation](../reviews/matched-sensitivity-verification.md)

## Physical attenuation verification

Protocol 92e3265 and outputs 1284ba2 passed independent recomputation of the distance holdout, block intervals and fixed-reference Q4 decisions. A clean checkout of a58d784 reproduced 92 CSV/JSON files byte-for-byte, six PNGs by decoded pixels and all 56 rendered manuscript pages. The team fields are blank, and body and references occupy pages 3–10. [Results](../docs/physical-attenuation.md) · [Independent recomputation](../reviews/physical-attenuation-verification.md)

## Acoustic transformation and onset verification

The analysis froze at 195a5af and ran at 4130bdd. Independent calculations verified the grouped acoustic predictions and paired intervals, latency MAEs, timing scores and all 54 cumulative probability rows. A clean checkout of 2f6b2ae reproduced 97 CSV/JSON files byte-for-byte, six PNGs by decoded pixels and all 59 PDF pages by extracted text and raster comparison. Body and references occupy pages 3–10 and the public team fields are blank. [Results](../docs/acoustic-onset.md) · [Independent recomputation](../reviews/acoustic-onset-verification.md)

## Noise power scenario verification

The scenarios were frozen at 5a0c8c0 and computed at c5fd3fd. Independent calculations verified the matched losses, radius intervals, attainment and responder count bounds. A clean checkout of 9d01ca5 reproduced 101 CSV/JSON files byte-for-byte, six PNGs by decoded pixels and all 61 PDF pages by extracted text and raster comparison. Body and references occupy pages 3–10 and the public team fields are blank. [Results](../docs/noise-scenarios.md) · [Independent recomputation](../reviews/noise-scenarios-verification.md)

## Final delivery verification

The figure and scenario-agreement protocol froze at 12cf2f9. A clean checkout of 012ee10 reproduced all 112 outputs with 105 CSV/JSON files identical byte-for-byte and seven PNGs identical by decoded pixels. The pagination-only revision 4ce9bf3 rebuilt in a clean checkout with identical extracted text and all 62 rendered pages. Both references appear on page 10, the appendices begin on page 11, and the public team fields and author metadata are blank. The independent review scored the revised manuscript 100/100 under the frozen rubric. [Results](../docs/final-delivery.md) · [Independent review](../reviews/delivery-paper-review.md)

## Strict playback verification

The protocol was frozen at 9e95367 and run at 5c951ca. Independent recomputation checked holdout coverage, predictive scores and all crossed margins. A clean checkout of b758f4d reproduced 112 CSV/JSON files byte-for-byte, seven PNGs by decoded pixels, and the manuscript's extracted text and all 66 rendered pages. The team fields are blank and the body and references occupy pages 3–11. [Results](../docs/strict-playback.md) · [Verification](../reviews/strict-playback-verification.md)

## False Bay sea-state verification

The protocol and snapshots froze at e86dfe1 and the analysis ran at 7bffe2b. Independent recomputation verified the hourly joins, slopes, strict fold scores and standardized contrasts. A clean checkout of d5c153f reproduced 118 CSV/JSON files byte-for-byte, seven PNGs by decoded pixels and the manuscript's extracted text and all 68 rendered pages. The public team fields are blank, and body and references occupy pages 3–11. [Results](../docs/false-bay.md) · [Verification](../reviews/false-bay-verification.md)

## WAVERYS and example-deletion verification

The protocol froze at ea42111 and the computations ran at a81e3ec. Independent recomputation verified WAVERYS interpolation, date slopes, strict validation, 336 radius rows and 504 Q4 rows. A clean checkout of 53f6f7c reproduced 125 CSV/JSON files byte-for-byte, seven PNGs by decoded pixels and all 70 PDF pages by text and raster comparison. Body and references occupy pages 3–11 and the public team fields are blank. [Results](../docs/example-sensitivity.md) · [Verification](../reviews/example-sensitivity-verification.md)

## Missing propagation comparison verification

The completion protocol was frozen at `87748d6`. In a detached checkout of `7150087`, `python main.py --data "<attachment directory>/date"` with the pinned requirements and default 300 draws reproduced 122 CSVs and seven JSON files byte-for-byte. All seven PNGs matched by decoded pixels. The independent numerical review checked every row of the four new tables, including exact Q4 attainment counts and decisions. [Results](../docs/missing-propagation.md) · [Numerical review](../reviews/missing-propagation-verification.md)

A detached checkout of `99dad78` built the anonymous manuscript with two runs of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/` and `SOURCE_DATE_EPOCH=1795731780`. The rebuilt and delivered PDF have SHA-256 `0abe1b4f4307790c26454a4b362f3884d108e31c45826862a657542752aba020`. Body and references occupy pages 3–12. Appendices begin on page 13 of 73, with the public team field and author metadata blank. [Manuscript review](../reviews/missing-propagation-paper-review.md) · [PDF](../paper/main.pdf)

## Group-size comparison verification

The protocol froze at `45165bd` and ran at `c21e0fe`. A detached checkout of that analysis commit reproduced 127 CSVs and seven JSON files byte-for-byte with `python main.py --data "<attachment directory>/date"` and the default 300 draws. All seven PNGs matched by decoded pixels. An independent implementation reproduced the paired contrasts, strict date and track folds, Q4 attainment and coverage. [Results](../docs/group-size.md) · [Numerical review](../reviews/group-size-verification.md)

A detached checkout of `21743a0` reproduced the anonymous PDF byte-for-byte with two runs of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/` and `SOURCE_DATE_EPOCH=1795731780`. SHA-256 is `ef22ff94b81c5ae06330160f6053e2ff1ecb4eefad57a44caf46113d0aaaf0e3`. The body and references occupy pages 3–12 and the appendices begin on page 13 of 73. [Manuscript review](../reviews/group-size-paper-review.md) · [PDF](../paper/main.pdf)

## Vocal-count comparison verification

The protocol froze at `4652deb` and ran at `6212e85`. A detached checkout of the analysis commit reproduced 133 CSVs and seven JSON files byte-for-byte with `python main.py --data "<attachment directory>/date"` and the default 300 draws. All seven PNGs matched by decoded pixels. Independent raw-data recomputation verified paired changes, strict scores, local coverage and the 18 Q4 decisions. [Results](../docs/vocal-counts.md) · [Numerical review](../reviews/vocal-counts-verification.md)

A detached checkout of `e898182` reproduced the anonymous PDF byte-for-byte with two runs of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/` and `SOURCE_DATE_EPOCH=1795731780`. SHA-256 is `db70b1404c9266ba9b05c1ab53f280f03e6c8405dd8b02c7bd371e733080d37b`. The body and references occupy pages 3–12 and appendices begin on page 13 of 73. [Manuscript review](../reviews/vocal-counts-paper-review.md) · [PDF](../paper/main.pdf)

## First-reply and event-order verification

The protocol froze at `19ae12e` and ran at `2221807`. A detached checkout reproduced 138 CSVs and seven JSON files byte-for-byte with `python main.py --data "<attachment directory>/date"` and the default 300 draws. All seven PNGs matched by decoded pixels. Independent raw-data recomputation checked all five new tables and confirmed the permutation result by exact enumeration. [Results](../docs/first-reply.md) · [Numerical review](../reviews/first-reply-verification.md)

A detached checkout of `5a9e68d` reproduced the anonymous PDF byte-for-byte with two runs of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/` and `SOURCE_DATE_EPOCH=1795731780`. SHA-256 is `aee75434e3e0dafd6a695479261b9a1fa2b38692af8e6958e83227ae7171f297`. The body and references occupy pages 3–12 and appendices begin on page 13 of 73. [Manuscript review](../reviews/first-reply-paper-review.md) · [PDF](../paper/main.pdf)

The played-call detail froze at `8de62a4` and ran at `abce327`. Independent recomputation matched all 27 cells and reconciled both denominators and reply counts with the natural arm. A detached checkout of `63978fd` reproduced 139 CSVs and seven JSON files byte-for-byte and seven PNGs by decoded pixels using the same command. A detached checkout of final manuscript `0b44adf` reproduced PDF SHA-256 `574a76c503b2398b1524a42d45e27161a758c34df103209eb1cc6c76d85df04d`. The body and references occupy pages 3–13 and appendices begin on page 14 of 74. [Detailed matrix](../results/first_reply_by_played_call.csv) · [Numerical review](../reviews/first-reply-verification.md) · [Manuscript review](../reviews/first-reply-paper-review.md)

## Supported annulus verification

The protocol froze at `a844b4d` and ran at `05bd6e8`. A detached checkout reproduced 146 CSVs and seven JSON files byte-for-byte using the default analysis command and 300 draws. All seven PNGs matched by decoded pixels. Independent recomputation checked all seven new tables, including 7,047 grid counts and 28 connected intervals. [Results](../docs/spatial-annulus.md) · [Numerical review](../reviews/spatial-annulus-verification.md)

A detached checkout of `1018047` reproduced the anonymous PDF byte-for-byte with two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` and `SOURCE_DATE_EPOCH=1795731780`. SHA-256 is `125f0236c896377d214a616beeb849d84ff9a85b075b337cbf3e2044561eed2b`. Body and references occupy pages 3–13 and appendices begin on page 14 of 74. [Manuscript review](../reviews/spatial-annulus-paper-review.md) · [PDF](../paper/main.pdf)

## Context and behavior priority verification

The protocol froze at `a2e82e9` and ran at `094fad4`. A detached checkout reproduced 150 CSVs and seven JSON files byte-for-byte with `python main.py --data "<attachment directory>/date"` and the default 300 draws. Seven PNGs matched by decoded pixels. Independent recomputation verified all four new tables and reproduced the archived clean empirical annulus point scores and intervals within 2.22e-16. [Results](../docs/context-priority.md) · [Numerical review](../reviews/context-priority-verification.md)

A detached checkout of `986443c` reproduced the anonymous PDF byte-for-byte with two runs of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/` and `SOURCE_DATE_EPOCH=1795731780`. SHA-256 is `53f6c961c1e19e136e9656d22a524d43b86122dc502db2a6ae29c5d168439536`. Body and references occupy pages 3–13 and appendices begin on page 14 of 74. [Manuscript review](../reviews/context-priority-paper-review.md) · [PDF](../paper/main.pdf)

## Historical correlation recovery verification

The protocol froze at `b0ae1b4` and ran at `6efac25`. A detached checkout reproduced 155 CSVs and seven JSON files byte-for-byte with `python main.py --data "<attachment directory>/date"` and the default 300 draws. All seven PNGs matched by decoded pixels. Independent recomputation verified the no-recovery endpoints, missing counts, all 351 cases and selected-plan intervals and directions. [Results](../docs/recovery-priority.md) · [Numerical review](../reviews/recovery-verification.md)

A detached checkout of `28f2f75` reproduced the anonymous PDF byte-for-byte with two runs of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/` and `SOURCE_DATE_EPOCH=1795731780`. SHA-256 is `00da7f8ece08ba9f949cac0915a90a844849be5e3493e76b633ec93c17c50a9d`. Body and references occupy pages 3–13 and appendices begin on page 14 of 74. [Manuscript review](../reviews/recovery-paper-review.md) · [PDF](../paper/main.pdf)

## Continuous recovery verification

The protocol froze at `cff2038` and ran at `49c0545`. A detached checkout reproduced 157 CSVs and seven JSON files byte-for-byte with the default analysis command. All seven PNGs matched by decoded pixels. Independent recomputation checked all four summary rows and 106 breakpoint rows. [Results](../docs/recovery-priority.md#continuous-recovery-certificate) · [Numerical review](../reviews/continuous-recovery-verification.md)

The anonymous manuscript at `ae23f49` was independently rebuilt and reviewed. SHA-256 is `b3ffff73973885fe346b56add74d74968fb8bd0757ed764fc6acdc99fb42910d`. [Manuscript review](../reviews/continuous-recovery-paper-review.md) · [PDF](../paper/main.pdf)
