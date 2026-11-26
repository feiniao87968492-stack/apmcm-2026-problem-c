"""Distance decay, acoustic thresholds, and propagation uncertainty for Q2."""
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy.optimize import isotonic_regression

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CALLS = ("flat", "mod", "tv")
METRICS = ("spectrogram", "amplitude_spectrum", "envelope")
KNOTS = np.array([4, 8, 16, 32, 64, 128, 256], dtype=float)
THRESHOLDS = (0.4, 0.5, 0.6, 0.7)
WEIGHTS = {
    "equal": (1 / 3, 1 / 3, 1 / 3),
    "frequency_first": (0.45, 0.45, 0.10),
    "envelope_first": (0.25, 0.25, 0.50),
}
BOOTSTRAP_NOTE = (
    "Pointwise percentiles conditional on wide-row resampling. "
    "The original files lack independent experimental identifiers."
)


def load_tables(data):
    tables = {}
    for call_index, call in enumerate(CALLS):
        arrays = []
        for metric_index in range(len(METRICS)):
            number = 3 + metric_index * len(CALLS) + call_index
            files = list(data.glob(f"Data{number:02d}*.csv"))
            if len(files) != 1:
                raise ValueError(f"Expected one Data{number:02d} CSV in {data}")
            frame = pd.read_csv(files[0])
            columns = [f"{d:g}m" for d in KNOTS]
            if list(frame.columns) != columns:
                raise ValueError(f"Unexpected propagation distances in {files[0].name}")
            values = frame.to_numpy(dtype=float)
            finite = values[np.isfinite(values)]
            if not finite.size or np.any(np.abs(finite) > 1):
                raise ValueError(f"Invalid correlations in {files[0].name}")
            arrays.append(values)
        tables[call] = np.stack(arrays)
    return tables


def fit_knots(metric_means, weights, monotone=True):
    pooled = np.clip(np.asarray(weights) @ metric_means, 0.0, 1.0)
    if monotone:
        return isotonic_regression(pooled, increasing=False).x
    return pooled


def radius(knots, threshold):
    """Return the final supported distance above the threshold and its status."""
    indices = np.flatnonzero(knots >= threshold)
    if not indices.size:
        return KNOTS[0], "below_support"
    last = indices[-1]
    if last == len(KNOTS) - 1:
        return KNOTS[-1], "above_support"
    fraction = (threshold - knots[last]) / (knots[last + 1] - knots[last])
    return float(KNOTS[last] * (KNOTS[last + 1] / KNOTS[last]) ** fraction), "crossing"


def interpolated(grid, knots):
    return np.interp(np.log(grid), np.log(KNOTS), knots)


def bootstrap_means(arrays, n_boot, rng, aligned=False):
    if aligned and not np.all(np.isnan(arrays) == np.isnan(arrays[:1])):
        raise ValueError("Aligned resampling requires matching missingness masks")
    n_metrics, n_rows, n_distances = arrays.shape
    draws = np.empty((n_boot, n_metrics, n_distances))
    for draw in range(n_boot):
        indices = rng.integers(n_rows, size=(1 if aligned else n_metrics, n_rows))
        samples = arrays[np.arange(n_metrics)[:, None], indices, :]
        counts = np.isfinite(samples).sum(axis=1)
        if np.any(counts == 0):
            raise ValueError("Bootstrap draw lacks observations at a propagation distance")
        draws[draw] = np.nansum(samples, axis=1) / counts
    return draws


