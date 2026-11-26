"""Summarize published noise decisions across matched scenario variants."""
import pandas as pd


def run(output):
    frame = pd.read_csv(output / "noise_q4_points.csv")
    key = ["db", "call", "distance_m"]
    counts = frame.groupby(key).passes_80.agg(["sum", "size"]).reset_index()
    counts = counts.rename(columns={"sum": "passing", "size": "variants"})
    counts["agreement"] = "mixed"
    counts.loc[counts.passing == 0, "agreement"] = "all_fail"
    counts.loc[counts.passing == counts.variants, "agreement"] = "all_pass"
    counts.to_csv(output / "noise_q4_agreement.csv", index=False)

    factors = {"shape": ("noise_power", "matched_uniform"),
               "link": ("acoustic_only", "coupled"),
               "resampling": ("expID", "date")}
    records = []
    noisy = frame.loc[frame.db.ne(0)]
    for factor, (first, second) in factors.items():
        index = key + [name for name in factors if name != factor]
        matched = noisy.pivot(index=index, columns=factor, values="passes_80").reset_index()
        for db, group in matched.groupby("db"):
            a, b = group[first], group[second]
            records.append({"factor": factor, "db": db, "first": first, "second": second,
                            "both_pass": (a & b).sum(), "both_fail": (~a & ~b).sum(),
                            "first_only": (a & ~b).sum(), "second_only": (~a & b).sum()})
    pd.DataFrame(records).to_csv(output / "noise_q4_agreement_by_factor.csv", index=False)
