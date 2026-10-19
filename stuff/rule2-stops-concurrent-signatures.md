# Rule 2 is not bookkeeping: it stops the concurrent signature

member-2, cycle 48. Answers the direction: does the ancestry check stop any
commit the set-difference fold (rule 1) would accept?

Yes. It stops exactly one class of commit, and rule 1 cannot see that class.

## Notation

`a` is a root key that stays live. `+k` adds key k, `-k` revokes it,
`[k]` means the commit is signed by k. Rule 1 checks a commit against its own
strict ancestors only. Rule 2 checks a merge: no commit reachable from one
parent and not from another may be signed by a key revoked in that other
parent's history.

## Case G: concurrent signature

```
B  +k [a]
├─ X:  R  -k [a]
└─ Y:  S  (change) [k]
M = merge(R, S) [a]
```

- Rule 1: S is valid (R is not in S's history). M is valid (signer a).
  live(M) = {a}. Rule 1 accepts every commit, and S stays in history,
  signed by a revoked key, with nothing against it.
- Rule 2: S is reachable from Y and not from X, and k was revoked on X.
  M is rejected.

So rule 2 rejects a merge that rule 1 accepts, even though the live set is
the same either way. The live set is the wrong measure: rule 1 governs
which keys may sign from now on, and rule 2 governs which past signatures a
branch may import. Cycle 47's case F (a concurrent add) is one instance; G
is the general one, since any commit, not only an add, can be signed by k.

A k-signature made after the merge needs no rule 2: R is then an ancestor
and rule 1 rejects it. Rule 2 matters only for signatures concurrent with
the revoke.

## Criss-cross: no new hole

```
M1 = merge(R, S) on X      M2 = merge(S, R) on Y
```

Rule 2 uses reachability sets, not a merge base, so having two merge bases
changes nothing. Both M1 and M2 import S across R and both are rejected.

## Octopus: one wording trap

```
P1: R -k [a]     P2: S [k]     P3: merge(P2, Q) [a]   (Q never saw R)
M = merge(P1, P2, P3)
```

S is reachable from P2 and from P3, and not from P1. If "brought in from
one parent" means "reachable from exactly one parent", S is skipped and M
passes. Rule 2 has to be checked for each ordered pair of parents (p, q):
commits in reach(p) \ reach(q) against the revokes in q's history. Checked
that way, M is rejected through the pair (P2, P1).

## The repair from cycle 47 launders a stolen key

Cycle 47 proposed that a branch clears a rejection by revoking the key
itself, so a k-signed commit is excused if it is an ancestor of some revoke
of k. Here is the attack, using only k:

```
B  +k [a]
├─ X:  R   -k [a]
└─ Y:  S1  +j [k]        valid under rule 1: k is live on Y
       S2  -k [j]        valid: j is live after S1
M = merge(R, S2) [a]
```

- Rule 2 as worded rejects M (S1 is signed by k).
- With the repair, S1 is an ancestor of S2, which revokes k, so M passes.
  live(M) = {a, j}. Whoever stole k now holds j, a live key that no revoke
  will ever reach.

Revoking k on Y proves nothing when the revoke can come from k or from a
key k created.

## Position

Keep rule 2 strict and per pair of parents. A branch that holds a
k-signature concurrent with a revoke of k cannot be merged until it is
rewritten without that commit. Do not add the revoke-it-yourself repair.
The only repair that would be safe is a revoke signed by a key whose add
chain contains no k-signature, and checking that is a third rule, not a
small change to rule 2.

Open: the test above is reasoned by hand, not run. A stuff turn that builds
G, the octopus and the laundering case in a throwaway repo and runs both
folds would confirm or break it.
