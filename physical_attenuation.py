"""Compare attenuation fits and hypothetical acquisition batches."""
import numpy as np
import pandas as pd
from scipy.optimize import least_squares, isotonic_regression

import q2
from q3 import REPRESENTATIVE
from q4 import environment


def curve(distance, parameters):
    ceiling, scale, exponent = np.asarray(parameters).T
    return ceiling[:, None] / np.sqrt(1 + (distance / scale[:, None]) ** exponent[:, None])


def fit(distance, observed, shared):
    def parameters(x):
        exponent = x[6] if shared else 2.
        return np.column_stack((x[:3], np.exp(x[3:6]), np.full(3, exponent)))

    def residual(x):
        return (curve(distance, parameters(x)) - observed).ravel()

    initial = [.9] * 3 + [np.log(100)] * 3
    lower = [0.] * 6
    upper = [1.] * 3 + [np.log(2048)] * 3
    if shared:
        initial.append(2.)
        lower.append(.25)
        upper.append(8.)
    solution = least_squares(residual, initial, bounds=(lower, upper), ftol=1e-11, xtol=1e-11, gtol=1e-11)
    if not solution.success:
        raise RuntimeError(solution.message)
    return parameters(solution.x)


def equal_means(metric_means):
    return np.clip(np.asarray(q2.WEIGHTS["equal"]) @ metric_means, 0, 1)


def validation(targets, output):
    records = []
    for i in range(1, len(q2.KNOTS) - 1):
        keep = np.arange(len(q2.KNOTS)) != i
        train, observed = q2.KNOTS[keep], targets[:, keep]
        distance = q2.KNOTS[i:i + 1]
        predictions = {
            "isotonic": [np.interp(np.log(distance[0]), np.log(train),
                                   isotonic_regression(row, increasing=False).x) for row in observed],
            "fixed_g": curve(distance, fit(train, observed, False))[:, 0],
            "shared_g": curve(distance, fit(train, observed, True))[:, 0],
        }
        for model, result in predictions.items():
            for j, call in enumerate(q2.CALLS):
                records.append({"model": model, "call": call, "distance_m": distance[0],
                                "observed": targets[j, i], "predicted": result[j],
                                "error": result[j] - targets[j, i]})
    folds = pd.DataFrame(records)
    folds.to_csv(output / "physical_q2_holdout.csv", index=False)
    all_calls = pd.concat([folds, folds.assign(call="pooled")])
    summary = all_calls.groupby(["model", "call"]).error.agg(
        rmse=lambda x: np.sqrt((x**2).mean()), mae=lambda x: x.abs().mean(),
    ).reset_index()
    scores = summary.pivot(index="model", columns="call", values="rmse")
    selected = min(("fixed_g", "shared_g"), key=lambda name: scores.loc[name, "pooled"])
    adopt = (scores.loc[selected, "pooled"] <= .95 * scores.loc["isotonic", "pooled"]
             and (scores.loc[selected, list(q2.CALLS)] <= scores.loc["isotonic", list(q2.CALLS)]).all())
    summary["selected_physical"] = summary.model.eq(selected)
    summary["adopt_as_primary"] = summary.model.eq(selected if adopt else "isotonic")
    summary.to_csv(output / "physical_q2_validation.csv", index=False)
    return selected


def block_means(arrays, rng, n_boot):
    metrics, rows, distances = arrays.shape
    blocks = rows // 10
    values = arrays.reshape(metrics, blocks, 10, distances)
    sums = np.nansum(values, axis=2)
    counts = np.isfinite(values).sum(axis=2)
    chosen = rng.integers(blocks, size=(n_boot, metrics, blocks))
    index = np.arange(metrics)[None, :, None]
    totals = sums[index, chosen].sum(axis=2)
    sample_counts = counts[index, chosen].sum(axis=2)
    if np.any(sample_counts == 0):
        raise ValueError("A block draw lacks measurements at a distance")
    return totals / sample_counts


def block_radii(tables, means, original, seed, n_boot, output):
    rng = np.random.default_rng(seed)
    blocks = [block_means(tables[c], rng, n_boot) for c in q2.CALLS]
    point = [q2.fit_knots(m, q2.WEIGHTS["equal"]) for m in means]
    records = []
    for scheme, draws in (("row", original), ("ten_row_block", blocks)):
        knots = [[q2.fit_knots(m, q2.WEIGHTS["equal"]) for m in call] for call in draws]
        for threshold in q2.THRESHOLDS:
            central = [q2.radius(k, threshold) for k in point]
            estimates = [[q2.radius(k, threshold) for k in call] for call in knots]
            distances = np.array([[value for value, _ in call] for call in estimates])
            point_distances = np.array([value for value, _ in central])
            order = np.argsort(-point_distances)
            strict = np.all(np.diff(distances[order], axis=0) < 0, axis=0)
            for i, call in enumerate(q2.CALLS):
                rank = 1 + np.count_nonzero(point_distances > point_distances[i])
                same_rank = (1 + (distances > distances[i]).sum(axis=0)) == rank
                low, high = np.quantile(distances[i], [.025, .975])
                records.append({
                    "scheme": scheme, "threshold": threshold, "call": call, "radius_m": central[i][0],
                    "status": central[i][1], "low_m": low, "high_m": high,
                    "draws_below": sum(s == "below_support" for _, s in estimates[i]),
                    "draws_above": sum(s == "above_support" for _, s in estimates[i]),
                    "point_rank": rank, "same_rank_share": same_rank.mean(),
                    "strict_order_share": strict.mean(),
                })
    pd.DataFrame(records).to_csv(output / "physical_q2_blocks.csv", index=False)


