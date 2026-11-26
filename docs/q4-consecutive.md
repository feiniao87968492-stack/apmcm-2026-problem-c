# Q4 consecutive-distance attainment

Each draw uses one common clean full-data isotonic net cutoff at 20 m. On the 0.5 m grid from 20 to 150 m, marginal counts assess each node on its own. Same-draw counts require each qualifying draw to pass at every grid node from 20 m through the reported radius. The four-shape rule additionally requires all four acoustic shapes to pass in that draw. [Frozen specification](model-spec.md#q4-consecutive-distance-attainment-freeze)

| Fit and losses | Shared point last | Shared marginal last | Shared marginal prefix | Shared same-draw prefix | Four-shape same-draw prefix |
|---|---:|---:|---:|---:|---:|
| Full, clean | 150 cap | 150 cap | 150 cap | 150 cap | 150 cap |
| Union deletion, clean | 150 cap | 150 cap | 150 cap | 150 cap | 150 cap |
| Full, both 20% | 150 cap | 110 | 110 | 109.5 | 96 |
| Union deletion, both 20% | 119.5 | 94.5 | 94.5 | 92.5 | 84 |

Radii are in metres. Every rule has a passing 20 m node. Under 20% losses the same-draw requirement moves the shared-exponent radius in by 0.5 m with full training and 2 m after union deletion. Requiring all four shapes moves those radii in a further 13.5 and 8.5 m. At these four-shape radii both counts are 3,847. The next nodes have 3,835 and 3,815 qualifying draws, respectively. Under clean conditions after union deletion, 3,858 draws qualify under all four shapes at 150 m and 3,850 qualify at every grid node through 150 m. [Radii and boundary counts](../results/q4_consecutive_radii.csv) · [Radius differences](../results/q4_consecutive_differences.csv) · [All grid counts](../results/q4_consecutive_counts.csv)

The retained two-voice natural and control ranges are 20–200 m and 5–200 m for the full fit, and 20–100 m and 5–120 m after union deletion. The latter clean cap therefore extrapolates for both arms. The counts condition on the models and 4,800 paired draws. Consecutive attainment refers to the evaluated nodes. [Retained ranges](../results/q4_consecutive_ranges.csv)

```sh
python main.py --data "<attachment directory>/date" --q4-consecutive
```
