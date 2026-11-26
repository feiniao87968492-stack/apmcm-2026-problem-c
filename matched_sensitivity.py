"""Distance-stratified responses, robust loss limits and weighted behavior indices."""
import numpy as np
import pandas as pd

import q3
from creative_inverse import limit, status
from q4 import environment, radius


def stratified_pairs(frame, sampled_dates):
    pairs = frame.pivot(index="expID", columns="Type", values=["Distance", "Npenguins", "mask", "Date"])
    delta = pairs["Distance"]["call"] - pairs["Distance"]["control"]
    natural = pairs["mask"]["call"].ne(0).to_numpy()
    control = pairs["mask"]["control"].ne(0).to_numpy()
    date = pairs["Date"]["call"].to_numpy()
    same_size = pairs["Npenguins"]["call"].eq(pairs["Npenguins"]["control"]).to_numpy()
    dates = sorted(set(date))
    records = []
    for label, selected in (("same", delta.eq(0)), ("nearer", delta.lt(0)), ("farther", delta.gt(0))):
        selected = selected.to_numpy()
        differences = natural.astype(int) - control
        totals = np.array([differences[selected & (date == d)].sum() for d in dates])
        sizes = np.array([(selected & (date == d)).sum() for d in dates])
        sampled_sizes = sizes[sampled_dates].sum(axis=1)
        valid = sampled_sizes > 0
        estimates = totals[sampled_dates[valid]].sum(axis=1) / sampled_sizes[valid]
        low, high = np.quantile(estimates, [.025, .975]) if valid.any() else (np.nan, np.nan)
        records.append({
            "natural_distance": label, "pairs": selected.sum(), "dates_with_pairs": np.count_nonzero(sizes),
            "same_group_size": (selected & same_size).sum(),
            "natural_responses": (selected & natural).sum(), "control_responses": (selected & control).sum(),
            "natural_only": (selected & natural & ~control).sum(),
            "control_only": (selected & control & ~natural).sum(),
            "response_difference": differences[selected].mean() if selected.any() else np.nan,
            "date_interval_low": low, "date_interval_high": high, "draws_with_support": valid.sum(),
        })
    return pd.DataFrame(records)


def loss_intersection(propagation, behavior, date_predictions):
    f = propagation["draws"]
    grid = np.arange(201) / 1000
    schemes = {"expID": (behavior["natural_draws"], behavior["control_draws"]),
               "date": (date_predictions[:, 0], date_predictions[:, 1])}
    cutoffs = {name: (f[:, :, 0] * p[:, :, 0]).mean(axis=1) / 2
               for name, (p, _) in schemes.items()}
    records = []
    for i, call in enumerate(propagation["calls"]):
        for distance in q3.REPRESENTATIVE:
            j = np.searchsorted(propagation["distance"], distance)
            for link in ("acoustic_only", "coupled"):
                passes = []
                result = {"call": call, "distance_m": distance, "link": link, "draws": len(f)}
                for name, (p, q) in schemes.items():
                    natural = p[:, i, j, None]
                    control = q[:, i, j, None] if link == "coupled" else natural
                    index, _ = environment(f[:, i, j, None], natural, control, grid, 0)
                    counts = (index >= cutoffs[name][:, None]).sum(axis=0)
                    ok = counts * 5 >= len(f) * 4
                    passes.append(ok)
                    result.update({
                        f"{name}_clean_share": counts[0] / len(f),
                        f"{name}_loss20_share": counts[-1] / len(f),
                        f"{name}_limit": limit(grid, ok), f"{name}_status": status(ok),
                    })
                joint = passes[0] & passes[1]
                result.update(intersection_limit=limit(grid, joint), intersection_status=status(joint))
                records.append(result)
    return pd.DataFrame(records)


def weighted_indices(propagation, behavior, output):
    distance, calls = propagation["distance"], propagation["calls"]
    f, fd = propagation["fidelity"], propagation["draws"]
    masks, mask_draws = behavior["natural_masks"], behavior["natural_mask_draws"]
    scores = {
        "any_response": (q3.MASKS != 0).astype(float),
        "equal": q3.BITS @ np.full(3, 1 / 3),
        "head02_vocal04_approach04": q3.BITS @ np.array([.2, .4, .4]),
    }
    points, radii = [], []
    for label, weights in scores.items():
        clean = f * (masks @ weights)
        clean_draws = fd * (mask_draws @ weights)
        cutoff = clean[:, 0].mean() / 2
        cutoff_draws = clean_draws[:, :, 0].mean(axis=1) / 2
        for loss in (0., .20):
            index, boot = (1 - loss) * clean, (1 - loss) * clean_draws
            locations = [radius(distance, curve, cutoff) for curve in index]
            for i, call in enumerate(calls):
                central, flag = locations[i]
                boot_radii = [radius(distance, curve, c) for curve, c in zip(boot[:, i], cutoff_draws)]
                estimates, statuses = zip(*boot_radii)
                low, high = np.quantile(estimates, [.025, .975])
                radii.append({
                    "index": label, "call": call, "loss": loss, "cutoff": cutoff, "radius_m": central,
                    "radius_status": flag, "radius_rank": 1 + sum(v > central for v, _ in locations),
                    "radius_low_m": low, "radius_high_m": high,
                    "draws_at_upper_support": statuses.count("above_support"),
                    "draws_below_support": statuses.count("below_support"),
                })
                for d in q3.REPRESENTATIVE:
                    j = np.searchsorted(distance, d)
                    margin = boot[:, i, j] - cutoff_draws
                    count = (margin >= 0).sum()
                    low, high = np.quantile(margin, [.025, .975])
                    points.append({
                        "index": label, "call": call, "loss": loss, "distance_m": d, "cutoff": cutoff,
                        "value": index[i, j], "point_rank": 1 + (index[:, j] > index[i, j]).sum(),
                        "point_attains": index[i, j] >= cutoff, "margin_low": low, "margin_high": high,
                        "attainment_share": count / len(margin), "passes_80": count * 5 >= len(margin) * 4,
                    })
    pd.DataFrame(points).to_csv(output / "matching_q4_weighted_points.csv", index=False)
    pd.DataFrame(radii).to_csv(output / "matching_q4_weighted_radii.csv", index=False)
