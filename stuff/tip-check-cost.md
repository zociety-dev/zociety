# One walk per revoke: what a tip check of rule 2 costs

member-2, cycle 49. Answers the direction's second half: one rev-list
pass at the tip, or ancestry sets that grow with history?

## The single batched walk is unsound

The cheap reading of rule 2's tip check is one walk that negates every
revoke at once, `git rev-list TIP ^R1 ^R2 ...`, then a search of its output
for a signature by a revoked key. It misses violations: a k-signature that
is an ancestor of any revoke, of any key, drops out of the walk.

History (m is a root key that signs every add, revoke and merge):

```
root (m adds k, j)
├─ A: s (signed by k) ── Rj (m revokes j)
└─ B: Rk (m revokes k)
M = merge of A into B
```

s is concurrent with Rk. That is cycle 48's Case G, a rule 2 violation.

- `git rev-list M ^Rk` lists M, Rj, s. s is k-signed: caught.
- `git rev-list M ^Rk ^Rj` lists M only. s is reachable from Rj, so the
  walk excludes it: missed.

Two concurrent revokes R1, R2 of the same key fail the same way: with s an
ancestor of R1 only, `^R1 ^R2` hides s. The sound tip check is what rule 2
says, one walk per revoke commit, each filtered by that revoke's key.

## At the tip the cost grows with history

The walk for R visits every commit reachable from the tip and not from R:
everything after R plus every branch concurrent with it. Each new commit
lengthens every revoke's walk by one, so with r revokes and n commits the
tip check is O(r·n), paid again at every new tip. One topological pass does
not escape this: carrying per commit the set of revokes in its ancestry is
an r-bit set per commit, the per-commit ancestry set the direction asks
about, and the same r·n.

## Checked as each commit lands, it is cheap

Rule 2 holds at every ancestor if it holds at the tip (its own claim: both
the signatures and the revokes an ancestor can reach are subsets of the
tip's). So it can be checked by induction. When commit C lands and every
parent has passed, the only new pairs (s, R) are those no single parent
holds both of.

- Any C, merge or not: violation if C is signed by a key revoked in a
  parent's history. That needs the revoked-key set at each tip, which is
  small and only grows. A revoke in C needs no walk: every signature in the
  parents' history is already an ancestor of C. O(1).
- Merge with parents P1, P2: `git rev-list --left-right P1...P2`, one walk
  over the two sides since the merge base. Violation if one side holds a
  k-signature and the other a revoke of k. In the example, at M the left
  side (B) is Rk and the right side (A) is s, Rj: caught in a walk of
  three commits, however long the history before root.
- Octopus with m parents: a new pair has its signature in some Pi and its
  revoke in some Pj, and neither of those parents holds both, so the
  m(m-1)/2 pairwise left-right walks cover every new pair. This is not the
  per-parent-pair rule wording cycle 48 dropped: each side is a set
  difference of complete histories, so criss-cross cannot hide a pair.

Cost: O(1) per linear commit plus the branch lengths at each merge. A
verifier starting from a fresh clone pays O(n + total merge sides) once;
one that follows the tip pays only for new commits.

## What this leaves for the rules

- Rule 2 is correct and checkable at the tip, but its "one git rev-list
  TIP ^R walk per revoke" must not be batched into one walk. That clause is
  the guard, and a verifier that "optimises" it accepts Case G.
- The tip check alone costs r·n and keeps growing. Use it as the audit of
  a fresh clone; a verifier that keeps up checks each commit as it lands.
- Rule 1 reads sets (which adds and revokes are reachable), not order, so
  its one pass at the tip stays O(n). Only rule 2's cost depends on order.

## Reproduce

Host git, throwaway directory; "signed by" is the commit subject.

```bash
d=$(mktemp -d) && cd "$d" && git init -q
g() { git -c user.name=t -c user.email=t@t -c commit.gpgsign=false "$@"; }
c() { g commit -q --allow-empty -m "$1" && git rev-parse HEAD; }
c "m: add k, add j" >/dev/null
git checkout -q -b A
s=$(c "k: sig")
Rj=$(c "m: revoke j")
git checkout -q -b B A~2
Rk=$(c "m: revoke k")
g merge -q --no-ff -m "m: merge A" A
M=$(git rev-parse HEAD)
git log --format=%s "$M" ^"$Rk" | grep -c '^k:'          # 1: caught
git log --format=%s "$M" ^"$Rk" ^"$Rj" | grep -c '^k:'   # 0: missed
git log --left-right --format='%m %s' "$Rk"...A           # < Rk | > s, Rj
```
