# Guardian admission protocol

Combines rule 1 (quorum co-sign plus 30-day probation) and rule 2 (only a
graduated guardian's co-sign gives a new guardian freeze power) into one
admission sequence. It also says what key creation has to fix in advance.

## Sequence

1. **Propose.** A quorum of the current roster (2 of 3 here) signs an
   enrollment record naming the new guardian G and its sponsor S. S must have
   completed probation.
2. **Probation (30 days).** G can sign and observe. Its outages add no
   freeze. If S is removed during probation, G's probation resets.
3. **Graduate.** At day 30, G's outages begin to count toward freeze, but
   they are charged to **S's** budget (the fix from
   graduated-guardian-collusion-bound.md). S and every guardian S sponsored
   share one floor of 2 x S's p99 outage.
4. **Earn its own budget.** After G has sponsored nobody and kept its p99
   history for a further 30 days, G gets its own floor, starting at the lower
   of S's floor and the roster median.

## Thief's best case

| Thief controls | Admission possible? | Extra freeze beyond honest outages |
|---|---|---|
| nothing | no | 0h |
| 1 graduated guardian C (floor 8h) | only with an honest co-signer | 0h; C's sponsored guardians share C's 8h |
| a graduated quorum | yes | unbounded: the thief already owns the roster |

## What key creation must fix

The last row can't be handled by admission rules. At key creation, the
owner commits to:
- **a roster size floor** N_min, so that a quorum always needs more than
  half of the guardians who were present at creation;
- **an absolute freeze cap** T_max (the turn limit), which no budget can
  exceed;
- **a creation-set anchor**: removing any creation-set guardian needs the
  owner's key, not just a quorum.

With these in place, a thief who captures a quorum still can't freeze for
longer than T_max. They also can't remove honest creation-set guardians to
make room for their own.

## Still open

Step 4's 30-day "own budget" wait is set by hand. It should be derived from
how long it takes to measure p99 with confidence.
