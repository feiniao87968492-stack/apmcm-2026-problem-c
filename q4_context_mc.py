"""Audit finite-draw precision of the bounded Q4 context extrema."""
from fractions import Fraction
from itertools import combinations, product

import numpy as np
import pandas as pd

from q4_context_exposure import CONTEXTS, DRAWS, WEIGHTS, allocate, prefix_indicators


LOW, HIGH, HALF = Fraction(3, 10), Fraction(7, 10), Fraction(1, 2)
BOOTSTRAPS, SEED = 10_000, 20261205
ARCHIVE_CONTEXTS = (*CONTEXTS, "standardized_archive_check")
STATES = ("clean", "noisy")


def vertices():
    result = set()
    for i, j in combinations(range(3), 2):
        k = 3 - i - j
        for first, second in product((LOW, HIGH), repeat=2):
            allocation = [None] * 3
            allocation[i], allocation[j] = first, second
            allocation[k] = (HALF - WEIGHTS[i] * first - WEIGHTS[j] * second) / WEIGHTS[k]
            if LOW <= allocation[k] <= HIGH:
                result.add(tuple(allocation))
    assert len(result) == 6
    return sorted(result)


def coefficients(allocation):
    return tuple(value for w, f in zip(WEIGHTS, allocation) for value in (w * (1-f), w * f))


def bootstrap_widths(scores):
    """Compute one half-width per fit using common paired draw indices."""
    rng = np.random.default_rng(SEED)
    observed = scores.mean(axis=0)
    deviations = []
    for _ in range(0, BOOTSTRAPS, 100):
        indices = rng.integers(DRAWS, size=(100, DRAWS))
        centered = scores[indices].mean(axis=1) - observed
        deviations.append(np.abs(centered).max(axis=2))
    return np.quantile(np.concatenate(deviations), .95, axis=0, method="linear")


def summarize(indicators, archive, output):
    """Reconcile archived counts and compute tables from the indexed masks."""
    count_table = pd.read_csv(archive / "q4_context_exposure_counts.csv").set_index(["model", "context"])
    checks = pd.read_csv(archive / "q4_context_exposure_checks.csv").set_index(["model", "f", "rule"])
    allocations = vertices()
    weights = np.array([coefficients(v) for v in allocations], dtype=float)
    scores = {}
    exact_bounds = {}
    for model, masks in indicators.items():
        clean, noisy = masks.sum(axis=0).reshape(-1, 2).T
        old_counts = count_table.loc[model].loc[list(ARCHIVE_CONTEXTS)]
        np.testing.assert_array_equal(clean, old_counts.clean_count)
        np.testing.assert_array_equal(noisy, old_counts.noisy_count)
        assert not (masks[:, 1::2] & ~masks[:, ::2]).any()
        counts = [int(x) for x in masks[:, :6].sum(axis=0)]
        losses = [a - b for a, b in zip(counts[::2], counts[1::2])]

        def exact_score(allocation):
            return sum(c * n for c, n in zip(coefficients(allocation), counts)) / DRAWS

        exact = [exact_score(v) for v in allocations]
        exact_bounds[model] = (min(exact), max(exact))
        uniform = exact_score((HALF,) * 3)
        for rule, bound in zip(("minimum", "maximum"), exact_bounds[model]):
            unrestricted = [x / w for x, w in zip(allocate(HALF, rule, losses), WEIGHTS)]
            endpoint = exact_score(unrestricted)
            assert abs(float(endpoint) - checks.loc[(model, .5, rule), "share"]) < 1e-14
            assert bound == uniform + 2 * (HIGH - HALF) * (endpoint - uniform)

        scores[model] = masks[:, :6] @ weights.T
        np.testing.assert_allclose(scores[model].mean(axis=0), np.array(exact, dtype=float),
                                   atol=1e-13, rtol=0)

    widths = bootstrap_widths(np.stack(list(scores.values()), axis=1))
    vertex_rows, bound_rows = [], []
    for (model, values), width in zip(scores.items(), widths):
        means = values.mean(axis=0)
        covariance = np.cov(values, rowvar=False, ddof=1) / DRAWS
        for i, (allocation, mean) in enumerate(zip(allocations, means)):
            vertex_rows.append(dict(
                model=model, vertex=i+1, **{f"f_{c}": str(f) for c, f in zip(CONTEXTS, allocation)},
                estimate=mean, mc_se=np.sqrt(covariance[i, i]),
                lower_95=mean-width, upper_95=mean+width,
                **{f"mean_cov_v{j+1}": entry for j, entry in enumerate(covariance[i])},
            ))
        lower, upper = exact_bounds[model]
        decision = "all_pass" if float(lower)-width >= .8 else (
            "all_fail" if float(upper)+width < .8 else "unresolved"
        )
        for bound, point in zip(("minimum", "maximum"), (lower, upper)):
            bound_rows.append(dict(model=model, bound=bound, estimate_exact=str(point),
                                   estimate=float(point), lower_95=float(point)-width,
                                   upper_95=float(point)+width, half_width_95=width,
                                   decision_80=decision))
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("vertices", vertex_rows), ("bounds", bound_rows)):
        pd.DataFrame(rows).to_csv(output / f"q4_context_mc_{name}.csv", index=False,
                                  lineterminator="\n")


def indicator_columns(model):
    return [f"{model}_{context}_{state}" for context in ARCHIVE_CONTEXTS for state in STATES]


def write(data, output, archive):
    indicators = {model: np.column_stack((masks.reshape(DRAWS, -1), standardized))
                  for model, masks, standardized in prefix_indicators(data, archive)}
    summarize(indicators, archive, output)
    columns = {"draw": np.arange(DRAWS)}
    for model, masks in indicators.items():
        columns.update(zip(indicator_columns(model), masks.astype(np.uint8).T))
    pd.DataFrame(columns).to_csv(output / "q4_context_mc_indicators.csv", index=False,
                                 lineterminator="\n")
