"""First vocal replies and group-level ordering of vocalizing and approach."""
from itertools import combinations

import numpy as np
import pandas as pd

from q3 import CALLS, STIMULI


def interval(draws):
    return np.quantile(draws, [.025, .975]) if len(draws) else (np.nan, np.nan)


def matrix(frame, vocal, date_indices, samples, output):
    contexts = sorted(frame.Context.unique())
    arms = [
        (dict(stimulus=stimulus, context=context),
         frame.Type.eq(stimulus) & frame.Context.eq(context))
        for stimulus in STIMULI for context in contexts
    ]
    natural = frame.Type.eq("call")
    detail = [
        (dict(played_call=call, context=context),
         natural & frame.assigned_call.eq(call) & frame.Context.eq(context))
        for call in CALLS for context in contexts
    ]
    for name, cells in (("matrix", arms), ("by_played_call", detail)):
        rows = matrix_rows(frame, vocal, date_indices, samples, cells)
        pd.DataFrame(rows).to_csv(output / f"first_reply_{name}.csv", index=False)


def matrix_rows(frame, vocal, date_indices, samples, cells):
    rows = []
    for labels, cell in cells:
        replied = cell & vocal
        trials = np.bincount(date_indices[cell], minlength=samples.shape[1])
        responses = np.bincount(date_indices[replied], minlength=samples.shape[1])
        for label in CALLS:
            matches = replied & frame.VR1.eq(label)
            counts = np.bincount(date_indices[matches], minlength=samples.shape[1])
            row = dict(labels, first_reply=label,
                       count=counts.sum(), unrecognized=(replied & ~frame.VR1.isin(CALLS)).sum(),
                       dates_with_trials=np.count_nonzero(trials),
                       dates_with_responses=np.count_nonzero(responses))
            draw_num = counts[samples].sum(axis=1)
            for name, den in (("response", responses), ("trial", trials)):
                totals = den[samples].sum(axis=1)
                keep = totals > 0
                low, high = interval(draw_num[keep] / totals[keep])
                row.update({f"{name}_denominator": den.sum(), f"{name}_draws": keep.sum(),
                            f"{name}_share": counts.sum() / den.sum() if den.sum() else np.nan,
                            f"{name}_low95": low, f"{name}_high95": high})
            rows.append(row)
    return rows


def validation(natural, date_indices, samples, output):
    names = ("pooled", "context", "context_played_call")
    played = natural.assigned_call.to_numpy()
    context = natural.Context.to_numpy()
    track = natural.PlaybackTrack.to_numpy()
    response = pd.Categorical(natural.VR1, categories=CALLS).codes
    known = natural.VocalYesNo.eq(1).to_numpy() & (response >= 0)

    def counts(mask):
        return np.bincount(response[mask], minlength=len(CALLS))

    rows, totals, sizes = [], [], []
    for index, date in enumerate(sorted(natural.Date.unique())):
        held = date_indices == index
        train = ~held & ~np.isin(track, track[held])
        test = held & known
        pooled_counts = counts(train & known) + .5
        pooled = pooled_counts / pooled_counts.sum()
        forecasts = []
        for g, call in zip(context[test], played[test]):
            group_mask = train & known & (context == g)
            context_counts = counts(group_mask) + 6 * pooled
            group = context_counts / context_counts.sum()
            call_counts = counts(group_mask & (played == call)) + 6 * group
            forecasts.append([pooled, group, call_counts / call_counts.sum()])
        p = np.asarray(forecasts).reshape(-1, len(names), len(CALLS))
        observed = np.eye(len(CALLS))[response[test]]
        loss = -(np.log(p) * observed[:, None, :]).sum(axis=(0, 2))
        brier = ((p - observed[:, None, :])**2).sum(axis=(0, 2))
        scores = np.column_stack((loss, brier))
        totals.append(scores)
        sizes.append(test.sum())
        for name, (ce, bs) in zip(names, scores):
            rows.append(dict(date=date, model=name, train_pairs=train.sum(), held_pairs=held.sum(),
                             purged_pairs=(~held & ~train).sum(), train_replies=(train & known).sum(),
                             test_replies=test.sum(), cross_entropy=ce / test.sum() if test.any() else np.nan,
                             brier=bs / test.sum() if test.any() else np.nan))
    pd.DataFrame(rows).to_csv(output / "first_reply_folds.csv", index=False)

    totals, sizes = np.asarray(totals), np.asarray(sizes)
    point = totals.sum(axis=0) / sizes.sum()
    denominators = sizes[samples].sum(axis=1)
    keep = denominators > 0
    draws = totals[samples[keep]].sum(axis=1) / denominators[keep, None, None]
    rows = []
    for i, j in combinations(range(len(names)), 2):
        delta = draws[:, j] - draws[:, i]
        low, high = np.quantile(delta, [.025, .975], axis=0)
        for k, metric in enumerate(("cross_entropy", "brier")):
            rows.append(dict(reference=names[i], model=names[j], metric=metric,
                             reference_score=point[i, k], score=point[j, k], delta=point[j, k]-point[i, k],
                             low95=low[k], high95=high[k], draws=keep.sum(), joint_gain=(high < 0).all()))
    pd.DataFrame(rows).to_csv(output / "first_reply_scores.csv", index=False)
    return natural.loc[known]


