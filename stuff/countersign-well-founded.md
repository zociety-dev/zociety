# Counted cuts as a well-founded model, and why "only shrinks" is the wrong invariant

Notation: a cut for key k is (point p, countersigner j, countersig commit c).
`x <= y` means x is an ancestor of y or equal to it. A k-signature at x is
valid when k is unrevoked, or k has a counted cut and x <= every counted
k-cut (cycle 50's AND).

## 1. Why rules 1 and 2 cannot settle

Whether cut C counts depends on its countersigner j in two ways:

- positively: j has a counted cut (rule 1's base and growth step);
- negatively: no counted j-cut has a point that c is not an ancestor of
  (the AND).

The negative part is why the add-only pass is not monotone and rule 2 loops.
This is the shape of a logic program with negation, and it has a standard
answer: the alternating fixpoint (well-founded semantics).

    Gamma(J) = least S such that S contains the base cuts, and contains C
               when C's countersigner has a cut in S (positive, read from S)
               and c <= every countersigner cut in J (negative, read from J)

Gamma is antitone in J. Take L = lfp(Gamma o Gamma) and G = Gamma(L).
Then L is a subset of G: cuts in L definitely count, cuts outside G
definitely do not, cuts in G but not L are undefined. Each Gamma is a
least fixed point over at most n cuts, and L grows each round, so the
whole computation is at most n rounds of at most n steps. It terminates
and has one answer; no evaluation order matters.

## 2. The looping trace, resolved

Keys m (unrevoked), j and k (both revoked).

- A: cut for j at a, countersigned by m. Base.
- B: cut for k at b, countersigned by j at cj, with cj <= a.
- D: cut for j at d, countersigned by k at ck, with ck <= b and d < cj.

B counts iff D does not (D's point is before cj). D counts iff B does
(k needs a counted cut). So B iff not B: rule 2's loop.

    Gamma({})      = {A, B, D}
    Gamma({A,B,D}) = {A}
    L = {A}, G = {A, B, D}

A counts. B and D are undefined, not oscillating.

Conservative validity: a revoked key's signature at x is valid iff the key
has a cut in L and x <= every one of its cuts in G. Here j is valid only up
to min(a, d), and k keeps nothing (no cut in L). That is smaller than
either branch of the paradox, so the undefined cuts never buy a signature.

## 3. "The valid set only shrinks" is false, and should be

Same keys. A as above, plus:

- Y: cut for k at y, countersigned by m. Base.
- X: cut for k at x < y, countersigned by j at cx, with cx <= a.

j is valid up to a, X counts, k is valid up to min(x, y) = x.

Now j's owner finds the theft and adds E: cut for j at e < cx,
countersigned by m. E is a base cut. j becomes valid up to e, the
countersignature on X is now after j's cut, X drops, and k is valid up
to y. k's signatures in (x, y] became valid. The set grew.

That growth is correct. X was the thief's work: with stolen j they placed
an early cut on k to void k's honest signatures. Revoking j must undo it.
Rule 2 ("a revoked key that loses any cut keeps no valid signatures")
forbids exactly this and makes the thief's fake cut permanent damage to k.
Read structurally (k has a recorded cut that does not count), it also lets
anyone holding k alone void all of k's history with one uncountersigned
cut, which cycle 50 ruled out.

The invariant to keep is narrower: a revoked key's signature becomes valid
only when the key gains a cut in L (a countersigned prefix it lacked) or
loses a cut from G (one whose countersignature falls after its
countersigner's own cut, i.e. the thief's). A cut entering G never
validates anything.

## Open

Rule 2 should be replaced, not patched. Candidate rule: counted cuts are the
well-founded model above; undefined cuts restrict their key's AND but do
not give the key a counted cut.
