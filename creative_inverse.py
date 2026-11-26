"""Invert the existing common-cutoff scenarios on their finite loss grid."""
import numpy as np
import pandas as pd

from q4 import environment


def loss_limits(propagation, behavior, output):
    fidelity = propagation["fidelity"]
    fidelity_draws = propagation["draws"]
    natural, control = behavior["natural"], behavior["control"]
    natural_draws, control_draws = behavior["natural_draws"], behavior["control_draws"]
    cutoff = .5 * (fidelity[:, 0] * natural[:, 0]).mean()
    draw_cutoffs = .5 * (fidelity_draws[:, :, 0] * natural_draws[:, :, 0]).mean(axis=1)
    losses = np.arange(201) / 1000
    distances = propagation["distance"]
    threshold_count = int(np.ceil(.8 * len(draw_cutoffs)))
    records = []
    for i, call in enumerate(propagation["calls"]):
        for j in np.flatnonzero(np.isin(distances, (50, 100, 150))):
            for link in ("acoustic_only", "coupled"):
                p_ctrl = natural[i, j] if link == "acoustic_only" else control[i, j]
                draw_ctrl = natural_draws[:, i, j] if link == "acoustic_only" else control_draws[:, i, j]
                point, _ = environment(fidelity[i, j], natural[i, j], p_ctrl, losses, 0)
                boot, _ = environment(fidelity_draws[:, i, j, None], natural_draws[:, i, j, None],
                                      draw_ctrl[:, None], losses, 0)
                point_margin = point - cutoff
                draw_margin = boot - draw_cutoffs[:, None]
                counts = (draw_margin >= 0).sum(axis=0)
                point_ok = point_margin >= 0
                support_ok = counts >= threshold_count
                last_draw_indices = np.maximum((draw_margin >= 0).sum(axis=1) - 1, 0)
                low, high = np.quantile(losses[last_draw_indices], [.025, .975])
                records.append({
                    "call": call, "distance_m": distances[j], "response_link": link, "cutoff": cutoff,
                    "clean_margin": point_margin[0], "loss_20_margin": point_margin[-1],
                    "point_limit_loss": limit(losses, point_ok), "point_status": status(point_ok),
                    "support_limit_loss": limit(losses, support_ok), "support_status": status(support_ok),
                    "clean_support": counts[0] / len(draw_cutoffs),
                    "loss_20_support": counts[-1] / len(draw_cutoffs),
                    "bounded_draw_limit_low": low, "bounded_draw_limit_high": high,
                    "draws_failing_clean": len(draw_cutoffs) - counts[0],
                    "draws_reaching_ceiling": counts[-1], "draws": len(draw_cutoffs),
                })
    pd.DataFrame(records).to_csv(output / "creative_q4_inverse_loss.csv", index=False)


def limit(losses, passes):
    return losses[np.flatnonzero(passes)[-1]] if passes.any() else np.nan


def status(passes):
    if not passes[0]:
        return "clean_failure"
    return "search_ceiling" if passes[-1] else "interior"
