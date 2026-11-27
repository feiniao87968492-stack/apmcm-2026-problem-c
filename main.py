"""Reproduce the C problem tables and figures from the contest CSVs."""
from argparse import ArgumentParser
from pathlib import Path

import behavior_ablation
import behavior_gap
import context_priority
import continuous_recovery
import control_subtraction
import distance_deletion

import creative_gate
import creative_inverse
import creative_q1
import creative_q3
import example_sensitivity
import final_analysis
import first_reply
import group_size
import matched_sensitivity
import missing_propagation
import noise_agreement
import noise_scenarios
import onset_analysis
import physical_attenuation
import playback_dependence
import post_hoc
import q1
import q1_candidate_sets
import q2
import q2_envelope_rank
import q2_shape_rank
import q2_spectral_allocation
import q3
import q3_direction
import q4
import q4_decision
import recovery
import round2
import sea_state
import spatial_annulus
import strict_playback
import vocal_counts


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path, help="Folder containing Data01 to Data11")
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--seed", type=int, default=20261126)
    parser.add_argument("--bootstrap", type=int, default=300)
    analyses = parser.add_mutually_exclusive_group()
    analyses.add_argument("--q4-tail-ablation", action="store_true",
                          help="Run the frozen 4,800-draw tail ablation")
    analyses.add_argument("--q4-envelope-attainment", action="store_true",
                          help="Run the frozen 4,800-draw Q4 envelope-weight analysis")
    analyses.add_argument("--q4-shape-propagation", action="store_true",
                          help="Compare four Q4 acoustic shapes in the frozen 4,800-draw analysis")
    analyses.add_argument("--q4-net-loss", action="store_true",
                          help="Compute Q4 boundaries for separate acoustic and response losses")
    analyses.add_argument("--q4-consecutive", action="store_true",
                          help="Compare the five Q4 consecutive-distance grid radii")
    analyses.add_argument("--q4-target-loss", action="store_true",
                          help="Compute Q4 loss boundaries for target distances")
    analyses.add_argument("--q4-matched-noise", action="store_true",
                          help="Compare local and matched uniform Q4 noise")
    analyses.add_argument("--q4-response-sensitivity", action="store_true",
                          help="Invert the Q4 response-retention scenario at 6 dB")
    analyses.add_argument("--appendix5-noise", action="store_true",
                          help="Simulate matched-power noise on the Supplementary 5 WAVs")
    analyses.add_argument("--q1-class-prior", action="store_true",
                          help="Compare Q1 class-prior rules on the frozen grouped folds")
    analyses.add_argument("--q1-location", action="store_true",
                          help="Run the frozen Q1 recording-location comparison")
    analyses.add_argument("--q1-q4-labels", action="store_true",
                          help="Propagate archived Q1 label errors into Q4 gross scores")
    analyses.add_argument("--q4-review-budget", action="store_true",
                          help="Evaluate ideal manual review in the frozen Q4 scenario")
    analyses.add_argument("--q3-first-playback", action="store_true",
                          help="Bound Q3 first-playback response differences")
    args = parser.parse_args()
    if args.q3_first_playback:
        from q3_first_playback import run

        run(args.data, args.output)
        return
    if args.q4_review_budget:
        from q4_review_budget import run

        run(Path(__file__).resolve().parent / "results", args.output)
        return
    if args.q1_q4_labels:
        from q1_q4_labels import run

        run(Path(__file__).resolve().parent / "results", args.output)
        return
    if args.q1_location:
        from q1_location import run

        run(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q1_class_prior:
        from q1_class_prior import run

        baseline = Path(__file__).resolve().parent / "results" / "q1_oof_predictions.csv"
        run(args.data, args.output, baseline)
        return
    if args.appendix5_noise:
        from appendix5_noise import run

        run(args.data, args.output)
        return
    if args.q4_response_sensitivity:
        from q4_response_sensitivity import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q4_matched_noise:
        from q4_matched_noise import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q4_target_loss:
        from q4_target_loss import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q4_consecutive:
        from q4_consecutive import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q4_net_loss:
        from q4_net_loss import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q4_shape_propagation:
        from q4_shape_propagation import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q4_envelope_attainment:
        from q4_envelope_attainment import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.q4_tail_ablation:
        from q4_tail_ablation import write

        write(args.data, args.output, Path(__file__).resolve().parent / "results")
        return
    if args.bootstrap < 2:
        parser.error("--bootstrap must be at least 2")
    for number in range(1, 12):
        if len(list(args.data.glob(f"Data{number:02d}*.csv"))) != 1:
            parser.error(f"Expected one Data{number:02d} CSV in {args.data}")
    args.output.mkdir(parents=True, exist_ok=True)
    q1.run(args.data, args.output, args.seed, args.bootstrap)
    q1_candidate_sets.run(args.data, args.output)
    propagation = q2.run(args.data, args.output, args.seed + 1, args.bootstrap)
    q2_envelope_rank.run(propagation["metric_means_and_draws"], args.output)
    q2_shape_rank.run(propagation["metric_means_and_draws"], args.output)
    q2_spectral_allocation.run(propagation["metric_means_and_draws"], args.output)
    behavior = q3.run(args.data, args.output, args.seed + 2, args.bootstrap)
    q3_direction.run(q3.load_playbacks(args.data), args.output)
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
    (frame, sampled_dates, date_predictions, point_masks, date_masks,
     point_mixed, date_mixed) = playback_dependence.run(
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
    sea_state.run(frame, args.output, args.seed, args.bootstrap)
    example_sensitivity.waverys(frame, args.output, args.seed, args.bootstrap)
    example_sensitivity.example_deletion(args.data, args.output, propagation, behavior, date_predictions, parameters)
    completion_curves, completed_means, missing_counts = missing_propagation.run(
        args.data, args.output, propagation, behavior, date_predictions,
    )
    spatial_annulus.run(propagation, behavior, date_predictions, parameters,
                        sampled_parameters, completion_curves, args.output)
    control_subtraction.run(propagation, behavior, date_predictions,
                            parameters, sampled_parameters, args.output)
    distance_deletion.run(frame, sampled_dates, propagation, behavior, date_predictions,
                          parameters, sampled_parameters, args.output)
    behavior_ablation.run(frame, sampled_dates, propagation, behavior, date_predictions,
                          parameters, sampled_parameters, args.output)
    recovery_plans = recovery.run(completed_means, missing_counts, propagation["distance"], behavior,
                                  date_predictions, args.output)
    continuous_recovery.run(completed_means, missing_counts, propagation["distance"],
                            behavior, recovery_plans, args.output)
    context_priority.run(frame, propagation["distance"], parameters, sampled_parameters,
                         point_masks, date_masks, args.output)
    behavior_gap.run(frame, sampled_dates, point_mixed, date_mixed, args.output)
    group_size.run(frame, sampled_dates, propagation, behavior, date_predictions, args.output)
    vocal_counts.run(frame, sampled_dates, propagation, behavior, date_predictions, args.output)
    first_reply.run(frame, sampled_dates, args.seed, args.output)
    print(f"Results written to {args.output.resolve()}")


if __name__ == "__main__":
    main()

