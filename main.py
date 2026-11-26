"""Reproduce the C problem tables and figures from the contest CSVs."""
from argparse import ArgumentParser
from pathlib import Path

import creative_gate
import creative_inverse
import creative_q1
import creative_q3
import final_analysis
import matched_sensitivity
import noise_agreement
import noise_scenarios
import onset_analysis
import physical_attenuation
import playback_dependence
import post_hoc
import q1
import q2
import q3
import q4
import q4_decision
import round2
import strict_playback


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path, help="Folder containing Data01 to Data11")
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--seed", type=int, default=20261126)
    parser.add_argument("--bootstrap", type=int, default=300)
    args = parser.parse_args()
    if args.bootstrap < 2:
        parser.error("--bootstrap must be at least 2")
    for number in range(1, 12):
        if len(list(args.data.glob(f"Data{number:02d}*.csv"))) != 1:
            parser.error(f"Expected one Data{number:02d} CSV in {args.data}")
    args.output.mkdir(parents=True, exist_ok=True)
    q1.run(args.data, args.output, args.seed, args.bootstrap)
    propagation = q2.run(args.data, args.output, args.seed + 1, args.bootstrap)
    behavior = q3.run(args.data, args.output, args.seed + 2, args.bootstrap)
    q4.run(propagation, behavior, args.output)
    round2.run(args.data, args.output, args.seed, args.bootstrap, propagation)
    reduced, reduced_draws = final_analysis.run(
        args.data, args.output, args.seed, args.bootstrap, propagation, behavior,
    )
    creative_q1.run(args.data, args.output, args.seed, args.bootstrap)
    creative_q3.run(args.data, args.output, args.seed, args.bootstrap)
    creative_gate.run(args.data, args.output, args.seed, args.bootstrap, propagation)
    creative_inverse.loss_limits(propagation, behavior, args.output)
    post_hoc.inverse_sensitivity(propagation, behavior, reduced, reduced_draws, args.output)
    q4_decision.run(propagation, behavior, args.output)
    frame, sampled_dates, date_predictions = playback_dependence.run(
        args.data, args.output, args.seed, args.bootstrap, propagation, behavior,
    )
    matched_sensitivity.stratified_pairs(frame, sampled_dates).to_csv(
        args.output / "matching_q3_strata.csv", index=False,
    )
    matched_sensitivity.loss_intersection(propagation, behavior, date_predictions).to_csv(
        args.output / "matching_q4_loss_limits.csv", index=False,
    )
    matched_sensitivity.weighted_indices(propagation, behavior, args.output)
    parameters, sampled_parameters = physical_attenuation.run(
        args.data, args.output, args.seed + 1, args.bootstrap, propagation, behavior,
    )
    noise_scenarios.run(propagation, behavior, date_predictions, parameters, sampled_parameters, args.output)
    onset_analysis.run(args.data, frame, sampled_dates, args.output, args.seed, args.bootstrap)
    noise_agreement.run(args.output)
    strict_playback.run(frame, propagation, behavior, date_predictions, args.output, args.seed, args.bootstrap)
    print(f"Results written to {args.output.resolve()}")


if __name__ == "__main__":
    main()

