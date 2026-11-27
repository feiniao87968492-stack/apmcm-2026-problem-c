"""Validate frequency-informed acoustic fidelity on the existing Q2 folds."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq, least_squares

import physical_attenuation as physical
import q2
from q2_forward import DRAWS, SEED, TARGETS, observed_and_support
from q2_partial_pooling import PENALTIES, pooled_fit
from q2_shape_rank import MODELS as ARCHIVED_SHAPES, fit_all


ABSORPTION = "pool_0.01_absorption"
ABLATION = "pool_0.01"
MODELS = (*ARCHIVED_SHAPES, *PENALTIES, ABSORPTION)
GRID = np.arange(4., 256.5, .5)
THRESHOLDS = {0.40: "Potential", 0.50: "Standard", 0.60: "Reliable", 0.70: "Sensitivity"}
PHYSICAL_INPUTS = dict(temperature_c=20., relative_humidity_percent=70., pressure_kpa=101.325)


def iso9613_absorption(frequency_hz, temperature_c, relative_humidity_percent, pressure_kpa):
    """ISO 9613-1 pure-tone atmospheric attenuation coefficient in dB/m."""
    temperature = temperature_c + 273.15
    temperature_ratio = temperature / 293.15
    pressure_ratio = pressure_kpa / 101.325
    saturation_ratio = 10 ** (-6.8346 * (273.16 / temperature) ** 1.261 + 4.6151)
    molar_humidity = relative_humidity_percent * saturation_ratio / pressure_ratio
    oxygen_relaxation = pressure_ratio * (
        24 + 4.04e4 * molar_humidity * (.02 + molar_humidity) / (.391 + molar_humidity)
    )
    nitrogen_relaxation = pressure_ratio / np.sqrt(temperature_ratio) * (
        9 + 280 * molar_humidity * np.exp(-4.17 * (temperature_ratio ** (-1 / 3) - 1))
    )
    frequency_squared = np.asarray(frequency_hz) ** 2
    classical = 1.84e-11 * np.sqrt(temperature_ratio) / pressure_ratio
    molecular = temperature_ratio ** (-2.5) * (
        .01275 * np.exp(-2239.1 / temperature)
        / (oxygen_relaxation + frequency_squared / oxygen_relaxation)
        + .1068 * np.exp(-3352 / temperature)
        / (nitrogen_relaxation + frequency_squared / nitrogen_relaxation)
    )
    return 8.686 * frequency_squared * (classical + molecular)


def absorption_from_recordings(data):
    path, = Path(data).glob("Data01*.csv")
    recordings = pd.read_csv(path)
    counts = recordings.groupby("CallType").Fpeak.count().reindex(q2.CALLS)
    frequency = recordings.groupby("CallType").Fpeak.median().reindex(q2.CALLS)
    if not (np.isfinite(frequency) & (frequency > 0)).all():
        raise ValueError("Every call type requires a finite positive median peak frequency.")
    alpha = iso9613_absorption(frequency.to_numpy(), **PHYSICAL_INPUTS)
    inputs = pd.DataFrame(dict(call=q2.CALLS, recordings=counts.to_numpy(),
                               median_fpeak_hz=frequency.to_numpy(), alpha_db_per_m=alpha,
                               absorption_256m_db=alpha * 255, **PHYSICAL_INPUTS))
    return alpha, inputs


def absorption_curve(distance, parameters, alpha):
    ceiling, scale, exponent = parameters.T
    relative_noise = ((distance / scale[:, None]) ** exponent[:, None]
                      * 10 ** (alpha[:, None] * (distance - 1) / 10))
    return ceiling[:, None] / np.sqrt(1 + relative_noise)


def fit_absorption(distance, observed, shared, alpha):
    initial = np.r_[shared[:, 0], np.log(shared[:, 1]), shared[:, 2]]
    lower = np.r_[np.zeros(6), np.full(3, .25)]
    upper = np.r_[np.ones(3), np.full(3, np.log(2048)), np.full(3, 8.)]

    def unpack(x):
        return np.column_stack((x[:3], np.exp(x[3:6]), x[6:]))

    def residual(x):
        error = absorption_curve(distance, unpack(x), alpha) - observed
        log_exponents = np.log(x[6:])
        penalty = np.sqrt(PENALTIES[ABLATION] / len(log_exponents))
        return np.r_[error.ravel() / np.sqrt(error.size),
                     penalty * (log_exponents - log_exponents.mean())]

    solution = least_squares(residual, initial, bounds=(lower, upper),
                             ftol=1e-11, xtol=1e-11, gtol=1e-11)
    if not solution.success:
        raise RuntimeError(solution.message)
    return unpack(solution.x)


def fit_models(distance, observed, alpha):
    fits = fit_all(distance, observed)
    initial = fits["shared_g"]
    fits.update({name: pooled_fit(distance, observed, initial, penalty)
                 for name, penalty in PENALTIES.items()})
    fits[ABSORPTION] = fit_absorption(distance, observed, initial, alpha)
    return fits


def evaluate(model, prediction_distances, training_distances, fit, alpha):
    if model == "isotonic":
        return np.stack([np.interp(np.log(prediction_distances),
                                   np.log(training_distances), row) for row in fit])
    if model == ABSORPTION:
        return absorption_curve(prediction_distances, fit, alpha)
    return physical.curve(prediction_distances, fit)


def validation(observed, alpha):
    holdouts, aggregate, comparisons = [], [], []
    designs = (("interior", q2.KNOTS[1:-1]), ("forward", np.array(TARGETS)))
    for design, targets in designs:
        estimates = np.empty((len(observed), len(MODELS), len(q2.CALLS), len(targets)))
        for j, target in enumerate(targets):
            training = q2.KNOTS != target if design == "interior" else q2.KNOTS < target
            training_distances = q2.KNOTS[training]
            selected_fits = []
    for i, draw in enumerate(observed):
                fits = fit_models(training_distances, draw[:, training], alpha)
                for k, model in enumerate(MODELS):
                    estimates[i, k, :, j] = evaluate(
                        model, np.array([target]), training_distances, fits[model], alpha,
                    )[:, 0]

        actual = observed[:, :, np.searchsorted(q2.KNOTS, targets)]
        residual = estimates - actual[:, None]
        for k, model in enumerate(MODELS):
            for c, call in enumerate(q2.CALLS):
                for j, target in enumerate(targets):
                    holdouts.append(dict(
                        design=design, model=model, call=call, distance_m=target,
                        observed=actual[0, c, j], predicted=estimates[0, k, c, j],
                        signed_error=residual[0, k, c, j],
                    ))
        scopes = {"primary": np.arange(len(targets)) if design == "interior" else np.array([1, 2])}
        if design == "forward":
            scopes["64m"] = np.array([0])
        for scope, indices in scopes.items():
            errors = residual[..., indices]
            for c, call in enumerate((*q2.CALLS, "pooled")):
                selected = errors[:, :, c:c+1] if call != "pooled" else errors
                rmse = np.sqrt((selected**2).mean(axis=(2, 3)))
                signed_error = selected.mean(axis=(2, 3))
                for name, values in (("rmse", rmse), ("signed_error", signed_error)):
                    for k, model in enumerate(MODELS):
                        low, high = np.quantile(values[1:, k], [.025, .975])
                        aggregate.append(dict(design=design, scope=scope, call=call,
                                              model=model, metric=name, estimate=values[0, k],
                                              low95=low, high95=high))
                for k, model in enumerate(MODELS[1:], 1):
                    references = (0, MODELS.index(ABLATION)) if model == ABSORPTION else (0,)
                    for reference in references:
                        difference = rmse[:, k] - rmse[:, reference]
                        low, high = np.quantile(difference[1:], [.025, .975])
                        comparisons.append(dict(design=design, scope=scope, call=call, model=model,
                                                reference=MODELS[reference], difference=difference[0],
                                                low95=low, high95=high))
    return pd.DataFrame(holdouts), pd.DataFrame(aggregate), pd.DataFrame(comparisons)


def select_production(scores, comparisons):
    pooled = comparisons.query("scope == 'primary' and call == 'pooled'")
    versus_iso = pooled.query("reference == 'isotonic'").pivot(
        index="model", columns="design", values="high95"
    )
    qualifies = (versus_iso < 0).all(axis=1)
    absorption_gain = pooled.query(
        "design == 'forward' and model == @ABSORPTION and reference == @ABLATION"
    ).high95.item()
    qualifies.loc[ABSORPTION] &= absorption_gain < 0
    rows = scores.query("scope == 'primary' and call == 'pooled' and metric == 'rmse'")
    rmse = rows.pivot(index="model", columns="design", values="estimate").reindex(MODELS)
    rmse["eligible_replacement"] = qualifies.reindex(MODELS, fill_value=False)
    eligible = [model for model in MODELS if rmse.loc[model, "eligible_replacement"]]
    selected = min(eligible, key=lambda model: tuple(rmse.loc[model, ["interior", "forward"]])
                   ) if eligible else "isotonic"
    rmse["selected"] = rmse.index == selected
    return selected, rmse.reset_index().rename_axis(None, axis=1)


def crossing(model, fit, call_index, threshold, curve, alpha):
    if curve[0] < threshold:
        return GRID[0], "below_support"
    if curve[-1] >= threshold:
        return GRID[-1], "above_support"
    if model == "isotonic":
        return q2.radius(fit[call_index], threshold)
    distance = brentq(
        lambda d: evaluate(model, np.array([d]), q2.KNOTS, fit, alpha)[call_index, 0]
        - threshold, GRID[0], GRID[-1],
    )
    return distance, "crossing"


def full_curves(observed, alpha, selected):
    predictions = np.empty((len(observed), len(MODELS), len(q2.CALLS), len(GRID)))
    point_fits = fit_models(q2.KNOTS, observed[0], alpha)
    selected_fits = []
    for i, draw in enumerate(observed):
        fits = point_fits if i == 0 else fit_models(q2.KNOTS, draw, alpha)
        if i:
            selected_fits.append(fits[selected])
        for j, model in enumerate(MODELS):
            predictions[i, j] = evaluate(model, GRID, q2.KNOTS, fits[model], alpha)
    low, high = np.quantile(predictions[1:], [.025, .975], axis=0)
    empirical = np.full((len(q2.CALLS), len(GRID)), np.nan)
    empirical[:, np.searchsorted(GRID, q2.KNOTS)] = observed[0]
    curves, radii = [], []
    for j, model in enumerate(MODELS):
        for k, call in enumerate(q2.CALLS):
            curves.append(pd.DataFrame(dict(
                model=model, call=call, distance_m=GRID, fidelity=predictions[0, j, k],
                lower95=low[j, k], upper95=high[j, k], empirical_equal_weight=empirical[k],
                selected=model == selected,
            )))
        for threshold in THRESHOLDS if model == selected else (.50, .70):
            for k, call in enumerate(q2.CALLS):
                distance, status = crossing(model, point_fits[model], k, threshold,
                                            predictions[0, j, k], alpha)
                row = dict(model=model, call=call, threshold=threshold, distance_m=distance,
                           status=status, selected=model == selected)
                if model == selected:
                    distances, statuses = zip(*[
                        crossing(model, fit, k, threshold, curve, alpha)
                        for fit, curve in zip(selected_fits, predictions[1:, j, k])
                    ])
                    lower, upper = np.quantile(distances, [.025, .975])
                    row.update(lower95_m=lower, upper95_m=upper, draws=len(distances),
                               draws_below_support=statuses.count("below_support"),
                               draws_above_support=statuses.count("above_support"))
                radii.append(row)
    return pd.concat(curves, ignore_index=True), pd.DataFrame(radii)


def plot_propagation(output, curves, selected):
    import matplotlib.pyplot as plt

    table = curves[curves.selected].drop(columns="selected")
    labels = ("Flat", "Modulated", "Two-voice")
    colors = ("#0072B2", "#D55E00", "#009E73")
    with plt.rc_context({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "legend.frameon": False, "font.family": "DejaVu Sans"}):
        fig, ax = plt.subplots(figsize=(6.25, 3.65), layout="constrained")
        for call, color, label, style in zip(q2.CALLS, colors, labels, ("-", "--", "-.")):
            part = table.loc[table.call.eq(call)]
            ax.fill_between(part.distance_m, part.lower95, part.upper95, color=color,
                            alpha=.16, linewidth=0)
            ax.plot(part.distance_m, part.fidelity, color=color, linestyle=style, label=label,
                    linewidth=1.9)
            ax.scatter(part.distance_m, part.empirical_equal_weight, color=color, s=14, zorder=3)
        for threshold, label in THRESHOLDS.items():
            ax.axhline(threshold, color="#787878", linestyle="--" if threshold == .70 else ":",
                       linewidth=.8)
            ax.text(.01, threshold+.011, f"{label} {threshold:.2f}", color="#424242",
                    transform=ax.get_yaxis_transform(), fontsize=7,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": .4})
        ax.set(xscale="log", xlim=(3.7, 278), ylim=(0, 1.04),
               xlabel="Propagation distance (m)", ylabel="Acoustic fidelity")
        ax.set_xticks(q2.KNOTS, [f"{d:g}" for d in q2.KNOTS])
        ax.minorticks_off()
        ax.legend(loc="upper right")
        fig.savefig(output / "core_q2_propagation.png", dpi=300)
        plt.close(fig)
    table.to_csv(output / "core_q2_propagation.csv", index=False, lineterminator="\n")
    metadata = dict(
        inputs=["Data01*.csv", *[f"Data{n:02d}*.csv" for n in range(3, 12)]],
        distance_unit="m", selected_model=selected, thresholds=THRESHOLDS,
        marks="Points are empirical equal-weight correlations. Lines use the production fit.",
        uncertainty=q2.BOOTSTRAP_NOTE, interval="95% pointwise row-resampling bands",
        seed=SEED, bootstrap_draws=DRAWS, source_data="core_q2_propagation.csv",
    )
    (output / "core_q2_propagation.meta.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8", newline="\n",
    )


def run(data, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    alpha, inputs = absorption_from_recordings(data)
    observed, support = observed_and_support(data)
    holdouts, scores, comparisons = validation(observed, alpha)
    selected, decision = select_production(scores, comparisons)
    curves, radii = full_curves(observed, alpha, selected)
    for name, table in (("absorption", inputs), ("support", pd.DataFrame(support)),
                        ("holdouts", holdouts), ("scores", scores), ("comparisons", comparisons),
                        ("decision", decision), ("curves", curves), ("radii", radii)):
        table.to_csv(output / f"core_q2_{name}.csv", index=False, lineterminator="\n")
    plot_propagation(output, curves, selected)
    return selected
