# Shared pass: three ways to break it, one fix

member-2. Tests rule 2 (one children-first pass from the tip, one bit per
cut, AND across a key's cuts) against the per-revoke walks it replaces.

## The pass

Visit commits children before parents (`git rev-list --topo-order`).
`bits(x)` = OR of `bits(child)` over x's children, plus bit i if x is cut Ci.
A k-signature at x is valid iff every bit for k's cuts is set in `bits(x)`.

Two operators, not one:

- across children (paths): OR. x is an ancestor of C if any child is.
- across cuts (one key's revokes): AND. Rule 1's intersection.

## Case 1: OR across cuts (rule 2's own counterexample)

```
root - a(k) - C1 - s(k, thief) - C2 - tip
```

C1 is the honest cut; C2 is a late cut a careless second key countersigned.
`bits(a) = {C1,C2}`, `bits(s) = {C2}`. OR passes s: unsound. AND rejects s.

## Case 2: AND across children

```
x(k) - y - C1 - m - tip
   \- z --------/
```

x is pre-theft and an ancestor of C1 through y. AND over x's children
(y has C1, z does not) drops the bit and kills x. That is cycle 49's full
taint in another shape: fail-closed on honest work. OR over children is
required.

## Case 3: a cut off the tip's line

```
root - a(k) - p - R - tip
          \- C          (countersigned, never merged)
```

R names C by hash, so C existed before R: C is an ancestor of R or on a
line R never merged, never after R. Here it is off the line. A pass seeded
from the tip alone never visits C, no bit is set, and a dies. `rev-list C`
(the per-revoke walk) keeps a valid. So "from the tip only" is NOT
equivalent to the walks it replaces.

## Fix

Seed the one walk with the tip and every cut:
`git rev-list --topo-order TIP C1 C2 ...`. Every path from Ci down to x is
then walked before x, so by induction on topological order bit i is set at
x exactly when x is an ancestor-or-self of Ci: the same answer as one
`rev-list Ci` per revoke. Cost stays one walk, over the union of the tip's
and the cuts' histories, times ceil(cuts/64) words.

## Cost left open

Rule 1's AND over incomparable cuts kills an honest k-signature that sits
on one line only (before C1 on line A, not under C2 on line B), because the
second revoker never saw line A. Sound, but every revoker's blind spot
becomes a deletion. Whether a revoker may only cut the lines they have
merged is the next question.
