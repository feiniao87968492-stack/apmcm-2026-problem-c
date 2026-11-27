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
               "rank_one_tilt", "nested_pool", "rank_one_distance_penalty",
               "call_aware_hurdle")
TIMING_MODELS = ("stimulus_time", "discrete_hazard", "finite_window")
ANY_TIMING_MODELS = (*TIMING_MODELS, "weibull_aft")
FACTOR_TIME = "factorized_time"
MASK_LIMITS = dict(ordinary_logloss=0., ordinary_brier=.01, tail_logloss=.10, tail_brier=.02)
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


def hurdle(frame, evaluation, contexts, design=compact_design):
    y = frame["mask"].to_numpy()
    positive = y > 0
    p = logistic_probability(design(frame, contexts), positive, design(evaluation, contexts))
    pooled = np.bincount(y[positive] - 1, minlength=7) + .5
    composition = stimulus_counts(frame.loc[positive], y[positive]-1, 7, evaluation,
                                  8 * pooled / pooled.sum())
    return np.column_stack((1-p, p[:, None] * composition))


def rank_one(frame, evaluation, contexts, distance_penalty=1.):
    y = frame["mask"].to_numpy()
    burden = q3.BITS.sum(axis=1)
    train = compact_design(frame, contexts)
    scaler = StandardScaler().fit(train)
    x = np.column_stack((np.ones(len(train)), scaler.transform(train)))
    offset = np.log(stimulus_counts(frame, y, 8, frame))
    observed = (np.arange(len(y)), y)
    penalty = np.ones(x.shape[1])
    penalty[2] = distance_penalty

    def objective(beta):
        logits = offset + (x @ beta)[:, None] * burden
        regularization = penalty * beta
        loss = (logsumexp(logits, axis=1) - logits[observed]).sum() + beta @ regularization / 2
        gradient = x.T @ (softmax(logits, axis=1) @ burden - burden[y]) + regularization
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
    if model == "call_aware_hurdle":
        return hurdle(frame, evaluation, contexts, design=q3.features)
    if model == "rank_one_tilt":
        return rank_one(frame, evaluation, contexts)
    if model == "rank_one_distance_penalty":
        return rank_one(frame, evaluation, contexts, distance_penalty=8.)
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


def weibull_probabilities(training, evaluation, onset):
    """Fit an observed zero atom and a Weibull model for the positive waiting time."""
    def features(frame):
        return np.column_stack((frame.Type.eq("call"), np.log1p(frame.Distance)))

    keep = onset > 0
    event = np.isfinite(onset[keep])
    time = np.log(np.minimum(onset[keep], EDGES[-1]))
    scaler = StandardScaler().fit(features(training.loc[keep]))
    x = np.column_stack((np.ones(keep.sum()), scaler.transform(features(training.loc[keep]))))

    def objective(params):
        shift = time - x @ params[:3]
        shape = np.exp(params[3])
        log_hazard = shape * shift
        # The cap prevents overflow during line search far from the optimum.
        hazard = np.exp(np.minimum(log_hazard, 500.))
        density_term = params[3] + log_hazard - time
        penalty = params[1:]
        loss = hazard.sum() - density_term[event].sum() + penalty @ penalty / 2
        residual = np.where(log_hazard <= 500., hazard, 0.) - event
        gradient = np.r_[-shape * x.T @ residual, residual @ log_hazard - event.sum()]
        gradient[1:] += penalty
        return loss, gradient

    fitted = minimize(objective, np.array([np.log(60.), 0., 0., 0.]), jac=True, method="L-BFGS-B",
                      bounds=[(None, None), (None, None), (0., None), (-3., 3.)],
                      options={"maxiter": 1000, "ftol": 1e-12, "gtol": 1e-7})
    if not fitted.success:
        raise RuntimeError(f"Weibull AFT fit failed: {fitted.message}")
    design = scaler.transform(features(evaluation))
    log_scale = fitted.x[0] + design @ fitted.x[1:3]
    log_hazard = np.exp(fitted.x[3]) * (np.log(EDGES[1:]) - log_scale[:, None])
    survival = np.exp(-np.exp(np.minimum(log_hazard, 500.)))
    atom = stimulus_counts(training, (onset == 0).astype(int), 2, evaluation)[:, 1]
    positive_cells = np.column_stack((1-survival[:, 0], -np.diff(survival, axis=1), survival[:, -1]))
    return np.column_stack((atom, (1-atom[:, None])*positive_cells))


