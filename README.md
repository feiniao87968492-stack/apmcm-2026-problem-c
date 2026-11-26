# 2026 APMCM Problem C

Reproducible analysis of acoustic communication and playback responses in African penguins. The original observations and supplementary material are available from the [study archive](https://zenodo.org/records/21376649).

## Reproduce

Use Python 3.10 in a virtual environment and the contest attachment folder containing Data01 through Data11. The default run uses 300 draws with the seeds recorded in the specification.

```sh
python -m pip install -r requirements.txt
python main.py --data "/path/to/C-attachments"
```

The six figures in `results/` each have a same-name CSV and JSON metadata file. To compile the English paper, run `pdflatex -halt-on-error main.tex` twice from `paper/`. Set the team number locally by defining `\TeamNumber` in `paper/team-local.tex` when preparing a team copy.

- [English paper](paper/main.pdf)
- [Frozen analysis assumptions and rationale](docs/model-spec.md)
- [Data audit](docs/data-audit.md)
- [Round-one comparisons and model decisions](docs/round1-results.md)
- [Round-two ablations and paired intervals](docs/round2-results.md)
- [Final behavior comparisons and recording-group influence](docs/final-followup-results.md)
- [Creative modeling comparisons and inverse loss limits](docs/creative-results.md)
- [Workflow and milestones](workflow.md)
- [Verification and evidence](gates/final.md)
