"""Compare fixed penalties on call-specific log attenuation exponents."""
import numpy as np
import pandas as pd
from scipy.optimize import least_squares

import physical_attenuation as physical
import q2
from q2_forward import TARGETS, observed_and_support, summarize
from q2_shape_rank import fit_all


PENALTIES = {"pool_0.0025": .0025, "pool_0.01": .01, "pool_0.04": .04}
MODELS = ("shared_g", "separate_g", *PENALTIES)


def pooled_fit(distance, observed, shared, penalty):
    initial = np.r_[shared[:, 0], np.log(shared[:, 1]), shared[:, 2]]
    lower = np.r_[np.zeros(6), np.full(3, .25)]
    upper = np.r_[np.ones(3), np.full(3, np.log(2048)), np.full(3, 8.)]

    def parameters(x):
        return np.column_stack((x[:3], np.exp(x[3:6]), x[6:]))

    def residual(x):
        error = physical.curve(distance, parameters(x)) - observed
        log_exponents = np.log(x[6:])
        return np.r_[error.ravel() / np.sqrt(error.size),
                     np.sqrt(penalty / len(log_exponents)) * (log_exponents - log_exponents.mean())]

    solution = least_squares(residual, initial, bounds=(lower, upper),
                             ftol=1e-11, xtol=1e-11, gtol=1e-11)
    if not solution.success:
        raise RuntimeError(solution.message)
    return parameters(solution.x)


def fit_models(distance, observed):
    endpoints = fit_all(distance, observed)
    return {
        "shared_g": endpoints["shared_g"],
        "separate_g": endpoints["separate_g"],
        **{model: pooled_fit(distance, observed, endpoints["shared_g"], penalty)
           for model, penalty in PENALTIES.items()},
    }


def fit_rows(fits, scope):
    for model, params in fits.items():
        for call, triple in zip(q2.CALLS, params):
            ceiling, scale, exponent = triple
            row = {**scope, "model": model, "lambda": PENALTIES.get(model), "call": call,
                   "ceiling": ceiling, "scale_m": scale, "exponent": exponent}
            if scope["fit"] == "full":
                for threshold in (.50, .70):
                    radius, status = physical.fitted_radius(triple, threshold)
                    row[f"radius_{threshold:.2f}_m"] = radius
                    row[f"status_{threshold:.2f}"] = status
            yield row


def check_archive(archive, holdouts, contrasts):
    keys = ["model", "call", "distance_m"]
    original = pd.read_csv(archive / "q2_forward_holdouts.csv").set_index(keys)
    endpoint = holdouts[holdouts.model.isin(MODELS[:2])].set_index(keys)
    pd.testing.assert_frame_equal(endpoint, original.loc[endpoint.index], check_dtype=False)

    keys = ["call", "target_m", "model", "reference", "metric"]
    original = pd.read_csv(archive / "q2_forward_contrasts.csv").set_index(keys)
    endpoint = contrasts[contrasts.model.eq("separate_g")].set_index(keys)
    pd.testing.assert_frame_equal(endpoint, original.loc[endpoint.index])


def write(data, output, archive):
    observed, _ = observed_and_support(data)
    predictions = np.empty((len(observed), len(MODELS), len(q2.CALLS), len(TARGETS)))
    parameters, holdouts = [], []
    for draw, targets in enumerate(observed):
        for k, distance in enumerate(TARGETS):
            train = q2.KNOTS < distance
            fits = fit_models(q2.KNOTS[train], targets[:, train])
            for m, (model, fitted) in enumerate(fits.items()):
                prediction = physical.curve(np.array([distance]), fitted)[:, 0]
                predictions[draw, m, :, k] = prediction
                if draw == 0:
                    actual = targets[:, q2.KNOTS == distance].ravel()
                    for call, value, pred in zip(q2.CALLS, actual, prediction):
                        holdouts.append({"model": model, "call": call, "distance_m": distance,
                                         "last_training_m": distance / 2, "observed": value,
                                         "predicted": pred, "error": pred - value})
            if draw == 0:
                parameters.extend(fit_rows(fits, {"fit": "forward", "target_m": distance}))
    full = fit_models(q2.KNOTS, observed[0])
    parameters.extend(fit_rows(full, {"fit": "full", "target_m": None}))
    scores, contrasts = summarize(observed, predictions, models=MODELS)
    contrasts = contrasts.loc[contrasts.reference.isin(MODELS[:2])]
    holdouts = pd.DataFrame(holdouts)
    check_archive(archive, holdouts, contrasts)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in (("holdouts", holdouts), ("scores", scores), ("contrasts", contrasts),
                        ("fits", pd.DataFrame(parameters))):
        table.to_csv(output / f"q2_partial_pooling_{name}.csv", index=False, lineterminator="\n")
