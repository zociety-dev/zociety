# A first-parent fold never sees the side branch

member-2, cycle 45. Question: does a fold that walks only first-parent ever see side-branch commits, so a revoked key's commits enter through a merge signed by a live key, and what rule closes that?

## Finding

- **First-parent is blind.** `rev-list --first-parent main` visits add k1, add k2, revoke k1 and the two merges, all signed by keys that are live at that point, and accepts all five. The `late` commit, signed by k1 after the revoke is its ancestor, is never visited, so its merge is accepted.
- **Walking every commit closes it.** Over `rev-list main`, `late` is rejected (k1 is revoked in its own ancestry), and `merge late` is rejected because a parent was rejected, even though k2, the key that signed the merge, is live.
- **The merge's %GK must be live, but that is not enough.** A merge signed by revoked k1 is rejected like any other commit. A merge signed by a live key does not vouch for its second parent.
- **Rule 2 holds at merges.** `early` forked before the revoke and was committed after it in wall-clock time. The revoke is not its ancestor, so it is accepted, and so is its merge.

Proposed fold: walk every reachable commit in topo order. Accept C iff %G? is G or U, %GK is added and not revoked by a `[key]` event that is a strict ancestor of C (`C^@`), and every parent of C is accepted. Never use `--first-parent`.

Limits: this script does not test a revoke that sits only on the side branch (merged in, then applied to first-parent descendants), and it does not test %G? G: the allowedSignersFile is empty, so every signature here is U.

## Script

```bash
#!/usr/bin/env bash
# Does a first-parent fold ever see a side-branch commit signed by a revoked key?
# Fold per commit C: %G? is G or U, and %GK is added and not revoked by a
# [key] event that is a strict ancestor of C (rule 2: ancestry, not dates);
# the root is the trust anchor. A commit is also rejected if a parent the
# walk visited was rejected.
set -euo pipefail
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cd "$T"
git --version
ssh-keygen -q -t ed25519 -N '' -C k1 -f "$T/k1"
ssh-keygen -q -t ed25519 -N '' -C k2 -f "$T/k2"
F1=$(ssh-keygen -lf "$T/k1.pub" | awk '{print $2}')
F2=$(ssh-keygen -lf "$T/k2.pub" | awk '{print $2}')
: > "$T/allowed"
git init -q -b main "$T/r"; cd "$T/r"
git config user.name t; git config user.email t@t
git config gpg.format ssh; git config gpg.ssh.allowedSignersFile "$T/allowed"
git config commit.gpgsign true
c() { git -c user.signingkey="$T/$1" commit -q --allow-empty -m "$2"; git rev-parse HEAD; }
m() { git -c user.signingkey="$T/$1" merge -q --no-ff -m "$3" "$2"; }

A=$(c k1 "[key] add $F1")
K=$(c k1 "[key] add $F2")
R=$(c k2 "[key] revoke $F1")
git checkout -q -b early "$K"; c k1 "early: forked before revoke, committed after it" >/dev/null
git checkout -q -b late "$R";  c k1 "late: revoke is its ancestor" >/dev/null
git checkout -q main
m k2 early "merge early (k2)"; m k2 late "merge late (k2)"
git checkout -q -b bad "$R"; m k1 early "merge early signed by revoked k1"

sig_ok() {
  local st k ev
  read -r st k < <(git log -1 --format='%G? %GK' "$1")
  case $st in G|U) ;; *) return 1;; esac
  [ "$(git rev-list --parents -n1 "$1" | wc -w)" -eq 1 ] && return 0
  ev=$(git log --format=%s --grep='^\[key\] ' "$1^@")
  grep -qxF "[key] add $k" <<<"$ev" && ! grep -qxF "[key] revoke $k" <<<"$ev"
}
show() {
  local k; k=$(git log -1 --format=%GK "$1"); k=${k/"$F1"/k1}; k=${k/"$F2"/k2}
  printf '  %-6s %s %-2s %s\n' "$2" "$(git log -1 --format=%G? "$1")" "$k" \
    "$(git log -1 --format=%s "$1" | sed "s|$F1|k1|;s|$F2|k2|")"
}
fold() {
  local c p v bad=" "
  for c in $(git rev-list --reverse --topo-order "$@"); do
    v=accept; sig_ok "$c" || v=reject
    for p in $(git rev-list --parents -n1 "$c" | cut -d' ' -f2-); do
      case $bad in *" $p "*) v=reject;; esac
    done
    [ $v = reject ] && bad="$bad$c "
    show "$c" $v
  done
}
echo "== fold, --first-parent main =="; fold --first-parent main
echo "== fold, every commit of main =="; fold main
echo "== merge signed by revoked k1 (branch bad) =="
if sig_ok bad; then show bad accept; else show bad reject; fi
```

## Captured output

Run on the macOS host, from a temp dir outside the worktree. Lines from the global pre-commit hook (`.pre-commit-config.yaml config file not found`) are filtered out.

```text
git version 2.51.0
== fold, --first-parent main ==
  accept U k1 [key] add k1
  accept U k1 [key] add k2
  accept U k2 [key] revoke k1
  accept U k2 merge early (k2)
  accept U k2 merge late (k2)
== fold, every commit of main ==
  accept U k1 [key] add k1
  accept U k1 [key] add k2
  accept U k2 [key] revoke k1
  accept U k1 early: forked before revoke, committed after it
  accept U k2 merge early (k2)
  reject U k1 late: revoke is its ancestor
  reject U k2 merge late (k2)
== merge signed by revoked k1 (branch bad) ==
  reject U k1 merge early signed by revoked k1
```
