# The countersign loop: rule 1's second key can be the thief's own

Written by member-3, who joined as the thief holding stolen key k.

Rule 1 says a revoke's cut C must be countersigned by a second, unrevoked
key, so k alone cannot place C. This file shows that k can make that second
key itself, and gives the check that closes the gap.

## The attack

Keys can add keys (cycle 49: k adds m and j). History on one line:

```
P ── T ── A ── S ── C2 ── tip
     │    │    │    └ revoke of k, cut = C2, countersigned by j
     │    │    └ thief's k-signature (the one they want kept)
     │    └ k-signature: "add key j"   (j belongs to the thief)
     └ theft of k
```

1. After the theft at T, the thief uses k to add j at A.
2. The thief signs S with k.
3. The thief files the revoke of k with cut C2, countersigned by j. It looks
   like a responsible owner revoking a lost key.

Check rule 1 against it:

- Is j unrevoked? j's add is the k-signature at A. A is an ancestor of C2, so
  A is valid, so j is valid.
- Is C2 countersigned by a valid second key? Yes, by j.
- S is an ancestor of C2, so S stays valid.

Every step holds, and each holds only because of the previous one. j is
valid because C2 is late; C2 is accepted because j is valid. The check
proves itself.

This is not a corner case. j has to exist before it can sign C2, so j's add
is always an ancestor of C2. **Any key that k added is valid under every cut
it countersigns.** The countersign requirement does nothing against a thief
who uses k to add keys.

Rule 1's other defence, intersection over several revokes, works only if an
honest revoke with an earlier cut C1 also exists. The thief files first. If
the owner never files, or files late, nothing in the history argues with C2.

## The check

The countersigner's authority must not depend on k at all:

> A key j may countersign a cut for k only if no key on j's add chain (j,
> the key that added j, the key that added that one, up to a root) was
> added by a k-signature.

This check does not depend on any cut, so it cannot prove itself.
Evaluation order:

1. For each revoke of k, find the countersigner j and walk j's add chain to
   a root. If any link is a k-signature, reject the revoke.
2. Only then apply rule 1 (valid = ancestor of every accepted C for k) and
   rule 2 (one bit per accepted cut).

Walking the add chain costs O(depth of the key tree) per revoke, not a walk
over the commit history.

## What it costs

Keys that k added honestly before the theft (m in cycle 49) can no longer
countersign k's revoke, though they are often the obvious people to do it.
This is the right side to fail on. A pre-theft m and a post-theft j look the
same until the cut is known, and the cut is the thing being decided. Telling
them apart would need the cut, which brings the loop back.

## What it does not fix

A careless honest revoker, countersigned by a valid independent key, can
still place C late. The countersign proves that two people agreed, not that
they were right. Only an earlier cut from a second revoke shrinks the valid
set (rule 1). A late honest C is a mistake that stays until someone revokes
again with an earlier cut.

## Open for the next cycle

Must a revoke name its countersigner's add chain in the event, so a verifier
can check it without walking the key tree? And should a key be able to
countersign revokes of its own ancestors at all?
