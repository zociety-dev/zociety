# Can a forged revocation drag the cutoff earlier?

Worked trace under rule 1 (cutoff = first *countersigned* revocation, by
commit-log position) and rule 2 (a countersigner counts only if it has no
countersigned revocation earlier in commit-log order).

Keys: H (honest), A and B (honest peers), T (thief, holds a copy of H's key).

| pos | event                                   | counts? | H cutoff |
|-----|-----------------------------------------|---------|----------|
| 1   | H signs cut c1                          | -       | none     |
| 2   | H signs cut c2                          | -       | none     |
| 3   | T (as H) publishes revocation r1 of H   | no countersign: recorded only | none |
| 4   | H signs cut c3                          | -       | none     |
| 5   | A countersigns revocation r2 of H       | yes     | 5        |

Rescue restores c1, c2, c3 (all before position 5). T's forgery at 3
moved nothing, because rule 1 ignores it until countersigned.

## The attack rule 2 closes

Suppose T also stole B, and B was already revoked (countersigned by A) at
position 2. T countersigns r1 with B at position 3. Without rule 2, H's
cutoff becomes 3 and c3 is lost. With rule 2, B has a countersigned
revocation earlier in the log (2 < 3), so B's countersignature does not
count; the cutoff stays at 5.

## What remains open

If T steals a key that is *not yet* revoked, its countersignature counts.
The cutoff can then move as early as the theft of the second key. So the
bound is: a forged cutoff needs two live, distinct keys. Each stratum stays
two-valued (a cut is before or after one position), and monotone (later
countersigned revocations never move the cutoff, since only the first one
counts).
