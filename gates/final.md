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

## Q3 response-gap verification

The protocol froze at `9795561` and ran at `49929bc`. A detached checkout reproduced 159 CSVs and seven JSON files byte-for-byte with the default 300-draw analysis. Seven PNGs matched by decoded pixels. Independent raw-data recomputation checked the archived marginals, all 20 raw rows and all 90 standardized rows. Every date draw was valid for decomposition. [Results](../docs/behavior-gap.md) · [Numerical review](../reviews/behavior-gap-verification.md)

The anonymous manuscript at `1c0b92e` has PDF SHA-256 `7bc15d45c2785eba781128a5b204ab0e0e87bd599a531a2c8a1415dc6cd2b3ac`. Body and references occupy pages 3–14 and appendices begin on page 15 of 75. [Manuscript review](../reviews/behavior-gap-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 control subtraction verification

The protocol froze at `f2d71da` and ran at `7b713f6`. A detached checkout reproduced 164 CSVs and seven JSON files byte-for-byte with the default 300-draw analysis. All seven PNGs matched by decoded pixels. Independent recomputation verified the archived gross baseline and all 225 rows in the five new tables. [Results](../docs/control-subtraction.md) · [Numerical review](../reviews/control-subtraction-verification.md)

The anonymous manuscript at `8f0d913` has SHA-256 `8342503fc4dbdceb445804981c78728527012e2a884d4f91389262c4c93f987a`. Body and references occupy pages 3–14 and appendices begin on page 15 of 75. [Manuscript review](../reviews/control-subtraction-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 behavior model ablation verification

The protocol froze at `aa170ea` and ran at `4adb6e7`. A detached checkout reproduced 168 CSVs and seven JSON files byte-for-byte with the default 300-draw analysis. All seven PNGs matched by decoded pixels. Independent recomputation verified the archived full-model baseline, the gross-minus-net identities and all 252 rows in the four new tables. [Results](../docs/behavior-ablation.md) · [Numerical review](../reviews/behavior-ablation-verification.md)

The anonymous manuscript at `5d58a82` has SHA-256 `4a46e23b571f145376b431481ba79f7f3a447cfd4b5b2e6ed5454a5d41065839`. Body and references occupy pages 3–14 and appendices begin on page 15 of 75. [Manuscript review](../reviews/behavior-ablation-paper-review.md) · [PDF](../paper/main.pdf)

## Contest source appendix verification

The official 2026 essay specifications require software names and all authored source code in the appendix. They limit the body to 25 pages and allow an appendix of any length. The appendix in `8c979da` covers all 33 tracked Python files exactly once, up from 23 in `a8268bd`. Appendix D.1 lists Python, the seven pinned analysis packages, the LaTeX build tool and Poppler.

The body and references occupy pages 3–14 (12 pages). The appendices start on page 15 and Appendix D starts on page 16. The software list is on page 16 and the ten added listings span pages 75–97. The summary, body and earlier appendix text match the prior PDF after normalizing the page headers. The contents page reflects the new appendix subsections. Modeling sources and outputs match `a8268bd`. The PDF has 97 pages and all team fields and the author field are blank.

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from `paper/`, with `SOURCE_DATE_EPOCH=1795731780`, produce SHA-256 `fd6e50a634c2159bcdf6b349a97f1d9aa989f09a547524066534273629b403c1`. [Independent review](../reviews/source-appendix-review.md) · [PDF](../paper/main.pdf)

## Q4 distance deletion verification

The protocol froze at `ddb3e30` and ran at `61b8151`. Running `python main.py --data "<attachment directory>/date"` with the default 300 draws in a detached checkout reproduced 172 CSVs and seven JSON files byte-for-byte. All seven PNGs matched by decoded pixels. Independent recomputation verified intact-pair selection, the 36 archived baseline rows and every field of the four new tables. All date draws were valid. [Results](../docs/distance-deletion.md) · [Numerical review](../reviews/distance-deletion-verification.md)

The anonymous manuscript at `ec785cf` has PDF SHA-256 `71484041597849721f34b67d5a45af3e29c93ee046bcfa4e6236ced917031e09`. Body and references occupy pages 3–14. Appendices begin on page 15 of 99 and list all 34 tracked Python modules. [Manuscript review](../reviews/distance-deletion-paper-review.md) · [PDF](../paper/main.pdf)

## Monte Carlo precision verification

The audit froze at `0e2899e` and ran at `8429d3e`. A detached checkout regenerated the audit CSV byte-for-byte with `python distance_deletion_mc.py --data "<attachment directory>/date"`. Its SHA-256 is `5f376ee433d5d9375870944713ad0d56075367024a99d2fb42bfd513ac3511aa`. The independent recomputation matched the counts, valid draws and both decision flags across all 48 rows. The maximum difference in exact interval endpoints was 2.22e-16. [Results](../docs/distance-deletion-mc.md) · [Numerical review](../reviews/distance-deletion-mc-verification.md)

A separate archived build of manuscript `c48f091` reproduced the PDF byte-for-byte using two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` and `SOURCE_DATE_EPOCH=1795731780`. PDF SHA-256 is `69f156697e7ea7f1ceadb6083cd5b297f14c7db0dac8796ff367d19ea19416d5`. Body and references occupy pages 3–14. Appendices begin on page 15 of 101 and list all 35 tracked Python modules. All team and author fields are blank. [Manuscript review](../reviews/distance-deletion-mc-paper-review.md) · [PDF](../paper/main.pdf)

## Fisher allocation verification

The planning protocol froze at `2fc20af` and ran at `bfd73f9`. In a detached checkout of `2a7e971`, `python q4_fisher.py --data "<attachment directory>/date" --output regenerated` reproduced both planning tables byte-for-byte. Independent verification used a different parameterization and numerical gradients and recovered all 60 allocation rows and 15 precision rows. [Results](../docs/q4-fisher.md) · [Numerical review](../reviews/q4-fisher-verification.md)

The anonymous PDF at `dddc541` has SHA-256 `fc872aad7a9b3cf241ffb5315cd43e0e9f631f5ddda020f26e6f3de4b2efe055`. Body and references occupy pages 3–14. Appendices begin on page 15 of 103 and list all 36 tracked Python modules. [Manuscript review](../reviews/q4-fisher-paper-review.md) · [PDF](../paper/main.pdf)

## Paired allocation verification

The protocol froze at `2bdbc6f` and ran at `b47db32`. In a detached checkout, `python q4_paired_planning.py --data "<attachment directory>/date" --output regenerated` reproduced all three planning tables byte-for-byte. The updated Fisher entry point also reproduced its two archived tables byte-for-byte. Independent enumeration of joint mask outcomes confirmed the preserved marginals and independent meat identity. All 48 allocation counts matched exactly, and the largest numerical discrepancy across the precision and summary tables was 1.18e-13. [Results](../docs/q4-paired-planning.md) · [Numerical review](../reviews/q4-paired-planning-verification.md)

The anonymous manuscript at `7b0bc15` has PDF SHA-256 `f6a3f138598510c75ac8a84a7460d06a8632bfb1d423cfac0105b9cdd11b884c`. The body and references occupy pages 3–14. The appendices start on page 15 of 105 and list all 37 tracked Python modules. [Manuscript review](../reviews/q4-paired-planning-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 extrapolation drift verification

The protocol froze at `4e5fac1` and ran at `39e3cf3`. A detached checkout reproduced the drift CSV byte-for-byte using `python q4_extrapolation_drift.py --data "<attachment directory>/date"`. The CSV SHA-256 is `b42790d4f8d7b9217cb48d99667630a9103139521db412ef8da81998208ae273`. The same checkout reproduced 172 core CSVs and seven JSON files byte-for-byte and seven figures by decoded pixels using `python main.py --data "<attachment directory>/date"`. Independent fitting and direct count bisection matched the exact counts and verified all numerical limits to an absolute difference of at most 8.89e-15. [Results](../docs/q4-extrapolation-drift.md) · [Numerical review](../reviews/q4-extrapolation-verification.md)

The anonymous manuscript at `acd5d0b` has PDF SHA-256 `0f62df7459d56314519f34e9303e6edc63f208ecfe8dda36c31945372e174804`. The body and references occupy pages 3–15. Appendices start on page 16 of 108 and list all 38 tracked Python modules. [Manuscript review](../reviews/q4-extrapolation-paper-review.md) · [PDF](../paper/main.pdf)

## Five-model Q4 tail ablation verification

The protocol froze at `09c0aca` and the results were published at `af53ccd`. A detached checkout of implementation `bcf8f8a` ran `python main.py --data "<attachment directory>/date" --q4-tail-ablation` and reproduced all six added CSVs byte-for-byte. The default run reproduced 172 core CSVs and seven JSON files byte-for-byte and seven PNGs by decoded pixels. Independent fitting and recomputation matched every Q4 attainment count and drift boundary count and confirmed the adoption decision. Across the independent comparisons, maximum absolute differences were 1.33e-8 for scored folds, 4.17e-9 for pooled validation, 2.34e-11 for Q4 margins, 8.83e-13 for tail probability changes and 7.47e-10 for drift quantities. The published multinomial remains the primary model under the frozen rule. [Results](../docs/q4-tail-ablation.md) · [Numerical review](../reviews/q4-tail-ablation-verification.md)

The anonymous manuscript at `83c7d17` has PDF SHA-256 `6e2b71ecaed074d1a4635dca541c2770b53ca211d1130ea2daefb89e17cfa783`. The body and references occupy pages 3–15, and the appendices start on page 16 of 116 and list all 40 tracked Python source files. [Manuscript review](../reviews/q4-tail-ablation-paper-review.md) · [PDF](../paper/main.pdf)

## Actual playback distance audit verification

The scoring protocol froze at `7d8e2c4` and the aggregate results were published at `6bc07fa`. A detached checkout reproduced both CSVs byte-for-byte with `python q4_tail_distance.py --data "<attachment directory>/date"`. The independent comparison matched the two coverage rows exactly and found a maximum absolute score or interval difference of 4.45e-16 across the 12 score rows. The weighted split deltas reconstruct the released pooled deltas within 1.15e-16. The audit uses the released tail validation fits and the same 4,800 scoring resamples, with the original adoption decision. [Results](../docs/q4-tail-ablation.md#scoring-by-actual-playback-distance) · [Numerical review](../reviews/q4-tail-distance-verification.md)

The anonymous PDF at `11d8a59` has SHA-256 `8388bf645a54b40d247b3dc90828940bda9cc9f90967b2b338ace966cafb7e3f`. Body and references occupy pages 3–15. The appendices start on page 16 of 117 and include all 41 Python sources. [Manuscript review](../reviews/q4-tail-distance-paper-review.md) · [PDF](../paper/main.pdf)

## Q1 candidate-set verification

The split and calibration specification froze at `bfb37d7`. Results were first published at `e3c79cb`, with count-scale bootstrap intervals and paired differences added at `0cb1f52`. Independent computation reproduced all 96 threshold records and 128 group-count records exactly. Summary and paired point estimates and interval endpoints matched within 2.78e-16. A detached checkout of `d0e833b` reproduced 176 CSVs, including the four candidate-set exports, and seven JSON files byte-for-byte, and seven PNGs by decoded pixels, with `python main.py --data "<attachment directory>/date"`. [Results](../docs/q1-candidate-sets.md) · [Numerical review](../reviews/q1-candidate-sets-verification.md)

The anonymous manuscript at `5e10f95` has PDF SHA-256 `e27ce96c619f85f2cecdadd46f103e68deeabc35cab0d33c1770216b37633787`. The body and references occupy pages 3–16. Appendices begin on page 17 of 121 and include all 42 tracked Python modules. [Manuscript review](../reviews/q1-candidate-sets-paper-review.md) · [PDF](../paper/main.pdf)

## Q2 envelope-weight rank verification

The protocol froze at `c19d712` and the result tables were published at `7f12a59`. A detached checkout ran `python main.py --data "<attachment directory>/date"` and reproduced 180 CSVs and seven JSON files byte-for-byte and seven PNGs by decoded pixels. Independent direct fits verified all 60 checkpoint radii, six interior ranking transitions and the endpoint tie. All 300 draw classifications matched. The largest difference between independently refined first-lead weights was 2.11e-15. [Results](../docs/q2-envelope-rank.md) · [Numerical review](../reviews/q2-envelope-rank-verification.md)

The anonymous manuscript at `6d3453b` has PDF SHA-256 `ad21a8fa253ea275213d05e7c58be510c0f58079e3f68042ddecfcb9579ddd34`. The body and references occupy pages 3–16. Appendices start on page 17 of 124 and include all 43 tracked Python modules. [Manuscript review](../reviews/q2-envelope-rank-paper-review.md) · [PDF](../paper/main.pdf)

## Q2 spectral allocation verification

The protocol froze at `1b9a23d` and the tables were published at `4a7effc`. The detached-checkout main entry point reproduced 183 CSVs and seven JSON files byte-for-byte and seven PNGs by decoded pixels. Independent direct fits confirmed 120 checkpoint radii and 20 recorded events, with maximum radius and event-weight discrepancies of 8.53e-14 m and 9.00e-15, respectively. The equal-spectral path reproduced the archived overlap. The fixed-envelope slice retains the same strict leader at 0.40 and 0.70 throughout, so the frozen condition for resampling did not trigger. [Results](../docs/q2-spectral-allocation.md) · [Numerical review](../reviews/q2-spectral-allocation-verification.md)

The anonymous manuscript at `0519946` has PDF SHA-256 `180664b498d3567d96e9888e173791b1724211590c9a2341963e058802a6b49a`. Body and references occupy pages 3–16. The appendices start on page 17 of 126 and include all 44 tracked Python modules. [Manuscript review](../reviews/q2-spectral-allocation-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 envelope-weight attainment verification

Protocol `b57162c` froze before calculation. A detached checkout of `03e5651` reproduced all three CSVs byte-for-byte with `python main.py --data "<attachment directory>/date" --q4-envelope-attainment`. Independent direct fits reproduced all 60 checkpoint counts and verified five point zeros and 12 closed attainment intervals. All 11 interior upper endpoints qualify with 3,840 draws and the count immediately beyond is 3,839. [Results and reproduction command](../docs/q4-envelope-attainment.md) · [Numerical review](../reviews/q4-envelope-attainment-verification.md)

The anonymous manuscript at `32bf8b4` has PDF SHA-256 `3f776e363dc0c3f72c22b35ba8df1e1851cc838d30518c22769d0364dd5d7b57`. Body and references occupy pages 3–16. The appendices begin on page 17 of 129 and contain all 45 Python sources. [Manuscript review](../reviews/q4-envelope-attainment-paper-review.md) · [PDF](../paper/main.pdf)

## Q3 discordant-pair direction verification

The initial specification was committed at `ba7fc52`. The equal-size fitting and scoring sample, equal-distance comparison and full-information Firth penalty were clarified before the first formal run. The final pre-run protocol is `9212008`. Numerical results are archived at `1f518da`. An independent fit reproduced all fold counts, fallbacks, 12 paired contrasts and 45 standardized predictions. A detached checkout of `1f518da` regenerated the five direction CSVs byte-for-byte using `python main.py --data "<attachment directory>/date"`. [Results](../docs/q3-direction.md) · [Numerical review](../reviews/q3-direction-verification.md)

The anonymous manuscript at `8affc5a` has SHA-256 `ad426f83bbb3aae643eeadccdb3c2a87eb33aa81c2a8fe01d23871cf0ce4347d`. The body and references occupy pages 3–17. Appendices begin on page 18 of 133 and include all 46 Python sources. [Manuscript review](../reviews/q3-direction-paper-review.md) · [PDF](../paper/main.pdf)

## Q2 attenuation shape and rank verification

The protocol froze at `d6115ba` and the results were published at `33815ef`. A detached checkout reproduced 195 CSVs and seven JSON files byte-for-byte and seven PNGs by decoded pixels with `python main.py --data "<attachment directory>/date"`. Independent fits verified the archived overlap, all 300 holdout predictions and 2,400 draw records. Support and rank labels matched exactly. Separate exponents met the equal-weight Q2 preference rule, with published Q4 inputs retained for this comparison. [Results](../docs/q2-shape-rank.md) · [Numerical review](../reviews/q2-shape-rank-verification.md)

The anonymous manuscript at `6ce2726` has PDF SHA-256 `67bfe8096b7708769636f7e7200da2450e4d3b2ef1221f5ac2e8bd8b0865e3cf`. Body and references occupy pages 3–17. The appendices start on page 18 of 135 and include all 47 Python sources. [Manuscript review](../reviews/q2-shape-rank-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 attenuation-shape propagation verification

The protocol froze at `a1dde71` and the results were published at `0b2f316`. A detached checkout reproduced the results CSV byte-for-byte with `python main.py --data "<attachment directory>/date" --q4-shape-propagation`. The CSV SHA-256 is `a177d82f3c9f119e9f013724a29775b6107496d533453cc76a9010b2544e31e1`. Independent fits matched all 24 counts, gains, losses and decisions. All 12 archived isotonic and shared-exponent marginal counts matched, and their point margins agreed within 1.05e-16. [Results](../docs/q4-shape-propagation.md) · [Numerical review](../reviews/q4-shape-propagation-verification.md)

The anonymous manuscript at `64f59c8` has PDF SHA-256 `658ace1af86b54523eee8998f1d88cb5482d23b788ae735bfe476337c07baa15`. The body and references occupy pages 3–17. The appendices start on page 18 of 137 and include all 48 Python sources. [Manuscript review](../reviews/q4-shape-propagation-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 two-loss net boundary verification

The protocol froze at `771a615` and the results were published at `7cf5d88`. A detached checkout of that commit reproduced all three CSVs byte-for-byte with `python main.py --data "<attachment directory>/date" --q4-net-loss`. The independent calculation confirmed positivity of the cutoff, all 20 requirements, 120 boundary rows, 180 checkpoints and 16 published overlap counts. All 54 solved boundaries qualified in 3,840 draws and lost one qualifying draw at the 1e-8 probe beyond the boundary. [Results](../docs/q4-net-loss.md) · [Numerical review](../reviews/q4-net-loss-verification.md)

The anonymous manuscript at `3628038` independently rebuilt to PDF SHA-256 `5aa85c3446a636cbb30b7a5cefe2c1d4169317d96dae85bcf54f9fce48f3639e`. Body and references occupy pages 3–17. The appendices start on page 18 of 139 and include all 49 Python sources. [Manuscript review](../reviews/q4-net-loss-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 consecutive-distance verification

The protocol froze at af6a147. A detached checkout of 57b5b99 regenerated all four CSVs byte-for-byte with the main entry point and its consecutive-distance flag. Independent refits verified 5,220 grid records, 20 radii, 40 differences and 20 published checkpoint counts. The clean union-deletion four-shape prefix count at 150 m is 3,850/4,800. Its exact 95% Monte Carlo interval is 79.05% to 81.33%. Both arms extrapolate there. [Results](../docs/q4-consecutive.md) · [Numerical review](../reviews/q4-consecutive-verification.md)

The anonymous manuscript at ecf2567 independently rebuilt byte-for-byte. Body and references span pages 3–17, with 50 source listings in the appendices. [Manuscript review](../reviews/q4-consecutive-paper-review.md) · [PDF](../paper/main.pdf)

## Q4 target-distance loss verification

The protocol froze at f854f68 and results were published at 82011ee. A detached checkout reproduced all three CSVs byte-for-byte using the main entry point with the target-loss flag. Independent direct score inversion verified 1,566 grid rows, 108 boundary rows and 12 inverse radii. At 20% loss in each component, the four-curve prefix recovers 96 m with full training and 84 m after union deletion. [Results](../docs/q4-target-loss.md) · [Review](../reviews/q4-target-loss-verification.md)
