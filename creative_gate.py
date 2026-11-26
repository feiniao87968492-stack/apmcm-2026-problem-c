"""Score a fixed smooth fidelity gate against two playback benchmarks."""
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import q2
import q3
from round2 import report_playback_scores, score_frame


def features(frame, contexts):
    full = q3.features(frame, contexts)
    background = full[:, 5:]
    excess = np.column_stack((full[:, 1:3], full[:, 5:-2], full[:, -1]))
    return full, background, excess


def smooth_gate(frame, propagation):
    distance = frame.Distance.to_numpy()
    fidelity = np.empty(len(frame))
    for call, (means, _) in propagation["metric_means_and_draws"].items():
        rows = frame.assigned_call.eq(call).to_numpy()
        knots = q2.fit_knots(means, q2.WEIGHTS["equal"])
        fidelity[rows] = q2.interpolated(distance[rows], knots)
    return fidelity, expit((fidelity - .50) / .05)


def excess_objective(parameters, design, response, background, gate):
    eta = design @ parameters
    excess, complement = expit(eta), expit(-eta)
    capacity = (1 - background) * gate
    p = background + capacity * excess
    one_minus_p = (1 - background) * ((1 - gate) + gate * complement)
    observed = np.where(response, p, one_minus_p)
    derivative = np.where(response, -1, 1) * capacity * excess * complement / observed
    penalty = parameters.copy()
    penalty[0] = 0
    loss = -np.log(observed).sum() + .5 * (penalty @ penalty)
    return loss, design.T @ derivative + penalty


def predict(train_features, train_y, train_natural, train_gate,
            test_features, test_natural, test_gate):
    full_x, background_x, excess_x = train_features
    test_full, test_background, test_excess = test_features
    binary = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000))
    published = binary.fit(full_x, train_y).predict_proba(test_full)[:, 1]
    controls = ~train_natural
    binary.fit(background_x[controls], train_y[controls])
    background_train = binary.predict_proba(background_x[train_natural])[:, 1]
    background_test = binary.predict_proba(test_background)[:, 1]

    scaler = StandardScaler().fit(excess_x[train_natural])
    design = np.column_stack((np.ones(train_natural.sum()), scaler.transform(excess_x[train_natural])))
    test_design = np.column_stack((np.ones(test_natural.sum()), scaler.transform(test_excess[test_natural])))
    result = {"published_binary": published}
    for model, gate_train, gate_test in (
        ("ungated_excess", np.ones(len(background_train)), np.ones(test_natural.sum())),
        ("smooth_gate", train_gate[train_natural], test_gate[test_natural]),
    ):
        fitted = minimize(
            excess_objective, np.zeros(design.shape[1]),
            args=(design, train_y[train_natural], background_train, gate_train),
            method="L-BFGS-B", jac=True, options={"maxiter": 1000, "gtol": 1e-7, "ftol": 1e-12},
        )
        if not fitted.success:
            raise RuntimeError(f"{model} excess fit did not converge: {fitted.message}")
        p = background_test.copy()
        p[test_natural] += (1 - p[test_natural]) * gate_test * expit(test_design @ fitted.x)
        result[model] = p
    return result


def take(features, rows):
    return tuple(matrix[rows] for matrix in features)


def run(data, output, seed, n_boot, propagation):
    frame = q3.load_playbacks(data)
    contexts = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    matrices = features(frame, tuple(contexts.index))
    response = frame["mask"].ne(0).to_numpy()
    natural = frame.Type.eq("call").to_numpy()
    supported = frame.Distance.between(20, 150).to_numpy()
    _, gate = smooth_gate(frame, propagation)
    folds = list(GroupKFold(5).split(frame, groups=frame.expID))
    names = ("published_binary", "ungated_excess", "smooth_gate")
    metrics = ("binary_log_loss", "any_response_brier")
    row_scores = np.full((len(frame), len(metrics), len(names)), np.nan)
    for train, test in folds:
        train = train[supported[train]]
        test = test[supported[test]]
        probabilities = predict(
            take(matrices, train), response[train], natural[train], gate[train],
            take(matrices, test), natural[test], gate[test],
        )
        for i, model in enumerate(names):
            p = probabilities[model]
            row_scores[test, :, i] = np.column_stack((
                -np.log(np.where(response[test], p, 1 - p).clip(1e-12)),
                (p - response[test]) ** 2,
            ))
    for benchmark, position in (("binary", 0), ("ungated", 1)):
        variants = (names[position], names[-1])
        scores = score_frame(frame, folds, row_scores[:, :, [position, 2]], metrics, variants, supported)
        report_playback_scores(scores, metrics, output, f"gate_vs_{benchmark}", seed + 3, n_boot, prefix="creative")

    direct = score_frame(frame, folds, row_scores[:, :, :2], metrics, names[:2], supported)
    report_playback_scores(direct, metrics, output, "q4_ungated", seed + 3, n_boot, prefix="posthoc")

    grid = q3.probability_grid(np.asarray(q3.REPRESENTATIVE), tuple(contexts.index), 8)
    grid_natural = grid.Type.eq("call").to_numpy()
    grid["fidelity"], grid["gate"] = smooth_gate(grid, propagation)
    probabilities = predict(
        take(matrices, supported), response[supported], natural[supported], gate[supported],
        features(grid, tuple(contexts.index)), grid_natural, grid.gate.to_numpy(),
    )
    for model, p in probabilities.items():
        grid[model] = p
    columns = ["fidelity", "gate", *names]
    weighted = grid[columns].mul(grid.Context.map(contexts), axis=0)
    weighted.groupby([grid.Type, grid.assigned_call, grid.Distance], sort=False).sum().reset_index().to_csv(
        output / "creative_gate_representative.csv", index=False,
    )