def responder_timing(frame, bins, evaluation):
    event = bins < 5
    return stimulus_counts(frame.loc[event], bins[event], 5, evaluation, pseudocount=0.)


def conditional_rate_table(frame):
    arms = pd.DataFrame({"Type": q3.STIMULI})
    bins = time_cells(recorded_onset(frame)[:, 0])
    rates = responder_timing(frame, bins, arms).cumsum(axis=1)
    return pd.DataFrame({"stimulus": np.repeat(q3.STIMULI, len(EDGES)),
                         "window_s": np.tile(EDGES, len(arms)),
                         "conditional_probability": rates.ravel()})


def factorized_probabilities(frame, evaluation, contexts, bins, mask_model):
    """Combine observable response by 60 s and the empirical timing among responders."""
    p = 1-predict_mask(frame, evaluation, mask_model, contexts)[:, 0]
    composition = responder_timing(frame, bins, evaluation)
    return np.column_stack((p[:, None] * composition, 1-p))


def predict_timing(frame, evaluation, model, contexts, endpoint="Any", bins=None,
                   onset=None, mask_model=None):
    """Return probabilities for five onset cells and no event by 60 s."""
    if onset is None and (bins is None or model == "weibull_aft"):
        onset = recorded_onset(frame)[:, ENDPOINTS.index(endpoint)]
    if bins is None:
        bins = time_cells(onset)
    if model == "stimulus_time":
        return stimulus_counts(frame, bins, 6, evaluation)
    if model == "weibull_aft":
        return weibull_probabilities(frame, evaluation, onset)
    if model == FACTOR_TIME:
        return factorized_probabilities(frame, evaluation, contexts, bins, mask_model)
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
    if model in ("stimulus_time", FACTOR_TIME):
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


def validate_timing(frame, contexts, mask_model):
    rows = []
    all_onsets = recorded_onset(frame)
    for date, train, test in purged_folds(frame):
        training, validation = frame.iloc[train], frame.iloc[test]
        for endpoint, onset in zip(ENDPOINTS, all_onsets.T):
            bins = time_cells(onset)
            models = (*ANY_TIMING_MODELS, FACTOR_TIME) if endpoint == "Any" else TIMING_MODELS
            for model in models:
                p = predict_timing(training, validation, model, contexts, endpoint, bins[train],
                                   onset=onset[train], mask_model=mask_model)
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


def select_mask(mask_summary, mask_delta):
    incumbent = "full_multinomial"
    candidates = MASK_MODELS[2:]
    differences = mask_delta.loc[mask_delta.reference.eq(incumbent)].set_index(
        ["scheme", "model", "metric"])
    rows = []
    for model in candidates:
        ordinary_loss = differences.loc[("ordinary", model, "mask_log_loss"), "ci_high"]
        ordinary_brier = differences.loc[("ordinary", model, "any_response_brier"), "ci_high"]
        tail_loss = max(differences.loc[(scheme, model, "mask_log_loss"), "difference"]
                        for scheme in ("tail", "actual_long"))
        tail_brier = max(differences.loc[(scheme, model, "any_response_brier"), "difference"]
                         for scheme in ("tail", "actual_long"))
        rows.append(dict(model=model, ordinary_logloss_upper=ordinary_loss,
                         ordinary_brier_upper=ordinary_brier, worst_tail_logloss=tail_loss,
                         worst_tail_brier=tail_brier,
                         logloss_pass=ordinary_loss < MASK_LIMITS["ordinary_logloss"],
                         brier_pass=ordinary_brier <= MASK_LIMITS["ordinary_brier"],
                         tail_pass=(tail_loss <= MASK_LIMITS["tail_logloss"]
                                    and tail_brier <= MASK_LIMITS["tail_brier"])))
    decisions = pd.DataFrame(rows)
    eligible = decisions.loc[decisions[["logloss_pass", "brier_pass", "tail_pass"]].all(axis=1), "model"]
    loss = mask_summary.query("scheme == 'ordinary' and metric == 'mask_log_loss'").set_index("model")
    selected = loss.loc[eligible].estimate.idxmin() if len(eligible) else incumbent
    decisions["selected"] = decisions.model.eq(selected)
    return selected, decisions


