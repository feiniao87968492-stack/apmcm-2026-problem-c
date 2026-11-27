"""Strict grouped validation for playback masks and 60 s event times."""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import logsumexp, softmax
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import q3
from creative_q3 import fit_structured
from round2 import mask_scores


MASK_MODELS = ("smoothed_stimulus", "full_multinomial", "pairwise_mask", "shrunken_hurdle",
               "rank_one_tilt", "nested_pool")
TIMING_MODELS = ("stimulus_time", "discrete_hazard", "finite_window")
ENDPOINTS = ("Any", *q3.BEHAVIORS)
EDGES = np.array([0, 5, 15, 30, 60])
INTEGRATION_WEIGHTS = np.diff(EDGES) / EDGES[-1]
POOL_WEIGHTS = np.linspace(0, 1, 5)
C = .25
SEED = 20261209
DRAWS = 10_000


def purged_folds(frame, tail=False):
    """Return trial positions while keeping each expID pair intact."""
    natural = frame.loc[frame.Type.eq("call")]
    dates = frame.expID.map(natural.set_index("expID").Date).to_numpy()
    tracks = frame.expID.map(natural.set_index("expID").PlaybackTrack).to_numpy()
    far = frame.Distance.ge(125).groupby(frame.expID).transform("any").to_numpy()
    for date in np.unique(dates):
        held = dates == date
        train = ~held & ~np.isin(tracks, np.unique(tracks[held]))
        test = held
        if tail:
            train &= ~far
            test = held & far
        if test.any() and train.any():
            yield date, np.flatnonzero(train), np.flatnonzero(test)


def stimulus_counts(frame, labels, n_cells, evaluation, pseudocount=.5):
    counts = np.stack([np.bincount(labels[frame.Type.eq(arm)], minlength=n_cells)
                       for arm in q3.STIMULI])
    smoothed = counts + pseudocount
    return (smoothed / smoothed.sum(axis=1, keepdims=True))[evaluation.Type.eq("control").astype(int)]


def compact_design(frame, contexts):
    return np.column_stack((
        frame.Type.eq("call"), np.log1p(frame.Distance), np.log1p(frame.Npenguins),
        *(frame.Context.eq(context) for context in contexts[1:]),
    ))


def logistic_probability(x, event, prediction):
    if len(np.unique(event)) < 2:
        return np.full(len(prediction), (event.sum() + .5) / (len(event) + 1))
    model = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=1000))
    return model.fit(x, event).predict_proba(prediction)[:, 1]


def hurdle(frame, evaluation, contexts):
    y = frame["mask"].to_numpy()
    positive = y > 0
    p = logistic_probability(compact_design(frame, contexts), positive,
                             compact_design(evaluation, contexts))
    pooled = np.bincount(y[positive] - 1, minlength=7) + .5
    composition = stimulus_counts(frame.loc[positive], y[positive]-1, 7, evaluation,
                                  8 * pooled / pooled.sum())
    return np.column_stack((1-p, p[:, None] * composition))


def rank_one(frame, evaluation, contexts):
    y = frame["mask"].to_numpy()
    burden = q3.BITS.sum(axis=1)
    train = compact_design(frame, contexts)
    scaler = StandardScaler().fit(train)
    x = np.column_stack((np.ones(len(train)), scaler.transform(train)))
    offset = np.log(stimulus_counts(frame, y, 8, frame))
    observed = (np.arange(len(y)), y)

    def objective(beta):
        logits = offset + (x @ beta)[:, None] * burden
        loss = (logsumexp(logits, axis=1) - logits[observed]).sum() + beta @ beta / 2
        gradient = x.T @ (softmax(logits, axis=1) @ burden - burden[y]) + beta
        return loss, gradient

    fitted = minimize(objective, np.zeros(x.shape[1]), jac=True, method="L-BFGS-B",
                      options={"maxiter": 1000, "gtol": 1e-7, "ftol": 1e-12})
    if not fitted.success:
        raise RuntimeError(f"Rank-one mask fit failed: {fitted.message}")
    z = np.column_stack((np.ones(len(evaluation)),
                         scaler.transform(compact_design(evaluation, contexts))))
    return softmax(np.log(stimulus_counts(frame, y, 8, evaluation))
                   + (z @ fitted.x)[:, None] * burden, axis=1)


def nested_weight(frame, contexts):
    losses = np.zeros(len(POOL_WEIGHTS))
    for _, train, test in purged_folds(frame):
        training, validation = frame.iloc[train], frame.iloc[test]
        y = validation["mask"].to_numpy()
        frequency = stimulus_counts(training, training["mask"].to_numpy(), 8, validation)
        candidate = hurdle(training, validation, contexts)
        for i, weight in enumerate(POOL_WEIGHTS):
            mixture = frequency + weight * (candidate - frequency)
            losses[i] += mask_scores(mixture, y)[:, 0].sum()
    return POOL_WEIGHTS[np.argmin(losses)]


