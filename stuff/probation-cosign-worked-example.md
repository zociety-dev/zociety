# Probation + co-sign: worked example

Applies rule 1 (quorum co-sign + 30-day probation, probation outages give no
freeze) and rule 2 (post-creation guardian adds freeze only when co-signed by a
guardian that has completed probation).

## Setup

- Key created with guardians A and B. Each has a grace floor of 2 × its p99
  outage: A = 6h, B = 8h. Turn limit = 24h.
- Honest freeze ceiling today: max(A, B) = 8h.

## Attack

1. Thief steals the key and enrolls guardian T (thief-controlled).
2. Rule 1: enrollment needs a quorum of A and B to co-sign. The thief holds
   neither, so T is never enrolled. Freeze gained: 0h.
3. Suppose the thief tricks A into co-signing. T is still on probation for 30
   days. The thief cuts T off at once. Rule 1: probation outages count toward
   no freeze. Freeze gained: 0h.
4. Suppose T finishes probation, then is cut off. Rule 2: T's outage adds
   freeze only if a guardian that has completed probation (A or B) co-signs
   the freeze. Honest A and B see their own path is up and refuse. Freeze
   gained: 0h beyond the honest 8h.

## Result

| Step                  | Thief freeze beyond honest ceiling |
|-----------------------|------------------------------------|
| Enroll without quorum | 0h (blocked)                       |
| Cut off in probation  | 0h                                 |
| Cut off after         | 0h unless an honest guardian signs |

The median-wait gap from cycle 62 closes: a new guardian never sets the wait by
itself, so with two guardians the thief cannot buy one guardian's floor.

## Remaining gap

If the thief controls a guardian that has completed probation, rule 2 lets it
co-sign T's freeze. That is the same power the thief already had through that
guardian, so the bound is unchanged, but the two outages now add, not overlap.