def matching(replies, seed, output):
    groups = [(part.assigned_call.to_numpy(), part.VR1.to_numpy())
              for _, part in replies.groupby(["Date", "Context"], sort=True)]
    count = sum(np.count_nonzero(played == reply) for played, reply in groups)
    expected = sum(sum(np.count_nonzero(played == label) * np.count_nonzero(reply == label)
                       for label in CALLS) / len(reply) for played, reply in groups)
    informative_sizes = [len(reply) for played, reply in groups
                         if len(set(played)) > 1 and len(set(reply)) > 1]
    rng = np.random.default_rng(seed)
    draws = np.array([
        sum(np.count_nonzero(played == rng.permutation(reply)) for played, reply in groups)
        for _ in range(19_999)
    ])
    low, high = interval(draws)
    pd.DataFrame([dict(replies=len(replies), blocks=len(groups),
                       informative_blocks=len(informative_sizes), informative_replies=sum(informative_sizes),
                       observed=count, expected=expected, observed_share=count / len(replies),
                       expected_share=expected / len(replies), null_low95=low, null_high95=high,
                       permutations=len(draws), p_upper=(1 + np.count_nonzero(draws >= count)) / (len(draws) + 1))
                  ]).to_csv(output / "first_reply_matching.csv", index=False)


def order(natural, date_indices, samples, output):
    both = natural.VocalYesNo.eq(1) & natural.ApproachYesNo.eq(1)
    lag = (natural.ApproachLatency - natural.VocalLatency).to_numpy()
    keep = both & np.isfinite(lag)
    blocks = [lag[keep & (date_indices == i)] for i in range(samples.shape[1])]
    full = lag[keep]
    resampled = [np.concatenate([blocks[i] for i in draw]) for draw in samples]
    resampled = [draw for draw in resampled if len(draw)]
    rows = []
    for name, statistic in (("vocal_first_share", lambda values: (values > 0).mean()),
                            ("mean_lag_s", np.mean), ("median_lag_s", np.median)):
        low, high = interval([statistic(draw) for draw in resampled])
        rows.append(dict(metric=name, both_events=both.sum(), eligible=len(full),
                         dates=sum(bool(len(x)) for x in blocks), vocal_first=(full > 0).sum(),
                         tied=(full == 0).sum(), approach_first=(full < 0).sum(),
                         estimate=statistic(full), low95=low, high95=high, draws=len(resampled)))
    pd.DataFrame(rows).to_csv(output / "first_reply_event_order.csv", index=False)


def run(frame, samples, seed, output):
    _, date_indices = np.unique(frame.Date, return_inverse=True)
    natural = frame.Type.eq("call")
    matrix(frame, frame.VocalYesNo.eq(1), date_indices, samples, output)
    replies = validation(frame.loc[natural], date_indices[natural], samples, output)
    matching(replies, seed + 3, output)
    order(frame.loc[natural], date_indices[natural], samples, output)
