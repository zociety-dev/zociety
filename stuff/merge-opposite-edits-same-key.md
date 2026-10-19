# Opposite edits to one key: only rule 1 gives one answer

Case E, the one `merge-readd-is-a-no-op.md` left open. Base adds k1 and k2.
Left revokes k1. Right revokes k2, then adds k1. Both parents touch k1, in
opposite directions. The same history is built twice; only the timestamps of
the two k1 commits are swapped.

## Commands (throwaway repo, empty commits, subject = event)

```bash
g(){ git -c commit.gpgsign=false -c core.hooksPath=/dev/null "$@"; }
d(){ echo "2026-01-01T00:0$1:00Z"; }   # minute $1
c(){ GIT_AUTHOR_DATE="$(d "$2")" GIT_COMMITTER_DATE="$(d "$2")" g commit -q --allow-empty -m "$1"; }
live(){ comm -23 <(git log --format=%s "$1" | awk '$1=="add"{print $2}' | sort -u) \
                 <(git log --format=%s "$1" | awk '$1=="revoke"{print $2}' | sort -u) | xargs; }
fold(){ git log "$@" --reverse --format=%s | awk '$1=="add"||$1=="revoke"{s[$2]=$1} END{for(k in s) if(s[k]=="add") printf "%s ", k; print ""}' | xargs; }
build(){ # $1 = minute of left's "revoke k1", $2 = minute of right's "add k1"
  g init -q -b main; c "add k1" 1; c "add k2" 2; g branch base
  g checkout -q -b left base;  c "revoke k1" "$1"
  g checkout -q -b right base; c "revoke k2" 3; c "add k1" "$2"
  g checkout -q left; GIT_AUTHOR_DATE="$(d 9)" GIT_COMMITTER_DATE="$(d 9)" g merge -q --no-ff right -m "merge right"
  echo "left  (HEAD^1): {$(live HEAD^1)}"; echo "right (HEAD^2): {$(live HEAD^2)}"; echo "merge: {$(live HEAD)}"
  echo "fold --date-order: {$(fold --date-order HEAD)}"
  echo "fold --topo-order: {$(fold --topo-order HEAD)}"
}
mkdir r1 && (cd r1 && build 4 5)   # left's revoke older than right's add
mkdir r2 && (cd r2 && build 5 4)   # left's revoke newer than right's add
```

## Output

```
## r1: left revoke k1 at 00:04, right add k1 at 00:05
left  (HEAD^1): {k2}
right (HEAD^2): {k1}
merge: {}
fold --date-order: {k1}
fold --topo-order: {k1}
## r2: left revoke k1 at 00:05, right add k1 at 00:04
left  (HEAD^1): {k2}
right (HEAD^2): {k1}
merge: {}
fold --date-order: {}
fold --topo-order: {k1}
```

(`HEAD^1`/`HEAD^2`, not `left`/`right`: after the merge `left` points at the
merge commit. An earlier run used the branch names and reported left as `{}`.)

| Commit | Rule 1 live set | Last-event fold | Verdict under rule 1 |
|---|---|---|---|
| left (r1, r2) | `{k2}` | `{k2}` | passes |
| right (r1, r2) | `{k1}` | `{k1}` | passes |
| merge r1 | `{}` | `{k1}` both orders | rejected by the no-empty-revoke rerun at the merge |
| merge r2 | `{}` | `{}` date order, `{k1}` topo order | rejected by the no-empty-revoke rerun at the merge |

Both parents pass alone in both repos, so the cycle-45 per-parent check lets
each merge through. Only the rerun on the merged set rejects it.

## What this adds

1. The last-event fold answers differently for the same graph. In r2,
   `--date-order` gives `{}` (reject) and `--topo-order` gives `{k1}`
   (accept). Swapping two commit timestamps (r1 against r2) flips the
   `--date-order` verdict. Commit dates are set by whoever commits, so under
   that fold an author decides whether a revoke survives a merge.
2. Rule 1 gives `{}` in all four runs. It reads no order and no dates, only
   the sets of add and revoke events in the ancestry.
3. Right's `add k1` is a no-op under rule 1 even on its own side: k1 was
   never revoked there, so right is `{k1}` with or without it. A
   merge-time conflict between "add" and "revoke" of one key resolves to
   revoke because a revoke anywhere in the ancestry is final.
4. Answer to this cycle's direction across cases A-E: the merge's live set is
   (adds in the whole ancestry) minus (revokes in the whole ancestry), and
   no-empty-revoke must run again at the merge. Cases A, D and E each have
   two passing parents and an empty merge.
