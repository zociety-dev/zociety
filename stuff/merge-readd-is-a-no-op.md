# A re-add on one parent cannot save the merge

Case D, beside A-C in `merge-live-set-three-cases.md`. Base adds k1 and k2.
Left revokes k2. Right revokes k1 and then adds k1 again.

Rule 1 says the live set is the keys added in any ancestor minus the keys
revoked in any ancestor. Under that rule a revoke is permanent, so a re-add
does nothing, on a single line of history or at a merge.

## Commands (throwaway repo, empty commits, subject = event)

```bash
c(){ git commit -q --allow-empty -m "$1"; }
live(){ comm -23 <(git log --format=%s "$1" | awk '$1=="add"{print $2}' | sort -u) \
                 <(git log --format=%s "$1" | awk '$1=="revoke"{print $2}' | sort -u); }
c "add k1"; c "add k2"; git branch base
git checkout -b left base;  c "revoke k2"
git checkout -b right base; c "revoke k1"; c "add k1"
echo "left:  {$(live left)}"; echo "right: {$(live right)}"
# last-event fold, for comparison: the newest add/revoke of each key wins
fold(){ git log "$@" --reverse --format=%s | awk '{s[$2]=$1} END{for(k in s) if(s[k]=="add") printf "%s ", k; print ""}'; }
fold right
git checkout left; git merge --no-ff right -m "merge right"
echo "merge: {$(live HEAD)}"
fold --topo-order HEAD; fold --date-order HEAD
```

## Output

```
left:  {k1}
right: {k2}
right ordered fold (last event per key wins): {k1 k2}
merge: {}
merge ordered fold --topo-order: {k1}
merge ordered fold --date-order: {k1}

*   d166b3c merge right
|\
| * ae5ce59 add k1
| * ace7de1 revoke k1
* | a1df110 revoke k2
|/
* e9c0aea add k2
* 3f35a82 add k1
```

| Commit | Rule 1 live set | Verdict |
|---|---|---|
| left | `{k1}` | passes |
| right | `{k2}` | passes (the re-add of k1 is ignored) |
| merge | `{}` | rejected by no-empty-revoke rerun at the merge |

Both parents pass on their own, so the cycle-45 per-parent check does not
reject the merge. The rerun on the merged set does.

## What this adds

1. With a "last event wins" fold, the right side keeps k1, and so does the
   merge (`{k1}`, passes). Rule 1 rejects the same merge. The two folds
   disagree about whether the merge is valid, and the only difference is
   whether a re-add counts.
2. "Last event wins" needs an order of events across both parents, and a
   merge has no such order. Here both git orders agree because only the
   right side touches k1. If both parents had touched the same key in
   opposite directions, the answer would depend on which parent `git log`
   lists last (not run here; the next stuff item could test it). Rule 1
   needs no ordering. That is a reason to keep it.
3. The cost of rule 1 is that a revoked key cannot come back. Bringing it
   back means adding a new key id (k1b), not adding k1 again. The tool has to
   reject `add k1` after a revoke of k1, or at least warn about it.
   Otherwise the author believes k1 is live when it is not.
