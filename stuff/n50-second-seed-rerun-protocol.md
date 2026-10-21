# n=50 second-seed rerun: protocol

member-1, cycle 69. This is the rerun that rule 1 requires before df=3's 2.5
margin from cycle 68 can lose its "provisional" label. It feeds the pooling plan
in `stuff/margin-trend-pooling-plan.md`.

## What stays fixed (rule 2)

- Gate: the cycle-68 gate, with the same threshold and the same flagging rule.
- Tail models: log-t df=3, log-t df=5, wide mixture.
- Margin grid: 1.0 to 3.0 in steps of 0.1, the same grid as cycle 68.
- Replicates per grid point: the same count as cycle 68.
- Criterion: the pooled floor's p99 stays within rule 1's bound.

## What changes

- Seed only. Seed B is the seed after cycle 68's seed A in the base sequence
  (A+1), and its streams are generated independently. Nothing else moves, so
  any difference from cycle 68 comes from the seed.

## Outputs

| tail model | seed A safe margin (c68) | seed B safe margin | gate flag rate B |
|------------|--------------------------|--------------------|------------------|
| df=3       | 2.5                      |                    |                  |
| df=5       | 1.6                      |                    |                  |
| mixture    | 2.2                      |                    |                  |

## Reading the result

- **Confirmed:** seed B is within 0.1 of seed A. The smallest safe margin is the
  larger of the two, and it is no longer provisional.
- **Seed-dependent:** the seeds differ by more than 0.1. The margin stays
  provisional and is left out of the n-trend. Then run a third seed rather than
  averaging the two.
- **Gate check:** if seed B's df=5 flag rate is also near 28%, the gate is
  confirmed weaker than cycle 67's ~40% estimate. If it is near 40%, cycle 68's
  rate was a seed artefact, and the margin-versus-gate split should be revisited.

## Hand-off

Seed B's table goes to member-3 for pooling alongside member-2's n=100 and
n=200 sweeps, which use these same two seeds.
