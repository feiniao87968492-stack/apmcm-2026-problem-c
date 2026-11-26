"""Date-level False Bay weather sensitivities from archived ERA5 snapshots."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import q3


def daily_weather(dates, output):
    source = Path(__file__).with_name("sources") / "false-bay"
    series = {}
    for label, key in (("wind", "wind_speed_10m"), ("wave", "wave_height")):
        snapshot = json.loads((source / f"{label}.json").read_bytes())
        if snapshot["utc_offset_seconds"] != 7200:
            raise ValueError("False Bay snapshots require local UTC+02:00 time")
        series[label] = pd.Series(snapshot["hourly"][key],
                                  index=pd.to_datetime(snapshot["hourly"]["time"]))
    hours = pd.DataFrame(series)
    hours = hours.loc[hours.index.normalize().isin(dates) & hours.index.hour.isin(range(8, 14))]
    daily = hours.groupby(hours.index.normalize())
    if not daily.count().eq(6).all().all() or len(daily) != len(dates):
        raise ValueError("Expected six wind and wave observations per playback date")
    hours.rename_axis("local_time").to_csv(output / "sea_state_hourly.csv")
    return daily.mean()


def date_slopes(pairs, weather, samples, output):
    records, inputs = [], []
    for name, indices in (("all", pairs.index), ("same_distance", pairs.index[pairs.same_distance])):
        daily = pairs.loc[indices].groupby("date").difference.agg(["mean", "size"]).reindex(weather.index)
        inputs.append(weather.join(daily).assign(subset=name))
        for variable in weather:
            x, y = weather[variable].to_numpy(), daily["mean"].to_numpy()

            def slope(ids):
                a, b = x[ids], y[ids]
                valid = np.isfinite(b)
                a, b = a[valid], b[valid]
                if np.unique(a).size < 2:
                    return np.nan
                centered = a - a.mean()
                return (centered @ b) / (centered @ centered)

            draws = np.array([slope(ids) for ids in samples])
            limits = np.nanquantile(draws, [.025, .975])
            records.append({"subset": name, "weather": variable, "dates": daily["size"].count(),
                            "pairs": len(indices), "slope": slope(np.arange(len(x))),
                            "low": limits[0], "high": limits[1], "draws": np.isfinite(draws).sum()})
    pd.concat(inputs).rename_axis("date").to_csv(output / "sea_state_daily.csv")
    pd.DataFrame(records).to_csv(output / "sea_state_slopes.csv", index=False)


def augment(design, values):
    return np.column_stack((design, values, design[:, 0] * values))


def probability(x, y, target):
    model = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000))
    return model.fit(x, y).predict_proba(target)[:, 1]


def compare(pairs, design, y, weather, samples, output):
    sizes, scores, coverage = [], [], []
    for date in weather.index:
        test = pairs.date.eq(date)
        train = ~test & ~pairs.track.isin(pairs.loc[test, "track"])
        tr, te = np.repeat(train.to_numpy(), 2), np.repeat(test.to_numpy(), 2)
        p = [probability(x[tr], y[tr], x[te]) for x in design.values()]
        estimates = np.column_stack(p)
        outcome = y[te, None]
        loss = -np.log(np.maximum(np.where(outcome, estimates, 1-estimates), 1e-12))
        brier = (estimates-outcome)**2
        scores.append(np.stack([loss.sum(0), brier.sum(0)]))
        sizes.append(te.sum())
        coverage.append({"date": date, "test_pairs": test.sum(), "train_pairs": train.sum(),
                         "purged_pairs": (~test & ~train).sum()})
    scores, sizes = np.asarray(scores), np.asarray(sizes)
    point = scores.sum(0)/sizes.sum()
    draws = scores[samples].sum(1)/sizes[samples].sum(1)[:, None, None]
    delta = draws - draws[..., :1]
    low, high = np.quantile(delta, [.025, .975], axis=0)
    records = []
    for m, name in enumerate(design):
        for j, metric in enumerate(("binary_log_loss", "brier")):
            records.append({"model": name, "metric": metric, "score": point[j,m],
                            "delta": point[j,m]-point[j,0], "low": low[j,m], "high": high[j,m],
                            "joint_gain": bool((high[:,m]<0).all())})
    pd.DataFrame(records).to_csv(output / "sea_state_validation.csv", index=False)
    pd.DataFrame(coverage).to_csv(output / "sea_state_coverage.csv", index=False)


def standardized(frame, pairs, designs, y, contexts, weights, weather, samples, output):
    grid = q3.probability_grid(np.array(q3.REPRESENTATIVE), contexts, 8)
    design = q3.features(grid, contexts)
    by_date = [np.flatnonzero(np.repeat(pairs.date.eq(date).to_numpy(), 2)) for date in weather.index]
    rows = [np.arange(len(frame))] + [np.concatenate([by_date[i] for i in draw]) for draw in samples]
    records = []
    for variable in weather:
        low, high = weather[variable].quantile([.25,.75])
        predictions = []
        for ids in rows:
            p = [probability(designs[variable][ids], y[ids], augment(design, np.full(len(grid), value)))
                 .reshape(2, 3, 3, len(contexts)) @ weights for value in (low, high)]
            a,b = p
            predictions.append(np.stack((a[0], a[1], a[0]-a[1], b[0], b[1], b[0]-b[1],
                                         (b[0]-b[1])-(a[0]-a[1]))))
        point = predictions[0]
        lo,hi = np.quantile(predictions[1:], [.025,.975], axis=0)
        for k,name in enumerate(("low_natural","low_control","low_gap","high_natural","high_control",
                                 "high_gap","gap_change")):
            for i,call in enumerate(q3.CALLS):
                for j,d in enumerate(q3.REPRESENTATIVE):
                    records.append({"weather":variable,"low_weather":low,"high_weather":high,
                                    "call":call,"distance_m":d,"contrast":name,
                                    "estimate":point[k,i,j],"low":lo[k,i,j],"high":hi[k,i,j]})
    pd.DataFrame(records).to_csv(output / "sea_state_standardized.csv", index=False)


def run(frame, output, seed, n_boot):
    natural, control = frame.iloc[::2], frame.iloc[1::2]
    dates = pd.to_datetime(natural.Date, format="%d/%m/%Y")
    pairs = pd.DataFrame({"date": dates.to_numpy(), "track": natural.PlaybackTrack.to_numpy(),
                          "same_distance": natural.Distance.to_numpy()==control.Distance.to_numpy(),
                          "difference": (natural["mask"].ne(0).astype(int).to_numpy()
                                         - control["mask"].ne(0).astype(int).to_numpy())})
    weather = daily_weather(dates.unique(), output)
    samples = np.random.default_rng(seed + 2).integers(len(weather), size=(n_boot,len(weather)))
    date_slopes(pairs, weather, samples, output)
    context_weights = natural.Context.value_counts(normalize=True).sort_index()
    contexts = tuple(context_weights.index)
    design = q3.features(frame, contexts)
    designs = {"baseline": design}
    for variable in weather:
        designs[variable] = augment(design, np.repeat(pairs.date.map(weather[variable]).to_numpy(), 2))
    y = frame["mask"].ne(0).to_numpy()
    compare(pairs, designs, y, weather, samples, output)
    standardized(frame, pairs, designs, y, contexts, context_weights.to_numpy(), weather, samples, output)
