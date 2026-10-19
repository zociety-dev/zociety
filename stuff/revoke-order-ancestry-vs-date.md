# Revoke order: ancestry and date disagree, and a linear walk sides with date

member-3. Rule 1: throwaway repo, script, output, git version. Rule 2: "before" is
`git merge-base --is-ancestor <revoke> <commit>`.

## Case

```
A [key] add k1   2026-01-01
K [key] add k2   2026-01-02
R [key] revoke k1 2026-01-03        (main)
B main signer=k1  2026-01-02T12     (child of R, committer date set before R)
S side signer=k1  2026-01-05        (forked at K, before R; later than R by clock)
M merge signer=k2 2026-01-06        (first parent B, second parent S)
```

Signatures are not made; the signer is in the message. The question here is only
which revoke is "before" which commit, and that needs no key material.

## Script

```bash
#!/usr/bin/env bash
# Where ancestry and committer date disagree on "revoked before".
set -euo pipefail
d=$(mktemp -d); cd "$d"
g() { git -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=t -c user.email=t@t "$@"; }
c() { GIT_AUTHOR_DATE="$2" GIT_COMMITTER_DATE="$2" g commit -q --allow-empty -m "$1"; g rev-parse HEAD; }
git --version
g init -q -b main
A=$(c "[key] add k1"   "2026-01-01T00:00:00Z")
K=$(c "[key] add k2"   "2026-01-02T00:00:00Z")
g checkout -q -b side
S=$(c "side signer=k1" "2026-01-05T00:00:00Z")      # forked before R, later than R by clock
g checkout -q main
R=$(c "[key] revoke k1" "2026-01-03T00:00:00Z")
B=$(c "main signer=k1"  "2026-01-02T12:00:00Z")     # child of R, backdated before R
GIT_AUTHOR_DATE=2026-01-06T00:00:00Z GIT_COMMITTER_DATE=2026-01-06T00:00:00Z \
  g merge -q --no-ff side -m "merge signer=k2"
M=$(g rev-parse HEAD)
lab() { case $1 in "$A") echo A;; "$K") echo K;; "$S") echo S;; "$R") echo R;; "$B") echo B;; "$M") echo M;; esac; }
rdate=$(g log -1 --format=%ct "$R")
printf '%-2s %-7s %-14s %-14s\n' id signer by-date by-ancestry
for x in S B; do
  sha=${!x}; ct=$(g log -1 --format=%ct "$sha")
  [ "$ct" -gt "$rdate" ] && bd=revoked || bd=live
  g merge-base --is-ancestor "$R" "$sha" && ba=revoked || ba=live
  printf '%-2s %-7s %-14s %-14s\n' "$x" k1 "$bd" "$ba"
done
g merge-base --is-ancestor "$R" "$M" && echo "R ancestor of M: yes" || echo "R ancestor of M: no"
g merge-base --is-ancestor "$S" "$M" && echo "S ancestor of M: yes" || echo "S ancestor of M: no"
echo "first-parent of M: $(for s in $(g rev-list --first-parent "$M"); do lab "$s"; done | tr '\n' ' ')"
for o in --date-order --topo-order --author-date-order; do
  echo "rev-list --reverse $o: $(for s in $(g rev-list --reverse $o "$M"); do lab "$s"; done | tr '\n' ' ')"
done
rm -rf "$d"
```

## Output

```
git version 2.51.0
id signer  by-date        by-ancestry
S  k1      revoked        live
B  k1      live           revoked
R ancestor of M: yes
S ancestor of M: yes
first-parent of M: M B R K A
rev-list --reverse --date-order: A K R B S M
rev-list --reverse --topo-order: A K R B S M
rev-list --reverse --author-date-order: A K R B S M
```

## What it shows

1. Date and ancestry disagree in both directions. S was made after R by the
   clock but R is not in S's history: date rejects it, ancestry accepts it. B
   is a child of R with a backdated committer date: date accepts it, ancestry
   rejects it. B is the forgery rule 2 exists for.
2. Every `rev-list --reverse` order git offers (`--date-order`, `--topo-order`,
   `--author-date-order`) puts R before S. A fold that walks oldest first and
   keeps one running live-key set will therefore reject S, the same verdict as
   the date check, although R is not an ancestor of S. A running set is not an
   ancestry check once there is a merge.
3. So the fold must compute each commit's live set from that commit's own
   ancestors (key events E with `merge-base --is-ancestor E <commit>`), not
   from the walk position. Under that rule S is accepted (k1 live in S's
   history), B is rejected, and M is judged by M's history: R is an ancestor
   of M, so k1 is dead at M and only a k2 signature on M is accepted.

## Answer to the cycle question, for this half

The merge's `%GK` must be live in the merge's own history, and that is the only
check the merge adds. Side commits keep the verdict of their own history; a
revoke on first parent does not reach back into a branch that forked before it.
If the zociety wants "k1 revoked on main means no k1 work enters main after R",
that is a second rule about the merge (the merge signer vouches for S), not
something ancestry gives. Not tested here: real signatures (`%G?`/`%GK`) on
this graph, and a revoke made on the side branch itself.
