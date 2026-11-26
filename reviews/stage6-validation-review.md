# Stage 6 independent validation review

## Reviewed scope

- `docs/model-spec.md`, `workflow.md`, `memory.md`, and `gates/baseline.md`
- `results/q1_oof_predictions.csv` and `results/q1_metrics.csv`
- Original Data02–Data11 attachments and `results/q2_radii.csv`
- `results/q3_paired_response.csv`, `results/q3_grouped_validation.csv`, and representative latency rows
- `results/q4_environment_curves.csv`, `results/q4_radii.csv`, and `results/q4_model_comparison.csv`

## Findings

### F1 — Q1 pooled performance matches the held-out records

- Type: metric-reproduction
- Severity: WARNING
- Evidence reference: `results/q1_oof_predictions.csv`, `results/q1_metrics.csv`
- Recommended action: Present the classifier as a low-performing baseline consistent with the grouped estimate.

Recalculating the three one-vs-rest F1 values from the exported predictions and averaging them gives 0.2250321228. The reported group bootstrap spans 0.145–0.286, and the fold-majority baseline is 0.207. The grouped predictions and uncertainty support weak discrimination with the six shared features.

### F2 — Q2 recognition radii reproduce from the original attachments

- Type: raw-data-cross-check
- Severity: WARNING
- Evidence reference: Original Data03–Data11, `results/q2_radii.csv`, `results/q2_fit_checks.csv`
- Recommended action: Describe the ranges as dependent on the chosen fidelity weights, threshold and row-resampling unit.

An independent calculation took marginal means using the original CSVs, pooled adjacent violations with a standard-library block implementation, and interpolated on the log-distance scale. At the 0.50 threshold it reproduced 84.72 m for flat, 144.56 m for modulated, and 169.73 m for two-voice calls. Their primary conditional intervals are 83.65–85.87 m, 142.27–147.05 m, and 168.90–170.59 m, respectively.

### F3 — Q3 paired counts reproduce directly

- Type: raw-data-cross-check
- Severity: INFO
- Evidence reference: Original Data02, `results/q3_paired_response.csv`, `results/q3_grouped_validation.csv`
- Recommended action: Retain the descriptive interpretation of the measured pair difference and the standardized interpretation of the model predictions.

Independent grouping of raw records recovered 139 pairs, with 90 natural-call responses, 18 control responses, and 90 pairs at different playback distances. The direct response-rate difference is 51.80 percentage points. Five held-out folds average about 1.245 mask log loss for the fitted model and 1.384 for pooled frequencies, with corresponding any-response Brier scores of 0.154 and 0.238.

### F4 — Q4 exported radii and environmental ordering reproduce

- Type: downstream-cross-check
- Severity: WARNING
- Evidence reference: `results/q4_environment_curves.csv`, `results/q4_radii.csv`, `results/q4_model_comparison.csv`
- Recommended action: Label the clean two-voice radius as at least 150 m within the common range and preserve censored interval endpoints in the paper.

Computing the last above-cutoff distance and linearly interpolating on the exported clean curves reproduced 87.00 m, 131.67 m, and the lower bound of 150 m. Their bounded bootstrap percentiles are 64.77–121.04 m, 85.29–150 m, and 144.27–150 m. The upper bound caps 71 of 300 modulated and 286 of 300 two-voice clean draws. Every environmental index curve remained at or below its clean curve throughout the grid. Under 20% fidelity loss, the respective operational radius values are 46.02, 70.41, and 124.28 m.

## Blocking risks

None for the evidence ceilings in `gates/baseline.md`.

## Non-blocking warnings

- Type: claim-scope
- Severity: WARNING
- Evidence reference: F1–F4 and `gates/baseline.md`
- Recommended action: Keep the low Q1 held-out performance, conditional Q2 intervals, descriptive Q3 pair comparison and range-bounded Q4 scenarios explicit in the paper.

## Required follow-up

- Freeze `claims/baseline-snapshot.md` with per-question entries per `references/baseline-snapshot-template.md`, using metrics actually verified in this review.
- Carry the F1–F4 qualifications into the relevant claims in `claims/claim-registry.md` and the paper.

## Reviewer recommendation

The independently checked quantities and observed validation outputs support the documented analysis at `feasible_baseline` level and `exploratory_analysis` for environmental projections. Freeze the first Stage 6 baseline in `claims/baseline-snapshot.md` and its per-question entries under the template.

Verdict: PASS_WITH_WARNINGS

## Required reads referenced

- `references/subagent-validation-paper.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/protocol-readiness-gate.md`
- `references/baseline-snapshot-template.md`
- `schemas/reviewer-output-schema.md`
- `schemas/reviewer-self-discipline-checklist.md`
- `stop-that-shit/SKILL.md`

## Confidence

high — the primary outputs agreed with independent calculations from raw data or exported point predictions, with Q4 bootstrapping assessed from the reported range bounds and counts.

## Forbidden-behavior self-check

- [OK] Did not confirm user decisions
- [OK] Did not clear blockers
- [OK] Did not mark stages or rounds complete
- [OK] Did not increase claim level on behalf of the main agent
- [OK] Did not invoke another subagent
- [OK] Did not write or edit project files outside the review output
- [OK] Did not write claims/baseline-snapshot.md
- [OK] Did not export when the final evidence gate has not passed

## Decision / gate / branch / rollback recommendation

Freeze the first validated baseline under `claims/baseline-snapshot.md` with per-question entries and retain the documented claim ceilings.

