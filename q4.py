"""Combine the acoustic and behavioral predictions on their common support."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def radius(distance, index, cutoff):
    """Use the last qualifying point to identify a sustained decline."""
    above = np.flatnonzero(index >= cutoff)
    if not above.size:
        return float(distance[0]), "below_support"
    j = above[-1]
    if j == len(distance) - 1:
        return float(distance[j]), "above_support"
    crossing = np.interp(cutoff, index[j:j + 2][::-1], distance[j:j + 2][::-1])
    return float(crossing), "crossing"


def environment(fidelity, natural, control, loss, threshold):
    altered = np.clip(fidelity * (1 - loss), 0, 1)
    retention = np.full_like(altered, 1 - loss)
    if threshold:
        retention = np.where(altered >= threshold, retention, 0)
    probability = natural - (1 - retention) * np.maximum(natural - control, 0)
    index = altered * probability
    if threshold:
        index = np.where(altered >= threshold, index, 0)
    return index, probability


def scenario_comparisons(distance, calls, fidelity, natural, control,
                         fidelity_draws, natural_draws, control_draws, output):
    clean = fidelity * natural
    clean_draws = fidelity_draws * natural_draws
    relative = .5 * clean[:, 0]
    relative_draws = .5 * clean_draws[:, :, 0]
    common = relative.mean()
    common_draws = relative_draws.mean(axis=1)
    policies = {
        "call_specific": (relative, relative_draws),
        "common": (np.full_like(relative, common),
                   np.broadcast_to(common_draws[:, None], relative_draws.shape)),
    }
    positions = np.flatnonzero(np.isin(distance, (20, 50, 100, 150)))
    radii, curves, comparisons = [], [], []
    for loss in (0, .05, .10, .15, .20):
        acoustic = fidelity * (1 - loss) * natural
        acoustic_draws = fidelity_draws * (1 - loss) * natural_draws
        coupled, coupled_p = environment(fidelity, natural, control, loss, 0)
        coupled_draws, coupled_p_draws = environment(
            fidelity_draws, natural_draws, control_draws, loss, 0,
        )
        if np.any(coupled > acoustic + 1e-12) or np.any(acoustic > clean + 1e-12):
            raise ValueError("Loss scenarios must reduce or preserve clean effectiveness")
        variants = (("clean", clean, clean_draws, natural, natural_draws),) if loss == 0 else (
            ("acoustic_only", acoustic, acoustic_draws, natural, natural_draws),
            ("coupled", coupled, coupled_draws, coupled_p, coupled_p_draws),
        )
        for link, index, boot, probability, p_draws in variants:
            low, high = np.quantile(boot, [.025, .975], axis=0)
            p_low, p_high = np.quantile(p_draws, [.025, .975], axis=0)
            if loss == 0:
                for i, j in ((1, 0), (2, 0), (2, 1)):
                    deltas = boot[:, i, positions] - boot[:, j, positions]
                    interval = np.quantile(deltas, [.025, .975], axis=0)
                    for k, pos in enumerate(positions):
                        comparisons.append({
                            "distance_m": distance[pos], "call": calls[i], "reference_call": calls[j],
                            "difference": index[i, pos] - index[j, pos],
                            "low": interval[0, k], "high": interval[1, k],
                        })
            for policy, (cutoffs, draw_cutoffs) in policies.items():
                for i, call in enumerate(calls):
                    cutoff = cutoffs[i]
                    estimate, status = radius(distance, index[i], cutoff)
                    draws = [radius(distance, values, c)
                             for values, c in zip(boot[:, i], draw_cutoffs[:, i])]
                    bounded_low, bounded_high = np.quantile([v for v, _ in draws], [.025, .975])
                    radii.append({
                        "threshold_policy": policy, "response_link": link, "loss": loss,
                        "call": call, "clean_cutoff": cutoff, "radius_m": estimate, "status": status,
                        "bounded_low_m": bounded_low, "bounded_high_m": bounded_high,
                        "draws_below_support": sum(s == "below_support" for _, s in draws),
                        "draws_above_support": sum(s == "above_support" for _, s in draws),
                    })
                    # Store the full comparison curves used by the figure and the audit.
                    curves.extend({
                        "threshold_policy": policy, "response_link": link, "loss": loss,
                        "call": call, "distance_m": d, "clean_cutoff": cutoff,
                        "index": index[i, k], "low": low[i, k], "high": high[i, k],
                        "response_probability": probability[i, k], "response_low": p_low[i, k],
                        "response_high": p_high[i, k], "meets_cutoff": index[i, k] >= cutoff,
                        "bootstrap_share_meeting_cutoff": (boot[:, i, k] >= draw_cutoffs[:, i]).mean(),
                    } for k, d in enumerate(distance))
    pd.DataFrame(radii).to_csv(output / "q4_comparison_radii.csv", index=False)
    pd.DataFrame(comparisons).to_csv(output / "q4_clean_index_differences.csv", index=False)
    frame = pd.DataFrame(curves)
    frame.to_csv(output / "q4_comparison_curves.csv", index=False)
    plot_comparisons(frame, calls, output)


def plot_comparisons(frame, calls, output):
    plotted = frame.loc[frame.threshold_policy.eq("common") & frame.loss.isin((0, .20))].copy()
    plotted.to_csv(output / "q4_loss_comparison.csv", index=False)
    figure, axes = plt.subplots(1, 3, figsize=(10, 3.5), sharex=True, sharey=True)
    styles = {
        "clean": ("#17686a", "-", "Clean"),
        "acoustic_only": ("#533d80", "--", "20% acoustic loss only"),
        "coupled": ("#a24c1f", "-.", "20% loss with response change"),
    }
    for axis, call, name in zip(axes, calls, ("Flat", "Modulated", "Two-voice")):
        block = plotted.loc[plotted.call.eq(call)]
        for link, (color, linestyle, label) in styles.items():
            series = block.loc[block.response_link.eq(link)]
            axis.plot(series.distance_m, series["index"], label=label, color=color, ls=linestyle, lw=1.7)
            if link == "clean":
                axis.fill_between(series.distance_m, series.low, series.high, color=color, alpha=.13)
        axis.axhline(block.clean_cutoff.iloc[0], color="#686868", lw=1, ls=":", label="Common cutoff")
        axis.set_title(name)
        axis.set_xlabel("Distance (m)")
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Communication effectiveness")
    handles, labels = axes[-1].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", ncol=4, frameon=False)
    figure.tight_layout(rect=(0, 0, 1, .9))
    figure.savefig(output / "q4_loss_comparison.png", dpi=300)
    plt.close(figure)
    (output / "q4_loss_comparison.meta.json").write_text(json.dumps({
        "sources": ["Data02–Data11", "docs/model-spec.md"],
        "support_m": [20, 150], "bands": "95% conditional combined bootstrap interval for clean",
        "threshold": "half the equal-call mean clean index at 20 m",
        "loss": .20, "response_links": list(styles),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")



def run(propagation, behavior, output):
    distance = propagation["distance"]
    calls = tuple(propagation["calls"])
    if calls != tuple(behavior["calls"]) or not np.array_equal(distance, behavior["distance"]):
        raise ValueError("Propagation and behavior must share call order and distance grid")
    fidelity = propagation["fidelity"]
    natural, control = behavior["natural"], behavior["control"]
    fidelity_draws = propagation["draws"]
    natural_draws, control_draws = behavior["natural_draws"], behavior["control_draws"]
    if fidelity_draws.shape != natural_draws.shape or natural_draws.shape != control_draws.shape:
        raise ValueError("Bootstrap arrays must share shape (draw, call, distance)")

    scenario_comparisons(distance, calls, fidelity, natural, control,
                         fidelity_draws, natural_draws, control_draws, output)

    specifications = [
        ("clean", 0, 0), ("threshold_0.50", 0, .50), ("threshold_0.60", 0, .60), ("threshold_0.70", 0, .70),
        *[(f"loss_{percent:02d}", percent / 100, 0) for percent in (5, 10, 15, 20)],
    ]
    records, curves, individuals = [], [], []
    clean = fidelity * natural
    clean_draws = fidelity_draws * natural_draws
    for scenario, loss, threshold in specifications:
        index, probability = environment(fidelity, natural, control, loss, threshold)
        boot, boot_probability = environment(fidelity_draws, natural_draws, control_draws, loss, threshold)
        if np.any(index > clean + 1e-12) or np.any(probability > natural + 1e-12):
            raise ValueError(f"Environmental scenario increases clean response: {scenario}")
        for i, call in enumerate(calls):
            for fraction in (.4, .5, .6):
                cutoff = clean[i, 0] * fraction
                estimate, status = radius(distance, index[i], cutoff)
                draw_results = [
                    radius(distance, values, reference[0] * fraction)
                    for values, reference in zip(boot[:, i], clean_draws[:, i])
                ]
                low, high = np.quantile([value for value, _ in draw_results], [.025, .975])
                records.append({
                    "call": call, "scenario": scenario, "reference_fraction": fraction,
                    "clean_cutoff": cutoff, "radius_m": estimate, "status": status,
                    "bounded_low_m": low, "bounded_high_m": high,
                    "draws_below_support": sum(s == "below_support" for _, s in draw_results),
                    "draws_above_support": sum(s == "above_support" for _, s in draw_results),
                })
            low, high = np.quantile(boot[:, i], [.025, .975], axis=0)
            p_low, p_high = np.quantile(boot_probability[:, i], [.025, .975], axis=0)
            for j, d in enumerate(distance):
                curves.append({
                    "call": call, "scenario": scenario, "distance_m": d,
                    "index": index[i, j], "low": low[j], "high": high[j],
                    "response_probability": probability[i, j],
                    "response_low": p_low[j], "response_high": p_high[j],
                })
                if d in (50, 100, 150):
                    for share in (.25, .5, .75):
                        count = max(1., 8 * share)
                        individuals.append({
                            "call": call, "scenario": scenario, "distance_m": d,
                            "assumed_share_if_responding": share,
                            "expected_responders": count * probability[i, j],
                            "low": count * p_low[j], "high": count * p_high[j],
                        })
    pd.DataFrame(records).to_csv(output / "q4_radii.csv", index=False)
    pd.DataFrame(individuals).to_csv(output / "q4_expected_responders.csv", index=False)
    sensitivity = []
    for i, call in enumerate(calls):
        alternatives = [("acoustics", fidelity[i]), ("behavior", natural[i]), ("combined", clean[i])]
        for name, values in alternatives:
            estimate, status = radius(distance, values, .5 * values[0])
            sensitivity.append({"call": call, "model": name, "radius_m": estimate, "status": status})
        for name, alternate in propagation.get("alternate_fidelity", {}).items():
            values = np.asarray(alternate)[i] * natural[i]
            estimate, status = radius(distance, values, .5 * values[0])
            sensitivity.append({"call": call, "model": name, "radius_m": estimate, "status": status})
    pd.DataFrame(sensitivity).to_csv(output / "q4_model_comparison.csv", index=False)

    plots = pd.DataFrame(curves)
    plots.to_csv(output / "q4_environment_curves.csv", index=False)
    plots = plots[plots.scenario.isin(("clean", "loss_20", "threshold_0.60"))].copy()
    figure, axes = plt.subplots(1, 3, figsize=(10, 3.5), sharex=True, sharey=True)
    styles = {"clean": ("#17686a", "Clean"), "loss_20": ("#a24c1f", "20% loss"),
              "threshold_0.60": ("#533d80", "Threshold 0.60")}
    for i, (axis, call) in enumerate(zip(axes, calls)):
        for scenario, (color, label) in styles.items():
            block = plots[(plots.call == call) & (plots.scenario == scenario)]
            axis.plot(block.distance_m, block["index"], color=color, label=label, lw=1.8)
            if scenario == "clean":
                axis.fill_between(block.distance_m, block.low, block.high, color=color, alpha=.16)
        axis.axhline(.5 * clean[i, 0], color="#686868", lw=1, ls=":")
        axis.set_title(("Flat", "Modulated", "Two-voice")[i])
        axis.set_xlabel("Distance (m)")
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Communication effectiveness")
    handles, labels = axes[-1].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", ncol=3, frameon=False)
    figure.tight_layout(rect=(0, 0, 1, .9))
    figure.savefig(output / "q4_scenarios.png", dpi=300)
    plt.close(figure)
    plots.to_csv(output / "q4_scenarios.csv", index=False)
    (output / "q4_scenarios.meta.json").write_text(json.dumps({
        "sources": ["Data02–Data11", "docs/model-spec.md"],
        "support_m": [20, 150], "bands": "95% conditional combined bootstrap interval",
        "threshold": "50% of clean index at 20 m, per call",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")



