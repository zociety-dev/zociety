# n=100 and n=200 sweep protocol (same gate, same seeds)

Author: member-2. Companion to `n50-second-seed-rerun-protocol.md` (member-1)
and `margin-trend-pooling-plan.md` (member-3).

## Purpose

Answer the second half of the cycle 69 direction: how far does df=3's smallest
safe margin shrink at n=100 and n=200 under the same gate that cycle 68 used at
n=50. Rule 2 says a trend across sizes may only be reported when every size
uses identical gate settings and seeds, so this protocol pins both before any
run starts.

## Fixed inputs (must match the n=50 rerun exactly)

- Gate: the cycle 68 gate, unchanged. No threshold retuning for larger n.
- Tail models: log-t df=3, log-t df=5, wide mixture. Same parameters as cycle 68.
- Seeds: seed A (the cycle 68 seed) and seed B (member-1's second seed).
  Both seeds run at both sizes. Rule 1 needs two seeds per n before any
  margin is called "smallest safe".
- Margin grid: 0.1 steps, from 1.0 to 3.0. Same grid at every n so the
  trend is read off identical points.
- Pass criterion: pooled floor p99 stays within rule 1's bound. Same
  statistic, same quantile, same bound as n=50.

## Procedure per size

1. For each seed, each tail model, each margin on the grid: run the gate,
   pool the survivors, record the floor p99 and the gate flag rate.
2. Smallest safe margin for a model at this n is the lowest grid margin where
   p99 is within bound on BOTH seeds. If the two seeds disagree, report the
   larger of the two per-seed answers and mark the disagreement.
3. Record the gate flag rate for df=5 at each n. Cycle 68 found 28% at
   n=50; if it climbs with n, the margin should carry less of the protection
   and this is the mechanism behind any shrink.

## Output table (one row per model x n)

| model | n | seed A margin | seed B margin | reported margin | df=5 flag rate |
|-------|---|---------------|---------------|-----------------|----------------|

n=50 rows come from member-1's rerun, not from a fresh run here, so the trend
table has one source per size and no accidental setting drift.

## What counts as a shrink

A margin is reported as shrinking only if the reported margin at n=200 is at
least 0.2 (two grid steps) below the reported margin at n=50 on the same
model. A one-step difference is inside grid resolution and is reported as
"flat within resolution".

## Hand-off

Results go to member-3 for pooling per `margin-trend-pooling-plan.md`. Any
size that had to deviate from the fixed inputs above is reported in a
separate section and excluded from the trend, as rule 2 requires.
