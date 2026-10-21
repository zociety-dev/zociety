# Floor ratchet walkthrough (rules 1 and 2 together)

Rule 1 sets the pooled grace floor from the heaviest-tailed fit the pooled
data cannot rule out. Rule 2 makes the floor move: any outage past it forces
a refit, and the floor only comes down when two refits in a row agree.
Between them they work like a ratchet. Raising the floor is easy and
lowering it is slow.

## A worked sequence

Start: pooled data can't rule out Pareto, so floor = 291 min (see
`pooled-floor-by-tail.md`).

| Step | Event | Refit says | Floor |
|------|-------|-----------|-------|
| 1 | 40 more outages, none > 291 | no trigger, no refit | 291 |
| 2 | scheduled refit: Pareto now rejected, Weibull ≈ 160 | lower (1st) | 291 |
| 3 | outage of 310 min (> floor) | forced refit: Pareto back in | 291+ (raise at once) |
| 4 | refit: Pareto rejected again, Weibull ≈ 165 | lower (1st, streak reset) | 3xx |
| 5 | refit: Weibull ≈ 162 | lower (2nd agreeing) | ≈ 165 |

Step 3 is where the protection shows. A single long outage resets the
lowering streak, so a tail that only *looks* lighter for a while can't
pull the floor down between two bad outages.

## Gaps the rules leave open

1. **Raising.** Rule 2 says when the floor may go down, not up. The table
   assumes a refit that calls for a higher floor applies right away. That
   should be written down explicitly.
2. **"Agree".** Two refits that both say "lower" but to different values
   (165 vs 162): the safe reading is to lower to the *higher* of the two.
3. **Refit cadence.** Only overruns force a refit. Without a scheduled
   refit (step 2) the floor could never come down. Some cadence is
   needed, e.g. every N new pooled outages.

Numbers in the table are illustrative, not fitted.
