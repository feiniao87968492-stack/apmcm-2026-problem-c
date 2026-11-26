# Stage 10 evidence and claim review

## Reviewed scope

- `paper/main.tex`, `paper/results.tex`, and `paper/latency-table.tex`
- `claims/claim-registry.md`, `gates/baseline.md`, `decisions/decision-baseline.md`, and `docs/model-spec.md`
- `figures/figure-index.md`, `reviews/stage6-validation-review.md`, and `reviews/stage9-figure-review.md`
- Q1 rank, feature, performance and importance outputs, Q2 radii and propagation metadata, Q3 paired, validation, combination, representative and covariate prediction tables, and Q4 radius, comparison, scenario and expected-responder outputs
- Official Problem C questions 1–4

## Findings

### F1 — Numerical claims trace to the baseline outputs

- Type: claim-grounding
- Severity: INFO
- Evidence reference: `claims/claim-registry.md`, `gates/baseline.md`, `paper/results.tex`, `reviews/stage6-validation-review.md`
- Recommended action: Preserve the distinction between grouped classifier performance, observed pair contrasts and standardized model predictions.

The summary and principal tables match the rounded source values. The grouped acoustic macro F1 and majority baseline are 0.225 and 0.207. The observed paired difference is 51.8 percentage points with a 43.9–60.1 point bootstrap interval. Grouped mask log loss averages 1.245 versus 1.384 and Brier scores average 0.154 versus 0.238. The cited flat vocal-only contrast at 50 m matches the corresponding prediction row.

### F2 — Recognition and environmental results stay within their evidence ceilings

- Type: claim-scope
- Severity: WARNING
- Evidence reference: `docs/model-spec.md`, `gates/baseline.md`, `results/q2_radii.csv`, `results/q4_radii.csv`, `results/q4_environment_curves.csv`, `results/q4_expected_responders.csv`
- Recommended action: Retain the conditional interpretation and show the two-voice clean radius as a lower bound at the support limit.

Q2 0.40–0.60 radii and rounded intervals match the primary resampling rows. At 0.70 the two higher equal-weight intervals overlap, and envelope weighting reverses their order. Q4 clean and 20% loss estimates match the source table. The 100 m response and expected-count examples match the scenario outputs. These modeled changes use a fixed clean cutoff and a hypothesized environmental response link.

### F3 — Figure and appendix evidence is available

- Type: export-grounding
- Severity: INFO
- Evidence reference: `figures/figure-index.md`, `reviews/stage9-figure-review.md`, `paper/latency-table.tex`, `results/q3_representative_latency.csv`
- Recommended action: Keep the appendix prediction conditions and show source-supported captions in the compiled manuscript.

The figure review verifies the five plot bundles and their intended meanings. The prediction appendix adds calls, controls and all three behaviors at the representative distances, with local support marks and an unavailable latency marker where appropriate. The baseline decision is recorded and no open branch or pending decision was found.

### F4 — The manuscript links Q1 to propagation and reports matched covariate contrasts

- Type: question-coverage
- Severity: WARNING
- Evidence reference: Problem C Q1 and Q3, `results/q3_adjusted_conditions.csv`, `results/q1_feature_importance.csv`, `paper/main.tex`
- Recommended action: Keep the matched Q3 example and the Q1 rationale for retaining the measured labels and spectral component.

The manuscript now reports the adjusted two-voice response contrasts by context and group size at 100 m. The acoustic section explains the use of measured call labels and retention of the spectral component.

## Blocking risks

None within the claim scope in `gates/baseline.md`.

## Non-blocking warnings

- Type: reporting-scope
- Severity: WARNING
- Evidence reference: F2 and F4
- Recommended action: Retain the interpretation limits and the question-coverage statements in the manuscript.

## Required follow-up

- Keep the support-bound and simulated-effect language in `paper/results.tex`.
- Keep the covariate example and Q1 handoff in `paper/main.tex` or `paper/results.tex`.
- Ensure the final `claims/claim-registry.md` table keeps the covariate example row with its supporting CSV.

## Reviewer recommendation

The claims and numerical outputs support the fixed baseline and the explicitly conditional conservation scenarios. The figure evidence and question-specific numerical appendix are present. Preserve the stated interpretation limits during final manuscript preparation.

Verdict: PASS_WITH_WARNINGS

## Required reads referenced

- references/subagent-validation-paper.md
- references/protocol-subagent-delegation.md
- references/evidence-gate.md
- references/anti-hallucination.md
- references/protocol-readiness-gate.md
- schemas/reviewer-output-schema.md
- schemas/reviewer-self-discipline-checklist.md
- claims/claim-registry.md
- gates/baseline.md
- decisions/decision-baseline.md
- figures/figure-index.md

## Confidence

high — The four question summaries, principal numerical tables, companion data and stated interpretation limits agree.

## Forbidden-behavior self-check

- [OK] Did not confirm user decisions
- [OK] Did not clear blockers
- [OK] Did not mark stages or rounds complete
- [OK] Did not increase claim level on behalf of the main agent
- [OK] Did not invoke another subagent
- [OK] Did not write or edit project files outside the review output
- [OK] Did not write gates/final-evidence-gate.md
- [OK] Audited every claim in claim-registry against its supporting gate's claim level

## Final Evidence Gate verdict suggestion: PASS_WITH_WARNINGS
