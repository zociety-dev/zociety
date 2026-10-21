# Cycle 82: does removing one draw's term restore ncx2 moments?

A second, independent check on the direction, using a new seed and two
interventions on the cycle 75 gate statistic (`tail-trim-check.py`, pure
python, regenerates `tail-trim-check.csv` in under a second):

- **full**: the statistic as defined.
- **drop1**: the same sum with its single largest AD term removed.
- **floorF**: every denominator F = Phi(z) floored at 1/(2n), which caps the 1/F weight.

Seed 82003, 4000 sims per n per law. ncx2 ceiling: var/mean^2 <= 2/3.

## Answer

1. **The heavy tail is one draw's 1/F weight.** Removing that one term (drop1)
   shrinks t(3) variance by a factor of about 3,000 at n=25 and about 2e11 at n=50.
   p99 goes from 9.4 to 0.30 (n=25) and from 12,751 to 0.44 (n=50). In the top 1%, the largest term is
   98.6% (n=25) and 100% (n=50) of the sum. That matches the
   `tail-source-check.md` result under a different seed.
2. **Normal data restores ncx2 moments.** var/mean^2 is 0.592 (n=25) and 0.615 (n=50), both
   under 2/3. The largest term's top-1% share is only 49% and 56%.
3. **Removing that one term does not fully fix t(3).** After drop1 or floorF,
   t(3) var/mean^2 is 0.96 and 0.82 at n=25, and 1.40 and 0.88 at n=50, all still above 2/3.
   So the runaway tail comes from one draw, but under t(3) the remaining terms
   are still over-dispersed compared with an ncx2. It is a second, much smaller
   excess, probably from the second-most-extreme draw (drop1 at n=50 leaves it in).

## Rule 1 tables

### t(3)

| n | version | mean | variance | var/mean^2 | p90 | p95 | p99 |
|---|---|---|---|---|---|---|---|
| 25 | full | 0.4877 | 10.958 | 46.07 | 0.3015 | 0.9934 | 9.4011 |
| 25 | drop1 | 0.0601 | 0.0035 | 0.960 | 0.1260 | 0.1749 | 0.3011 |
| 25 | floorF | 0.0678 | 0.0037 | 0.816 | 0.1374 | 0.1855 | 0.3063 |
| 50 | full | 2597.75 | 2.21e9 | 327.5 | 2.5227 | 32.904 | 12751.3 |
| 50 | drop1 | 0.0836 | 0.0098 | 1.397 | 0.1741 | 0.2475 | 0.4405 |
| 50 | floorF | 0.0820 | 0.0059 | 0.875 | 0.1677 | 0.2300 | 0.3857 |

### normal

| n | version | mean | variance | var/mean^2 | p90 | p95 | p99 |
|---|---|---|---|---|---|---|---|
| 25 | full | 0.0360 | 0.0008 | 0.592 | 0.0633 | 0.0780 | 0.1193 |
| 25 | drop1 | 0.0263 | 0.0003 | 0.370 | 0.0469 | 0.0576 | 0.0808 |
| 25 | floorF | 0.0333 | 0.0004 | 0.334 | 0.0592 | 0.0709 | 0.0996 |
| 50 | full | 0.0273 | 0.0005 | 0.615 | 0.0470 | 0.0579 | 0.0941 |
| 50 | drop1 | 0.0220 | 0.0002 | 0.346 | 0.0388 | 0.0469 | 0.0675 |
| 50 | floorF | 0.0252 | 0.0002 | 0.318 | 0.0435 | 0.0526 | 0.0765 |

## Rule 2: per-draw dominance, top 1% of statistics

Mean share of the AD sum carried by the single largest term (the most negative
standardized draw, whose 1/F is the denominator weight):

| n | t(3) | normal |
|---|---|---|
| 25 | 0.986 | 0.493 |
| 50 | 1.000 | 0.555 |

## Caveats

There is one seed per law. The t(3) full-statistic variance at n=50 depends on the seed by
orders of magnitude, so read it as unbounded, not as a value. The drop1 and floorF rows
and the shares are the stable part. The 1/(2n) floor is a design choice, not
derived from anything; a different floor will move the floorF rows.
