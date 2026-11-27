"""Stress-test the Q4 endpoint decisions while holding both draw margins fixed."""
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching

import q2
from q4_envelope_attainment import DISTANCES, DRAWS, REQUIRED
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities


def attaining_permutation(edges):
    assignment = maximum_bipartite_matching(csr_matrix(edges), perm_type="column")
    matched = assignment >= 0
    unused = np.setdiff1d(np.arange(len(assignment)), assignment[matched])
    assignment[~matched] = unused
    np.testing.assert_array_equal(np.sort(assignment), np.arange(len(assignment)))
    assert edges[np.arange(len(assignment)), assignment].sum() == matched.sum()
    return assignment


def crossed_passes(curves, probabilities, cutoff, distance, loss):
    target = np.searchsorted(DISTANCES, distance)
    tv = q2.CALLS.index("tv")
    excess = probabilities[1:, 0, tv, target] - probabilities[1:, 1, tv, target]
    response = (1-loss) * (excess - loss * np.maximum(excess, 0))
    passes = np.ones(cutoff.shape, dtype=bool)
    for curve in curves.values():
        passes &= curve[1:, tv, target, None] * response >= cutoff
    return passes


def write(data, output, baseline):
    curves = acoustic_fidelities(data)
    old = pd.read_csv(baseline / "q4_net_loss_counts.csv")
    original = old.loc[old["shape"].eq("all_four")].set_index(
        ["model", "distance_m", "acoustic_loss", "response_loss"]
    )["count"]
    rows, witnesses = [], []
    indices = np.arange(DRAWS)
    for model, probabilities in behavior_probabilities(data):
        if model == "full":
            iso = curves["isotonic"][1:, :, 0]
            response = probabilities[1:, 0, :, 0] - probabilities[1:, 1, :, 0]
            cutoff = (iso @ response.T) / (2 * len(q2.CALLS))
            assert cutoff.shape == (DRAWS, DRAWS) and np.isfinite(cutoff).all()

        for distance, loss in ((100, .2), (150, 0.)):
            passes = crossed_passes(curves, probabilities, cutoff, distance, loss)
            diagonal = int(passes.trace())
            assert diagonal == original.loc[model, distance, loss, loss]
            crossed = int(passes.sum())
            label = {"model": model, "distance_m": distance, "loss_each": loss}
            bounds = {}
            for bound, graph in (("minimum", ~passes), ("maximum", passes)):
                assignment = attaining_permutation(graph)
                attained = passes[indices, assignment]
                bounds[bound] = int(attained.sum())
                witnesses.append(pd.DataFrame({
                    **label, "bound": bound, "acoustic_draw": indices + 1,
                    "behavior_draw": assignment + 1, "passes": attained,
                }))
            assert bounds["minimum"] <= diagonal <= bounds["maximum"]
            assert bounds["minimum"] * DRAWS <= crossed <= bounds["maximum"] * DRAWS
            rows.append({
                **label, "draws": DRAWS, "required": REQUIRED, "crossed_pairs": DRAWS**2,
                "original_count": diagonal, "crossed_count": crossed,
                "minimum_count": bounds["minimum"], "maximum_count": bounds["maximum"],
                "original_share": diagonal / DRAWS, "crossed_share": crossed / DRAWS**2,
                "minimum_share": bounds["minimum"] / DRAWS, "maximum_share": bounds["maximum"] / DRAWS,
                "original_passes_80": diagonal >= REQUIRED,
                "crossed_passes_80": crossed >= REQUIRED * DRAWS,
                "permutation_can_flip_80": bounds["minimum"] < REQUIRED <= bounds["maximum"],
            })

    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output / "q4_draw_rematching.csv", index=False, lineterminator="\n")
    pd.concat(witnesses).to_csv(output / "q4_draw_rematching_witnesses.csv", index=False,
                                lineterminator="\n")
