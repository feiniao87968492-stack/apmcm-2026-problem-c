"""Decision criteria, crossed variance and matched-playback design for Q4."""
import numpy as np
import pandas as pd

from q4 import environment


def decisions(fidelity, natural, control, f_draws, n_draws, c_draws,
              cutoff, draw_cutoffs, scenarios, cells):
    records = []
    for loss, link in scenarios:
        fixed_control = control if link == "coupled" else natural
        fixed_control_draws = c_draws if link == "coupled" else n_draws
        index, response = environment(fidelity, natural, fixed_control, loss, 0)
        boot, boot_response = environment(f_draws, n_draws, fixed_control_draws, loss, 0)
        for i, j, call, distance in cells:
            acoustic = (1 - loss) * fidelity[i, j]
            excess = response[i, j] - control[i, j]
            fidelity_ok = (1 - loss) * f_draws[:, i, j] >= .50
            product_ok = boot[:, i, j] >= draw_cutoffs
            for threshold in (.10, .20, .30):
                excess_ok = boot_response[:, i, j] - c_draws[:, i, j] >= threshold
                joint = fidelity_ok & excess_ok
                counts = [int(mask.sum()) for mask in (fidelity_ok, excess_ok, joint, product_ok)]
                n = len(joint)
                records.append({
                    "call": call, "distance_m": distance, "loss": loss, "link": link,
                    "excess_threshold": threshold, "fidelity": acoustic, "response_excess": excess,
                    "product_margin": index[i, j] - cutoff,
                    "dual_point_attains": acoustic >= .50 and excess >= threshold,
                    "product_point_attains": index[i, j] >= cutoff, "draws": n,
                    **{f"{key}_count": count for key, count in
                       zip(("fidelity", "excess", "dual", "product"), counts)},
                    **{f"{key}_share": count / n for key, count in
                       zip(("fidelity", "excess", "dual", "product"), counts)},
                    "dual_minus_product_share": (counts[2] - counts[3]) / n,
                    "dual_pass_80": counts[2] * 5 >= n * 4,
                    "product_pass_80": counts[3] * 5 >= n * 4,
                })
    return pd.DataFrame(records)


def crossed_variance(f_draws, n_draws, c_draws, cells):
    cutoffs = f_draws[:, :, 0] @ n_draws[:, :, 0].T / (2 * f_draws.shape[1])
    records = []
    for loss, link in ((0., "clean"), (.20, "coupled")):
        for i, j, call, distance in cells:
            product, _ = environment(f_draws[:, i, j, None], n_draws[None, :, i, j],
                                     c_draws[None, :, i, j], loss, 0)
            margin = product - cutoffs
            mean = margin.mean()
            acoustic = margin.mean(axis=1, keepdims=True) - mean
            behavior = margin.mean(axis=0, keepdims=True) - mean
            residual = margin - mean - acoustic - behavior
            amounts = [np.mean(term**2) for term in (acoustic, behavior, residual)]
            total = margin.var()
            if not np.isclose(sum(amounts), total, rtol=1e-10, atol=1e-15):
                raise ArithmeticError("Crossed components do not sum to total variance")
            record = {"call": call, "distance_m": distance, "loss": loss, "link": link,
                      "acoustic_draws": len(f_draws), "behavior_draws": len(n_draws),
                      "mean_margin": mean, "total_variance": total}
            for name, amount in zip(("acoustic", "behavior", "interaction"), amounts):
                record[f"{name}_variance"] = amount
                record[f"{name}_share"] = amount / total if total else np.nan
            records.append(record)
    return pd.DataFrame(records)


def minimax_counts(contrast_numerators, total_per_arm=60, minimum=5):
    # The optimal maximum is one of the cell variances at a feasible cell count.
    counts = np.arange(minimum, total_per_arm - minimum * (len(contrast_numerators) - 1) + 1)
    variances = contrast_numerators[:, None] / counts
    for upper in np.unique(variances):
        feasible = variances <= upper
        if feasible.any(axis=1).all():
            minima = counts[feasible.argmax(axis=1)]
            if minima.sum() <= total_per_arm:
                # Put any slack in the final cell for the lexicographically first optimum.
                minima[-1] += total_per_arm - minima.sum()
                return minima
    raise ValueError("No feasible trial allocation")


def trial_design(natural, control, cells):
    p = np.asarray([natural[i, j] for i, j, _, _ in cells])
    q = np.asarray([control[i, j] for i, j, _, _ in cells])
    natural_var = p * (1 - p)
    control_var = q * (1 - q)
    base = natural_var + control_var
    covariance_min = np.maximum(0, p + q - 1) - p * q
    covariance_max = np.minimum(p, q) - p * q
    allocations = {"equal": np.full(len(cells), 10), "minimax": minimax_counts(2 * base)}
    records = []
    for rho in (-.25, 0., .25):
        covariance = np.clip(rho * np.sqrt(natural_var * control_var), covariance_min, covariance_max)
        pair_var = base - 2 * covariance
        for label, allocation in allocations.items():
            contrast_var = 2 * pair_var / allocation
            for k, (_, _, call, distance) in enumerate(cells):
                records.append({
                    "call": call, "distance_m": distance, "allocation": label, "assumed_rho": rho,
                    "applied_rho": covariance[k] / np.sqrt(natural_var[k] * control_var[k]),
                    "reference_arm_pairs": allocation[k], "elevated_arm_pairs": allocation[k],
                    "clean_p_natural": p[k], "clean_p_control": q[k],
                    "natural_variance": natural_var[k], "control_variance": control_var[k],
                    "paired_covariance": covariance[k], "within_pair_difference_variance": pair_var[k],
                    "contrast_variance": contrast_var[k], "standard_error": np.sqrt(contrast_var[k]),
                    "half_width_95": 1.96 * np.sqrt(contrast_var[k]),
                    "worst_cell": contrast_var[k] == contrast_var.max(),
                })
    return pd.DataFrame(records)


def run(propagation, behavior, output):
    f, f_draws = propagation["fidelity"], propagation["draws"]
    p, q = behavior["natural"], behavior["control"]
    p_draws, q_draws = behavior["natural_draws"], behavior["control_draws"]
    distance = propagation["distance"]
    cells = [(i, j, call, distance[j]) for i, call in enumerate(propagation["calls"])
             for j in np.flatnonzero(np.isin(distance, (50, 100, 150)))]
    scenarios = [(0., "clean")] + [(loss, link) for loss in (.10, .20)
                                    for link in ("acoustic_only", "coupled")]
    cutoff = .5 * (f[:, 0] * p[:, 0]).mean()
    draw_cutoffs = .5 * (f_draws[:, :, 0] * p_draws[:, :, 0]).mean(axis=1)
    decisions(f, p, q, f_draws, p_draws, q_draws, cutoff, draw_cutoffs,
              scenarios, cells).to_csv(output / "decision_q4_dual.csv", index=False)
    crossed_variance(f_draws, p_draws, q_draws, cells).to_csv(
        output / "decision_q4_variance.csv", index=False,
    )
    trial_design(p, q, [cell for cell in cells if cell[-1] >= 100]).to_csv(
        output / "decision_q4_trial.csv", index=False,
    )
