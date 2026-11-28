"""Estimate vocal transition information and propagate it through noise scenarios."""
import numpy as np
import pandas as pd
from scipy.special import rel_entr

import core_q2
import core_q3
import mechanistic_behavior as behavior
import mechanistic_propagation as propagation
from core_paper_figures import save_figure
from q4 import radius as gross_crossing
import q3


STATES = ("flat", "mod", "tv", "modflat")
LOG_TWO = np.log(2.)
DISTANCES = np.arange(20., 150.5, .5)
BACKGROUND_DB = (0., 3., 6.)
GROSS_CUTOFF = 0.28759819888730354


def weighted_transitions(frame):
    """Give each trial with at least two known replies unit transition weight."""
    fields = frame[[f"VR{i}" for i in range(1, 20)]]
    mapping = {state: i for i, state in enumerate(STATES)}
    recorded = fields.stack()
    if not recorded.isin(STATES).all():
        raise ValueError("An unknown vocal reply code occurs in Data02.")
    codes = fields.apply(lambda col: col.map(mapping)).fillna(-1).to_numpy(dtype=int)
    known_pairs = (codes[:, :-1] >= 0) & (codes[:, 1:] >= 0)
    lengths = known_pairs.sum(axis=1)
    trial, first = np.where(known_pairs)
    matrix = np.zeros((len(frame), len(STATES), len(STATES)))
    np.add.at(matrix, (trial, codes[trial, first], codes[trial, first+1]), 1 / lengths[trial])
    return matrix, lengths


def fit_channel(counts, labels):
    by_call = np.stack([counts[labels == c].sum(axis=0) for c in range(len(q3.CALLS))])
    pooled = by_call.sum(axis=0) + .5
    pooled /= pooled.sum(axis=-1, keepdims=True)
    smoothed = by_call + 8 * pooled
    q_call = smoothed / smoothed.sum(axis=-1, keepdims=True)
    previous = by_call.sum(axis=-1) + .5
    mixture = previous / previous.sum(axis=0, keepdims=True)
    q0 = np.sum(mixture[..., None] * q_call, axis=0)
    return q_call, q0, previous, by_call


def conditional_information(q_call, q0, previous, cue_retention):
    """Bits from the played-call cue after unobserved erasure."""
    result = np.zeros_like(cue_retention, dtype=float)
    for weight, predicted, reference in zip(previous, q_call, q0):
        for q, p in zip(predicted, reference):
            mixed = p + cue_retention * (q - p)
            result += weight * rel_entr(mixed, p)
    return np.maximum(result / LOG_TWO, 0.)


def vocal_analysis(frame):
    counts, lengths = weighted_transitions(frame)
    labels = pd.Categorical(frame.assigned_call, categories=q3.CALLS).codes
    eligible = frame.Type.eq("call").to_numpy() & (lengths > 0)
    rows = []
    for date, train, test in core_q3.purged_folds(frame):
        training = train[eligible[train]]
        validation = test[eligible[test]]
        q_call, q0, _, _ = fit_channel(counts[training], labels[training])
        labels_test = labels[validation]
        for model, probabilities in (("pooled_vr", q0), ("call_aware_vr", q_call[labels_test])):
            loss = -(counts[validation] * np.log2(probabilities)).sum(axis=(1, 2))
            rows.append(pd.DataFrame(dict(
                **behavior.fold_metadata(frame, date, validation), scheme="ordinary",
                model=model, transition_pairs=lengths[validation], log_loss_bits=loss,
            )))
    held_out = pd.concat(rows, ignore_index=True)
    scores = behavior.score_table(held_out, ["log_loss_bits"], ["pooled_vr"])

    q_call, q0, previous, weighted_counts = fit_channel(counts[eligible], labels[eligible])
    previous_given_call = previous / previous.sum(axis=-1, keepdims=True)
    local_weight = previous / previous.sum()
    entropy = -np.sum(q_call * np.log2(q_call), axis=-1)
    cross_entropy = -np.sum(q_call * np.log2(q0), axis=-1)
    information = [conditional_information(q_call[c], q0, previous_given_call[c], 1.)
                   for c in range(len(q3.CALLS))]
    totals = []
    for c, call in enumerate(q3.CALLS):
        tallied = eligible & (labels == c)
        totals.append(dict(
            call=call, trials=tallied.sum(), transitions=lengths[tallied].sum(),
            pooled_cross_entropy_bits=previous_given_call[c] @ cross_entropy[c],
            call_entropy_bits=previous_given_call[c] @ entropy[c],
            information_bits=float(information[c]),
        ))
    totals.append(dict(
        call="all", trials=eligible.sum(), transitions=lengths[eligible].sum(),
        pooled_cross_entropy_bits=np.sum(local_weight * cross_entropy),
        call_entropy_bits=np.sum(local_weight * entropy),
        information_bits=np.sum(local_weight.sum(axis=-1) * information),
    ))
    fit_table = pd.DataFrame([
        dict(call=call, previous_reply=STATES[x], next_reply=STATES[y],
             weighted_transitions=weighted_counts[c, x, y], previous_probability=previous_given_call[c, x],
             pooled_probability=q0[x, y], call_probability=q_call[c, x, y])
        for c, call in enumerate(q3.CALLS) for x in range(len(STATES)) for y in range(len(STATES))
    ])
    return (q_call, q0, previous_given_call, information), held_out, scores, pd.DataFrame(totals), fit_table


