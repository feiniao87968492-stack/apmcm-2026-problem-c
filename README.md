# 2026 APMCM Problem C

Reproducible analysis of acoustic communication and playback responses in African penguins. The original observations and supplementary material are available from the [study archive](https://zenodo.org/records/21376649).

## Reproduce

Use Python 3.10 in a virtual environment and the contest attachment folder containing Data01 through Data11. The default run uses 300 draws with the seeds recorded in the specification.

```sh
python -m pip install -r requirements.txt
python main.py --data "/path/to/C-attachments"
```

The seven figures in `results/` each have a same-name CSV and JSON metadata file. To compile the English paper, run `pdflatex -halt-on-error main.tex` twice from `paper/`. Set the team number locally by defining `\TeamNumber` in `paper/team-local.tex` when preparing a team copy.

- [English paper](paper/main.pdf)
- [Frozen analysis assumptions and rationale](docs/model-spec.md)
- [Data audit](docs/data-audit.md)
- [Round-one comparisons and model decisions](docs/round1-results.md)
- [Round-two ablations and paired intervals](docs/round2-results.md)
- [Final behavior comparisons and recording-group influence](docs/final-followup-results.md)
- [Creative modeling comparisons and inverse loss limits](docs/creative-results.md)
- [Post hoc checks on sparse masks and inverse loss](docs/posthoc-results.md)
- [Q4 decision rules, variance decomposition and trial design](docs/q4-decision-results.md)
- [Workflow and milestones](workflow.md)
- [Verification and evidence](gates/final.md)

- [Playback grouping, date-block uncertainty and trial precision](docs/playback-dependence.md)

- [Matched distance, loss limits and weighted behaviors](docs/matched-sensitivity.md)
- [Attenuation fits and acquisition-batch sensitivity](docs/physical-attenuation.md)

- [Acoustic transformations and recorded onset](docs/acoustic-onset.md)

- [Hypothetical noise power and responder counts](docs/noise-scenarios.md)

- [Final Figure 2 and noise agreement](docs/final-delivery.md)

- [Strict playback holdouts and crossed resampling](docs/strict-playback.md)

- [False Bay sea-state sensitivity](docs/false-bay.md)

- [WAVERYS and assumed propagation example deletions](docs/example-sensitivity.md)
- [Missing propagation comparisons](docs/missing-propagation.md)
- [Group size in playback and Q4](docs/group-size.md)
- [Vocal counts and contact scenarios](docs/vocal-counts.md)
- [First vocal replies and group event order](docs/first-reply.md)
- [Q4 averages and attainment over the supported annulus](docs/spatial-annulus.md)
- [Q4 ranking by context and behavior priority](docs/context-priority.md)
- [Historical correlation recovery priorities](docs/recovery-priority.md)
- [Q3 response-gap decomposition](docs/behavior-gap.md)
- [Q4 control subtraction and cutoff sensitivity](docs/control-subtraction.md)
- [Q4 behavior model sensitivity](docs/behavior-ablation.md)
- [Q4 distance deletion diagnosis](docs/distance-deletion.md)
