"""Reproduce the C problem tables and figures from the contest CSVs."""
from argparse import ArgumentParser
from pathlib import Path

import creative_gate
import creative_inverse
import creative_q1
import creative_q3
import final_analysis
import post_hoc
import q1
import q2
import q3
import q4
import round2


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
    print(f"Results written to {args.output.resolve()}")


if __name__ == "__main__":
    main()

