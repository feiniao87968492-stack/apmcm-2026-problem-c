"""Plan same-distance playback pairs for three Q4 margin gradients."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import helmert, solve
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import noise_scenarios
import q3

DISTANCES = (20, 50, 100, 150)
TARGETS = (("tv", 150, "clean", "net_own"),
           ("tv", 100, "coupled", "net_own"),
           ("mod", 100, "clean", "gross"))


def fisher(weights, design, probabilities, contrasts):
    projected = probabilities @ contrasts
    covariance = (np.einsum("nk,ki,kj->nij", probabilities, contrasts, contrasts)
                  - np.einsum("ni,nj->nij", projected, projected))
    info = np.einsum("n,nij,na,nb->iajb", weights, covariance, design, design)
    size = contrasts.shape[1] * design.shape[1]
    return info.reshape(size, size)


def probability_and_gradient(frame, results):
    weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    contexts = tuple(weights.index)
    grid = q3.probability_grid(np.array(DISTANCES), contexts, 8)
    observed = q3.features(frame, contexts)
    scaler = StandardScaler().fit(observed)
    train = scaler.transform(observed)
    model = LogisticRegression(C=1, max_iter=1000).fit(train, frame["mask"])
    target = scaler.transform(q3.features(grid, contexts))
    train_p, target_p = model.predict_proba(train), model.predict_proba(target)
    train_design = np.column_stack((np.ones(len(train)), train))
    design = np.column_stack((np.ones(len(target)), target))
    class_basis = helmert(len(model.classes_), full=False).T
    zero = np.flatnonzero(model.classes_ == 0).item()
    # d(1-P0)/d(logits) projected into sum-zero class coordinates.
    class_gradient = target_p[:, zero, None] * (target_p @ class_basis - class_basis[zero])
    gradient = (class_gradient[:, :, None] * design[:, None, :]).reshape(len(grid), -1)
    shape = (len(q3.STIMULI), len(q3.CALLS), len(DISTANCES), len(contexts))
    mixed_p = (1 - target_p[:, zero]).reshape(shape) @ weights.to_numpy()
    mixed_gradient = np.einsum("scdjk,j->scdk", gradient.reshape(*shape, -1), weights)
    penalty = np.tile(np.r_[0., np.ones(train.shape[1])], class_basis.shape[1])
    current = fisher(np.ones(len(frame)), train_design, train_p, class_basis) + np.diag(penalty)

    cell_info = []
    for call in q3.CALLS:
        for distance in DISTANCES:
            selected = grid.assigned_call.eq(call) & grid.Distance.eq(distance)
            cell_info.append(fisher(np.tile(weights.to_numpy(), len(q3.STIMULI)),
                                    design[selected], target_p[selected], class_basis))

    params = pd.read_csv(results / "physical_q2_parameters.csv").query("model == 'shared_g'")
    params = params.set_index("call").loc[list(q3.CALLS), ["ceiling", "scale_m", "exponent"]]
    physical = noise_scenarios.fidelity(np.array(DISTANCES), params.to_numpy(), 0)
    iso = pd.read_csv(results / "q2_propagation.csv").query("distance_m == 20").set_index("call")
    reference = iso.loc[list(q3.CALLS), "fidelity"].to_numpy()
    return mixed_p, mixed_gradient, physical, reference, current, np.stack(cell_info)


def margins(p, gradient, physical, reference):
    net, net_gradient = p[0] - p[1], gradient[0] - gradient[1]
    points, gradients = [], []
    for call, distance, link, definition in TARGETS:
        i, j = q3.CALLS.index(call), DISTANCES.index(distance)
        if definition == "gross":
            values, slopes = p[0], gradient[0]
        else:
            values, slopes = net, net_gradient
        cutoff = (reference * values[:, 0]).mean() / 2
        cutoff_gradient = (reference @ slopes[:, 0]) / (2 * len(q3.CALLS))
        retention = 1.
        if link == "coupled":
            retention = .8 * (.8 if net[i, j] > 0 else 1.)
        factor = physical[i, j] * retention
        points.append(factor * values[i, j] - cutoff)
        gradients.append(factor * slopes[i, j] - cutoff_gradient)
    return np.asarray(points), np.stack(gradients)


def variances(info, gradients):
    return np.einsum("ij,ji->i", gradients, solve(info, gradients.T, assume_a="pos"))


def greedy(start, current, information, gradients, baseline):
    counts = start.copy()
    info = current + np.einsum("i,ijk->jk", counts, information)
    for _ in range(120 - counts.sum()):
        scores = [np.max(variances(info + increment, gradients) / baseline)
                  for increment in information]
        chosen = np.flatnonzero(np.asarray(scores) <= np.min(scores) + 1e-12)[0]
        counts[chosen] += 1
        info += information[chosen]
    return counts


def run(data, results, output):
    frame = q3.load_playbacks(data)
    p, dp, physical, iso, current, increments = probability_and_gradient(frame, results)
    points, gradients = margins(p, dp, physical, iso)
    released = pd.read_csv(results / "control_subtraction_points.csv").set_index(
        ["call", "distance_m", "link", "definition"],
    )
    np.testing.assert_allclose(points, released.loc[list(TARGETS), "margin"], atol=1e-12, rtol=0)
    base = variances(current, gradients)
    cells = [(call, distance) for call in q3.CALLS for distance in DISTANCES]
    focal = np.array([(call, distance) in {(c, d) for c, d, _, _ in TARGETS}
                      for call, distance in cells])
    empty = np.zeros(len(cells), dtype=int)
    plans = {
        "current": empty,
        "uniform": np.full(len(cells), 10),
        "focal_only": 40 * focal,
        "greedy": greedy(empty, current, increments, gradients, base),
        "greedy_focal_min": greedy(10 * focal, current, increments, gradients, base),
    }

    def plan_variance(counts):
        return variances(current + np.einsum("i,ijk->jk", counts, increments), gradients)

    uniform_se = np.sqrt(plan_variance(plans["uniform"]))
    allocations, precision = [], []
    for name, counts in plans.items():
        variance = plan_variance(counts)
        deviations = np.sqrt(variance)
        allocations.extend(dict(plan=name, call=call, distance_m=distance, focal=is_focal,
                                pairs=count)
                           for (call, distance), count, is_focal in zip(cells, counts, focal))
        for (call, distance, link, definition), point, value, se, start, uniform in zip(
                TARGETS, points, variance, deviations, base, uniform_se):
            precision.append(dict(plan=name, call=call, distance_m=distance, link=link,
                                  definition=definition, point_margin=point, variance=value,
                                  relative_variance=value/start, se=se,
                                  uniform_se_reduction=1-se/uniform))
    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(allocations).to_csv(output / "q4_fisher_allocations.csv", index=False)
    pd.DataFrame(precision).to_csv(output / "q4_fisher_precision.csv", index=False)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Contest attachment CSV directory")
    parser.add_argument("--results", type=Path, default=Path("results"), help="Released Q2 and Q4 tables")
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    run(args.data, args.results, args.output)
