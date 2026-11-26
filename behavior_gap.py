"""Decompose natural-minus-control behavior probability gaps."""
import numpy as np
import pandas as pd

import q3

EVENTS = (*q3.BEHAVIORS, *(f"mask_{i}" for i in q3.MASKS[1:]))
INDICATORS = np.column_stack((q3.BITS, np.eye(len(q3.MASKS), dtype=int)[:, 1:]))


def divide(numerator, denominator):
    out = np.full(np.shape(numerator), np.nan, dtype=float)
    return np.divide(numerator, denominator, out=out, where=denominator > 0)


def components(probabilities):
    any_response = 1 - probabilities[..., 0]
    event = probabilities @ INDICATORS
    conditional = divide(event, any_response[..., None])
    p_n, p_c = any_response[..., 0, None], any_response[..., 1, None]
    q_n, q_c = conditional[..., 0, :], conditional[..., 1, :]
    gap = event[..., 0, :] - event[..., 1, :]
    frequency = (p_n - p_c) * (q_n + q_c) / 2
    composition = (p_n + p_c) * (q_n - q_c) / 2
    valid = np.isfinite(frequency)
    np.testing.assert_allclose((frequency + composition)[valid], gap[valid], atol=1e-12, rtol=0)
    return dict(
        p_natural=np.broadcast_to(p_n, gap.shape), p_control=np.broadcast_to(p_c, gap.shape),
        q_natural=q_n, q_control=q_c, marginal_natural=event[..., 0, :],
        marginal_control=event[..., 1, :], gap=gap,
        frequency=frequency, composition=composition,
    )


def summarize(point, draws, **labels):
    estimates, samples = components(point), components(draws)
    for i, event in enumerate(EVENTS):
        row = dict(labels, event=event, draws=len(draws))
        both = np.isfinite(samples["frequency"][:, i])
        row.update(gap_valid_draws=np.isfinite(samples["gap"][:, i]).sum(),
                   decomposition_valid_draws=both.sum())
        for name, values in samples.items():
            vector = values[:, i]
            eligible = both if name.startswith("q_") else np.isfinite(vector)
            low, high = np.quantile(vector[eligible], [.025, .975]) if eligible.any() else (np.nan, np.nan)
            row.update({name: estimates[name][i], f"{name}_low95": low, f"{name}_high95": high})
        yield row


def raw(frame, samples):
    pairs = frame["mask"].to_numpy().reshape(-1, 2)
    dates = frame.Date.to_numpy()[::2]
    conditions = frame[["Distance", "Npenguins"]].to_numpy()
    matched = (conditions[::2] == conditions[1::2]).all(axis=1)
    rows = []
    for subset, keep in (("all", np.ones(len(pairs), dtype=bool)), ("same_distance_size", matched)):
        blocks = [
            np.stack([np.bincount(x, minlength=len(q3.MASKS)) for x in pairs[keep & (dates == day)].T])
            for day in sorted(set(dates))
        ]
        blocks = np.stack(blocks)
        counts = blocks.sum(axis=0)
        draws = blocks[samples].sum(axis=1)
        summaries = summarize(divide(counts, counts.sum(axis=-1, keepdims=True)),
                              divide(draws, draws.sum(axis=-1, keepdims=True)), subset=subset)
        events = counts @ INDICATORS
        for i, row in enumerate(summaries):
            for arm, name in enumerate(("natural", "control")):
                row.update({f"{name}_trials": counts[arm].sum(),
                            f"{name}_responders": counts[arm, 1:].sum(),
                            f"{name}_events": events[arm, i]})
            rows.append(row)
    return rows


def standardized(frame, point, draws):
    rows = []
    for i, call in enumerate(q3.CALLS):
        for j, distance in enumerate(q3.REPRESENTATIVE):
            nearby = frame.assigned_call.eq(call) & frame.Distance.sub(distance).abs().le(25)
            support = [frame.loc[nearby & frame.Type.eq(stimulus)] for stimulus in q3.STIMULI]
            counts = [np.bincount(part["mask"], minlength=len(q3.MASKS)) for part in support]
            events = np.stack(counts) @ INDICATORS
            summaries = summarize(point[:, i, j], draws[:, :, i, j], call=call, distance_m=distance)
            for event, row in enumerate(summaries):
                for arm, (name, part) in enumerate(zip(("natural", "control"), support)):
                    row.update({f"{name}_local_trials": len(part),
                                f"{name}_local_responders": counts[arm][1:].sum(),
                                f"{name}_local_events": events[arm, event],
                                f"{name}_local_dates": part.Date.nunique()})
                rows.append(row)
    return rows


def run(frame, samples, point, draws, output):
    pd.DataFrame(raw(frame, samples)).to_csv(output / "behavior_gap_raw.csv", index=False)
    pd.DataFrame(standardized(frame, point, draws)).to_csv(
        output / "behavior_gap_standardized.csv", index=False,
    )