def predict_mask(frame, evaluation, model, contexts, pool_weight=None):
    """Return probabilities for masks 0–7, ordered as in q3.MASKS."""
    y = frame["mask"].to_numpy()
    if model == "smoothed_stimulus":
        return stimulus_counts(frame, y, 8, evaluation)
    if model == "shrunken_hurdle":
        return hurdle(frame, evaluation, contexts)
    if model == "rank_one_tilt":
        return rank_one(frame, evaluation, contexts)
    if model == "nested_pool":
        weight = nested_weight(frame, contexts) if pool_weight is None else pool_weight
        frequency = stimulus_counts(frame, y, 8, evaluation)
        return frequency + weight * (hurdle(frame, evaluation, contexts) - frequency)
    train, test = q3.features(frame, contexts), q3.features(evaluation, contexts)
    if model == "full_multinomial":
        return q3.fit_masks(train, y, test)
    if model == "pairwise_mask":
        return fit_structured(train, y, test, interactions=True)
    raise ValueError(f"Unknown mask model: {model}")


def recorded_onset(frame):
    flags = frame[[b + "YesNo" for b in q3.BEHAVIORS]].to_numpy(dtype=bool)
    seconds = frame[[b + "Latency" for b in q3.BEHAVIORS]].to_numpy(dtype=float)
    if not np.all(np.isfinite(seconds[flags]) & (seconds[flags] >= 0) & (seconds[flags] <= 60)):
        raise ValueError("Flagged events require a recorded onset within 0–60 s.")
    recorded = np.where(flags, seconds, np.inf)
    return np.column_stack((recorded.min(axis=1), recorded))


def time_cells(onset):
    return np.searchsorted(EDGES, onset, side="left")


