"""Compare local and 100 m matched noise for the four-shape Q4 net prefix."""
from itertools import product

import numpy as np
import pandas as pd

import noise_scenarios
import q2
from control_subtraction import reference
from q4_consecutive import GRID
from q4_envelope_attainment import DRAWS, REQUIRED
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities

TARGETS = (50, 100)
CAP = 6.
MATCH = np.searchsorted(GRID, 100)


def prefix_counts(clean_score, cutoff, retention, coupled):
    factor = retention**2 if coupled else retention
    # Negative excess cannot attain the positive cutoff in either scenario.
    margin = clean_score * factor - cutoff[:, None]
    return np.count_nonzero(np.logical_and.accumulate(margin >= 0, axis=1), axis=0)


def boundary(count_at, clean, at_cap):
    if clean < REQUIRED:
        return np.nan, "infeasible", None, None
    if at_cap >= REQUIRED:
        return CAP, "cap", at_cap, None
    low, high = 0., CAP
    # Preserve a passing lower bracket and a failing upper bracket.
    while high - low > 1e-9:
        mid = (low + high) / 2
        if count_at(mid) >= REQUIRED:
            low = mid
        else:
            high = mid
    return low, "boundary", count_at(low), high


def write(data, output, baseline):
    curves, shared_parameters = acoustic_fidelities(data, distances=GRID, include_shared=True)
    tv = q2.CALLS.index("tv")
    parameters = shared_parameters[1:, tv, None, :]
    clean_shared = noise_scenarios.fidelity(GRID, parameters, 0)[:, 0]
    weakest = np.minimum.reduce([curve[1:, tv] for curve in curves.values()])
    archived = pd.read_csv(baseline / "q4_consecutive_counts.csv")
    ranges = pd.read_csv(baseline / "q4_consecutive_ranges.csv").set_index(["model", "arm"])
    targets, radii = [], []
    for model, probabilities in behavior_probabilities(data, distances=GRID):
        excess = probabilities[:, 0] - probabilities[:, 1]
        if model == "full":
            cutoff = reference(curves["isotonic"], excess)[1:]
            assert np.all(np.isfinite(cutoff) & (cutoff > 0))
        score = weakest * excess[1:, tv]
        natural, control = (ranges.loc[(model, arm)] for arm in ("call", "control"))

        def flags(distance):
            return dict(prefix_outside_natural_range=GRID[0] < natural.min_m or distance > natural.max_m,
                        prefix_outside_control_range=GRID[0] < control.min_m or distance > control.max_m)

        clean = prefix_counts(score, cutoff, 1., False)
        old = archived.query("model == @model and scenario == 'clean' and shape == 'all_four'")
        np.testing.assert_array_equal(clean, old.sort_values("distance_m").prefix_count)
        for spatial, link in product(("local", "uniform"), ("acoustic_only", "coupled")):
            coupled = link == "coupled"
            label = dict(model=model, spatial=spatial, link=link, draws=DRAWS)

            def evaluate(db, end):
                stop = max(end, MATCH+1) if spatial == "uniform" else end
                ratio = noise_scenarios.fidelity(GRID[:stop], parameters, db)[:, 0] / clean_shared[:, :stop]
                retention = ratio[:, MATCH:MATCH+1] if spatial == "uniform" else ratio
                return prefix_counts(score[:, :end], cutoff, retention, coupled)

            counts = {db: evaluate(db, len(GRID)) for db in (3, 6)}
            for db, count in counts.items():
                passing = np.flatnonzero(count >= REQUIRED)
                node = passing[-1] if len(passing) else None
                radius = GRID[node] if node is not None else None
                status = "empty_at_20" if node is None else "grid_cap" if radius == GRID[-1] else "interior"
                radii.append(dict(label, db=db, radius_m=radius, status=status, count_at_20=count[0],
                                  count_at_radius=None if node is None else count[node],
                                  count_next=None if node is None or node == len(GRID)-1 else count[node+1],
                                  **(flags(radius) if node is not None else {})))
            for distance in TARGETS:
                j = np.searchsorted(GRID, distance)

                def count_at(db):
                    return int(evaluate(db, j+1)[-1])

                maximum, status, count, next_db = boundary(count_at, clean[j], counts[6][j])
                targets.append(dict(label, distance_m=distance, count_0db=clean[j], count_3db=counts[3][j],
                                    count_6db=counts[6][j], max_db=maximum, status=status, count_at_limit=count,
                                    failing_db=next_db, failing_count=None if next_db is None else count_at(next_db),
                                    **flags(distance)))

    output.mkdir(parents=True, exist_ok=True)
    for suffix, rows in (("targets", targets), ("radii", radii)):
        pd.DataFrame(rows).to_csv(output / f"q4_matched_noise_{suffix}.csv", index=False, lineterminator="\n")
