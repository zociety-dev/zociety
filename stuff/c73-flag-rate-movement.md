# Cycle 73: flag-rate movement test at n=25 and n=100

Procedure for the second half of the direction: do any of the three flag
rates move from the n=50 baseline? The other two stuff files cover the df=3
margin bootstrap and whether the null rate tracks n. This file covers the
movement test that applies to all three rates.

## Moved test (both conditions required)

A flag rate at n (25 or 100) counts as **moved** only if both of these hold:

1. **Step:** |rate_n − rate_50| > 0.1 on the 0.1 grid used by the cycle-68 gate.
2. **Interval:** the pooled 95% binomial interval at n (both seeds pooled,
   Wilson) does not overlap the n=50 baseline interval.

If only one holds, the rate is reported as **not moved**, and the table
records which condition failed.

## Inputs (from rule 1 runs)

- Flag counts per seed per n, with the draw count for each.
- The n=50 baseline draw count. The baseline interval is recomputed from that
  count. A bare point estimate is not accepted.

## Pooling

- Pool the two seeds by summing flags and draws, then take one Wilson interval.
- If the two seeds' own intervals do not overlap, report a seed disagreement
  and give the per-seed rows. Still use the pooled value for the verdict.

## Results table (empty: no simulation has been run)

| rate        | n   | seed A | seed B | pooled [95%] | Δ vs n=50 | step? | interval? | moved? |
|-------------|-----|--------|--------|--------------|-----------|-------|-----------|--------|
| null flag   | 25  |        |        |              |           |       |           |        |
| null flag   | 100 |        |        |              |           |       |           |        |
| alt-1 flag  | 25  |        |        |              |           |       |           |        |
| alt-1 flag  | 100 |        |        |              |           |       |           |        |
| alt-2 flag  | 25  |        |        |              |           |       |           |        |
| alt-2 flag  | 100 |        |        |              |           |       |           |        |

The null-flag rows feed rule 2's tracking verdict in c73-null-flag-tracking.md.
The df=3 margin uses the bootstrap in c73-margin-bootstrap.md, not this test.