def select_timing(time_summary, time_delta):
    selected_timing = {}
    for endpoint in ENDPOINTS:
        result = time_delta.query("endpoint == @endpoint and model != @FACTOR_TIME")
        log_loss = result.query("metric == 'censored_log_loss'").set_index("model")
        brier = result.query("metric == 'integrated_brier'").set_index("model")
        valid = (log_loss.ci_high < 0) & (brier.difference <= 0)
        candidates = log_loss.loc[valid].index
        losses = time_summary.query("endpoint == @endpoint and metric == 'censored_log_loss'").set_index("model")
        selected_timing[endpoint] = losses.loc[candidates].estimate.idxmin() if len(candidates) else "stimulus_time"
    return selected_timing


def prediction_table(frame, contexts, weights, mask_model, timing_models):
    rows, masks = [], []
    median_size = float(frame.Npenguins.median())
    for endpoint in ENDPOINTS:
        distances = np.arange(20., 150.5, .5) if endpoint == "Any" else q3.REPRESENTATIVE
        grid = q3.probability_grid(distances, contexts, median_size)
        grid_columns = grid.iloc[::len(contexts)].rename(columns={"Type": "stimulus",
                          "assigned_call": "call", "Distance": "distance_m",
                          "Npenguins": "group_size"}).drop(columns="Context")
        models = (*ANY_TIMING_MODELS, FACTOR_TIME) if endpoint == "Any" else TIMING_MODELS
        planning_model = timing_models[endpoint]
        if endpoint == "Any" and planning_model == "stimulus_time":
            planning_model = FACTOR_TIME
        for model in models:
            probs = predict_timing(frame, grid, model, contexts, endpoint, mask_model=mask_model)
            agg = weights @ probs.reshape(-1, len(contexts), 6)
            cumulative = agg[:, :5].cumsum(axis=1)
            for i, edge in enumerate(EDGES):
                rows.append(grid_columns.assign(family="timing", endpoint=endpoint,
                           model=model, window_s=edge, probability=cumulative[:, i],
                           selected=model == planning_model,
                           validated_selection=model == timing_models[endpoint]))
        if endpoint == "Any":
            for model in dict.fromkeys(("full_multinomial", mask_model)):
                p = predict_mask(frame, grid, model, contexts)
                mean = np.einsum("c,rcm->rm", weights, p.reshape(-1, len(contexts), 8))
                rows.append(grid_columns.assign(family="mask", endpoint=endpoint, model=model,
                           window_s=60, probability=1-mean[:, 0], selected=model == mask_model,
                           validated_selection=model == mask_model))
                if model == mask_model:
                    mask_rows = grid_columns.assign(model=model)
                    for i in q3.MASKS:
                        mask_rows[f"mask_{i}"] = mean[:, i]
                    masks.append(mask_rows[mask_rows.distance_m.isin(q3.REPRESENTATIVE)])
    return pd.concat(rows, ignore_index=True), pd.concat(masks, ignore_index=True)


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
    mask_long = mask.query("scheme == 'tail' and distance_m >= 125").assign(scheme="actual_long")
    mask = pd.concat((mask, mask_long), ignore_index=True)
    mask_metrics = ["mask_log_loss", "any_response_brier"]
    timing_metrics = ["censored_log_loss", "integrated_brier", "conditional_mae_s"]
    mask_scores_table, mask_delta = pool_scores(mask, ["scheme"], mask_metrics,
                                                MASK_MODELS[:2])
    selected_mask, decisions = select_mask(mask_scores_table, mask_delta)
    timing = validate_timing(frame, contexts, selected_mask)
    timing_scores_table, time_delta = pool_scores(timing, ["endpoint"], timing_metrics,
                                                  TIMING_MODELS[:1])
    selected_timing = select_timing(timing_scores_table, time_delta)
    predictions, representative_masks = prediction_table(
        frame, contexts, context_weights.to_numpy(), selected_mask, selected_timing)
    tables = {
        "coverage": coverage,
        "mask_scores": mask_scores_table,
        "mask_deltas": mask_delta,
        "mask_date_scores": mask.groupby(["scheme", "date", "model"])[mask_metrics].mean().reset_index(),
        "timing_scores": timing_scores_table,
        "timing_deltas": time_delta,
        "timing_date_scores": timing.groupby(["endpoint", "date", "model"])[timing_metrics].mean().reset_index(),
        "predictions": predictions,
        "representative_masks": representative_masks,
        "conditional_rates": conditional_rate_table(frame),
        "mask_decision": decisions,
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
