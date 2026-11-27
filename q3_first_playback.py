"""Attainable bounds on observed first-playback response contrasts."""
from fractions import Fraction

import pandas as pd

from q3 import load_playbacks


CELLS = ((0, 0), (0, 1), (1, 0), (1, 1))


def endpoints(pairs, name):
    n = len(pairs)
    totals = pairs.control.sum()
    for m in range(1, n):
        weights = (n - m) * pairs.call + m * pairs.control
        record = {"sample": name, "n": n, "m": m}
        for bound, ascending in (("lower", True), ("upper", False)):
            first = pairs.loc[weights.sort_values(ascending=ascending, kind="stable").index[:m]]
            natural = int(first.call.sum())
            control = int(totals - first.control.sum())
            value = Fraction(natural, m) - Fraction(control, n - m)
            record.update({f"{bound}_natural_responses": natural,
                           f"{bound}_control_responses": control,
                           f"{bound}_exact": str(value), f"{bound}_pp": float(100 * value)})
            for a, b in CELLS:
                record[f"{bound}_natural_first_{a}{b}"] = int(
                    (first.call.eq(a) & first.control.eq(b)).sum()
                )
        record["positive_guaranteed"] = Fraction(record["lower_exact"]) > 0
        yield record


def summarize(rows):
    n = rows[0]["n"]
    restrictions = {
        "unrestricted": rows,
        "nearest_half": [r for r in rows if abs(2 * r["m"] - n) <= n % 2],
        "45_to_55_pct": [r for r in rows if 45 * n <= 100 * r["m"] <= 55 * n],
        "40_to_60_pct": [r for r in rows if 40 * n <= 100 * r["m"] <= 60 * n],
    }
    for assumption, eligible in restrictions.items():
        lower = min(eligible, key=lambda r: Fraction(r["lower_exact"]))
        upper = max(eligible, key=lambda r: Fraction(r["upper_exact"]))
        result = {"sample": rows[0]["sample"], "n": n, "assumption": assumption,
                  "m_min": eligible[0]["m"], "m_max": eligible[-1]["m"],
                  "positive_guaranteed": lower["positive_guaranteed"]}
        for bound, witness in (("lower", lower), ("upper", upper)):
            result[f"{bound}_m"] = witness["m"]
            result.update({key: val for key, val in witness.items() if key.startswith(bound + "_")})
        yield result


def run(data, output):
    frame = load_playbacks(data)
    if not frame.ResponseYesNo.isin((0, 1)).all():
        raise ValueError("Expected binary response outcomes")
    fields = frame.pivot(index="expID", columns="Type",
                         values=["Distance", "Npenguins", "ResponseYesNo"]).sort_index()
    matched = fields.Distance.call.eq(fields.Distance.control) & fields.Npenguins.call.eq(fields.Npenguins.control)
    pairs = fields.ResponseYesNo.astype(int)
    bounds, summary = [], []
    for name, sample in (("matched", pairs.loc[matched]), ("all", pairs)):
        rows = list(endpoints(sample, name))
        bounds.extend(rows)
        summary.extend(summarize(rows))
    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(bounds).to_csv(output / "q3_first_playback_bounds.csv", index=False, lineterminator="\n")
    pd.DataFrame(summary).to_csv(output / "q3_first_playback_summary.csv", index=False, lineterminator="\n")
