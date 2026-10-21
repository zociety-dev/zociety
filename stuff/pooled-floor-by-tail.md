# Pooled grace floor by tail shape

Worked example for rule 1. Take a pooled outage sample with median 10 min and
p90 40 min. Fit each candidate tail through those two points and read off p99:

| Fit       | Shape parameter          | Pooled p99 |
|-----------|--------------------------|-----------:|
| Weibull   | k = ln(ln10/ln2)/ln4 ≈ 0.87 |  ≈ 89 min |
| Lognormal | σ = ln4 / 1.2816 ≈ 1.08  |  ≈ 124 min |
| Pareto    | α = ln5 / ln4 ≈ 1.16     |  ≈ 291 min |

The same two quantiles give p99 values that differ by more than 3x. If the
pooled data cannot rule out Pareto, rule 1 sets the floor at about 291 min, not
124. A lognormal-only floor would be exceeded by about 1 Pareto outage in 37
(S(124) ≈ 0.027), not 1 in 100.

Rule 2 is what makes this affordable: each outage past the floor forces a
refit, so a Pareto tail that the data later rules out stops setting the floor
once two refits in a row agree it can come down.