def noisy_fidelity(fidelity, ceiling, variance_multiplier):
    return ceiling / np.sqrt(1 + variance_multiplier * ((ceiling / fidelity)**2 - 1))


def integrated_radii(scenarios, group_response, channel):
    """Evaluate paired threshold crossings under the same weather and calibration draws."""
    parameters, alpha = scenarios
    q_call, q0, previous, information = channel
    use_100m = np.searchsorted(DISTANCES, 100.)
    rows = []
    for c, call in enumerate(q3.CALLS):
        base = core_q2.absorption_curve(DISTANCES, parameters[:, c], alpha[:, c])
        ceiling = parameters[:, c, :1]
        natural30, control30 = group_response[30][:, c]
        natural60, control60 = group_response[60][:, c]
        excess30 = np.maximum(natural30 - control30, 0.)
        excess60 = np.maximum(natural60 - control60, 0.)
        for db in BACKGROUND_DB:
            fidelity = noisy_fidelity(base, ceiling, 10**(db/10)) if db else base
            variance_retained = (fidelity / base)**2
            links = {"acoustic_only": np.ones_like(base)}
            if db:
                retained = conditional_information(q_call[c], q0, previous[c], variance_retained)
                links["entropy_transfer"] = retained/information[c] if information[c] > 0 else links["acoustic_only"]
            reference_radius = None
            for link, retention in links.items():
                probability = natural30 - (1-retention)*excess30
                probability60 = natural60 - (1-retention)*excess60
                met = (fidelity >= .5) & (probability >= .5)
                n_pass = np.logical_and.accumulate(met, axis=1).sum(axis=1)
                radius = DISTANCES[np.maximum(n_pass-1, 0)]
                if reference_radius is None:
                    reference_radius = radius
                low, center, high = np.quantile(radius, propagation.PERCENTILES,
                                                method="inverted_cdf")
                drop_low, drop_center, drop_high = np.quantile(
                    reference_radius - radius, propagation.PERCENTILES, method="inverted_cdf")
                gross_radii, gross_status = zip(*(
                    gross_crossing(DISTANCES, curve, GROSS_CUTOFF)
                    for curve in fidelity * probability60
                ))
                gross_low, gross_center, gross_high = np.quantile(gross_radii, propagation.PERCENTILES)
                rows.append(dict(
                    call=call, noise_increase_db=db, behavior=link,
                    p05_m=low, median_m=center, p95_m=high,
                    paired_reduction_p05_m=drop_low, paired_reduction_median_m=drop_center,
                    paired_reduction_p95_m=drop_high,
                    below_support=(n_pass == 0).sum(), above_support=(n_pass == len(DISTANCES)).sum(),
                    fidelity_retention_100m=np.median(variance_retained[:, use_100m]**.5),
                    behavior_excess_retention_100m=np.median(retention[:, use_100m]),
                    natural_p30_100m=np.median(probability[:, use_100m]),
                    natural_p60_100m=np.median(probability60[:, use_100m]),
                    gross_p05_m=gross_low, gross_median_m=gross_center, gross_p95_m=gross_high,
                    gross_below_support=gross_status.count("below_support"),
                    gross_above_support=gross_status.count("above_support"),
                    gross_cutoff=GROSS_CUTOFF, draws=len(radius),
                ))
    return pd.DataFrame(rows)