def predict_timing(frame, evaluation, model, contexts, endpoint="Any", bins=None):
    """Return probabilities for five onset cells and no event by 60 s."""
    if bins is None:
        bins = time_cells(recorded_onset(frame)[:, ENDPOINTS.index(endpoint)])
    if model == "stimulus_time":
        return stimulus_counts(frame, bins, 6, evaluation)
    x = q3.features(frame, contexts)
    target = q3.features(evaluation, contexts)
    if model == "finite_window":
        event = bins < 5
        p = logistic_probability(x, event, target)
        timing = stimulus_counts(frame.loc[event], bins[event], 5, evaluation)
        return np.column_stack((p[:, None] * timing, 1-p))
    if model == "discrete_hazard":
        rows, periods = np.where(bins[:, None] >= np.arange(5))
        train = np.column_stack((x[rows], np.eye(5)[periods, 1:]))
        test = np.column_stack((np.repeat(target, 5, axis=0),
                                np.tile(np.eye(5)[:, 1:], (len(target), 1))))
        hazard = logistic_probability(train, bins[rows] == periods, test).reshape(-1, 5)
        survival = np.cumprod(1-hazard, axis=1)
        return np.column_stack((hazard * np.column_stack((np.ones(len(test)//5),
                                                          survival[:, :-1])), survival[:, -1]))
    raise ValueError(f"Unknown event-time model: {model}")


def timing_scores(probability, test, onset, bins):
    realized = probability[np.arange(len(test)), bins[test]]
    cumulative = probability[:, :5].cumsum(axis=1)[:, 1:]
    observed = onset[test, None] <= EDGES[None, 1:]
    return np.column_stack((-np.log(realized.clip(1e-12)),
                            (cumulative - observed)**2 @ INTEGRATION_WEIGHTS))


def conditional_times(training, evaluation, probability, model, onset, bins):
    responders = np.isfinite(onset)
    if model == "stimulus_time":
        pooled = np.median(onset[responders])
        times = []
        for arm in q3.STIMULI:
            recorded = onset[responders & training.Type.eq(arm)]
            times.append(np.median(recorded) if len(recorded) else pooled)
        return np.asarray(times)[evaluation.Type.eq("control").astype(int)]
    pooled_by_bin = np.array([
        np.median(onset[bins == j]) if np.any(bins == j) else edge
        for j, edge in enumerate(EDGES)
    ])
    cumulative = probability[:, :5].cumsum(axis=1)
    median_bin = (cumulative < cumulative[:, [-1]] / 2).sum(axis=1)
    return pooled_by_bin[median_bin]


def validate_masks(frame, contexts):
    rows, coverage = [], []
    for tail in (False, True):
        scheme = "tail" if tail else "ordinary"
        for date, train, test in purged_folds(frame, tail=tail):
            training, validation = frame.iloc[train], frame.iloc[test]
            weight = nested_weight(training, contexts)
            y = validation["mask"].to_numpy()
            coverage.append(dict(scheme=scheme, date=date, train_pairs=len(train)//2,
                                 test_pairs=len(test)//2, nested_hurdle_weight=weight,
                                 actual_long_trials=validation.Distance.ge(125).sum()))
            for model in MASK_MODELS:
                probs = predict_mask(training, validation, model, contexts, pool_weight=weight)
                scores = mask_scores(probs, y)
                for i, (_, trial) in enumerate(validation.iterrows()):
                    rows.append(dict(scheme=scheme, date=date, position=test[i], model=model,
                                     distance_m=trial.Distance, mask_log_loss=scores[i, 0],
                                     any_response_brier=scores[i, 1]))
    return pd.DataFrame(rows), pd.DataFrame(coverage)


def validate_timing(frame, contexts):
    rows = []
    all_onsets = recorded_onset(frame)
    for date, train, test in purged_folds(frame):
        training, validation = frame.iloc[train], frame.iloc[test]
        for endpoint, onset in zip(ENDPOINTS, all_onsets.T):
            bins = time_cells(onset)
            for model in TIMING_MODELS:
                p = predict_timing(training, validation, model, contexts, endpoint, bins[train])
                scores = timing_scores(p, test, onset, bins)
                times = conditional_times(training, validation, p, model, onset[train], bins[train])
                error = np.where(np.isfinite(onset[test]), np.abs(onset[test] - times), np.nan)
                for i, pos in enumerate(test):
                    rows.append(dict(endpoint=endpoint, date=date, position=pos, model=model,
                                     censored_log_loss=scores[i, 0], integrated_brier=scores[i, 1],
                                     conditional_mae_s=error[i]))
    return pd.DataFrame(rows)


def pool_scores(scores, strata, metrics, references):
    rows, differences = [], []
    for keys, group in scores.groupby(strata, sort=False):
        labels = dict(zip(strata, keys if isinstance(keys, tuple) else (keys,)))
        for metric in metrics:
            wide = group.pivot(index=["date", "position"], columns="model", values=metric).dropna()
            if wide.empty:
                continue
            date_totals = wide.groupby(level="date").sum()
            sizes = wide.groupby(level="date").size().to_numpy()
            indices = np.random.default_rng(SEED).integers(len(sizes), size=(DRAWS, len(sizes)))
            means = wide.mean()
            for model in wide.columns:
                rows.append(dict(**labels, model=model, metric=metric, estimate=means[model],
                                 trials=len(wide), dates=len(sizes)))
                for reference in references:
                    if model == reference:
                        continue
                    delta = date_totals[model].to_numpy() - date_totals[reference].to_numpy()
                    draws = delta[indices].sum(axis=1) / sizes[indices].sum(axis=1)
                    low, high = np.quantile(draws, [.025, .975])
                    differences.append(dict(**labels, model=model, reference=reference, metric=metric,
                                            difference=means[model] - means[reference],
                                            ci_low=low, ci_high=high))
    return pd.DataFrame(rows), pd.DataFrame(differences)


def model_selection(mask_summary, mask_delta, time_summary, time_delta):
    mask_candidates = mask_delta.loc[mask_delta.scheme.eq("ordinary")
                                     & mask_delta.model.isin(MASK_MODELS[3:])]
    qualifying_masks = mask_candidates.groupby("model").ci_high.max().loc[lambda s: s < 0].index
    loss = mask_summary.query("scheme == 'ordinary' and metric == 'mask_log_loss'").set_index("model")
    selected_mask = loss.loc[qualifying_masks].estimate.idxmin() if len(qualifying_masks) else "full_multinomial"
    selected_timing = {}
    for endpoint in ENDPOINTS:
        result = time_delta.query("endpoint == @endpoint")
        log_loss = result.query("metric == 'censored_log_loss'").set_index("model")
        brier = result.query("metric == 'integrated_brier'").set_index("model")
        valid = (log_loss.ci_high < 0) & (brier.difference <= 0)
        candidates = log_loss.loc[valid].index
        losses = time_summary.query("endpoint == @endpoint and metric == 'censored_log_loss'").set_index("model")
        selected_timing[endpoint] = losses.loc[candidates].estimate.idxmin() if len(candidates) else "stimulus_time"
    return selected_mask, selected_timing


def prediction_table(frame, contexts, weights, mask_model, timing_models):
    rows = []
    median_size = float(frame.Npenguins.median())
    for endpoint in ENDPOINTS:
        distances = np.arange(20., 150.5, .5) if endpoint == "Any" else q3.REPRESENTATIVE
        grid = q3.probability_grid(distances, contexts, median_size)
        grid_columns = grid.iloc[::len(contexts)].rename(columns={"Type": "stimulus",
                          "assigned_call": "call", "Distance": "distance_m",
                          "Npenguins": "group_size"}).drop(columns="Context")
        for model in TIMING_MODELS:
            probs = predict_timing(frame, grid, model, contexts, endpoint)
            agg = weights @ probs.reshape(-1, len(contexts), 6)
            cumulative = agg[:, :5].cumsum(axis=1)
            for i, edge in enumerate(EDGES):
                rows.append(grid_columns.assign(family="timing", endpoint=endpoint,
                           model=model, window_s=edge, probability=cumulative[:, i],
                           selected=model == timing_models[endpoint]))
        if endpoint == "Any":
            for model in dict.fromkeys(("full_multinomial", mask_model)):
                p = 1-predict_mask(frame, grid, model, contexts)[:, 0]
                rows.append(grid_columns.assign(family="mask", endpoint=endpoint, model=model,
                           window_s=60, probability=p.reshape(-1, len(contexts)) @ weights,
                           selected=model == mask_model))
    return pd.concat(rows, ignore_index=True)


def representative_latency(frame, timing_models):
    onset = recorded_onset(frame)
    rows = []
    for i, endpoint in enumerate(ENDPOINTS):
        observed = np.isfinite(onset[:, i])
        for stimulus in q3.STIMULI:
            values = onset[observed & frame.Type.eq(stimulus), i]
            for distance in q3.REPRESENTATIVE:
                rows.append(dict(endpoint=endpoint, stimulus=stimulus, distance_m=distance,
                                 group_size=8, model=timing_models[endpoint],
                                 pooled_responders=len(values),
                                 median_latency_s=np.median(values) if len(values) else None,
                                 status="pooled_by_stimulus" if len(values) else "unestimable"))
    return pd.DataFrame(rows)


def support_table(frame):
    onset = recorded_onset(frame)
    rows = []
    for (stimulus, call), part in frame.groupby(["Type", "assigned_call"]):
        for distance in q3.REPRESENTATIVE:
            selected = part.loc[part.Distance.sub(distance).abs().le(25)]
            row = dict(stimulus=stimulus, call=call, distance_m=distance, nearby_trials=len(selected),
                       nearby_dates=selected.Date.nunique(), min_observed_m=part.Distance.min(),
                       max_observed_m=part.Distance.max())
            row.update({f"{e}_events": np.isfinite(onset[selected.index, i]).sum()
                        for i, e in enumerate(ENDPOINTS)})
            rows.append(row)
    return pd.DataFrame(rows)


def run(data, output):
    frame = q3.load_playbacks(data)
    context_weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    contexts = tuple(context_weights.index)
    mask, coverage = validate_masks(frame, contexts)
    timing = validate_timing(frame, contexts)
    mask_long = mask.query("scheme == 'tail' and distance_m >= 125").assign(scheme="actual_long")
    mask = pd.concat((mask, mask_long), ignore_index=True)
    mask_metrics = ["mask_log_loss", "any_response_brier"]
    timing_metrics = ["censored_log_loss", "integrated_brier", "conditional_mae_s"]
    mask_scores_table, mask_delta = pool_scores(mask, ["scheme"], mask_metrics,
                                                MASK_MODELS[:2])
    timing_scores_table, time_delta = pool_scores(timing, ["endpoint"], timing_metrics,
                                                  TIMING_MODELS[:1])
    selected_mask, selected_timing = model_selection(mask_scores_table, mask_delta,
                                                      timing_scores_table, time_delta)
    tables = {
        "coverage": coverage,
        "mask_scores": mask_scores_table,
        "mask_deltas": mask_delta,
        "mask_date_scores": mask.groupby(["scheme", "date", "model"])[mask_metrics].mean().reset_index(),
        "timing_scores": timing_scores_table,
        "timing_deltas": time_delta,
        "timing_date_scores": timing.groupby(["endpoint", "date", "model"])[timing_metrics].mean().reset_index(),
        "predictions": prediction_table(frame, contexts, context_weights.to_numpy(),
                                        selected_mask, selected_timing),
        "support": support_table(frame),
        "representative_latency": representative_latency(frame, selected_timing),
    }
    output.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output / f"core_q3_{name}.csv", index=False, lineterminator="\n")
    return selected_mask, selected_timing


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    print(run(args.data, args.output))
