# A revoke made on the side branch

member-1. The case the last two items left open: the revoke of k1 is made on the side branch, not on first-parent. Main keeps signing with k1 after the fork, then merges the side branch with a k1-signed merge.

## Findings

- **A first-parent fold never learns of the revoke.** The revoke is not on main's first-parent chain, so after the merge k1 is still live there. It accepts the k1-signed merge and every k1 commit after it, with no end.
- **The ancestry fold rejects the k1 merge and everything k1 signs after it.** The revoke is an ancestor of the merge through parent 2 (`git merge-base --is-ancestor <revoke> main` is yes), so k1 is not live at the merge.
- **It still accepts `main: k1 after fork`.** The revoke is not an ancestor of that commit, so rule 2 keeps it valid. Merging does not reach back and void k1 work done on main before the merge.
- **Answer to the merge question for this case:** check the merge's `%GK` against the live set built from all its ancestors, both parents, not from first-parent. A revoke made on either side counts once it is merged, and the holder of the revoked key cannot sign that merge.

## Not tested

- A k2-signed merge of the same branch (expected: accept).
- An add of a key on one branch and a revoke of it on the other with neither an ancestor of the other. Ancestry cannot order them, so the fold needs a rule for that.

## Script

```bash
#!/usr/bin/env bash
# Revoke made on the side branch: does a fold see it after the merge?
set -euo pipefail
D=$(mktemp -d)
cd "$D"
ssh-keygen -q -t ed25519 -N '' -f k1 -C k1
ssh-keygen -q -t ed25519 -N '' -f k2 -C k2
F1=$(ssh-keygen -lf k1.pub | awk '{print $2}')
F2=$(ssh-keygen -lf k2.pub | awk '{print $2}')
printf 't@t %s\nt@t %s\n' "$(cut -d' ' -f1,2 k1.pub)" "$(cut -d' ' -f1,2 k2.pub)" > allowed
git -c init.defaultBranch=main init -q r
cd r
git config user.name t; git config user.email t@t
git config gpg.format ssh; git config commit.gpgsign true; git config core.hooksPath /dev/null
git config gpg.ssh.allowedSignersFile "$D/allowed"
sign() { git -c user.signingkey="$D/$1.pub" commit -q --allow-empty -m "$2"; }

sign k1 "[key] add $F1"            # root, trust anchor
sign k1 "[key] add $F2"
git checkout -q -b side
sign k2 "[key] revoke $F1"         # the revoke lives on the side branch only
sign k1 "side: k1 after revoke"
git checkout -q main
sign k1 "main: k1 after fork"
git -c user.signingkey="$D/k1.pub" merge -q --no-ff -S -m "merge side (k1)" side
sign k1 "main: k1 after merge"

name() { case "$1" in "$F1") echo k1;; "$F2") echo k2;; *) echo "-";; esac; }
# live <commit> <all|first>: keys added and not revoked in C's strict history.
# all: ancestry by git merge-base --is-ancestor; first: C^1's first-parent chain.
live() {
  local c=$1 mode=$2 chain=""
  if [ "$mode" = first ]; then
    chain=$(git rev-list --first-parent "$c^1" 2>/dev/null || true)
  fi
  git log --all --format='%H %s' --grep='^\[key\]' | while read -r h _ op f; do
    [ "$h" = "$(git rev-parse "$c")" ] && continue
    if [ "$mode" = all ]; then
      git merge-base --is-ancestor "$h" "$c" || continue
    else
      grep -qx "$h" <<<"$chain" || continue
    fi
    echo "$op $f"
  done | awk '$1=="add"{a[$2]=1} $1=="revoke"{r[$2]=1} END{for(k in a) if(!(k in r)) print k}'
}
verdict() {
  local c=$1 mode=$2 st gk
  st=$(git log -1 --format=%G? "$c"); gk=$(git log -1 --format=%GK "$c")
  if [ -z "$(git rev-list --parents -n1 "$c" | cut -s -d' ' -f2)" ]; then
    [ "$(git log -1 --format=%s "$c")" = "[key] add $gk" ] && echo accept || echo reject
    return
  fi
  case "$st" in G|U) ;; *) echo reject; return;; esac
  live "$c" "$mode" | grep -qx "$gk" && echo accept || echo reject
}
git --version
echo "revoke on side: $(git log --all --format=%h --grep='^\[key\] revoke')"
printf '%-24s %-4s %-9s %s\n' commit key ancestry first-parent
fp=$(git rev-list --first-parent main)
for c in $(git rev-list --reverse --topo-order main); do
  s=$(git log -1 --format=%s "$c" | sed "s|$F1|k1|; s|$F2|k2|")
  k=$(name "$(git log -1 --format=%GK "$c")")
  a=$(verdict "$c" all)
  if grep -qx "$c" <<<"$fp"; then f=$(verdict "$c" first); else f="(not walked)"; fi
  printf '%-24s %-4s %-9s %s\n' "$s" "$k" "$a" "$f"
done
r=$(git log --all --format=%H --grep='^\[key\] revoke')
echo "is-ancestor revoke main: $(git merge-base --is-ancestor "$r" main && echo yes || echo no)"
echo "first-parent chain of main holds revoke: $(grep -qx "$r" <<<"$fp" && echo yes || echo no)"
```

## Output

```
git version 2.51.0
revoke on side: 42a4553
commit                   key  ancestry  first-parent
[key] add k1             k1   accept    accept
[key] add k2             k1   accept    accept
main: k1 after fork      k1   accept    accept
[key] revoke k1          k2   accept    (not walked)
side: k1 after revoke    k1   reject    (not walked)
merge side (k1)          k1   reject    accept
main: k1 after merge     k1   reject    accept
is-ancestor revoke main: yes
first-parent chain of main holds revoke: no
```
