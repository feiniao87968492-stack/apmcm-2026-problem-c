"""Compare Q4 allocations under paired response dependence."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import solve

import q3
from q4_fisher import DISTANCES, TARGETS, design_inputs, margins, probability_and_gradient
from strict_playback import joint_table


def pair_cross(design, probabilities, basis, responded, log_odds, weights):
    """Expected cross-arm score covariance from the coupled state distribution."""
    any_p = probabilities[..., responded].sum(axis=-1)
    conditional = np.stack([
        (probabilities * (responded == state))
        / probabilities[..., responded == state].sum(axis=-1, keepdims=True)
        for state in (0, 1)
    ], axis=-2)
    centered = conditional @ basis - (probabilities @ basis)[..., None, :]
    scores = (centered[..., None] * design[..., None, None, :]).reshape(
        len(design), 2, 2, -1,
    )
    states = joint_table(any_p[:, 0], any_p[:, 1], log_odds).reshape(-1, 2, 2)
    np.testing.assert_allclose(states.sum(axis=2)[:, 1], any_p[:, 0], atol=1e-12, rtol=0)
    np.testing.assert_allclose(states.sum(axis=1)[:, 1], any_p[:, 1], atol=1e-12, rtol=0)
    cross = np.einsum("n,nst,nsi,ntj->ij", weights, states, scores[:, 0], scores[:, 1])
    return cross + cross.T


def meats(inputs, log_odds, current_info, cell_info):
    weights, _, design, train, predicted, observed, basis, classes = inputs
    n_contexts = len(weights)
    training = (train.reshape(-1, 2, train.shape[-1]), observed.reshape(-1, 2, len(classes)))
    pair_design = np.moveaxis(design.reshape(2, len(cell_info), n_contexts, -1), 0, 2)
    pair_p = np.moveaxis(predicted.reshape(2, len(cell_info), n_contexts, -1), 0, 2)
    penalty = np.tile(np.r_[0., np.ones(train.shape[1] - 1)], basis.shape[1])
    unpenalized = current_info - np.diag(penalty)
    historical, prospective = [], []
    for eta in log_odds:
        former = pair_cross(*training, basis, classes != 0, eta, np.ones(len(training[0])))
        future = np.stack([
            pair_cross(x, p, basis, classes != 0, eta, weights.to_numpy())
            for x, p in zip(pair_design, pair_p)
        ])
        historical.append(unpenalized + former)
        prospective.append(cell_info + future)
    np.testing.assert_allclose(historical[0], unpenalized, atol=1e-12, rtol=0)
    np.testing.assert_allclose(prospective[0], cell_info, atol=1e-12, rtol=0)
    return np.stack(historical), np.stack(prospective)


def variance(bread, meat, gradients):
    slopes = solve(bread, gradients.T, assume_a="pos").T
    return np.einsum("ij,sjk,ik->si", slopes, meat, slopes)


def greedy(start, bread, updates, meat, pair_meat, gradients, baseline, scenarios):
    counts = start.copy()
    bread = bread + np.einsum("n,nij->ij", counts, updates)
    meat = meat[scenarios] + np.einsum("n,snij->sij", counts, pair_meat[scenarios])
    for _ in range(120 - counts.sum()):
        scores = np.array([
            (variance(bread + update, meat + increment, gradients) / baseline[scenarios]).max()
            for update, increment in zip(updates, np.moveaxis(pair_meat[scenarios], 1, 0))
        ])
        chosen = np.flatnonzero(scores <= scores.min() + 1e-12)[0]
        counts[chosen] += 1
        bread += updates[chosen]
        meat += pair_meat[scenarios, chosen]
    return counts


def run(data, results, output):
    frame = q3.load_playbacks(data)
    inputs = design_inputs(frame)
    p, dp, physical, iso, bread, updates = probability_and_gradient(frame, results, inputs)
    points, gradients = margins(p, dp, physical, iso)
    folds = pd.read_csv(results / "strict_q3_pair_folds.csv")
    dependent = folds.loc[folds.model.eq("shared_odds_ratio"), "log_odds_ratio"]
    lower, upper = dependent.min(), dependent.max()
    log_odds = (0., lower, (lower + upper) / 2, upper)
    meat, increments = meats(inputs, log_odds, bread, updates)
    baseline = variance(bread, meat, gradients)
    cells = [(call, distance) for call in q3.CALLS for distance in DISTANCES]
    focal = {(call, distance) for call, distance, _, _ in TARGETS}
    minimum = np.array([10 * (cell in focal) for cell in cells])
    archived = pd.read_csv(results / "q4_fisher_allocations.csv")
    released = archived.loc[archived.plan.eq("greedy_focal_min")].set_index(["call", "distance_m"])
    fisher = released.loc[cells, "pairs"].to_numpy()
    plans = {"uniform": np.full(len(cells), 10), "fisher_constrained": fisher}
    for name, scenarios in (("midpoint_greedy", [2]), ("worst_case_greedy", list(range(4)))):
        plans[name] = greedy(minimum, bread, updates, meat, increments, gradients, baseline, scenarios)

    def evaluate(counts):
        information = bread + np.einsum("n,nij->ij", counts, updates)
        covariance = meat + np.einsum("n,snij->sij", counts, increments)
        return variance(information, covariance, gradients)

    independent_fisher = (evaluate(fisher) / baseline)[0].max()
    allocations, precision, summary = [], [], []
    for plan, counts in plans.items():
        values = evaluate(counts)
        ratios = values / baseline
        maxima = ratios.max(axis=1)
        for (call, distance), count in zip(cells, counts):
            allocations.append(dict(plan=plan, call=call, distance_m=distance, pairs=count))
        totals = {f"pairs_{d}m": sum(n for (_, distance), n in zip(cells, counts) if distance == d)
                  for d in (20, 150)}
        summary.append(dict(plan=plan, **totals, max_ratio=maxima.max(),
                            independent_cost=maxima[0] - independent_fisher))
        for i, scenario in enumerate(("independent", "fold_min", "fold_midpoint", "fold_max")):
            for j, (call, distance, link, definition) in enumerate(TARGETS):
                precision.append(dict(plan=plan, scenario=scenario, log_odds_ratio=log_odds[i],
                                      call=call, distance_m=distance, link=link, definition=definition,
                                      point_margin=points[j], current_variance=baseline[i, j],
                                      variance=values[i, j], se=np.sqrt(values[i, j]),
                                      relative_variance=ratios[i, j], scenario_max=maxima[i]))
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("allocations", allocations), ("precision", precision), ("summary", summary)):
        pd.DataFrame(rows).to_csv(output / f"q4_paired_planning_{name}.csv", index=False)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--results", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    run(args.data, args.results, args.output)
