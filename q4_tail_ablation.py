"""Compare five playback extrapolations using the released acoustic and date draws."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import expit, logit

import physical_attenuation
import q3
from control_subtraction import reference, score_curves
from distance_deletion import pair_filters
from distance_deletion_mc import DATE_SEED, PREFIXES, acoustics
from q4_extrapolation_drift import ANCHORS, tolerances
from q4_tail_models import MODELS, Design, validate

DISTANCES = np.array([20, 100, 150])
GRID = np.array([20, 100, 120, 150])
TARGETS = (("tv", 150, "clean", "net_own"), ("tv", 100, "coupled", "net_own"),
           ("mod", 100, "clean", "gross"))
DRAWS = PREFIXES[-1]
REQUIRED = 4 * DRAWS // 5


def refits(design, frame, included, sampled, weights):
    grid = q3.probability_grid(GRID, tuple(weights.index), 8)
    blocks = [np.flatnonzero(included & frame.Date.eq(date)) for date in sorted(frame.Date.unique())]
    training = [np.flatnonzero(included), *[np.concatenate([blocks[i] for i in draw]) for draw in sampled]]
    predictions = {model: np.full((len(training), 2, 3, len(GRID)), np.nan) for model in MODELS}
    for i, rows in enumerate(training):
        for model in MODELS:
            try:
                masks, _ = design.predict(model, rows, grid, joint=model == "D")
            except RuntimeError:
                continue
            prediction = (1 - masks[:, 0]).reshape(2, 3, len(GRID), -1) @ weights.to_numpy()
            predictions[model][i] = prediction
        if np.isfinite(predictions["D"][i]).all():
            np.testing.assert_array_equal(predictions["D"][i], predictions["A"][i])
    return predictions


def interval(values):
    values = values[np.isfinite(values)]
    return np.quantile(values, [.025, .975]) if len(values) else (np.nan, np.nan)


def margins(predictions, fidelity, cutoffs):
    for call, distance, link, kind in TARGETS:
        i, j = q3.CALLS.index(call), np.searchsorted(GRID, distance)
        k = np.searchsorted(DISTANCES, distance)
        loss = .20 if link == "coupled" else 0.
        by_model = {}
        for model, p in predictions.items():
            valid = np.isfinite(p[:, :, i, j]).all(axis=1)
            gross, net = score_curves(fidelity[valid, i, k], p[valid, 0, i, j], p[valid, 1, i, j],
                                      loss, loss > 0)
            margin = np.full(len(p), np.nan)
            margin[valid] = (gross if kind == "gross" else net) - cutoffs[kind][valid]
            by_model[model] = margin
            delta = margin - by_model["A"]
            low, high = interval(margin[1:])
            delta_low, delta_high = interval(delta[1:])
            count = int(np.count_nonzero(margin[1:] >= 0))
            valid_draws = int(np.isfinite(margin[1:]).sum())
            yield dict(model=model, call=call, distance_m=distance, link=link, definition=kind,
                       p_n=p[0, 0, i, j], p_c=p[0, 1, i, j], cutoff=cutoffs[kind][0],
                       margin=margin[0], low95=low, high95=high, delta_a=delta[0],
                       delta_low95=delta_low, delta_high95=delta_high,
                       count=count, valid_draws=valid_draws, failed_draws=DRAWS-valid_draws,
                       paired_draws=int(np.isfinite(delta[1:]).sum()), support=count/DRAWS,
                       passes_80=count >= REQUIRED, point_attains=bool(margin[0] >= 0))


def drift(model, p, fidelity, cutoff):
    valid = np.isfinite(p).all(axis=1) & np.isfinite(fidelity) & np.isfinite(cutoff)
    margin = fidelity * (p[:, 0] - p[:, 1]) - cutoff
    qualifies = margin >= 0
    count = int(np.count_nonzero(qualifies[1:]))
    common = dict(model=model, zero_count=count, valid_draws=int(valid[1:].sum()))
    yield dict(common, scenario="zero", feasible=bool(qualifies[0] and count >= REQUIRED),
               lambda_max=0., odds_factor=1., point_margin=margin[0],
               delta_p_n=0., delta_p_c=0., count=count, support=count/DRAWS)
    for name, signs in (("natural_only", (-1, 0)), ("control_only", (0, 1)), ("both", (-1, 1))):
        slopes = np.log2(150 / ANCHORS) * signs
        roots = np.full(len(p), -np.inf)
        logits = logit(p[valid])
        roots[valid] = tolerances(logits, fidelity[valid], cutoff[valid], slopes, qualifies[valid])
        point = roots[0]
        support = np.partition(roots[1:], DRAWS - REQUIRED)[DRAWS - REQUIRED]
        limit = min(point, support)
        row = dict(common, scenario=name, feasible=bool(limit >= 0),
                   lambda_point=point if point >= 0 else np.nan,
                   lambda_support=support if support >= 0 else np.nan)
        if limit >= 0:
            changed = p[0].copy()
            active = slopes != 0
            changed[active] = expit(logit(p[0, active]) + slopes[active] * limit)
            at = int(np.count_nonzero(roots[1:] >= limit))
            row.update(lambda_max=limit, odds_factor=np.exp(limit),
                       delta_p_n=changed[0]-p[0, 0], delta_p_c=changed[1]-p[0, 1],
                       point_margin=fidelity[0] * (changed[0]-changed[1]) - cutoff[0],
                       count=at, count_above=int(np.count_nonzero(roots[1:] > limit)) if np.isfinite(limit) else np.nan,
                       support=at/DRAWS, binding="both" if point == support else
                       ("point" if point < support else "support"))
        yield row


def run(data, output, baseline):
    frame = q3.load_playbacks(data)
    natural = frame.loc[frame.Type.eq("call")]
    weights = natural.Context.value_counts(normalize=True).sort_index()
    assert np.array_equal(frame.Date.to_numpy()[::2], frame.Date.to_numpy()[1::2])
    dates = natural.Date.nunique()
    sampled = np.random.default_rng(DATE_SEED).integers(dates, size=(DRAWS, dates))
    design = Design(frame, tuple(weights.index))
    tables = validate(design, sampled)
    filters, _ = pair_filters(frame)
    iso, fidelity = acoustics(data, DISTANCES)
    params = pd.read_csv(baseline / "physical_q2_parameters.csv").query("model == 'shared_g'")
    params = params.set_index("call").loc[list(q3.CALLS), ["ceiling", "scale_m", "exponent"]]
    fidelity = np.concatenate((physical_attenuation.curve(DISTANCES, params.to_numpy())[None], fidelity))
    point_iso = pd.read_csv(baseline / "q2_propagation.csv").query("distance_m == 20")
    point_iso = point_iso.set_index("call").loc[list(q3.CALLS), ["fidelity"]].to_numpy()
    iso = np.concatenate((point_iso[None], iso))
    full = refits(design, frame, filters["full"], sampled, weights)
    anchor = full["A"]
    cutoffs = {"gross": reference(iso, anchor[:, 0]),
               "net_own": reference(iso, anchor[:, 0] - anchor[:, 1])}
    union = refits(design, frame, filters["drop_union"], sampled, weights)
    tables["margins"] = pd.DataFrame(
        dict(row, training=name)
        for name, predictions in (("full", full), ("drop_union", union))
        for row in margins(predictions, fidelity, cutoffs)
    )

    drift_rows, tail_rows = [], []
    tv = q3.CALLS.index("tv")
    for model, probability in union.items():
        for arm, arm_name in enumerate(q3.STIMULI):
            anchor_index = np.searchsorted(GRID, ANCHORS[arm])
            arm_probability = probability[:, arm, tv]
            delta = arm_probability[:, -1] - arm_probability[:, anchor_index]
            low, high = interval(delta[1:])
            tail_rows.append(dict(model=model, stimulus=arm_name, anchor_m=ANCHORS[arm],
                                  p_anchor=arm_probability[0, anchor_index], p_150=arm_probability[0, -1],
                                  delta=delta[0], low95=low, high95=high,
                                  valid_draws=int(np.isfinite(delta[1:]).sum())))
        drift_rows.extend(drift(model, probability[:, :, tv, -1], fidelity[:, tv, -1], cutoffs["net_own"]))
    tables["tail"] = pd.DataFrame(tail_rows)
    tables["drift"] = pd.DataFrame(drift_rows)
    archived = pd.read_csv(baseline / "distance_deletion_mc.csv")
    archived = archived.query("source == 'fresh' and requested_draws == 4800")
    for row in tables["margins"].loc[lambda t: t.model.eq("A")].itertuples():
        old = archived.loc[archived.model.eq(row.training) & archived.call.eq(row.call)
                           & archived.distance_m.eq(row.distance_m) & archived.link.eq(row.link)
                           & archived.definition.eq(row.definition)].iloc[0]
        assert row.count == old["count"] and row.valid_draws == old["valid_draws"]
    old = pd.read_csv(baseline / "q4_extrapolation_drift.csv").dropna(subset=["lambda_point"])
    current = tables["drift"].query("model == 'A' and scenario != 'zero'")
    np.testing.assert_allclose(current.lambda_max, old.lambda_max, atol=1e-12, rtol=0)

    ranking = tables["validation"].pivot(index="model", columns="assessment", values="mask_log_loss")
    ranking = ranking.rename(columns={"tail": "tail_mask_loss", "ordinary": "ordinary_mask_loss"})
    ranking["validation_eligible"] = tables["validation"].groupby("model").validation_eligible.all()
    ranking["q4_complete"] = tables["margins"].groupby("model").apply(
        lambda rows: rows.failed_draws.eq(0).all() and rows.margin.notna().all(), include_groups=False,
    )
    ranked = ranking.loc[ranking.validation_eligible & ranking.q4_complete].sort_values(
        ["tail_mask_loss", "ordinary_mask_loss", "model"],
    )
    chosen = ranked.index[0] if len(ranked) else "A"
    ranking["adopted"] = ranking.index == chosen
    tables["adoption"] = ranking.reset_index()
    return tables


def write(data, output, baseline):
    tables = run(data, output, baseline)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output / f"q4_tail_ablation_{name}.csv", index=False, lineterminator="\n")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", default=Path("results"), type=Path)
    parser.add_argument("--baseline", default=Path("results"), type=Path)
    args = parser.parse_args()
    write(args.data, args.output, args.baseline)
