# Q4 context-dependent opportunity exposure through 100 m

The context weights for after feeding, commuting and searching are 36, 65 and 38 of 139 observed pairs. For each context and state, the analysis counts draws that pass all four curves at every half-metre node from 20 to 100 m with eight birds. Each draw retains the full-data, context-standardized, clean isotonic net reference at 20 m. Thresholding each context before combining its indicators gives a different estimand from thresholding after standardizing responses. [Frozen design](model-spec.md#q4-context-dependent-intermittent-exposure-freeze)

| Fit | After feeding clean / noisy | Commuting clean / noisy | Searching clean / noisy | Responses aggregated before scoring |
|---|---:|---:|---:|---:|
| Full | 4,707 / 2,884 | 4,592 / 2,702 | 4,785 / 4,369 | 4,776 / 3,230 |
| Union deletion | 4,494 / 1,309 | 4,439 / 2,224 | 4,765 / 4,253 | 4,753 / 2,430 |

Each count uses 4,800 draws. The last column reproduces the archive. For each fit, the allocation uses the same predicted responses throughout. Assigning noisy opportunities first to contexts with the largest clean-to-noisy pass reduction attains the minimum. Assigning them first to contexts with the smallest reduction attains the maximum. Uniform exposure uses the same noisy share in every context. [Counts and pass fractions](../results/q4_context_exposure_counts.csv)

| Fit | Pass fraction at 50% (minimum / uniform / maximum) | Largest noisy share meeting 80% (minimum / uniform / maximum) |
|---|---:|---:|
| Full | 77.74% / 82.08% / 86.41% | 44.16% / 56.78% / 66.39% |
| Union deletion | 66.33% / 73.79% / 81.26% | 22.05% / 35.11% / 52.73% |

All six limits are interior crossings. At a 50% overall noisy share, the full-fit minimum uses 12.5% after feeding, 100% commuting and 0% searching. Its maximum uses 87.5%, 0% and 100%. After deletion, the corresponding allocations are (100%, 51.54%, 0%) and (0%, 48.46%, 100%). The exports report allocations at all five checkpoints and all six limits. [Checkpoints and allocations](../results/q4_context_exposure_checks.csv) · [Exact limits and allocations](../results/q4_context_exposure_limits.csv)

Within 75–125 m, the full fit has 7/6, 12/11 and 6/7 natural/control trials in context order. After deletion those counts are 7/6, 11/11 and 5/6. Searching has no retained trials below 40 m in either arm, so its prefix uses predictions below observed context-specific support. These opportunity shares are hypothetical. Receiver noise and behavioral response to noise have no measured exposure link, and interpreting the shares as time shares requires uniform opportunity timing. [Trial support and response counts](../results/q4_context_exposure_support.csv)

Run the analysis with the contest CSV directory.

    python main.py --data "<attachment directory>/date" --output generated --q4-context-exposure

[Independent verification](../reviews/q4-context-exposure-verification.md)

## Bounded context imbalance at 50% overall exposure

Let each context's noisy-opportunity share lie within `0.50 ± δ`, preserving the weighted overall share of 0.50. Each feasible allocation is the uniform allocation plus `2δ` times a feasible deviation at the unrestricted endpoint. Since the pass fraction is affine in the allocation, both sharp bounds interpolate linearly. The archived context counts are sufficient for this calculation. [Frozen specification](model-spec.md#q4-bounded-context-imbalance-at-half-exposure-freeze)

| Maximum context displacement (percentage points) | Full fit pass bounds | Union-deleted fit pass bounds |
|---:|---:|---:|
| 0 | 82.08–82.08% | 73.79–73.79% |
| 10 | 81.21–82.94% | 72.30–75.29% |
| **20** | **80.34–83.81%** | **70.81–76.78%** |
| 30 | 79.48–84.68% | 69.31–78.27% |
| 40 | 78.61–85.54% | 67.82–79.77% |
| 50 | 77.74–86.41% | 66.33–81.26% |

In the full fit, the minimum first equals 80% at `δ = 13859/57821`, or **23.9688003 percentage points**. An attaining allocation, in after-feeding, commuting and searching order, is `(74065/231284, 85539/115642, 30103/115642)`. Equality passes the inclusive rule. A failing allocation exists for every strictly larger displacement through 50 points.

In the union-deleted fit, the maximum first equals 80% at `δ = 82833/199268`, or **41.5686412 percentage points**. An attaining allocation is `(16801/199268, 1577636/3238105, 182467/199268)`. This allocation passes at equality, and all allocations fail at smaller displacements.

The illustrative ±20-point cap keeps every context between 30% and 70% noisy. Every allocation passes in the full fit and every allocation fails in the union-deleted fit. The cap is a scenario assumption about playback opportunities. [Independent vertex verification](../reviews/q4-context-imbalance-verification.md)

Run the following Python code from the repository root to recover the archived extrema as exact fractions, rescale the allocations and invert the two bounds.

```python
from csv import DictReader
from fractions import Fraction as F
from pathlib import Path

contexts = ("after", "commuting", "searching")
sizes = (36, 65, 38)
weights = [F(n, 139) for n in sizes]
half, target = F(1, 2), F(4, 5)
root = Path("results")

with (root / "q4_context_exposure_counts.csv").open(newline="") as source:
    counts = {(r["model"], r["context"]): (int(r["clean_count"]), int(r["noisy_count"]))
              for r in DictReader(source)}
with (root / "q4_context_exposure_checks.csv").open(newline="") as source:
    endpoints = {(r["model"], r["rule"]): r for r in DictReader(source)
                 if F(r["f"]) == half}

for fit, crossing_rule in (("full", "minimum"), ("drop_union", "maximum")):
    cells = [counts[fit, context] for context in contexts]

    def attainment(shares):
        return sum(w * ((1 - f) * a + f * b)
                   for w, f, (a, b) in zip(weights, shares, cells)) / 4800

    uniform = attainment([half] * len(contexts))
    extremes = {}
    for rule in ("minimum", "maximum"):
        archived = endpoints[fit, rule]
        witness = [F(archived[f"f_{c}"]).limit_denominator(2 * n)
                   for c, n in zip(contexts, sizes)]
        assert sum(w * f for w, f in zip(weights, witness)) == half
        assert abs(float(attainment(witness)) - float(archived["share"])) < 1e-14
        extremes[rule] = witness

    def allocation(rule, delta):
        return [half + 2 * delta * (f - half) for f in extremes[rule]]

    print(fit)
    for step in range(6):
        delta = F(step, 10)
        print(str(delta), *(f"{float(100 * attainment(allocation(rule, delta))):.5f}%"
                            for rule in extremes))
    extreme = attainment(extremes[crossing_rule])
    crossing = (target - uniform) / (2 * (extreme - uniform))
    witness = allocation(crossing_rule, crossing)
    assert attainment(witness) == target
    print("crossing", crossing, f"{float(100 * crossing):.7f} pp", list(map(str, witness)))
```


## Monte Carlo precision at 30–70% context exposure

The 4,800 paired draws reproduce all archived context and standardized counts and the exact bounded extrema. Each of the six feasible allocations has one score per draw, formed by weighting the paired clean and noisy prefix indicators. The sample covariance across vertices divided by 4,800 estimates the covariance of their Monte Carlo means. Across 10,000 paired draw-index resamples (seed 20261205), the 95th percentile of the centered maximum absolute deviation gives a common half-width of 0.63645 percentage points for the full fit and 0.65458 for union deletion. Taking minima and maxima of the simultaneous limits projects the band onto the allocation extrema. [Frozen specification](model-spec.md#q4-bounded-context-monte-carlo-precision-freeze)

| Fit | Bound | Point estimate | MC SE at attaining vertex (pp) | Projected 95% interval |
|---|---|---:|---:|---:|
| Full | Minimum | 80.343945% | 0.31150 | 79.707497%–80.980393% |
| Full | Maximum | 83.810432% | 0.28693 | 83.173984%–84.446879% |
| Union deletion | Minimum | 70.805860% | 0.30790 | 70.151283%–71.460438% |
| Union deletion | Maximum | 76.779122% | 0.30255 | 76.124544%–77.433699% |

The full-fit all-pass decision is unresolved at this simulation precision because its minimum interval crosses 80%. The union-deletion all-fail decision survives because its maximum interval lies below 80%. These intervals measure conditional Monte Carlo error with the available data, model and exposure scenario fixed. [Draw indicators](../results/q4_context_mc_indicators.csv) · [Vertex means, SEs, covariance and band](../results/q4_context_mc_vertices.csv) · [Projected bounds](../results/q4_context_mc_bounds.csv)

Regenerate the paired indicators and tables from the contest attachments.

    python main.py --data "<attachment directory>/date" --output generated --q4-context-mc

To reproduce just the precision tables from the published indicators, run this from the repository root.

```python
from pathlib import Path

import pandas as pd

from q4_context_mc import indicator_columns, summarize

archive = Path("results")
draws = pd.read_csv(archive / "q4_context_mc_indicators.csv")
masks = {fit: draws[indicator_columns(fit)].to_numpy(dtype=bool)
         for fit in ("full", "drop_union")}
summarize(masks, archive, Path("generated"))
```