def plot_propagation(output, curve, seed, n_boot):
    palette = {"flat": "#0072B2", "mod": "#D55E00", "tv": "#009E73"}
    names = {"flat": "Flat", "mod": "Modulated", "tv": "Two-voice"}
    styles = {"flat": "-", "mod": "--", "tv": "-."}
    with plt.rc_context({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "legend.frameon": False, "font.family": "sans-serif",
                         "font.sans-serif": ["DejaVu Sans"], "pdf.fonttype": 42,
                         "svg.fonttype": "none"}):
        fig, ax = plt.subplots(figsize=(6.25, 3.65), layout="constrained")
        for call in CALLS:
            part = curve[curve["call"] == call]
            ax.fill_between(part.distance_m, part.lower95, part.upper95,
                            color=palette[call], alpha=0.14, linewidth=0)
            ax.plot(part.distance_m, part.fidelity, color=palette[call],
                    linestyle=styles[call], label=names[call], linewidth=1.9)
            observed = part[part.distance_m.isin(KNOTS)]
            ax.scatter(observed.distance_m, observed.empirical_equal_weight,
                       color=palette[call], s=14, zorder=3)
        for cutoff in THRESHOLDS[:3]:
            ax.axhline(cutoff, color="#7A7A7A", linestyle=":", linewidth=0.7, zorder=0)
        ax.set(xscale="log", xlim=(3.7, 278), ylim=(0, 1.04),
               xlabel="Propagation distance (m)", ylabel="Acoustic fidelity")
        ax.set_xticks(KNOTS, [f"{d:g}" for d in KNOTS])
        ax.minorticks_off()
        ax.legend(loc="upper right", ncol=1)
        fig.savefig(output / "q2_propagation.png", dpi=300)
        plt.close(fig)

    curve.to_csv(output / "q2_propagation.csv", index=False)
    metadata = {
        "inputs": [f"Data{number:02d}*.csv" for number in range(3, 12)],
        "distance_unit": "m",
        "marks": "Points are empirical equal-weight means. Lines are isotonic curves.",
        "uncertainty": BOOTSTRAP_NOTE,
        "interval": "95% pointwise percentile band",
        "horizontal_reference_thresholds": list(THRESHOLDS[:3]),
        "seed": seed,
        "bootstrap_draws": n_boot,
        "source_data": "q2_propagation.csv",
    }
    (output / "q2_propagation.meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


def run(data: Path, output: Path, seed: int, n_boot: int) -> dict:
    """Write Q2 tables and figure and supply common-support curves for Q4."""
    if n_boot < 1:
        raise ValueError("Q2 requires at least one bootstrap draw")
    output.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    tables = load_tables(data)
    shared = np.arange(20.0, 150.5, 0.5)
    dense = np.unique(np.r_[np.arange(4.0, 256.5, 0.5), KNOTS])
    shared_draws = np.empty((n_boot, len(CALLS), shared.size))
    shared_fidelity = np.empty((len(CALLS), shared.size))
    alternate_fidelity = {key: np.empty_like(shared_fidelity) for key in WEIGHTS if key != "equal"}
    metric_rows, curves, radii, validation = [], [], [], []
    for call_index, call in enumerate(CALLS):
        arrays = tables[call]
        counts = np.isfinite(arrays).sum(axis=1)
        means = np.nanmean(arrays, axis=1)
        for metric_index, metric in enumerate(METRICS):
            for dist_index, distance in enumerate(KNOTS):
                metric_rows.append({
                    "call": call, "metric": metric, "distance_m": distance,
                    "n_available": int(counts[metric_index, dist_index]),
                    "mean_correlation": means[metric_index, dist_index],
                    "sd_correlation": np.nanstd(arrays[metric_index, :, dist_index], ddof=1),
                })

        mean_draws = {"independent_metric_rows": bootstrap_means(arrays, n_boot, rng)}
        if np.all(np.isnan(arrays) == np.isnan(arrays[:1])):
            mean_draws["aligned_metric_rows_sensitivity"] = bootstrap_means(
                arrays, n_boot, rng, aligned=True
            )
        fits = {key: fit_knots(means, weights) for key, weights in WEIGHTS.items()}
        fits["equal_unconstrained"] = fit_knots(means, WEIGHTS["equal"], monotone=False)
        empirical = fits["equal_unconstrained"]
        primary_draws = None

        for fit_name, knots in fits.items():
            weights = WEIGHTS["equal" if fit_name == "equal_unconstrained" else fit_name]
            for scheme, mean_draw in mean_draws.items():
                draw_knots = np.stack([
                    fit_knots(draw, weights, monotone=fit_name != "equal_unconstrained")
                    for draw in mean_draw
                ])
                if fit_name == "equal" and scheme == "independent_metric_rows":
                    primary_draws = draw_knots
                for threshold in THRESHOLDS:
                    estimate, status = radius(knots, threshold)
                    intervals, statuses = zip(*(radius(draw, threshold) for draw in draw_knots))
                    lower, upper = np.quantile(intervals, (0.025, 0.975))
                    radii.append({
                        "call": call, "fit": fit_name, "resampling": scheme,
                        "threshold": threshold, "radius_m": estimate, "status": status,
                        "lower95_m": lower, "upper95_m": upper,
                        "fraction_below_support": statuses.count("below_support") / n_boot,
                        "fraction_above_support": statuses.count("above_support") / n_boot,
                    })

        if primary_draws is None:
            raise RuntimeError("Missing primary propagation bootstrap")
        primary = fits["equal"]
        empirical_dense = pd.Series(empirical, index=KNOTS).reindex(dense).to_numpy()
        curve_draws = np.stack([interpolated(dense, draw) for draw in primary_draws])
        lower, upper = np.quantile(curve_draws, (0.025, 0.975), axis=0)
        curves.append(pd.DataFrame({
            "call": call, "distance_m": dense, "fidelity": interpolated(dense, primary),
            "lower95": lower, "upper95": upper, "empirical_equal_weight": empirical_dense,
        }))
        shared_fidelity[call_index] = interpolated(shared, primary)
        shared_draws[:, call_index] = np.stack([interpolated(shared, draw) for draw in primary_draws])
        for key, values in alternate_fidelity.items():
            values[call_index] = interpolated(shared, fits[key])
        validation.append({
            "call": call, "raw_increasing_steps": int(np.count_nonzero(np.diff(empirical) > 0)),
            "max_isotonic_adjustment": float(np.max(np.abs(primary - empirical))),
            "aligned_missingness": "aligned_metric_rows_sensitivity" in mean_draws,
        })

    if np.any(np.diff(shared_fidelity, axis=-1) > 1e-12) or np.any(np.diff(shared_draws, axis=-1) > 1e-12):
        raise RuntimeError("Primary propagation curves must be nonincreasing")
    pd.DataFrame(metric_rows).to_csv(output / "q2_metric_summary.csv", index=False)
    pd.DataFrame(radii).to_csv(output / "q2_radii.csv", index=False)
    pd.DataFrame(validation).to_csv(output / "q2_fit_checks.csv", index=False)
    plot_propagation(output, pd.concat(curves, ignore_index=True), seed, n_boot)
    return {
        "distance": shared, "calls": CALLS, "fidelity": shared_fidelity,
        "draws": shared_draws, "alternate_fidelity": alternate_fidelity,
    }
