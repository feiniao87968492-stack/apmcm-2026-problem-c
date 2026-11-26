# Q4 control subtraction

The analysis froze at `f2d71da` and ran at `7b713f6`. The gross reference is 0.287598. The own net reference is 0.194371. Both are half the equal-call mean at 20 m using clean isotonic fidelity and the corresponding response term. The shared-exponent fidelity supplies the score curves. References are fixed across losses within each of the 300 paired acoustic and date draws.

| Scenario | Gross decisions passing | Net with gross reference | Net with own reference |
|---|---:|---:|---:|
| Clean | 5/9 | 3/9 | 6/9 |
| 20% acoustic-only | 2/9 | 2/9 | 5/9 |
| 20% coupled | 2/9 | 0/9 | 3/9 |

Across the 27 decisions, subtracting control under the gross cutoff changes four passes to failures. Setting the net reference to its own clean scale restores those four and adds five more relative to the gross comparison. Under coupling, two-voice at 100 m reaches the cutoff in 47.7% of gross draws, 17.0% of net draws with the gross cutoff and 81.7% of net draws with their own cutoff. [Decisions](../results/control_subtraction_decisions.csv) · [Fixed-distance margins and intervals](../results/control_subtraction_points.csv)

The clean normalized area means in flat, modulated and two-voice order are 0.259, 0.381 and 0.435 for gross scores, and 0.210, 0.328 and 0.370 for net scores. Both retain the same point ranking across the three scenarios. Subtraction at fixed loss removes exactly the attenuated fidelity times the fixed control probability. When the clean natural-minus-control excess is positive, acoustic-only loss scales the net score by 0.80 and coupling by 0.64. When that excess is negative, both links scale the net score by 0.80 and preserve its sign. [Area means](../results/control_subtraction_area.csv) · [Paired area gaps](../results/control_subtraction_area_gaps.csv)

Under coupling, gross radii are 50.4, 79.7 and 102.8 m. With the gross cutoff, net scores never qualify on the grid for flat and two-voice, while modulated crosses at 32.6 m. With their own cutoff the net radii are 58.3, 113.4 and at least 150 m, with the last value at the support boundary. These are descriptive changes in the index and its reference. [Bounded radii, intervals and boundary counts](../results/control_subtraction_radii.csv)
