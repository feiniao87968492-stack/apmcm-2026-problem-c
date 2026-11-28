"""Validate call-by-distance effects and individual-hazard assumptions on group outcomes."""
from itertools import product

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.preprocessing import StandardScaler

import core_q3
import q3
from round2 import mask_scores

MASK_MODELS = ("rank_one_distance_penalty", "call_main", "call_by_distance")
INTERACTION_PENALTIES = (128., 32., 8., 2.)
LATENCY_MODELS = {
    "iid_fixed_size": (0., False),
    "frailty_fixed_size": (1., False),
    "iid_free_size": (0., True),
    "frailty_free_size": (1., True),
}
WINDOW_CELL = np.searchsorted(core_q3.EDGES, 30)
SCORE_FLOOR = 1e-12


def mask_predictions(training, evaluation, contexts, model, penalty):
    return core_q3.rank_one(
        training, evaluation, contexts, distance_penalty=8.,
        call_penalty=None if model == MASK_MODELS[0] else 8.,
        interaction_penalty=penalty if model == MASK_MODELS[2] else None,
    )


def tune_interaction(frame, contexts):
    loss = np.zeros(len(INTERACTION_PENALTIES))
    for _, fit_rows, valid_rows in core_q3.purged_folds(frame):
        train, valid = frame.iloc[fit_rows], frame.iloc[valid_rows]
        for index, penalty in enumerate(INTERACTION_PENALTIES):
            probability = mask_predictions(train, valid, contexts, MASK_MODELS[2], penalty)
            loss[index] += mask_scores(probability, valid["mask"].to_numpy())[:, 0].sum()
    return INTERACTION_PENALTIES[np.argmin(loss)]


def fold_metadata(frame, date, indices):
    trial = frame.iloc[indices]
    return dict(date=date, position=indices, expID=trial.expID.to_numpy(),
                stimulus=trial.Type.to_numpy(), call=trial.assigned_call.to_numpy(),
                distance_m=trial.Distance.to_numpy(), birds=trial.Npenguins.to_numpy())


def score_table(rows, metrics, references):
    summary, deltas = core_q3.pool_scores(rows, ["scheme"], metrics, references)
    return summary.merge(deltas, how="left", on=["scheme", "model", "metric"])


