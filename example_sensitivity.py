"""WAVERYS and assumed example-level sensitivity analyses."""
from itertools import product
import json
from pathlib import Path

import numpy as np
import pandas as pd

import physical_attenuation as attenuation
import q2
import q3
from q4 import environment
from sea_state import augment, compare, date_slopes


def waverys(frame, output, seed, n_boot):
    source = Path(__file__).with_name("sources") / "false-bay" / "waverys.json"
    points = pd.DataFrame(json.loads(source.read_bytes())["points"])
    points["hour"] = pd.to_datetime(points.local_time).dt.hour
    weather = {}
    for name, latitude in (("waverys_nearshore", -34.2), ("waverys_offshore", -34.4)):
        cell = points.loc[points.latitude.eq(latitude) & points.longitude.eq(18.6)]
        hourly = cell.pivot(index="date", columns="hour", values="wave_height_m")[[8, 11, 14]]
        weather[name] = [np.interp(np.arange(8, 14), [8, 11, 14], row).mean()
                         for row in hourly.to_numpy()]
    weather = pd.DataFrame(weather, index=pd.to_datetime(hourly.index))
    natural, control = frame.iloc[::2], frame.iloc[1::2]
    pairs = pd.DataFrame({
        "date": pd.to_datetime(natural.Date, format="%d/%m/%Y").to_numpy(),
        "track": natural.PlaybackTrack.to_numpy(),
        "same_distance": natural.Distance.to_numpy() == control.Distance.to_numpy(),
        "difference": natural.ResponseYesNo.to_numpy() - control.ResponseYesNo.to_numpy(),
    })
    if set(weather.index) != set(pairs.date) or weather.isna().any().any():
        raise ValueError("WAVERYS must cover each playback date and both study cells.")
    draws = np.random.default_rng(seed + 2).integers(len(weather), size=(n_boot, len(weather)))
    date_slopes(pairs, weather, draws, output, prefix="waverys")

    x = q3.features(frame, tuple(sorted(natural.Context.unique())))
    designs = {"baseline": x}
    for name, values in weather.items():
        designs[name] = augment(x, np.repeat(pairs.date.map(values).to_numpy(), 2))
    compare(pairs, designs, frame.ResponseYesNo.to_numpy(), weather, draws, output, prefix="waverys")
    for table, keys in (("slopes", ["subset", "weather"]), ("validation", ["model", "metric"])):
        original = pd.read_csv(output / f"sea_state_{table}.csv")
        alternative = pd.read_csv(output / f"waverys_{table}.csv")
        pd.concat([original, alternative]).drop_duplicates(keys).to_csv(
            output / f"waverys_{table}.csv", index=False,
        )


def example_deletion(data, output, propagation, behavior, date_predictions, full_parameters):
    tables = q2.load_tables(data)
    targets = [[attenuation.equal_means(np.nanmean(array[:, np.arange(300) // 100 != block], axis=1))
                for block in range(3)] for array in (tables[call] for call in q2.CALLS)]
    parameters = {"full": full_parameters}
    for omitted in product(range(3), repeat=3):
        name = "-".join(str(group + 1) for group in omitted)
        means = np.array([targets[i][group] for i, group in enumerate(omitted)])
        parameters[name] = attenuation.fit(q2.KNOTS, means, shared=True)

    radii, margins = [], []
    distance = propagation["distance"]
    natural, control = behavior["natural"], behavior["control"]
    p, c = date_predictions[:, 0], date_predictions[:, 1]
    cutoff = (propagation["fidelity"][:, 0] * natural[:, 0]).mean() / 2
    draw_cutoffs = (propagation["draws"][:, :, 0] * p[:, :, 0]).mean(axis=1) / 2
    for name, fit in parameters.items():
        for threshold in q2.THRESHOLDS:
            crossings = [attenuation.fitted_radius(row, threshold) for row in fit]
            for i, call in enumerate(q2.CALLS):
                value, flag = crossings[i]
                radii.append({"deleted_groups": name, "threshold": threshold, "call": call,
                              "radius_m": value, "status": flag, "rank": 1 + sum(r > value for r, _ in crossings)})
        f = attenuation.curve(distance, fit)
        for loss in (0., .20):
            point, _ = environment(f, natural, control, loss, 0)
            samples, _ = environment(f, p, c, loss, 0)
            for i, call in enumerate(q2.CALLS):
                for d in q3.REPRESENTATIVE:
                    j = np.searchsorted(distance, d)
                    values = samples[:, i, j] - draw_cutoffs
                    low, high = np.quantile(values, [.025, .975])
                    successes = np.count_nonzero(values >= 0)
                    margins.append({
                        "deleted_groups": name, "call": call, "distance_m": d, "coupled_loss": loss,
                        "point_margin": point[i, j] - cutoff, "margin_low": low, "margin_high": high,
                        "support_share": successes / len(values), "passes_80": 5 * successes >= 4 * len(values),
                    })
    pd.DataFrame(radii).to_csv(output / "example_deletion_radii.csv", index=False)
    margins = pd.DataFrame(margins)
    margins.to_csv(output / "example_deletion_q4.csv", index=False)
    keys = ["call", "distance_m", "coupled_loss"]
    summary = margins.loc[margins.deleted_groups.ne("full")].groupby(keys).agg(
        combinations=("passes_80", "size"), combinations_passing=("passes_80", "sum"),
        min_support=("support_share", "min"), max_support=("support_share", "max"),
    )
    reference = margins.loc[margins.deleted_groups.eq("full")].set_index(keys)
    summary.join(reference[["support_share", "passes_80"]].add_prefix("full_")).to_csv(
        output / "example_deletion_q4_summary.csv",
    )
