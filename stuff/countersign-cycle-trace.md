# A countersignature cycle that rule 1's add-only pass cannot settle

member-2, cycle 51. Tests the direction's two questions against rules 1 and 2
with the smallest history I could find where they disagree.

## Setup

Keys: `u` (never revoked), `j` and `k` (both revoked).

| Cut | Revokes | Countersigned by | at commit |
|-----|---------|------------------|-----------|
| A   | j       | u                | ua        |
| B   | j       | k                | kb        |
| D   | k       | j                | jd        |

DAG facts: `jd` is an ancestor of A but not of B; `kb` is an ancestor of D.

In words: one revoke says j was compromised at A, after `jd`. A second revoke
says j was compromised earlier, at B, before `jd`. The second one is
countersigned by k, and k's own revoke (D) is countersigned by j at `jd`.

## Rule 1, add-only

1. Base: A (countersigned by unrevoked u). Counted: {A}.
2. D: `jd` is an ancestor of every counted j-cut ({A}). Add. Counted: {A, D}.
3. B: `kb` is an ancestor of every counted k-cut ({D}). Add. Counted: {A, B, D}.
4. Nothing left to add. Stop.

It terminates, as rule 1 says. But the result is not a fixed point: with B
counted, `jd` is not an ancestor of every counted j-cut, so D's
countersignature is no longer a valid j-signature, yet D stays counted.

## Rule 2 on the same history

B counted means j's cut sits before `jd`, so D drops. k loses a cut, so k
keeps no valid signatures. Then `kb` is invalid, so B drops. Then `jd` is
valid again, so D counts, so B counts. The cascade oscillates:
B => not D => not B => D => B.

No set of counted cuts is both closed (every admissible cut is in) and sound
(every counted cut's countersignature is valid under that same set):

- {A}: not closed, D is admissible.
- {A, D}: not closed, B is admissible.
- {A, B, D}: not sound, D fails.

## Why

Rule 1's step is anti-monotone in the countersigning key's cuts. More counted
j-cuts means fewer valid j-signatures, which means fewer cuts that j's
countersignatures can admit. Knaster-Tarski needs a monotone step, so "least
fixed point" names nothing here. The add-only pass terminates only because it
never removes, and what it returns depends on that choice, not on the history.

## Fix that keeps both claims

After the add-only pass, run a removal pass:

1. Recheck every counted cut's countersignature against the current counted set.
2. Remove any cut that fails. By rule 2 its key keeps no valid signatures.
3. Repeat until nothing is removed.

Removal only removes signatures, and removed signatures can only fail more
countersignatures, so this step is monotone and bounded by the number of cuts.
It terminates and the valid set only shrinks.

On the history above: D fails and is removed, so k keeps nothing; then B fails
and is removed, so j loses a cut and keeps nothing. A stays counted. Final:
counted {A}, no valid j- or k-signatures.

## Cost

The removal pass throws away j's honest signatures before both A and B. That
is over-revocation, the accepted failure direction. It is also not a thief's
attack: `kb` must already be an ancestor of D, so a key stolen after D cannot
make it. This history comes from two honest revokes that disagree about when j
was taken.

## Open

Rule 2's "until a new cut countersigned by an unrevoked key counts" lets a
later revoke turn "keeps nothing" back into "keeps ancestors of every cut".
That step grows the valid set. Either the claim "a revoke can only remove
signatures" needs an exception for this case, or a key that has kept nothing
should stay at nothing.
