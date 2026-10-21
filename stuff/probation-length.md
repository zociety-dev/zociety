# How long probation must run (rules 1 and 2 worked through)

Rule 1 ends probation when the 95% upper bound on a guardian's p99 outage is
within 25% of the estimate. Rule 2 only counts outages whose check windows sit
at least one p99-outage length from other counted windows. This note works out
what those two rules imply for probation length, so the stopping point comes
from data and not from "30 days".

## Distribution-free bound: at least 299 intervals

With no assumption about the outage distribution, a 95% upper bound on the
99th percentile exists only if the largest of n observations has a 95% chance
of exceeding it:

    1 - 0.99^n >= 0.95   =>   n >= ln(0.05) / ln(0.99) = 298.1   =>   n >= 299

So with one check interval per day, a distribution-free grace floor needs at
least 299 days. That bound is just the worst observed outage, so the "within
25%" test cannot usually be met. A 30-day probation gives no p99 bound at all
under this method.

## Exponential outage durations: about 68 counted outages

If outage durations are exponential with mean m, then p99 = m * ln(100), and
the ratio of upper bound to estimate is the same for p99 as for m. With k
counted outages, the 95% upper bound on m is 2k*m_hat / chi2_{0.05}(2k).
Using chi2_{0.05}(2k) ~ 2k - 1.645*sqrt(4k):

    upper / estimate ~ 1 / (1 - 1.645 / sqrt(k)) <= 1.25
    =>  sqrt(k) >= 8.22   =>   k >= 68

| counted outages k | upper/estimate (approx) |
|-------------------|-------------------------|
| 10                | 2.08                    |
| 30                | 1.43                    |
| 68                | 1.25                    |
| 100               | 1.20                    |

The probation length is then 68 divided by the rate of *counted* outages. Rule
2 lowers that rate: outages that cluster inside one p99 length of each other
count once, so a guardian that fails in bursts takes longer to graduate. That is
intended, because a burst is one incident and not 68 pieces of evidence.

## Rule of thumb

- Count spaced outages (rule 2), not days.
- Under an exponential fit, stop at about 68 counted outages plus 30
  outage-free intervals (rule 1). The grace floor is the upper bound at that
  point, about 1.25x the p99 estimate.
- A guardian that almost never fails will not reach 68 outages. It needs the
  distribution-free path (299+ intervals) or a fixed default floor, not an early
  graduation.
- Check the exponential fit before relying on it. A heavy tail (for example,
  rare multi-day outages) makes the 68 figure too optimistic.
