"""Hypothetical noise power and individual response counts on the Q4 grid."""
import numpy as np
import pandas as pd

from q3 import REPRESENTATIVE
from q4 import radius


def fidelity(distance, parameters, db):
    ceiling, scale, exponent = np.moveaxis(parameters, -1, 0)
    u = (distance / scale[..., None]) ** exponent[..., None]
    return ceiling[..., None] / np.sqrt(1 + 10**(db / 10) * u)


def scenario(distance, parameters, db, matched):
    clean = fidelity(distance, parameters, 0)
    physical = fidelity(distance, parameters, db)
    loss = 1 - physical / clean
    reference = np.searchsorted(distance, 100)
    mean_loss = loss[..., reference].mean(axis=-1)
    if matched:
        loss = np.broadcast_to(mean_loss[..., None, None], clean.shape)
    return clean * (1 - loss), loss, mean_loss


def response(natural, control, loss, coupled):
    return natural - loss * np.maximum(natural - control, 0) if coupled else natural


def count_options(p):
    independent = -8 * np.expm1(np.log1p(-p) / 8)
    return np.stack((p, 8 * p, independent, 2 * p, 4 * p, 6 * p), axis=-1)


def run(propagation, behavior, dates, parameters, sampled_parameters, output):
    distance = propagation["distance"]
    f, fd = propagation["fidelity"], propagation["draws"]
    natural, control = behavior["natural"], behavior["control"]
    cutoff = (f[:, 0] * natural[:, 0]).mean() / 2
    schemes = {
        "expID": (behavior["natural_draws"], behavior["control_draws"]),
        "date": (dates[:, 0], dates[:, 1]),
    }
    scenarios = [(0, "clean", "clean")] + [
        (db, shape, link) for db in (3, 6)
        for shape in ("noise_power", "matched_uniform")
        for link in ("acoustic_only", "coupled")
    ]
    points, radii, counts, losses = [], [], [], []
    for db, shape, link in scenarios:
        matched = shape == "matched_uniform"
        coupled = link == "coupled"
        acoustic, loss, matching_loss = scenario(distance, parameters, db, matched)
        acoustic_draws, loss_draws, matching_draws = scenario(distance, sampled_parameters, db, matched)
        p = response(natural, control, loss, coupled)
        score = acoustic * p
        if link in ("clean", "acoustic_only"):
            for i, call in enumerate(propagation["calls"]):
                for d in REPRESENTATIVE:
                    j = np.searchsorted(distance, d)
                    low, high = np.quantile(loss_draws[:, i, j], [.025, .975])
                    losses.append({"db": db, "shape": shape, "call": call, "distance_m": d,
                                   "relative_loss": loss[i, j], "low": low, "high": high,
                                   "mean_matched_loss_100m": matching_loss,
                                   "mean_match_low": np.quantile(matching_draws, .025),
                                   "mean_match_high": np.quantile(matching_draws, .975)})
        for scheme, (np_draws, cp_draws) in schemes.items():
            cutoffs = (fd[:, :, 0] * np_draws[:, :, 0]).mean(axis=1) / 2
            p_draws = response(np_draws, cp_draws, loss_draws, coupled)
            boot = acoustic_draws * p_draws
            for i, call in enumerate(propagation["calls"]):
                key = {"db": db, "shape": shape, "link": link, "resampling": scheme, "call": call}
                value, status = radius(distance, score[i], cutoff)
                values, statuses = zip(*(radius(distance, v, c) for v, c in zip(boot[:, i], cutoffs)))
                low, high = np.quantile(values, [.025, .975])
                radii.append({**key, "radius_m": value, "status": status, "low_m": low, "high_m": high,
                              "draws_below": statuses.count("below_support"),
                              "draws_above": statuses.count("above_support")})
                for d in REPRESENTATIVE:
                    j = np.searchsorted(distance, d)
                    margin = boot[:, i, j] - cutoffs
                    low, high = np.quantile(margin, [.025, .975])
                    n_attain = np.count_nonzero(margin >= 0)
                    points.append({**key, "distance_m": d, "cutoff": cutoff,
                                   "margin": score[i, j] - cutoff, "margin_low": low, "margin_high": high,
                                   "point_attains": score[i, j] >= cutoff,
                                   "attainment_share": n_attain / len(margin),
                                   "passes_80": n_attain * 5 >= len(margin) * 4})
                    if shape == "clean" or (shape == "noise_power" and coupled):
                        estimates = count_options(p[i, j])
                        low, high = np.quantile(count_options(p_draws[:, i, j]), [.025, .975], axis=0)
                        for k, model in enumerate(("sharp_lower", "sharp_upper", "independent",
                                                    "share_25", "share_50", "share_75")):
                            counts.append({**key, "distance_m": d, "group_probability": p[i, j],
                                           "assumption": model, "expected_count": estimates[k],
                                           "low": low[k], "high": high[k]})
    for name, rows in (("losses", losses), ("points", points), ("radii", radii), ("responders", counts)):
        pd.DataFrame(rows).to_csv(output / f"noise_q4_{name}.csv", index=False)