def plot_radii(acoustic, communication, output):
    """Compare modeled radius distributions on a common distance scale."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    acoustic = acoustic.loc[acoustic.threshold.eq(.50) & acoustic.regime.eq("joint")].copy()
    display = communication[communication.noise_increase_db.gt(0)].copy()
    kinds = ("flat", "mod", "tv")
    labels = ("Flat", "Modulated", "Two-voice")
    teal, gray, ink = "#17686a", "#777f88", "#29323c"
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.3, 3.5), sharey=True,
                                      gridspec_kw={"wspace": .12})
    fig.subplots_adjust(left=.17, right=.98, bottom=.31, top=.89)
    y = {"flat": 2, "mod": 1, "tv": 0}

    def interval(ax, row, position, color, marker):
        ax.errorbar(row.median_m, position,
                    xerr=[[row.median_m-row.p05_m], [row.p95_m-row.median_m]],
                    ms=3.3, lw=1.35, capsize=2.5, color=color, marker=marker, mfc="white",
                    mew=1.15, zorder=3)

    for row in acoustic.itertuples():
        interval(left, row, y[row.call]+.10, teal, "D")
        left.plot(row.reference_m, y[row.call]-.11, marker="x", color=gray, ms=5)
    for (call, noise), group in display.groupby(["call", "noise_increase_db"], sort=False):
        position = y[call] + (.17 if noise == 3 else -.17)
        by_link = group.set_index("behavior")
        x1 = by_link.loc["acoustic_only", "median_m"]
        x2 = by_link.loc["entropy_transfer", "median_m"]
        right.hlines(position, min(x1, x2), max(x1, x2), color="#c5cbd0", lw=1, zorder=2)
        marker = "o" if noise == 3 else "s"
        interval(right, by_link.loc["acoustic_only"], position, gray, marker)
        interval(right, by_link.loc["entropy_transfer"], position, teal, marker)
    left.set_title("A  Acoustic propagation", loc="left", fontsize=10, color=ink, pad=9)
    right.set_title("B  Joint 30 s planning", loc="left", fontsize=10, color=ink, pad=9)
    left.set(yticks=[y[call] for call in kinds], yticklabels=labels, ylim=(-.55, 2.55))
    right.tick_params(axis="y", labelleft=False)
    for ax in (left, right):
        ax.set(xlim=(15, 195), xticks=(20, 60, 100, 140, 180), xlabel="Radius (m)")
        ax.grid(axis="x", color="#e0e4e7", lw=.7)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.spines["bottom"].set_color("#9ba2a8")
        ax.tick_params(axis="both", length=0, labelsize=9)
        ax.xaxis.label.set_size(9)
    left.legend(handles=[
        Line2D([], [], marker="D", color=teal, mfc="white", label="Weather and fit"),
        Line2D([], [], marker="x", color=gray, ls="", label="Fixed reference"),
    ], loc="upper center", bbox_to_anchor=(.5, -.20), fontsize=8, frameon=False, ncol=1)
    right.legend(handles=[
        Line2D([], [], color=gray, label="Acoustic only"),
        Line2D([], [], color=teal, label="Entropy transfer"),
        Line2D([], [], marker="o", color=ink, mfc="white", ls="", label="+3 dB"),
        Line2D([], [], marker="s", color=ink, mfc="white", ls="", label="+6 dB"),
    ], loc="upper center", bbox_to_anchor=(.50, -.20), fontsize=8, columnspacing=1.1,
       frameon=False, ncol=2)
    acoustic = acoustic.assign(panel="A")
    display = display.assign(panel="B")
    save_figure(fig, pd.concat((acoustic, display), ignore_index=True), output, "mechanistic_ranges",
                panels={"A": "0.50 acoustic fidelity crossing", "B": "0.50 fidelity and 0.50 natural response by 30 s"},
                intervals="5th and 95th percentiles of 10,000 paired climate and fit scenarios",
                distance_unit="m")


def run(data, output):
    frame = q3.load_playbacks(data)
    contexts = tuple(sorted(frame.Context.unique()))
    bins = core_q3.time_cells(core_q3.recorded_onset(frame)[:, 0])
    selected, penalty, mask_oof, mask_scores, settings = behavior.validate_interactions(frame, contexts)
    risk, response, implied = behavior.standardized_response(frame, contexts, bins, selected, penalty, DISTANCES)
    timing_oof, timing_scores, responder_counts = behavior.group_timing(frame, contexts, bins)
    channel, vr_oof, vr_scores, information, transitions = vocal_analysis(frame)
    climate, radii = propagation.scenarios(data)
    joint = integrated_radii(climate, risk, channel)
    outputs = {
        "mechanistic_q2_radii": radii,
        "mechanistic_q3_scores": mask_scores,
        "mechanistic_q3_folds": settings,
        "mechanistic_q3_oof": mask_oof,
        "mechanistic_q3_probabilities": response,
        "mechanistic_vr_scores": vr_scores,
        "mechanistic_vr_oof": vr_oof,
        "mechanistic_vr_information": information,
        "mechanistic_vr_transitions": transitions,
        "mechanistic_q4_radii": joint,
        "mechanistic_latency_scores": timing_scores,
        "mechanistic_latency_oof": timing_oof,
        "mechanistic_latency_responders": responder_counts,
        "mechanistic_latency_fixed_risk": implied,
    }
    output.mkdir(parents=True, exist_ok=True)
    plot_radii(radii, joint, output)
    for name, table in outputs.items():
        table.to_csv(output / f"{name}.csv", index=False, lineterminator="\n")
