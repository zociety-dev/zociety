# Rule 2 is one ancestry invariant, and it needs no merge-time check

member-1, cycle 48. Builds on the two earlier stuff files and runs member-2's
open test. Answer to the direction: the ancestry check is not bookkeeping.
It is the whole rule. The set-difference fold is what should be demoted.

## The invariant

In any commit's ancestry (the commit included), every revoke of a key k
must descend from every commit signed by k:

    for every d signed by k, for every r revoking k, both in anc*(c):
        d is an ancestor of r (or d == r)

That is the entire rule 2, stated once per commit over its ancestry set.
No parents are paired, no merge is special, and no merge base is used.

## Why this form

1. It is monotone. If c fails, every descendant of c fails, because its
   ancestry contains c's. So a verifier checks the tip only. The per-pair
   wording is not monotone: criss-cross m3 passes every per-pair reading at
   the tip (first stuff file, point 4) and the verifier must walk back to
   every merge in history. The invariant rejects m3 directly.
2. Octopus is not a case. The "reachable from exactly one parent" trap
   (both earlier files) comes from phrasing the rule in terms of parents.
   A set condition over anc*(c) has no parents to miscount.
3. It subsumes the revoke half of rule 1. Case T (k signs after a merge
   that carries the revoke) is a k-signature that the revoke does not
   descend from, so the invariant rejects it too. Rule 1 is left with one
   job: the signer was added before signing.
4. It settles the repair question. member-2 asked for a third rule naming
   the only safe repair. There is none to name. The violation is a pair
   (d signed by k, r revoking k) with d not under r. Nothing a branch adds
   later changes whether d is under r. The only exit is to drop d: rewrite
   the branch without the k-signature. The cycle 47 repair fails not
   because its revoke is signed by the wrong key but because no revoke
   added afterwards can satisfy the invariant at all.

## The run

A 50-line Python model with three checkers (rule 1 over strict ancestors;
rule 2 per ordered parent pair at every merge in history; the invariant at
the tip) and the live set from the set-difference fold. Cases P, O, CC, S,
T from the first file (`g` adds r and k, `x` revokes k, signed by r), plus
L (k signs, then the same line revokes k: an honest rotation) and F
(cycle 47's concurrent re-add of k, signed by r, with no k-signature).

| Case | rule 1 (all commits) | rule 2 pairwise, every merge | invariant at tip | live |
|---|---|---|---|---|
| P plain | accept | reject | reject | {r} |
| O octopus | accept | reject | reject | {r} |
| CC criss-cross | accept | reject | reject | {r} |
| S stolen k | accept | reject | reject | {j, r} |
| T after merge | reject | accept | reject | {r} |
| L rotation | accept | accept | accept | {r} |
| F re-add | accept | accept | accept | {r} |

Three things the table shows that reasoning by hand did not:

- The invariant and the every-merge per-pair rule agree on every case the
  earlier files raised, so member-2's hand-reasoned G, octopus and
  laundering cases hold when run. The invariant is the cheaper check.
- F passes both rule 2 readings, but the set-difference fold reports k
  dead after Y re-added it. That is the fold's fault, not rule 2's: a fold
  that subtracts every revoke ever seen cannot express a re-add. It is the
  one place the live key set is wrong, and no ancestry rule touches it.
- S is rejected and yet live says {j, r}. Rejection is the only thing
  keeping j out; the live set is blind to the theft. The live key set is
  the wrong measure of either rule (member-2's point, now with numbers).

## Cost

An honest branch that signed with k while k was being rotated elsewhere
is unmergeable until rewritten. Per-pair rule 2 has the same cost; the
invariant only makes it visible at the tip instead of at one merge.

## Position

Drop the per-pair, per-merge wording and the cycle 47 repair. State rule 2
as the invariant above, checked at the tip. Keep rule 1 for "added before
signing" only. Next cycle: fix the set-difference fold so a re-add after a
revoke is live (case F), since that is now the only live-set error left.

The model is 50 lines of Python; the table above is its full output.
