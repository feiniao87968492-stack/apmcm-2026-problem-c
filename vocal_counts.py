"""Paired vocal counts, out-of-date prediction, and contact scenarios."""
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.special import xlogy
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import q3
from q4 import environment
from sea_state import probability


def paired_counts(frame, before, after, eligible, dates, samples, output):
    changes = (after - before).reshape(-1, 2)
    matched = np.all(frame[["Distance", "Npenguins"]].to_numpy()[::2]
                     == frame[["Distance", "Npenguins"]].to_numpy()[1::2], axis=1)
    rows = []
    for subset, pairs in (("all", np.ones(len(dates), dtype=bool)), ("matched", matched)):
        keep = pairs & eligible
        blocks = [keep & (dates == d) for d in sorted(set(dates))]
        count = np.array([part.sum() for part in blocks])
        totals = np.array([changes[part].sum(axis=0) for part in blocks])
        denominators = count[samples].sum(axis=1)
        valid = denominators > 0
        draws = totals[samples[valid]].sum(axis=1) / denominators[valid, None]
        point = changes[keep].mean(axis=0)
        for label, estimate, bootstrap in zip(
                ("natural_change", "control_change", "difference_in_differences"),
                (*point, point[0] - point[1]),
                (*draws.T, draws[:, 0] - draws[:, 1])):
            low, high = np.quantile(bootstrap, [.025, .975])
            rows.append(dict(subset=subset, contrast=label, total_pairs=pairs.sum(),
                             pairs=keep.sum(), dates=np.count_nonzero(count), draws=valid.sum(),
                             estimate=estimate, low95=low, high95=high))
    pd.DataFrame(rows).to_csv(output / "vocal_count_pairs.csv", index=False)

    flag = frame.VocalYesNo.to_numpy(dtype=bool)
    audit = frame[["Type"]].assign(
        paired_counts=np.repeat(eligible, 2), before_available=np.isfinite(before),
        after_available=np.isfinite(after), scored_vocal=flag,
        count_increased=(after > before), positive_after=(after > 0),
        flag_vs_positive=(flag != (after > 0)) & np.isfinite(after),
        flag_vs_increase=(flag != (after > before)) & np.isfinite(before) & np.isfinite(after),
    )
    audit.groupby("Type").agg(trials=("Type", "size"), **{
        name: (name, "sum") for name in audit.columns[1:]
    }).to_csv(output / "vocal_count_audit.csv")


def validate(frame, before, after, eligible, dates, tracks, design, samples, output):
    augmented = np.column_stack((design, np.log1p(before)))
    names = ("stimulus_mean", "poisson_full", "poisson_before")
    stimulus = frame.Type.to_numpy()
    rows, score_totals, sizes = [], [], []
    for date in sorted(set(dates)):
        held = dates == date
        train = ~held & ~np.isin(tracks, tracks[held])
        tr, te = np.repeat(train & eligible, 2), np.repeat(held & eligible, 2)
        means = {s: after[tr & (stimulus == s)].mean() for s in q3.STIMULI}
        predictions = [np.array([means[s] for s in stimulus[te]])]
        for x in (design, augmented):
            model = make_pipeline(StandardScaler(), PoissonRegressor(
                alpha=1 / tr.sum(), max_iter=1000, tol=1e-9))
            predictions.append(model.fit(x[tr], after[tr]).predict(x[te]))
        mu = np.column_stack(predictions)
        y = after[te, None]
        safe = np.maximum(mu, 1e-12)
        deviance = 2 * (xlogy(y, y / safe) - y + safe)
        totals = np.column_stack((deviance.sum(axis=0), np.abs(y - mu).sum(axis=0)))
        score_totals.append(totals)
        sizes.append(te.sum())
        for name, (dev, mae) in zip(names, totals / te.sum()):
            rows.append(dict(date=date, model=name, train_pairs=tr.sum() // 2,
                             test_pairs=te.sum() // 2, purged_pairs=(~held & ~train).sum(),
                             poisson_deviance=dev, mae=mae))
    pd.DataFrame(rows).to_csv(output / "vocal_count_folds.csv", index=False)
    totals, sizes = np.asarray(score_totals), np.asarray(sizes)
    point = totals.sum(axis=0) / sizes.sum()
    draws = totals[samples].sum(axis=1) / sizes[samples].sum(axis=1)[:, None, None]
    rows = []
    for i, j in combinations(range(len(names)), 2):
        delta = draws[:, j] - draws[:, i]
        low, high = np.quantile(delta, [.025, .975], axis=0)
        for k, metric in enumerate(("poisson_deviance", "mae")):
            rows.append(dict(reference=names[i], model=names[j], metric=metric,
                             reference_score=point[i, k], score=point[j, k],
                             delta=point[j, k] - point[i, k], low95=low[k], high95=high[k],
                             joint_gain=(high < 0).all()))
    pd.DataFrame(rows).to_csv(output / "vocal_count_scores.csv", index=False)


