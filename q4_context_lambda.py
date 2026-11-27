"""Invert the fixed-draw Q4 bounds under variable behavioral noise retention."""
import numpy as np
import pandas as pd

from q4_context_exposure import CONTEXTS, DRAWS, pass_indicators, prefix_scores
from q4_context_mc import HALF, coefficients, indicator_columns, vertices


CHECKPOINTS = (0., .5, 1., 1.5, 2.)
DENOMINATOR = 1390 * DRAWS
REQUIRED = 4 * DENOMINATOR // 5


def critical_lambda(scores, cutoff, squared_ratio):
    log_retention = .5 * np.log(squared_ratio)
    positive = scores > 0
    with np.errstate(divide="ignore", invalid="ignore"):
        node_limits = (np.log(cutoff[:, :, None] / scores)
                       / log_retention[:, :, None]) - 1
    return np.where(positive, node_limits, -np.inf).min(axis=1)


def allocation_units(allocations):
    counts = [[weight * 1390 for weight in coefficients(v)] for v in allocations]
    assert all(weight.denominator == 1 for row in counts for weight in row)
    return np.array(counts, dtype=int)


def write(data, output, archive):
    archived = pd.read_csv(archive / "q4_context_mc_indicators.csv")
    previous = pd.read_csv(archive / "q4_context_mc_bounds.csv").set_index(["model", "bound"])
    allocations = vertices()
    units = allocation_units([*allocations, (HALF,) * 3])
    checks, crossings = [], []
    for model, scores, standard, cutoff, squared_ratio in prefix_scores(data):
        limits = critical_lambda(scores, cutoff, squared_ratio)
        clean = (scores >= cutoff[:, :, None]).all(axis=1)
        assert limits.shape == clean.shape == (DRAWS, len(CONTEXTS))
        archive_masks = np.stack((clean, limits >= 1), axis=2).reshape(DRAWS, -1)
        old = pass_indicators(standard, cutoff, squared_ratio)
        np.testing.assert_array_equal(np.column_stack((archive_masks, old)),
                                      archived[indicator_columns(model)].to_numpy())
        clean_counts = clean.sum(axis=0)
        sorted_limits = np.sort(limits, axis=0)
        inside = limits[(limits > 0) & (limits < 2)]
        points = np.unique(np.concatenate((inside, CHECKPOINTS)))
        noisy_counts = np.column_stack([
            DRAWS - np.searchsorted(column, points, side="left") for column in sorted_limits.T
        ])
        masses = clean_counts @ units[:, ::2].T + noisy_counts @ units[:, 1::2].T
        minimum = masses[:, :-1].min(axis=1)
        maximum = masses[:, :-1].max(axis=1)
        assert (np.diff(masses, axis=0) <= 0).all()

        for value in CHECKPOINTS:
            idx = np.searchsorted(points, value)
            counts = {f"{context}_{state}": count for context, a, b in
                      zip(CONTEXTS, clean_counts, noisy_counts[idx])
                      for state, count in (("clean", a), ("noisy", b))}
            checks.append(dict(model=model, lambda_value=value, minimum=minimum[idx]/DENOMINATOR,
                               uniform=masses[idx, -1]/DENOMINATOR, maximum=maximum[idx]/DENOMINATOR,
                               all_pass=minimum[idx] >= REQUIRED, any_pass=maximum[idx] >= REQUIRED,
                               **counts))
        one = np.searchsorted(points, 1.)
        for bound, extrema, arg in (("all", minimum, np.argmin), ("any", maximum, np.argmax)):
            old_bound = "minimum" if bound == "all" else "maximum"
            assert abs(extrema[one] / DENOMINATOR - previous.loc[(model, old_bound), "estimate"]) < 1e-14
            passing = np.flatnonzero(extrema >= REQUIRED)
            if not len(passing):
                status, idx = "infeasible", 0
            else:
                idx = int(passing[-1])
                status = "capped" if points[idx] == 2 else "crossing"
            vertex = int(arg(masses[idx, :-1]))
            shares = {f"f_{c}": str(f) for c, f in zip(CONTEXTS, allocations[vertex])}
            after = None
            if status == "crossing":
                # With no intervening events, the next point's inclusive mass is the right limit.
                after = int(extrema[idx + 1])
                assert after < REQUIRED
            crossings.append(dict(model=model, rule=bound, status=status,
                                  largest_lambda=None if status == "infeasible" else points[idx],
                                  evaluated_lambda=points[idx], share=extrema[idx]/DENOMINATOR,
                                  share_right_limit=None if after is None else after/DENOMINATOR,
                                  vertex=vertex+1, **shares))

    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("checks", checks), ("crossings", crossings)):
        pd.DataFrame(rows).to_csv(output / f"q4_context_lambda_{name}.csv",
                                  index=False, lineterminator="\n")
