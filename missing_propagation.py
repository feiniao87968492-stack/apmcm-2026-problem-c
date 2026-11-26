"""Propagate bounded and low-quality completions of missing correlations."""
import numpy as np
import pandas as pd

import physical_attenuation as attenuation
import q2
from q3 import REPRESENTATIVE
from q4 import environment

NOMINAL_COUNT = 300


def completed_means(data, output):
    arrays = np.stack(list(q2.load_tables(data).values()))
    counts = np.isfinite(arrays).sum(axis=2)
    if np.any((counts == 0) | (counts > NOMINAL_COUNT)):
        raise ValueError("Completion analysis requires 1–300 observed correlations per cell")
    observed = np.nansum(arrays, axis=2)
    missing = NOMINAL_COUNT - counts
    means = observed / counts
    lower = (observed - missing) / NOMINAL_COUNT
    upper = (observed + missing) / NOMINAL_COUNT

    cells = pd.MultiIndex.from_product(
        [q2.CALLS, q2.METRICS, q2.KNOTS], names=["call", "representation", "distance_m"]
    ).to_frame(index=False)
    for name, values in (("n_available", counts), ("n_missing", missing),
                         ("available_mean", means), ("lower_mean", lower), ("upper_mean", upper)):
        cells[name] = values.ravel()
    cells.to_csv(output / "missing_q2_cells.csv", index=False)
    return {"available": means, "lower": lower, "upper": upper}, missing


def isotonic_curves(means):
    return np.stack([q2.fit_knots(values, q2.WEIGHTS["equal"]) for values in means])


def radius_rows(model, parameters, **labels):
    crossing = q2.radius if model == "isotonic" else attenuation.fitted_radius
    for threshold in q2.THRESHOLDS:
        estimates = [crossing(row, threshold) for row in parameters]
        for call, (radius, status) in zip(q2.CALLS, estimates):
            yield dict(labels, model=model, threshold=threshold, call=call,
                       radius_m=radius, status=status, rank=1 + sum(r > radius for r, _ in estimates))


def q4_margins(curves, propagation, behavior, date_predictions, output):
    distance = propagation["distance"]
    p, c = behavior["natural"], behavior["control"]
    pd_, cd = date_predictions[:, 0], date_predictions[:, 1]
    cutoff = (propagation["fidelity"][:, 0] * p[:, 0]).mean() / 2
    draw_cutoffs = (propagation["draws"][:, :, 0] * pd_[:, :, 0]).mean(axis=1) / 2
    rows = []
    for loss in (0., .20):
        comparisons = {}
        for completion, knots in curves.items():
            fidelity = np.stack([q2.interpolated(distance, row) for row in knots])
            point, _ = environment(fidelity, p, c, loss, 0)
            draws, _ = environment(fidelity, pd_, cd, loss, 0)
            comparisons[completion] = point - cutoff, draws - draw_cutoffs[:, None, None]

        for i, call in enumerate(q2.CALLS):
            for d in REPRESENTATIVE:
                j = np.searchsorted(distance, d)
                row = {"call": call, "distance_m": d, "coupled_loss": loss, "cutoff": cutoff,
                       "n_draws": len(draw_cutoffs)}
                for completion, (point, samples) in comparisons.items():
                    values = samples[:, i, j]
                    low, high = np.quantile(values, [.025, .975])
                    count = np.count_nonzero(values >= 0)
                    row.update({f"{completion}_margin": point[i, j],
                                f"{completion}_margin_low95": low,
                                f"{completion}_margin_high95": high,
                                f"{completion}_attainment": count / len(values),
                                f"{completion}_passes_80": 5 * count >= 4 * len(values)})
                if row["lower_passes_80"]:
                    row["decision"] = "all_completions_pass"
                elif not row["upper_passes_80"]:
                    row["decision"] = "all_completions_fail"
                else:
                    row["decision"] = "completion_dependent"
                rows.append(row)
    pd.DataFrame(rows).to_csv(output / "missing_q4_attainment.csv", index=False)


def run(data, output, propagation, behavior, date_predictions):
    completions, missing = completed_means(data, output)
    curves = {name: isotonic_curves(means) for name, means in completions.items()}
    rows = []
    for name, knots in curves.items():
        rows.extend(radius_rows("isotonic", knots, completion=name))
    pd.DataFrame(rows).to_csv(output / "missing_q2_radius_bounds.csv", index=False)

    rows = []
    for quality in np.arange(101) / 100:
        means = completions["available"] * (1 - (1 - quality) * missing / NOMINAL_COUNT)
        targets = np.stack([attenuation.equal_means(values) for values in means])
        rows.extend(radius_rows("isotonic", isotonic_curves(means), quality=quality))
        rows.extend(radius_rows("shared_exponent", attenuation.fit(q2.KNOTS, targets, shared=True),
                                quality=quality))
    pd.DataFrame(rows).to_csv(output / "missing_q2_quality_grid.csv", index=False)
    q4_margins(curves, propagation, behavior, date_predictions, output)
    return curves, completions, missing