def scenarios(frame, eligible, contact, design, contexts, weights, dates, samples,
              propagation, behavior, date_predictions, output):
    distances = np.asarray(q3.REPRESENTATIVE)
    locations = np.searchsorted(propagation["distance"], distances)
    target = q3.features(q3.probability_grid(distances, contexts, 8), contexts)
    shape = (len(q3.STIMULI), len(q3.CALLS), len(distances), len(contexts))
    blocks = [np.flatnonzero(np.repeat((dates == d) & eligible, 2)) for d in sorted(set(dates))]

    def predict(rows):
        return probability(design[rows], contact[rows], target).reshape(shape) @ weights

    contact_point = predict(np.concatenate(blocks))
    contact_draws = np.stack([predict(np.concatenate([blocks[i] for i in draw])) for draw in samples])
    any_point = np.stack([behavior[key][:, locations] for key in ("natural", "control")])
    any_draws = date_predictions[..., locations]
    fidelity = propagation["fidelity"][:, locations]
    fidelity_draws = propagation["draws"][:, :, locations]
    rows, coverage = [], []
    for loss in (0., .20):
        outcomes = {}
        for endpoint, point, draws in (("any_response", any_point, any_draws),
                                       ("count_increase", contact_point, contact_draws)):
            _, natural = environment(fidelity, *point, loss, 0)
            _, natural_draws = environment(fidelity_draws, draws[:, 0], draws[:, 1], loss, 0)
            outcomes[endpoint] = natural, point[1], natural_draws - draws[:, 1]
        for i, call in enumerate(q3.CALLS):
            for j, distance in enumerate(distances):
                f_pass = fidelity_draws[:, i, j] * (1 - loss) >= .50
                f_point = fidelity[i, j] * (1 - loss)
                delta = (outcomes["count_increase"][2] - outcomes["any_response"][2])[:, i, j]
                dl, dh = np.quantile(delta, [.025, .975])
                row = dict(call=call, distance_m=distance, loss=loss,
                           fidelity=f_point, fidelity_count=f_pass.sum(), draws=len(samples),
                           excess_delta_low95=dl, excess_delta_high95=dh)
                indicators = []
                for endpoint, (p, c, draws) in outcomes.items():
                    excess = p[i, j] - c[i, j]
                    sample = draws[:, i, j]
                    low, high = np.quantile(sample, [.025, .975])
                    joint = f_pass & (sample >= .20)
                    indicators.append(joint)
                    count = joint.sum()
                    row.update({f"{endpoint}_{key}": value for key, value in dict(
                        natural=p[i, j], control=c[i, j], excess=excess, low95=low, high95=high,
                        point_pass=f_point >= .50 and excess >= .20, joint_count=count,
                        joint_share=count / len(samples), pass_80=count * 5 >= len(samples) * 4,
                    ).items()})
                row.update(excess_delta=row["count_increase_excess"] - row["any_response_excess"],
                           contact_only_draws=(indicators[1] & ~indicators[0]).sum(),
                           any_only_draws=(indicators[0] & ~indicators[1]).sum())
                rows.append(row)
    for call in q3.CALLS:
        for distance in distances:
            local = (frame.assigned_call.eq(call) & frame.Distance.sub(distance).abs().le(25)
                     & np.repeat(eligible, 2))
            for stimulus in q3.STIMULI:
                selected = local & frame.Type.eq(stimulus)
                coverage.append(dict(call=call, distance_m=distance, stimulus=stimulus,
                                     trials=selected.sum(), increases=contact[selected].sum(),
                                     dates=frame.loc[selected, "Date"].nunique()))
    pd.DataFrame(rows).to_csv(output / "vocal_contact_q4.csv", index=False)
    pd.DataFrame(coverage).to_csv(output / "vocal_contact_coverage.csv", index=False)


def run(frame, samples, propagation, behavior, date_predictions, output):
    before = frame.VocalNcallsBefore.to_numpy(dtype=float)
    after = frame.VocalNcalls.to_numpy(dtype=float)
    eligible = (np.isfinite(before) & np.isfinite(after)).reshape(-1, 2).all(axis=1)
    natural = frame.iloc[::2]
    dates = natural.Date.to_numpy()
    weights = natural.Context.value_counts(normalize=True).sort_index()
    contexts = tuple(weights.index)
    design = q3.features(frame, contexts)
    paired_counts(frame, before, after, eligible, dates, samples, output)
    validate(frame, before, after, eligible, dates, natural.PlaybackTrack.to_numpy(),
             design, samples, output)
    scenarios(frame, eligible, after > before, design, contexts, weights.to_numpy(), dates,
              samples, propagation, behavior, date_predictions, output)
