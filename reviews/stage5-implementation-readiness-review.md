# Stage 5 implementation readiness review

## Reviewed scope

- docs/model-spec.md and docs/data-audit.md
- workflow.md and memory.md
- reviews/stage4-algorithm-model-review.md
- Contest attachments Data01 through Data11
- Dispatcher interface and inherited Python import probe

## Findings

### F1 Within-pair covariates vary between stimuli

- Type: data relationship
- Severity: WARNING
- Evidence reference: Data02 columns expID, Type, Date, Context, Distance, and Npenguins
- Recommended action: Match and resample by expID, retain each stimulus row's measured covariates, and standardize modeled contrasts on the same grid.

All 139 IDs contain a call and a control. Date and Context agree across each pair, while Distance differs in 90 pairs and Npenguins differs in two pairs. The unadjusted paired response contrast describes the observed design.

### F2 Sparse behavior outcomes require explicit probability and latency contracts

- Type: implementation interface
- Severity: WARNING
- Evidence reference: Data02 behavior flags and docs/model-spec.md Q3
- Recommended action: Map each fitted estimator's class labels to eight fixed mask columns, preserve unsupported-cell flags, and mark unavailable conditional latencies.

All eight masks appear in the pooled dataset. No control approach is recorded. Cross-validation folds and bootstrap replicates can omit rare masks. Fit grouping and prediction postprocessing should preserve eight-column probability ordering and row sums of one. A nonzero fitted probability for empirically empty strata depends on regularization.

### F3 Integrated model can use a checked shared grid

- Type: reproducibility
- Severity: INFO
- Evidence reference: docs/model-spec.md Q2–Q4, Data02 Distance and Data03–Data11 headers
- Recommended action: Validate call labels, distances, quantity names, and draw identifiers at the Q4 boundary and retain censoring flags for each draw.

Call-specific playback ranges are 5–200 m for flat, 10–150 m for mod, and 20–200 m for tv. The common range supports the 20–150 m integration grid at 0.5 m spacing. Q2 and Q3 can hand off keyed point and bootstrap predictions without placeholder observations. Reproducible pairing of independent acoustic and behavior draws is a model-based uncertainty convention.

### F4 Runtime and dependencies are available for the baseline

- Type: reproducibility
- Severity: INFO
- Evidence reference: Inherited Python import probe and docs/model-spec.md
- Recommended action: Pin tested package versions, record the Python version and canonical seed, and record file hashes for the raw CSVs in the reproduction manifest.

All eleven required CSVs were readable. The project shell import probe passed for NumPy, pandas, SciPy, scikit-learn, matplotlib, and statsmodels. A dependency manifest had yet to appear at inspection. The baseline requires no specialized solver. Exact dependency pins and locator validation belong in implementation.

## Blocking risks

The agreed conditional analyses can proceed within the claim ceiling below.

## Non-blocking warnings

### F1–F4 Integration and inference checks

- Type: implementation and claim calibration
- Severity: WARNING
- Evidence reference: F1–F4 and reviews/stage4-algorithm-model-review.md
- Recommended action: Freeze the data interface and reproducibility conventions and record the observational and scenario-conditioned claim ceilings.

## Required follow-up

- Update docs/data-audit.md with the within-pair covariate audit and the uncertain propagation sampling units.
- Update docs/model-spec.md with fixed mask ordering, undefined latency behavior, keyed grid interfaces, and deterministic draw handling.
- Pin the tested runtime under requirements.txt and verify the raw-input locator and repeatable invocation in the implementation.
- Record the Stage 5 claim ceiling in gates/ and include coverage and censoring checks in independent validation.

## Reviewer recommendation

The frozen baseline is implementable with the supplied data and the observed Python environment. Support descriptive and grouped predictive results from the playbacks, conditional propagation uncertainty, and explicit scenario projections. Evidence for causal noise effects, independently replicated propagation uncertainty, and individual detection thresholds falls outside the available claim ceiling.

Verdict: PASS_WITH_WARNINGS

## Required reads referenced

- references/subagent-model-building.md
- references/protocol-subagent-delegation.md
- references/protocol-readiness-gate.md
- references/protocol-rollback.md
- references/protocol-fallback-and-deviation.md
- schemas/reviewer-output-schema.md
- schemas/reviewer-self-discipline-checklist.md
- docs/model-spec.md
- docs/data-audit.md
- workflow.md
- memory.md
- reviews/stage4-algorithm-model-review.md

## Confidence

high — the available input shapes, pair structure, sparse control responses and common distance range were checked directly.

## Forbidden-behavior self-check

- [OK] Did not confirm user decisions
- [OK] Did not clear blockers
- [OK] Did not mark stages or rounds complete
- [OK] Did not increase claim level on behalf of the main agent
- [OK] Did not invoke another subagent
- [OK] Did not write or edit project files outside the review output
- [OK] Did not execute shell commands or install packages

## Decision / gate / branch / rollback recommendation

Record the Stage 5 gate with grouped predictive and conditional scenario claims. No additional decision, branch, or rollback is needed for the approved baseline.
