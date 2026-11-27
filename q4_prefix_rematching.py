"""Sharp Q4 consecutive-radius bounds under draw bijections."""
import numpy as np
import pandas as pd

import q2
from q4_consecutive import GRID, SCENARIOS
from q4_draw_rematching import attaining_permutation
from q4_envelope_attainment import DRAWS, REQUIRED
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities


def first_failure(curves, probabilities, cutoff, loss):
    """Store the first failing grid index for each acoustic-behavior pair."""
    tv = q2.CALLS.index("tv")
    excess = probabilities[1:, 0, tv] - probabilities[1:, 1, tv]
    # With a positive cutoff, a nonpositive excess cannot pass any shape.
    fidelity = np.minimum.reduce([curve[1:, tv] for curve in curves.values()])
    response = (1 - loss) * (excess - loss * np.maximum(excess, 0))
    failure = np.full(cutoff.shape, len(GRID), dtype=np.int16)
    for start in range(0, DRAWS, 128):
        block = slice(start, start + 128)
        first = failure[block]
        alive = np.ones(first.shape, dtype=bool)
        for k in range(len(GRID)):
            passed = fidelity[block, k, None] * response[:, k] >= cutoff[block]
            first[alive & ~passed] = k
            alive &= passed
    return failure


def radius_bounds(failure, original, scenario, endpoint_witness=None):
    indices = np.arange(DRAWS)
    for bound in ("minimum", "maximum"):
        cache = {}

        def count_at(k):
            if k not in cache:
                mask = failure > k
                assignment = attaining_permutation(~mask if bound == "minimum" else mask)
                count = int(mask[indices, assignment].sum())
                cache[k] = count, assignment
            return cache[k]

        if bound == "maximum" and scenario == "clean":
            passing, failing = len(GRID) - 1, len(GRID)
        else:
            passing, failing = -1, len(GRID)
            if bound == "minimum" and original < len(GRID) - 1:
                failing = original + 1
            if bound == "minimum" and endpoint_witness is not None:
                failing = len(GRID) - 1
            if bound == "maximum":
                passing = original
                failing = int(np.searchsorted(GRID, 100))
            # The sentinel nodes denote an empty prefix and an unevaluated beyond-cap node.
            while failing - passing > 1:
                middle = (passing + failing) // 2
                if count_at(middle)[0] >= REQUIRED:
                    passing = middle
                else:
                    failing = middle

        at_count = count_at(passing)[0] if passing >= 0 else None
        next_count = count_at(failing)[0] if failing < len(GRID) else None
        witness_node = failing if bound == "minimum" and next_count is not None else passing
        if witness_node < 0:
            witness_node = 0
        assignment = count_at(witness_node)[1]
        first = failure[indices, assignment]
        at_witness = int((first > passing).sum()) if passing >= 0 else None
        next_witness = int((first > failing).sum()) if failing < len(GRID) else None
        if at_count is not None:
            assert at_count >= REQUIRED and at_witness >= REQUIRED
        if next_count is not None:
            assert next_count < REQUIRED and next_witness < REQUIRED
        yield {
            "bound": bound, "radius_m": GRID[passing] if passing >= 0 else None,
            "status": "empty_at_20" if passing < 0 else "grid_cap" if next_count is None else "interior",
            "bound_count_at_radius": at_count, "bound_count_next": next_count,
            "next_distance_m": GRID[failing] if next_count is not None else None,
            "witness_count_at_radius": at_witness, "witness_count_next": next_witness,
        }, assignment, first


def write(data, output, baseline):
    archived = pd.read_csv(baseline / "q4_consecutive_counts.csv")
    diagonal = archived.loc[archived["shape"].eq("all_four")].set_index(
        ["model", "scenario", "distance_m"]
    ).prefix_count
    endpoint = pd.read_csv(baseline / "q4_draw_rematching.csv")
    assert (endpoint.loc[endpoint.distance_m.eq(100), "maximum_count"] < REQUIRED).all()
    endpoint_assignment = pd.read_csv(baseline / "q4_draw_rematching_witnesses.csv").query(
        "model == 'drop_union' and distance_m == 150 and bound == 'minimum'"
    ).sort_values("acoustic_draw").behavior_draw.to_numpy() - 1
    curves = acoustic_fidelities(data, distances=GRID)
    indices = np.arange(DRAWS)
    rows, witnesses = [], []
    for model, probabilities in behavior_probabilities(data, distances=GRID):
        if model == "full":
            iso = curves["isotonic"][1:, :, 0]
            excess = probabilities[1:, 0, :, 0] - probabilities[1:, 1, :, 0]
            cutoff = (iso @ excess.T) / (2 * len(q2.CALLS))
            assert np.all(np.isfinite(cutoff) & (cutoff > 0))
        for scenario, loss in SCENARIOS:
            failure = first_failure(curves, probabilities, cutoff, loss)
            original_counts = (failure[indices, indices, None] > np.arange(len(GRID))).sum(axis=0)
            np.testing.assert_array_equal(original_counts, diagonal.loc[model, scenario].reindex(GRID))
            original = int(np.flatnonzero(original_counts >= REQUIRED)[-1])
            endpoint_prefix = None
            if model == "drop_union" and scenario == "clean":
                endpoint_prefix = int((failure[indices, endpoint_assignment] == len(GRID)).sum())
                assert endpoint_prefix <= 3818
            label = {"model": model, "scenario": scenario}
            for result, assignment, first in radius_bounds(failure, original, scenario, endpoint_prefix):
                rows.append({**label, "original_radius_m": GRID[original],
                             "original_count_at_radius": original_counts[original],
                             "archived_endpoint_witness_prefix_150": endpoint_prefix, **result})
                witnesses.append(pd.DataFrame({
                    **label, "bound": result["bound"], "acoustic_draw": indices + 1,
                    "behavior_draw": assignment + 1,
                    "first_failed_m": np.where(first == len(GRID), np.nan, GRID[0] + .5 * first),
                }))
                print(model, scenario, result, flush=True)
    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output / "q4_prefix_rematching.csv", index=False, lineterminator="\n")
    pd.concat(witnesses).to_csv(output / "q4_prefix_rematching_witnesses.csv", index=False,
                                lineterminator="\n")
