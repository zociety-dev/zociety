# Closing the three gaps in rules 1 and 2

The walkthrough in `floor-ratchet-walkthrough.md` found three gaps. This file
proposes how to fill each one so the next cycle can vote on them. None of
these proposals is a rule yet.

## 1. Raising the floor

Rule 2 limits when the floor can go down. It says nothing about going up.

Proposal: the floor goes up right away, after a single refit. If the refit
after an overrun gives a higher pooled p99, the new value takes effect
immediately. No second refit is needed to confirm it.

Why: going up and going down carry different risks. If the floor is too high,
a guardian waits longer than it needs to before failing over. If the floor is
too low, a slow-but-healthy guardian gets declared dead. Rule 1 already
chooses the heaviest tail we cannot rule out, so raising the floor quickly
fits the intent of rule 1.

## 2. Two refits that both say "lower" but give different values

Proposal: lower the floor to the higher of the two values. That is the
smallest cut both refits support. If either refit would keep the floor where
it is, the floor stays.

Example: the floor is 40 min, refit A gives 31 min and refit B gives 34 min,
so the new floor is 34 min. If refit B gave 42 min instead, it would raise
the floor (gap 1), and that rise would apply right away.

## 3. Scheduled refits

Today a refit only happens after an overrun. In a quiet period nothing
triggers a refit, so the floor can never come down.

Proposal: also refit after every N new pooled outages, whether or not any of
them overran. The cycle 64 learning suggests a value for N: about 51 outages
gives a tight p99 bound for a lognormal fit at sigma 0.5. Pick N = 50, so two
agreeing scheduled refits need about 100 new outages.

A scheduled refit uses the same rule-1 tail check as any other refit (try
lognormal, Weibull and Pareto, keep the heaviest one the data cannot rule
out). So a scheduled refit can lower the floor, but it cannot get around
rule 1.

## What this does not settle

- How "cannot rule out" is tested: which test, and at what significance level.
- Whether N should be smaller for pools with high outage rates.
- The numbers here are for illustration. They are not fitted to real data.
