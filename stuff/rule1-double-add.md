# Rule 1 after rule 2: the cascade needs taint, not "only add"

member-3, cycle 49. This answers the first half of the direction: what work
is left for rule 1 once rule 2 handles the ordering.

## Rule 2 alone holds at the tip

Take the explicit revokes only. Suppose some tip T fails: a k-signed commit S
and a revoke R of k are both reachable from T, and S is not an ancestor of R.
Every descendant of T can still reach S and R, and S is still not an ancestor
of R. So a failure never goes away later in history, and a pass at T is a pass
at every ancestor of T. The single check at the tip therefore gives the same
answer as checking every merge. A k-signature merged in after R is a descendant
of R or concurrent with it, so it is never an ancestor of R and it fails.

My join claim, that a later merge could slip a k-signature past the tip check,
does not hold for explicit revokes.

## Rule 1's cascade breaks it

Rule 1: "Revoking k also revokes every key whose only reachable add was signed
by k." It goes one level and looks at one signer. The thief needs only k:

```
A1  add m, signed k
A2  add j, signed k
A3  add j, signed m
R   revoke k
```

- m: its only add (A1) is signed by k, so the cascade kills m.
- j: it has two adds, signed by k and by m. Its only add is not k's, and its
  only add is not m's either, so neither cascade kills it. The first sentence
  ("live once an add signed by a live key is reachable") already made j live
  at A2, when k was live.
- So the thief keeps j. This is the same laundering that cycle 48 removed from
  the revoke-it-yourself repair, just moved one add further along.

It also breaks the monotone property above if rule 2 counts cascade revokes.
At a tip that has only A2 and R, R kills j, and a j-signed commit after R
fails. Merge in an honest add of j by a live key and j has two adds, the
cascade no longer reaches it, and the same commit passes. A failure that goes
away later in history means checking once at the tip is no longer enough.

## What rule 1 should say instead

A key is dead at the tip if it was revoked, or if any key that signed any
reachable add of it is dead. Death follows the add edges forward from every
revoked key, through every add, not only through a key's single add.

- Double add: k dead, so m is dead (A1) and j is dead (A2 or A3).
- More history only adds revokes and adds, and each of those can only kill
  more keys, so a key that is dead at T is dead at every descendant of T. A
  second honest add cannot bring j back. This is rule 1's "never re-added;
  its holder makes a new key", applied to the cascade too.
- Cost: one pass over the add/revoke events at the tip, following each add
  edge once. It does not depend on the order of events, so rule 1 stays a
  single pass.

## The one piece rule 1 still owes rule 2

Rule 1 says which keys are dead. Rule 2 has to know which revoke each death
came from. For a key j killed by the cascade, its kill set is every revoke R
of a key on an add chain leading to j. Rule 2 then reads: every j-signed
commit reachable from the tip is an ancestor of every R in j's kill set. Kill
sets only grow, so this wording keeps the monotone property and a tip check is
still enough. The cost is one `rev-list TIP ^R` walk per revoke, as in
`tip-check-cost.md`. Each walk now marks the signatures of every key that
revoke kills, not only those of the key it names.
