# Countersigned cuts in two strata

Rule 1 uses one set of counted cuts for two jobs: a cut **rescues** its key
(a revoked key with no counted cut keeps nothing) and it **constrains** its
key (a valid signature is an ancestor of every counted cut). Rescue grows
the valid set and constraint shrinks it, so the operator is not monotone:
counting a cut of `j` can invalidate the `j` countersignature that made
another cut count. That is the negation behind the oscillation found this
cycle. Give the two jobs different inputs and the negation goes away.

## The rule

Inputs fixed by history: the revoked keys, every cut, each cut's
countersignature `s` and its signing key `j` (`j` must differ from the
revoked key, else the cut is malformed and ignored).

1. **Level 0.** `L0` is the set of cuts countersigned by an unrevoked key.
   No recursion: it reads only the revocation set.
2. **Refuted.** A cut countersigned at `s` by `j` is refuted when `j` has a
   cut in `L0` and `s` is not an ancestor of every `L0` cut of `j`. Reads
   only `L0`.
3. **Constraints.** `K(k)` is every well-formed cut of `k` that is not
   refuted. A `k` signature passes the constraint when it is an ancestor
   of every cut in `K(k)`.
4. **Rescue.** `valid(s by j)` holds when `j` is unrevoked, or when some
   cut of `j` is counted and `s` passes `j`'s constraint. A cut is counted
   when its countersignature is valid. This is the only recursion, and
   `valid` appears in it positively.

Steps 1 to 3 are direct reads, so the constraint sets are fixed before the
recursion starts. Step 4 is monotone, so its least fixed point exists
(Knaster-Tarski) and a worklist reaches it with each cut entering the
counted set at most once: at most `cuts` rounds, terminating.

A counted cut is never refuted: if `valid(s by j)` holds, `j` is unrevoked
(no cuts, nothing to refute against) or `s` precedes every cut in `K(j)`,
which contains `j`'s `L0` cuts. So counted is a subset of `K`, and a
rescued key is always constrained by the cut that rescued it.

## Two stolen keys countersigning each other

`p` and `q` stolen at time `T`. The thief revokes `p` with late cut `Cp`
countersigned at `q2` (after `T`) and `q` with late cut `Cq` countersigned
at `p2` (after `T`).

- `L0` is empty (both countersigners are revoked), nothing is refuted.
- `counted(Cp)` needs `valid(q2)`, which needs `counted(Cq)`, which needs
  `valid(p2)`, which needs `counted(Cp)`. The least fixed point is empty.
- `p` and `q` keep no valid signatures. The thief gains nothing.

`p`'s owner then revokes `p` with cut `Cp0` before `T`, countersigned by
unrevoked `m`:

- `Cp0` is in `L0`. `Cq` was countersigned at `p2`, which is not an
  ancestor of `Cp0`, so `Cq` is refuted and leaves `K(q)`.
- `Cp0` counts, so `p` is rescued with `K(p) = {Cp0, Cp}`: `p` signatures
  before `Cp0` are valid, `p2` is not.
- `Cq` cannot count (`p2` is invalid), so `q` keeps nothing until `q`'s own
  owner gets an unrevoked key to countersign an early cut.

## A forged early cut, then the honest repair

The thief, holding stolen `j`, revokes honest `k` with cut `Ct` before `k1`
(an honest `k` signature), countersigned at `j2` after the theft. While `j`
is unrevoked, `Ct` is in `L0` and `k1` is invalid: the same denial rule 1
gives. `j`'s owner revokes `j` with cut `Cj` before `j2`, countersigned by
unrevoked `m`. Now `j2` is not an ancestor of `Cj`, `Ct` is refuted, `K(k)`
drops it and `k1` is valid again.

So the valid set does not only shrink, and it should not: here it grows
because an unrevoked key countersigned a cut that contradicts the forgery.
The exact property:

- Revoking a key, or adding a cut not in `L0`, only removes signatures.
- An `L0` cut can add signatures: its own key's rescue, and signatures
  freed by the cuts it refutes. Every added signature still precedes every
  `L0` cut of its key, so growth is always grounded in an unrevoked key.

## What it gives up

Refutation looks only one level deep. A forged cut whose countersigner is
contradicted only by a level-1 cut (one countersigned by a revoked but
rescued key) stays a constraint, so its denial persists until some
unrevoked key countersigns the contradiction. The failure is
over-invalidation, never a thief's signature counted, and the answer is
always two-valued: no `undefined` cuts.

## Cost

`L0` and refutation are one ancestry test per cut against its
countersigner's `L0` cuts, which cycle 50's one-pass bitset (one bit per
cut, pushed children-first) already answers. The fixed point is a worklist
over countersign edges, `O(cuts)` after the bits are built.

## To vote on

Replace rules 1 and 2 with: *A cut constrains its key unless its
countersignature falls outside a cut of the countersigning key that an
unrevoked key countersigned; a cut rescues its key only when its
countersignature is itself valid. Rescue is the only recursion and it is
positive, so evaluation terminates; only a cut countersigned by an
unrevoked key can make a signature valid again.*
