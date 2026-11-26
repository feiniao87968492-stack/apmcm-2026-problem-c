# Stage 4 algorithm and model review

## Reviewed scope

- User-approved four-question execution plan
- workflow.md, memory.md, and docs/data-audit.md
- 2026 APMCM Problem C.pdf, questions 1–4
- Attachment Data01 and Data02
- Attachment Data03–Data11 structure and Supplementary 4 propagation notes
- Attachment Code1 and Code2 R reference methods

## Findings

### F1 Acoustic classification requires the shared feature set

- Type: feature-availability leakage
- Severity: WARNING
- Evidence reference: Data01 F02 field and docs/data-audit.md
- Recommended action: Keep Date-by-Location grouped, fold-local preprocessing and the seven shared numeric features as primary, with F02 availability reported only as a sensitivity analysis.

F02 is present for all 24 two-voice recordings and absent for all 84 other recordings. Univariate rank tests should report their effective samples and describe the limits imposed by recording-group dependence. A common-sample report should never construct a fictitious second frequency for the other calls.

### F2 Propagation row resampling has an uncertain sampling unit

- Type: evidence-path constraint
- Severity: WARNING
- Evidence reference: Data03–Data11 headers and Supplementary 4 description of counts between 190 and 300
- Recommended action: Carry a complete row of available distances when resampling within each table, treat cross-modality dependence as unidentified, and label interval estimates as conditional variation under the stated row-level working assumption.

Files contain seven distance columns and lack recording or experiment identifiers. Document the distinction between preserving row structure mechanically and certifying independent experiment-level replication. Compare alternate acoustic weights and report threshold bounds when a curve stays on one side of the criterion across 4–256 m.

### F3 Paired response and sparse latency require different estimands

- Type: sample support
- Severity: WARNING
- Evidence reference: Data02 expID, Type, three binary behaviors, and three latency fields
- Recommended action: Retain pairs for binary contrasts and resampling, report the empirical zero for approaches among 139 controls, and record control approach latency as non-estimable.

Overall response matches the union of the three behaviors in the supplied rows. Controls support only no response, head-only and vocal-only combinations. Any fitted mass for absent cells reflects regularization. Positive lag estimates must use their matching latency columns and distinguish response counts, positive-duration/intensity measures, and onset.

### F4 Integrated communication scenarios require a fixed baseline and bounded claim

- Type: estimand and identification
- Severity: WARNING
- Evidence reference: User-approved Q4 plan, problem statement Q4, Data02 Distance and Data03–Data11
- Recommended action: Define the clean-reference cutoff once for each call, use the shared supported range of 20–150 m and specify a first sustained crossing rule, then report noise-related response changes only under an explicit scenario link.

Re-normalizing by the near-distance value in each scenario can cancel uniform fidelity loss. The product of acoustic fidelity and modeled response probability is an index with two separately estimated components. A behavioral response change under simulated noise needs an additional assumed mapping, such as a fidelity retention multiplier applied to the natural-call response excess over control. Describe any such response quantity as a scenario prediction. The playback tables describe group responses and have no individual outcome labels.

## Blocking risks

No blocker for implementing the proposed conditional and model-based analyses. Independence-based propagation intervals, directly measured noise effects, and individual detection claims exceed the available evidence.

## Non-blocking warnings

### F1–F4 Implementation safeguards

- Type: data support and inference
- Severity: WARNING
- Evidence reference: F1–F4 above
- Recommended action: Carry all four evidence limitations into the model specification, result-table metadata, and eventual paper captions.

## Required follow-up

- Update the model specification and docs/data-audit.md with the provenance and resampling distinctions in F2, the zero-cell handling in F3, and the radius and scenario rules in F4.
- Record the Stage 4 and Stage 5 claim ceilings under gates/ before releasing model results.
- Require the independent validation to check threshold bounds and scenario monotonicity at the frozen clean cutoff.

## Reviewer recommendation

The main route is suitable for model freeze after the specification documents the supported estimands and scenario conventions. Retain qualified, population- and design-conditional inference for uncertain propagation replication and modeled environmental change.

Verdict: PASS_WITH_WARNINGS

## Required reads referenced

- references/subagent-model-building.md
- references/protocol-subagent-delegation.md
- references/protocol-readiness-gate.md
- references/protocol-rollback.md
- references/anti-hallucination.md
- schemas/reviewer-output-schema.md
- schemas/reviewer-self-discipline-checklist.md
- workflow.md
- memory.md
- docs/data-audit.md

## Confidence

high — the central concerns are corroborated by the question text, attachment headers and direct tabulation of the playback and acoustic records.

## Forbidden-behavior self-check

- [OK] Did not confirm user decisions
- [OK] Did not clear blockers
- [OK] Did not mark stages or rounds complete
- [OK] Did not increase claim level on behalf of the main agent
- [OK] Did not invoke another subagent
- [OK] Did not write or edit project files outside the review output

## Decision / gate / branch / rollback recommendation

Record a Stage 4 readiness gate with conditional propagation and noise-scenario claims. The review identifies no additional blocking decision, branch, or rollback.
