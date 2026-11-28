"""Compare group head-raising duration, timely response and external noise."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import core_q2
import core_q3
import q2
import q3
from q4 import environment


SEED = 20261128
DRAWS = 10_000
WINDOW_CELL = np.searchsorted(core_q3.EDGES, 30)
DISTANCES = np.arange(20., 150.5, .5)
MASK_MODEL = "rank_one_distance_penalty"
TIMELY_MODELS = ("stimulus_time", core_q3.FACTOR_TIME, "direct_stimulus", "direct_distance")


def head_summary(frame):
    """Estimate seconds per group trial and the two terms of the contrast."""
    natural = frame[frame.Type.eq("call")].set_index("expID").sort_index()
    control = frame[frame.Type.eq("control")].set_index("expID").loc[natural.index]
    conditions = ["Distance", "Npenguins"]
    matched = natural[conditions].eq(control[conditions]).all(axis=1)
    durations = np.column_stack((natural.HeadsUpDuration, control.HeadsUpDuration))
    positive = durations > 0
    totals = pd.DataFrame(np.column_stack((np.ones(len(natural)), positive, durations)),
                          index=natural.index)
    summary, support = [], []
    for sample, keep in (("matched", matched), ("all", pd.Series(True, index=natural.index))):
        by_date = totals.loc[keep].groupby(natural.Date).sum().to_numpy()
        draws = np.random.default_rng(SEED).integers(len(by_date), size=(DRAWS, len(by_date)))
        counts = np.vstack((by_date.sum(axis=0), by_date[draws].sum(axis=1)))
        events = counts[:, 1:3]
        durations_sum = counts[:, 3:]
        risk = events / counts[:, :1]
        positive_mean = np.divide(durations_sum, events, out=np.full_like(events, np.nan),
                                  where=events > 0)
        mean = durations_sum / counts[:, :1]
        frequency_term = (risk[:, 0] - risk[:, 1]) * positive_mean.mean(axis=1)
        duration_term = (positive_mean[:, 0] - positive_mean[:, 1]) * risk.mean(axis=1)
        metrics = (
            ("head_raising_probability", risk, risk[:, 0] - risk[:, 1]),
            ("seconds_among_responders", positive_mean, positive_mean[:, 0] - positive_mean[:, 1]),
            ("seconds_per_trial", mean, mean[:, 0] - mean[:, 1]),
            ("frequency_component_seconds", None, frequency_term),
            ("duration_component_seconds", None, duration_term),
        )
        for metric, by_arm, delta in metrics:
            available = delta[1:][np.isfinite(delta[1:])]
            low, high = np.quantile(available, [.025, .975])
            summary.append(dict(sample=sample, pairs=int(keep.sum()), dates=len(by_date),
                                metric=metric, natural=None if by_arm is None else by_arm[0, 0],
                                control=None if by_arm is None else by_arm[0, 1],
                                difference=delta[0], low95=low, high95=high,
                                retained_draws=len(available)))
        for call, rows in natural.loc[keep].groupby("assigned_call"):
            pair_ids = rows.index
            support.append(dict(sample=sample, call=call, pairs=len(rows),
                                dates=rows.Date.nunique(),
                                natural_positive=int(natural.loc[pair_ids].HeadsUpDuration.gt(0).sum()),
                                control_positive=int(control.loc[pair_ids].HeadsUpDuration.gt(0).sum())))
    return pd.DataFrame(summary), pd.DataFrame(support)


def duration_design(frame, contexts, by_call):
    base = core_q3.compact_design(frame, contexts)
    if by_call:
        natural = frame.Type.eq("call")
        return np.column_stack((base, *(natural & frame.assigned_call.eq(call)
                                         for call in q3.CALLS[1:])))
    return base


def head_predictions(training, evaluation, contexts):
    duration = training.HeadsUpDuration.to_numpy()
    responders = duration > 0
    means = training.groupby("Type").HeadsUpDuration.mean()
    predictions = {"stimulus_mean": evaluation.Type.map(means).to_numpy()}
    for model, by_call in (("pooled_hurdle", False), ("call_hurdle", True)):
        train = duration_design(training, contexts, by_call)
        test = duration_design(evaluation, contexts, by_call)
        probability = core_q3.logistic_probability(train, responders, test)
        positive_model = make_pipeline(StandardScaler(), Ridge(alpha=8))
        positive_model.fit(train[responders], duration[responders])
        positive_mean = np.clip(positive_model.predict(test), 0, 60)
        predictions[model] = probability * positive_mean
    return predictions


def timely_predictions(training, evaluation, contexts, bins):
    event = bins <= WINDOW_CELL
    probabilities = {}
    for model in TIMELY_MODELS[:2]:
        cells = core_q3.predict_timing(training, evaluation, model, contexts, bins=bins,
                                       mask_model=MASK_MODEL)
        probabilities[model] = cells[:, :WINDOW_CELL + 1].sum(axis=1)
    probabilities["direct_stimulus"] = core_q3.stimulus_counts(
        training, event.astype(int), 2, evaluation)[:, 1]
    probabilities["direct_distance"] = core_q3.logistic_probability(
        core_q3.compact_design(training, contexts), event,
        core_q3.compact_design(evaluation, contexts))
    return probabilities


def held_out_predictions(frame, contexts, bins):
    head, timely = [], []
    for tail in (False, True):
        for date, train, test in core_q3.purged_folds(frame, tail=tail):
            if tail:
                test = test[frame.Distance.iloc[test].ge(125).to_numpy()]
            training, evaluation = frame.iloc[train], frame.iloc[test]
            if evaluation.empty:
                continue
            labels = dict(date=date, position=test, expID=evaluation.expID.to_numpy(),
                          stimulus=evaluation.Type.to_numpy(), distance_m=evaluation.Distance.to_numpy())
            if not tail:
                observed = evaluation.HeadsUpDuration.to_numpy()
                for model, predicted in head_predictions(training, evaluation, contexts).items():
                    head.append(pd.DataFrame(dict(**labels, scheme="ordinary", model=model,
                                                  observed_s=observed, predicted_s=predicted,
                                                  squared_error=(observed - predicted)**2)))
            observed = bins[test] <= WINDOW_CELL
            for model, predicted in timely_predictions(training, evaluation, contexts, bins[train]).items():
                correct_probability = np.where(observed, predicted, 1 - predicted)
                timely.append(pd.DataFrame(dict(
                    **labels, scheme="actual_long" if tail else "ordinary", model=model,
                    observed=observed, predicted=predicted, brier=(observed - predicted)**2,
                    log_loss=-np.log(np.clip(correct_probability, 1e-12, 1)),
                )))
    return pd.concat(head, ignore_index=True), pd.concat(timely, ignore_index=True)


def scores(predictions, metrics, reference):
    estimates, deltas = core_q3.pool_scores(predictions, ["scheme"], metrics, [reference])
    return estimates.merge(deltas, how="left", on=["scheme", "model", "metric"])


def shorter_propagation(inputs):
    """Refit the production curve using measurements through 128 m."""
    released = pd.read_csv(inputs / "core_q2_propagation.csv")
    model, = released.model.unique()
    ablation, measure = core_q2.ABSORPTION_MODELS[model]
    coefficients = pd.read_csv(inputs / "core_q2_absorption.csv")
    alpha = {measure: coefficients[coefficients.frequency_measure.eq(measure)]
             .set_index("call").loc[list(q2.CALLS), "alpha_db_per_m"].to_numpy()}
    table = released.pivot(index="call", columns="distance_m", values="empirical_equal_weight")
    observed = table.loc[list(q2.CALLS), q2.KNOTS].to_numpy()
    training = q2.KNOTS[:-1]
    means = observed[:, :-1]
    shared = core_q2.fit_all(training, means)["shared_g"]
    fit = core_q2.fit_absorption(training, means, shared, alpha[measure],
                                 core_q2.PENALTIES[ablation])
    predicted = core_q2.evaluate(model, core_q2.GRID, training, fit, alpha)
    full_radii = pd.read_csv(inputs / "core_q2_radii.csv")
    full_radii = full_radii[full_radii.model.eq(model)].set_index(["call", "threshold"])
    changes, shorter = [], {}
    for index, call in enumerate(q2.CALLS):
        shorter[call] = np.interp(DISTANCES, core_q2.GRID, predicted[index])
        for threshold in (.40, .50, .60):
            radius, status = core_q2.crossing(model, fit, index, threshold, predicted[index], alpha)
            full_radius = full_radii.loc[(call, threshold), "distance_m"]
            changes.append(dict(call=call, threshold=threshold, full_radius_m=full_radius,
                                short_fit_radius_m=radius, short_fit_status=status,
                                radius_difference_m=radius-full_radius, beyond_128m=radius > 128.,
                                observed_256m=observed[index, -1],
                                short_fit_256m=predicted[index, -1],
                                short_fit_error_256m=predicted[index, -1]-observed[index, -1]))
    return released, shorter, pd.DataFrame(changes)


def planning_radii(frame, contexts, weights, bins, acoustic, shorter):
    grid = pd.MultiIndex.from_product(
        [q3.STIMULI, q3.CALLS, DISTANCES, contexts],
        names=["Type", "assigned_call", "Distance", "Context"],
    ).to_frame(index=False).assign(Npenguins=8)
    projections = timely_predictions(frame, grid, contexts, bins)
    selected = acoustic[acoustic.distance_m.isin(DISTANCES)].set_index(["call", "distance_m"])
    radii = []
    for model, projected in projections.items():
        array = projected.reshape(len(q3.STIMULI), len(q3.CALLS), len(DISTANCES), len(contexts))
        probability = array @ weights
        for index, call in enumerate(q3.CALLS):
            full_curve = selected.loc[call, "fidelity"].reindex(DISTANCES).to_numpy()
            acoustic_fits = {"all_distances": full_curve}
            if model == core_q3.FACTOR_TIME:
                acoustic_fits["through_128m"] = shorter[call]
            for fit_name, fidelity in acoustic_fits.items():
                for loss in (0., .20):
                    _, response = environment(fidelity, *probability[:, index], loss, 0)
                    modified = (1-loss) * fidelity
                    passes = np.logical_and.accumulate((modified >= .5) & (response >= .5))
                    failures = np.flatnonzero(~passes)
                    radius, status, failing, binding = None, "below_support", None, "support"
                    if passes.any():
                        radius = DISTANCES[passes][-1]
                        status = "above_support" if passes.all() else "last_passing_node"
                    if len(failures):
                        first = failures[0]
                        failing = DISTANCES[first]
                        binding = ("both" if modified[first] < .5 and response[first] < .5 else
                                   "fidelity" if modified[first] < .5 else "response")
                    radii.append(dict(call=call, model=model, acoustic_fit=fit_name, loss=loss,
                                      radius_m=radius, status=status, first_failing_m=failing,
                                      binding=binding, response_at_20m=response[0],
                                      response_at_100m=response[np.searchsorted(DISTANCES, 100.)],
                                      response_at_150m=response[-1]))
    radii = pd.DataFrame(radii)
    ranges = []
    for (call, loss), cases in radii.query("acoustic_fit == 'all_distances'").groupby(["call", "loss"]):
        supported = cases.radius_m.dropna()
        shared = cases.radius_m.min() if cases.radius_m.notna().all() else None
        ranges.append(dict(call=call, loss=loss, models=len(cases), shared_prefix_m=shared,
                           largest_passing_m=supported.max(),
                           above_support_models=int(cases.status.eq("above_support").sum()),
                           no_passing_models=int(cases.status.eq("below_support").sum())))
    return radii, pd.DataFrame(ranges)


def stony_point(path):
    """Compare before/during vigilance shares among visible paired birds."""
    frame = pd.read_csv(path, sep=";")
    total = frame.filter(regex="_count$").sum(axis=1, min_count=1)
    frame["share"] = frame.vigilance_count / total.where(total > 0)
    individuals = frame.pivot(index=["noise", "video", "individual"], columns="time", values="share")
    individuals = individuals[["Pre_playback", "Playback"]].dropna()
    videos = individuals.groupby(level=["noise", "video"]).mean()
    rows = []
    for level, low, high in (("low", 61, 64), ("medium", 67, 70), ("high", 73, 76)):
        pairs = videos.loc[level]
        difference = pairs.Playback - pairs.Pre_playback
        indices = np.random.default_rng(SEED).integers(len(pairs), size=(DRAWS, len(pairs)))
        sampling = difference.to_numpy()[indices].mean(axis=1)
        lower, upper = np.quantile(sampling, [.025, .975])
        rows.append(dict(noise=level, noise_low_db=low, noise_high_db=high, videos=len(pairs),
                         individuals=len(individuals.loc[level]), before=pairs.Pre_playback.mean(),
                         during=pairs.Playback.mean(), difference=difference.mean(),
                         low95=lower, high95=upper))
    return pd.DataFrame(rows)


def run(data, output, inputs):
    frame = q3.load_playbacks(data)
    weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    contexts = tuple(weights.index)
    bins = core_q3.time_cells(core_q3.recorded_onset(frame)[:, 0])

    summary, support = head_summary(frame)
    head_oof, timely_oof = held_out_predictions(frame, contexts, bins)
    acoustic, shorter, leverage = shorter_propagation(inputs)
    radii, ranges = planning_radii(frame, contexts, weights.to_numpy(), bins, acoustic, shorter)
    source = Path(__file__).parent / "sources" / "stony-point" / "DataTable_analysis3.csv"
    tables = {
        "q3_head_duration": summary,
        "q3_head_duration_support": support,
        "q3_head_duration_oof": head_oof,
        "q3_head_duration_scores": scores(head_oof, ["squared_error"], "stimulus_mean"),
        "q4_timely30_oof": timely_oof,
        "q4_timely30_scores": scores(timely_oof, ["brier", "log_loss"], "direct_stimulus"),
        "q2_256m_sensitivity": leverage,
        "q4_timely30_radii": radii,
        "q4_timely30_model_range": ranges,
        "q4_stony_point_vigilance": stony_point(source),
    }
    output.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output / f"{name}.csv", index=False, lineterminator="\n")
