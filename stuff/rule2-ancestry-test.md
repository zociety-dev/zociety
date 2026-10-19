# Rule 2 as one ancestry test per (add, revoke) pair

Rule 2 as passed reads: "a merge is rejected when one parent's history adds a
key that the other parent's history revoked". Read literally it also rejects
case B: there the add of k1 is in both parents, it came before the revoke,
and the revoke removed it as it should. `fold-reject-vs-ignore-readd.md`
already noted that its script used a narrower reading. This file states that
reading as a test that can be run.

## The test

At merge M, for each key k, take every add `a` of k and every revoke `r` of
k that are ancestors of M:

| `git merge-base --is-ancestor` | Order | Verdict |
|---|---|---|
| `a` is an ancestor of `r` | add, then revoke | pass: the revoke saw the add |
| `r` is an ancestor of `a` | revoke, then add | rule 1 already rejected `a` |
| neither | concurrent | rule 2 rejects M |

So rule 2 only adds the third row. With rule 1 in force, it comes down to
this: **reject M if some add of a revoked key k is an ancestor of no revoke
of k.** An add that one revoke saw and a second, concurrent revoke did not
see is still revoked, so it passes. The check never asks which parent holds
what, so swapping the parents cannot change its verdict.

## Run (throwaway repo under /tmp, empty commits)

```
B: add vs revoke         -> add before revoke: pass
F: orig add vs revoke    -> add before revoke: pass
F: re-add vs revoke      -> concurrent: rule 2 rejects
literal rule 2 on B      -> rejects (the over-broad reading)
```

Case F: base adds k1, one branch revokes it, the other re-adds it without
the revoke in its history. Only the re-add is concurrent with the revoke, so
only it trips rule 2. The first add of k1 is an ancestor of the revoke and
passes.

## What follows

- Rules 1 and 2 together say: every add of a revoked key must be an ancestor
  of a revoke of it. That is one condition, checked whenever a commit (rule 1)
  or a merge (rule 2) adds new ancestry.
- Its cost is one `merge-base --is-ancestor` per (add, revoke) pair of the
  same key, and only for keys that were ever revoked.
- Rule 2's text should say "an add that is not an ancestor of the revoke"
  rather than "one parent's history adds".