def q4_comparison(selected, fitted, boot_physical, propagation, behavior, output):
    f, fd = propagation["fidelity"], propagation["draws"]
    distance = propagation["distance"]
    p, c = behavior["natural"], behavior["control"]
    pd_, cd = behavior["natural_draws"], behavior["control_draws"]
    cutoff = (f[:, 0] * p[:, 0]).mean() / 2
    cutoffs = (fd[:, :, 0] * pd_[:, :, 0]).mean(axis=1) / 2
    point_physical = curve(distance, fitted)
    records = []
    for loss, link in ((0., "clean"), (.20, "acoustic_only"), (.20, "coupled")):
        point_control, draw_control = (c, cd) if link == "coupled" else (p, pd_)
        base, _ = environment(f, p, point_control, loss, 0)
        candidate, _ = environment(point_physical, p, point_control, loss, 0)
        base_draw, _ = environment(fd, pd_, draw_control, loss, 0)
        candidate_draw, _ = environment(boot_physical, pd_, draw_control, loss, 0)
        for i, call in enumerate(q2.CALLS):
            for d in REPRESENTATIVE:
                j = np.searchsorted(distance, d)
                a, b = base[i, j] - cutoff, candidate[i, j] - cutoff
                da, db = base_draw[:, i, j] - cutoffs, candidate_draw[:, i, j] - cutoffs
                al, ah = np.quantile(da, [.025, .975])
                bl, bh = np.quantile(db, [.025, .975])
                low, high = np.quantile(db - da, [.025, .975])
                a_count, b_count = np.count_nonzero(da >= 0), np.count_nonzero(db >= 0)
                records.append({
                    "candidate": selected, "call": call, "distance_m": d, "loss": loss, "link": link,
                    "cutoff": cutoff, "isotonic_margin": a, "physical_margin": b, "difference": b - a,
                    "isotonic_low": al, "isotonic_high": ah, "physical_low": bl, "physical_high": bh,
                    "difference_low": low, "difference_high": high,
                    "isotonic_attainment": a_count / len(da), "physical_attainment": b_count / len(db),
                    "isotonic_point_pass": a >= 0, "physical_point_pass": b >= 0,
                    "isotonic_pass_80": a_count * 5 >= len(da) * 4,
                    "physical_pass_80": b_count * 5 >= len(db) * 4,
                })
    pd.DataFrame(records).to_csv(output / "physical_q4_margins.csv", index=False)


def fitted_radius(parameters, threshold):
    ceiling, scale, exponent = parameters
    distance = scale * max(0., (ceiling / threshold)**2 - 1)**(1 / exponent)
    if distance < q2.KNOTS[0]:
        return q2.KNOTS[0], "below_support"
    if distance >= q2.KNOTS[-1]:
        return q2.KNOTS[-1], "above_support"
    return distance, "crossing"


def run(data, output, seed, n_boot, propagation, behavior):
    means, original = zip(*(propagation["metric_means_and_draws"][c] for c in q2.CALLS))
    targets = np.array([equal_means(m) for m in means])
    selected = validation(targets, output)
    fits = {name: fit(q2.KNOTS, targets, name == "shared_g") for name in ("fixed_g", "shared_g")}
    pd.concat([pd.DataFrame(values, columns=["ceiling", "scale_m", "exponent"]).assign(
        model=name, call=q2.CALLS) for name, values in fits.items()], ignore_index=True).to_csv(
        output / "physical_q2_parameters.csv", index=False,
    )
    block_radii(q2.load_tables(data), means, original, seed, n_boot, output)
    boot_parameters = np.array([fit(
        q2.KNOTS, np.array([equal_means(m) for m in sample]), selected == "shared_g",
    ) for sample in zip(*original)])
    records = []
    for i, call in enumerate(q2.CALLS):
        central = [fitted_radius(fits[selected][i], threshold) for threshold in q2.THRESHOLDS]
        for threshold, (value, status) in zip(q2.THRESHOLDS, central):
            draws = [fitted_radius(sample[i], threshold) for sample in boot_parameters]
            values, statuses = zip(*draws)
            low, high = np.quantile(values, [.025, .975])
            records.append({
                "model": selected, "call": call, "threshold": threshold, "radius_m": value,
                "status": status, "low_m": low, "high_m": high,
                "draws_below": statuses.count("below_support"),
                "draws_above": statuses.count("above_support"),
            })
    pd.DataFrame(records).to_csv(output / "physical_q2_radii.csv", index=False)
    boot = np.array([curve(propagation["distance"], sample) for sample in boot_parameters])
    q4_comparison(selected, fits[selected], boot, propagation, behavior, output)
    return fits[selected], boot_parameters
