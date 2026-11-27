"""Sharp bounds under hypothetical corrections to the second playback."""
from fractions import Fraction
from itertools import product

import pandas as pd

from q3_first_playback import CELLS, paired_responses


DIRECTIONS = {"two_sided": (0, 1), "suppressive": (0,), "enhancing": (1,)}


def capacities(counts):
    """Find the order allocation with greatest capacity in each direction."""
    n = sum(counts)
    best = {}
    for first in product(*(range(count + 1) for count in counts)):
        orders = ["unrestricted"]
        if abs(2 * sum(first) - n) <= n % 2:
            orders.append("nearest_half")
        second = tuple(count - x for count, x in zip(counts, first))
        for direction, eligible in DIRECTIONS.items():
            # Natural-first allows control correction, and vice versa.
            down, up = [0] * 8, [0] * 8
            for i, (natural, control) in enumerate(CELLS):
                if control in eligible:
                    (up if control else down)[2 * i] = first[i]
                if natural in eligible:
                    (down if natural else up)[2 * i + 1] = second[i]
            for order in orders:
                for bound, slots in (("lower", down), ("upper", up)):
                    key = (order, direction, bound)
                    capacity = sum(slots)
                    if key not in best or capacity > best[key][0]:
                        best[key] = (capacity, first, slots)
    return best


def witness(budget, slots):
    flips = []
    for available in slots:
        used = min(available, budget)
        flips.append(used)
        budget -= used
    return flips


def run(data, output):
    records, summary = [], []
    for sample, pairs in paired_responses(data):
        counts = [int((pairs.call.eq(a) & pairs.control.eq(b)).sum()) for a, b in CELLS]
        n = len(pairs)
        baseline = counts[2] - counts[1]
        best = capacities(counts)
        for order in ("unrestricted", "nearest_half"):
            for direction in DIRECTIONS:
                start = len(records)
                for budget in range(n + 1):
                    row = {"sample": sample, "n": n, "order": order, "carryover": direction,
                           "budget": budget, "observed_numerator": baseline}
                    for bound, sign in (("lower", -1), ("upper", 1)):
                        capacity, first, slots = best[order, direction, bound]
                        flips = witness(budget, slots)
                        numerator = baseline + sign * sum(flips)
                        row.update({f"{bound}_numerator": numerator,
                                    f"{bound}_exact": str(Fraction(numerator, n)),
                                    f"{bound}_pp": 100 * numerator / n,
                                    f"{bound}_natural_first": sum(first),
                                    f"{bound}_capacity": capacity})
                        for i, (a, b) in enumerate(CELLS):
                            row[f"{bound}_natural_first_{a}{b}"] = first[i]
                            row[f"{bound}_flip_natural_first_{a}{b}"] = flips[2 * i]
                            row[f"{bound}_flip_control_first_{a}{b}"] = flips[2 * i + 1]
                    records.append(row)
                section = records[start:]
                crossing = next((r for r in section if r["lower_numerator"] <= 0), None)
                summary.append({
                    "sample": sample, "n": n, "order": order, "carryover": direction,
                    "observed_pp": 100 * baseline / n,
                    "full_budget_lower_pp": section[-1]["lower_pp"],
                    "full_budget_upper_pp": section[-1]["upper_pp"],
                    "minimum_changes_nonpositive": crossing["budget"] if crossing else "",
                })
    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(output / "q3_carryover_bounds.csv", index=False, lineterminator="\n")
    pd.DataFrame(summary).to_csv(output / "q3_carryover_summary.csv", index=False, lineterminator="\n")
