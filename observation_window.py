"""Compare paired responses under shorter observation windows."""
import numpy as np
import pandas as pd

import q3


WINDOWS = np.array([5, 15, 30, 60])
SEED = 20261208
DRAWS = 10_000


def run(data, output):
    frame = q3.load_playbacks(data)
    flags = frame[[b + "YesNo" for b in q3.BEHAVIORS]].to_numpy(dtype=bool)
    latency = frame[[b + "Latency" for b in q3.BEHAVIORS]].to_numpy(dtype=float)
    if not np.all(np.isfinite(latency[flags]) & (latency[flags] >= 0) & (latency[flags] <= 60)):
        raise ValueError("Flagged latencies must be finite and within the 60 s window.")
    onset = np.where(flags, latency, np.inf).min(axis=1).reshape(-1, 2)
    events = onset[:, :, None] <= WINDOWS
    np.testing.assert_array_equal(events[:, :, -1], frame.ResponseYesNo.to_numpy().reshape(-1, 2))
    waiting = np.minimum(onset, 60)
    dates = frame.Date.to_numpy().reshape(-1, 2)
    if not np.all(dates[:, 0] == dates[:, 1]):
        raise ValueError("Both playbacks in each pair must share a date.")
    dates = dates[:, 0]
    covariates = frame[["Distance", "Npenguins"]].to_numpy().reshape(-1, 2, 2)
    matched = (covariates[:, 0] == covariates[:, 1]).all(axis=1)

    rd = events[:, 0].astype(int) - events[:, 1]
    change = rd - rd[:, [-1]]
    wait_diff = waiting[:, 0] - waiting[:, 1]
    contrasts = np.column_stack((rd, change, wait_diff))
    summary, leave_out = [], []
    for sample, keep in (("matched", matched), ("all", np.ones(len(dates), dtype=bool))):
        selected_dates = np.unique(dates[keep])
        blocks = keep[None, :] & (selected_dates[:, None] == dates)
        sizes = blocks.sum(axis=1)
        totals = blocks @ contrasts
        n_pairs = keep.sum()
        point = contrasts[keep].mean(axis=0)
        sampled = np.random.default_rng(SEED).integers(len(sizes), size=(DRAWS, len(sizes)))
        bootstrap = totals[sampled].sum(axis=1) / sizes[sampled].sum(axis=1)[:, None]
        low, high = np.quantile(bootstrap, [.025, .975], axis=0)
        omitted = (totals.sum(axis=0) - totals) / (n_pairs - sizes)[:, None]
        counts = events[keep].sum(axis=0)
        wait_means = waiting[keep].mean(axis=0)
        for j, window in enumerate(WINDOWS):
            k = j + len(WINDOWS)
            summary.append(dict(
                sample=sample, window_s=window, pairs=n_pairs, dates=len(sizes),
                natural_events=counts[0, j], control_events=counts[1, j],
                natural_risk=counts[0, j]/n_pairs, control_risk=counts[1, j]/n_pairs,
                natural_missed=counts[0, -1]-counts[0, j],
                control_missed=counts[1, -1]-counts[1, j],
                risk_difference=point[j], rd_low=low[j], rd_high=high[j],
                rd_change_vs_60=point[k], change_low=low[k], change_high=high[k],
                natural_wait_s=wait_means[0] if window == 60 else None,
                control_wait_s=wait_means[1] if window == 60 else None,
                wait_difference_s=point[-1] if window == 60 else None,
                wait_low=low[-1] if window == 60 else None,
                wait_high=high[-1] if window == 60 else None,
            ))
            for date, size, row in zip(selected_dates, sizes, omitted):
                leave_out.append(dict(sample=sample, window_s=window, omitted_date=date,
                                      pairs=n_pairs-size, risk_difference=row[j],
                                      rd_change_vs_60=row[k],
                                      wait_difference_s=row[-1] if window == 60 else None))
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("summary", summary), ("leave_date_out", leave_out)):
        pd.DataFrame(rows).to_csv(output / f"observation_window_{name}.csv", index=False,
                                  lineterminator="\n")