def validate_interactions(frame, contexts):
    predictions, settings = [], []
    names = ["mask_log_loss", "any_response_brier"]
    for tail in (False, True):
        scheme = "actual_long" if tail else "ordinary"
        for date, train, test in core_q3.purged_folds(frame, tail=tail):
            if tail:
                test = test[frame.Distance.iloc[test].ge(125).to_numpy()]
            if len(test) == 0:
                continue
            training, evaluation = frame.iloc[train], frame.iloc[test]
            penalty = tune_interaction(training, contexts)
            settings.append(dict(scheme=scheme, date=date, train_pairs=len(train)//2,
                                 test_trials=len(test), interaction_penalty=penalty))
            metadata = fold_metadata(frame, date, test)
            response = evaluation["mask"].to_numpy()
            for model in MASK_MODELS:
                p = mask_predictions(training, evaluation, contexts, model, penalty)
                scored = dict(zip(names, mask_scores(p, response).T))
                predictions.append(pd.DataFrame(dict(
                    **metadata, scheme=scheme, model=model, observed_mask=response,
                    probability_observed=p[np.arange(len(p)), response], any_probability=1-p[:, 0], **scored,
                )))

    predictions = pd.concat(predictions, ignore_index=True)
    scores = score_table(predictions, names, MASK_MODELS[:2])
    contrasts = scores.set_index(["scheme", "model", "reference", "metric"]).sort_index()
    qualifying = []
    for model in MASK_MODELS[1:]:
        logloss = contrasts.loc[("ordinary", model, MASK_MODELS[0], names[0])]
        brier = contrasts.loc[("ordinary", model, MASK_MODELS[0], names[1])]
        tail = contrasts.loc[("actual_long", model, MASK_MODELS[0])]
        beat_main = (model == MASK_MODELS[1] or
                     contrasts.loc[("ordinary", model, MASK_MODELS[1], names[0]), "ci_high"] < 0)
        if (logloss.ci_high < 0 and beat_main and brier.ci_high <= .01
                and tail.loc[names[0], "difference"] <= .10 and tail.loc[names[1], "difference"] <= .02):
            qualifying.append((logloss.estimate, model))
    selected = min(qualifying)[1] if qualifying else MASK_MODELS[0]
    scores["selected"] = scores.model.eq(selected)
    settings = pd.DataFrame(settings)
    full_penalty = tune_interaction(frame, contexts)
    settings.loc[len(settings)] = ["full", "", len(frame)//2, 0, full_penalty]
    return selected, full_penalty, predictions, scores, settings


def log_survival(cumulative, theta):
    return -np.log1p(theta*cumulative)/theta if theta else -cumulative


def latency_design(frame, contexts):
    return np.delete(core_q3.compact_design(frame, contexts), 2, axis=1)


def fit_group_latency(training, bins, evaluation, contexts, theta, free_size):
    """Group first-event survival and marginal bird survival under a shared frailty."""
    x = latency_design(training, contexts)
    scaler = StandardScaler().fit(x)
    x = scaler.transform(x)
    n_train = np.log(training.Npenguins.to_numpy())
    start = np.r_[np.repeat(np.log(.1), len(core_q3.EDGES)), np.zeros(x.shape[1])]
    limits = [(-9., 2.5)] * len(core_q3.EDGES) + [(-6., 6.)] * x.shape[1]
    if free_size:
        start = np.r_[start, 1.]
        limits.append((-2., 2.))

    def evaluate(parameters, design, log_size):
        increments = parameters[:len(core_q3.EDGES)]
        beta = parameters[len(increments):len(increments)+x.shape[1]]
        kappa = parameters[-1] if free_size else 1.
        cumulative = np.exp(design @ beta + kappa*log_size)[:, None] * np.exp(increments).cumsum()
        survival = log_survival(cumulative, theta)
        previous = np.column_stack((np.zeros(len(survival)), survival[:, :-1]))
        event_mass = np.exp(previous) * -np.expm1(survival - previous)
        probabilities = np.column_stack((event_mass, np.exp(survival[:, -1])))
        return probabilities, cumulative, kappa

    observed = (np.arange(len(bins)), bins)

    def objective(parameters):
        probability, _, _ = evaluate(parameters, x, n_train)
        delta = parameters - start
        delta[:len(core_q3.EDGES)] *= np.sqrt(.1)
        return -np.log(probability[observed].clip(SCORE_FLOOR, 1.)).sum() + delta @ delta/2

    fit = minimize(objective, start, method="L-BFGS-B", bounds=limits,
                   options={"maxiter": 500, "ftol": 1e-10})
    if not fit.success:
        raise RuntimeError(f"Group latency fit failed: {fit.message}")
    p, cumulative, kappa = evaluate(fit.x, scaler.transform(latency_design(evaluation, contexts)),
                                    np.log(evaluation.Npenguins.to_numpy()))
    bird_p30 = -np.expm1(log_survival(cumulative[:, WINDOW_CELL]/evaluation.Npenguins.to_numpy(),
                                   theta))
    return p, bird_p30, kappa


def trials_by_context(contexts, distances, birds):
    return pd.MultiIndex.from_product(
        [q3.STIMULI, q3.CALLS, distances, contexts],
        names=["Type", "assigned_call", "Distance", "Context"],
    ).to_frame(index=False).assign(Npenguins=birds)


def group_timing(frame, contexts, bins):
    evaluation = trials_by_context(contexts, (100.,), 8)
    weight = evaluation.Context.map(
        frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True)).to_numpy()
    scored, estimates = [], []
    names = ("stimulus_time", core_q3.FACTOR_TIME, *LATENCY_MODELS)
    for date, train, test in core_q3.purged_folds(frame):
        validation = frame.iloc[test]
        metadata = fold_metadata(frame, date, test)
        for name in names:
            if name in LATENCY_MODELS:
                probability, _, kappa = fit_group_latency(frame.iloc[train], bins[train],
                                                          validation, contexts, *LATENCY_MODELS[name])
            else:
                probability = core_q3.predict_timing(frame.iloc[train], validation, name, contexts,
                                                     bins=bins[train], mask_model=MASK_MODELS[0])
                kappa = np.nan
            p30 = probability[:, :WINDOW_CELL+1].sum(axis=1)
            loss = -np.log(probability[np.arange(len(test)), bins[test]].clip(SCORE_FLOOR, 1.))
            scored.append(pd.DataFrame(dict(
                **metadata, scheme="ordinary", model=name, size_exponent=kappa, onset_cell=bins[test],
                p30=p30, bin_log_loss=loss, brier30=(p30-(bins[test] <= WINDOW_CELL))**2,
            )))

    scored = pd.concat(scored, ignore_index=True)
    strata = pd.concat((scored, scored[scored.birds.eq(1)].assign(scheme="singleton")), ignore_index=True)
    references = ["stimulus_time", core_q3.FACTOR_TIME, "iid_fixed_size", "frailty_fixed_size"]
    scores = score_table(strata, ["bin_log_loss", "brier30"], references)
    for name, (theta, free_size) in LATENCY_MODELS.items():
        probability, individual, kappa = fit_group_latency(frame, bins, evaluation, contexts, theta, free_size)
        p30 = probability[:, :WINDOW_CELL+1].sum(axis=1)
        for arm in q3.STIMULI:
            keep = evaluation.Type.eq(arm) & evaluation.assigned_call.eq("flat")
            group = p30[keep] @ weight[keep]
            expected = 8 * (individual[keep] @ weight[keep])
            estimates.append(dict(model=name, stimulus=arm, birds=8, distance_m=100.,
                                  frailty_variance=theta, size_exponent=kappa, group_probability=group,
                                  expected_responders=expected, lower=group, upper=8*group))
    return scored, scores, pd.DataFrame(estimates)


