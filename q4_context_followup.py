"""Independent full-fit simulation of the bounded Q4 context extrema."""
from fractions import Fraction

import numpy as np
import pandas as pd

from q4_context_exposure import CONTEXTS, DRAWS, prefix_indicators
from q4_context_mc import BOOTSTRAPS, coefficients, indicator_columns, vertices


BLOCKS = 8
ACOUSTIC_SEED = 20261300
PLAYBACK_SEED = 20261400
BOOTSTRAP_SEED = 20261500
BITS = [f"{context}_{state}" for context in CONTEXTS for state in ("clean", "noisy")]
BLOCK_COLUMNS = [f"block_{b}" for b in range(BLOCKS)]


def collect(data):
    rows = []
    for block in range(BLOCKS):
        [(model, states, _)] = prefix_indicators(
            data, acoustic_seed=ACOUSTIC_SEED + block, date_seed=PLAYBACK_SEED + block,
            models=("full",),
        )
        assert model == "full"
        assert states.shape == (DRAWS, len(CONTEXTS), 2)
        assert not (states[:, :, 1] & ~states[:, :, 0]).any()
        bits, counts = np.unique(states.reshape(DRAWS, -1).astype(np.uint8), axis=0,
                                 return_counts=True)
        rows.append(pd.DataFrame(bits, columns=BITS).assign(block=block, count=counts))
        print(f"Completed block {block + 1}/{BLOCKS}", flush=True)
    profiles = pd.concat(rows).pivot(index=BITS, columns="block", values="count")
    profiles = profiles.fillna(0).astype(int).sort_index()
    profiles.columns = BLOCK_COLUMNS
    return profiles.assign(count=profiles.sum(axis=1)).reset_index()


def summarize(profiles, archive, output):
    allocations = vertices()
    weights = np.array([coefficients(v) for v in allocations])
    bits = profiles[BITS].to_numpy(dtype=int)
    counts = profiles["count"].to_numpy()
    total = DRAWS * BLOCKS
    assert np.all(profiles[BLOCK_COLUMNS].sum(axis=0) == DRAWS)
    np.testing.assert_array_equal(counts, profiles[BLOCK_COLUMNS].sum(axis=1))
    scores = bits @ weights.astype(float).T
    marginal = counts @ bits
    exact = [sum(w * int(n) for w, n in zip(row, marginal)) / total for row in weights]
    means = np.array(exact, dtype=float)
    centered = scores - means
    covariance = (centered.T * counts) @ centered / ((total - 1) * total)
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    resamples = rng.multinomial(total, counts / total, size=BOOTSTRAPS)
    deviations = (resamples - counts) @ scores / total
    width = np.quantile(np.abs(deviations).max(axis=1), .95, method="linear")

    old_vertices = (pd.read_csv(archive / "q4_context_mc_vertices.csv")
                    .query("model == 'full'").sort_values("vertex"))
    old_bounds = (pd.read_csv(archive / "q4_context_mc_bounds.csv")
                  .query("model == 'full'").set_index("bound"))
    old_draws = pd.read_csv(archive / "q4_context_mc_indicators.csv")
    old_bits = old_draws[indicator_columns("full")[:len(BITS)]].to_numpy()
    np.testing.assert_allclose((old_bits @ weights.astype(float).T).mean(axis=0),
                               old_vertices.estimate, rtol=0, atol=1e-13)
    for i, context in enumerate(CONTEXTS):
        assert list(map(Fraction, old_vertices[f"f_{context}"])) == [v[i] for v in allocations]
    rows = [
        dict(vertex=i+1, **{f"f_{c}": str(f) for c, f in zip(CONTEXTS, allocation)},
             estimate_exact=str(exact[i]), estimate=means[i], mc_se=np.sqrt(covariance[i, i]),
             lower_95=means[i]-width, upper_95=means[i]+width,
             **{f"mean_cov_v{j+1}": value for j, value in enumerate(covariance[i])})
        for i, allocation in enumerate(allocations)
    ]
    low, high = int(means.argmin()), int(means.argmax())
    decision = "all_pass" if means[low]-width >= .8 else (
        "all_pass_fails" if means[low]+width < .8 else "unresolved"
    )
    bounds = []
    for bound, index in (("minimum", low), ("maximum", high)):
        old = old_bounds.loc[bound]
        old_index = old_vertices.estimate.idxmin() if bound == "minimum" else old_vertices.estimate.idxmax()
        bounds.append(dict(bound=bound, vertex=index+1, estimate=means[index],
                           lower_95=means[index]-width, upper_95=means[index]+width,
                           half_width_95=width, decision_80=decision,
                           archive_vertex=old_vertices.loc[old_index, "vertex"],
                           archive_estimate=old.estimate, archive_lower_95=old.lower_95,
                           archive_upper_95=old.upper_95, archive_half_width_95=old.half_width_95,
                           archive_decision_80=old.decision_80))
    pd.DataFrame(rows).to_csv(output / "q4_context_followup_vertices.csv", index=False,
                               lineterminator="\n")
    pd.DataFrame(bounds).to_csv(output / "q4_context_followup_bounds.csv", index=False,
                                 lineterminator="\n")


def write(data, output, archive):
    profiles = collect(data)
    output.mkdir(parents=True, exist_ok=True)
    profiles.to_csv(output / "q4_context_followup_profiles.csv", index=False, lineterminator="\n")
    summarize(profiles, archive, output)