def standardized_response(frame, contexts, bins, selected, penalty, distances):
    """Use the selected rank-one mask and stimulus-conditional response timing."""
    grid = trials_by_context(contexts, distances, 8)
    weight = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).reindex(contexts).to_numpy()
    conditional_cdf = core_q3.responder_timing(frame, bins, grid)[:, :WINDOW_CELL+1].sum(axis=1)
    shape = (len(q3.STIMULI), len(q3.CALLS), len(distances), len(contexts))
    rows = []
    for name in MASK_MODELS:
        p60 = 1-mask_predictions(frame, grid, contexts, name, penalty)[:, 0]
        by_context = (p60 * conditional_cdf).reshape(shape)
        natural_and_control = by_context @ weight
        summary60 = p60.reshape(shape) @ weight
        if name == selected:
            prediction = {30: natural_and_control, 60: summary60}
            individual_scenarios = implied_at_same_group_risk(
                by_context[:, :, np.searchsorted(distances, 100.)], weight)
        for arm, call, distance in product(q3.STIMULI, q3.CALLS, (50., 100., 150.)):
            index = (q3.STIMULI.index(arm), q3.CALLS.index(call), np.searchsorted(distances, distance))
            rows.append(dict(model=name, selected=name == selected, stimulus=arm, call=call,
                             distance_m=distance, birds=8, p60=summary60[index],
                             p30=natural_and_control[index]))
    return prediction, pd.DataFrame(rows), individual_scenarios


def implied_at_same_group_risk(group_probabilities, context_weights):
    """Compare dependence assumptions at common group risks in every context."""
    rows = []
    for a, arm in enumerate(q3.STIMULI):
        for c, call in enumerate(q3.CALLS):
            probability = group_probabilities[a, c]
            survival = 1 - probability
            group_mean = probability @ context_weights
            for theta in (0., 1.):
                cumulative = (survival**(-theta)-1)/theta if theta else -np.log(survival)
                individual = -np.expm1(log_survival(cumulative/8, theta))
                rows.append(dict(stimulus=arm, call=call, distance_m=100., birds=8,
                                 frailty_variance=theta, group_probability=group_mean,
                                 expected_responders=8 * (individual @ context_weights),
                                 lower=group_mean, upper=8*group_mean))
    return pd.DataFrame(rows)
