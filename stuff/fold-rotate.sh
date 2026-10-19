#!/usr/bin/env bash
# Throwaway repo (rule 2): two SSH keys, an EMPTY allowedSignersFile, seven
# first-parent commits. Rotation: k1 adds k2 first, then revokes itself; then
# k1 and k2 each try to work, and k2, now the last live key, revokes itself.
# Same fold as fold-last-revoke.sh (accept iff %G? is G or U AND %GK is live),
# run with and without the guard that refuses a revoke leaving no live key.
# Question: does the guard still allow add-then-revoke rotation?
# Run: bash stuff/fold-rotate.sh
set -euo pipefail
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
cd "$T"
for k in k1 k2; do ssh-keygen -q -t ed25519 -N '' -C "$k" -f "$k"; done
: > allowed
fp() { ssh-keygen -lf "$T/$1.pub" | awk '{print $2}'; }
f1=$(fp k1)
f2=$(fp k2)
git init -q r
cd r
git config user.name t
git config user.email t@example.invalid
git config gpg.format ssh
git config gpg.ssh.allowedSignersFile "$T/allowed"
c() { git -c user.signingkey="$T/$1" commit -q --allow-empty -S -m "$2"; }
c k1 "genesis"
c k1 "[key] add $f2"
c k1 "[key] revoke $f1"
c k1 "work by k1 after its revoke"
c k2 "work by k2"
c k2 "[key] revoke $f2"
c k2 "work by k2 after its revoke"
short() { local s=${1//"$f1"/k1}; echo "${s//"$f2"/k2}"; }
fold() { # $1: 1 = refuse a revoke that empties the live set
  local live=" $f1 " g k s v next
  while IFS='|' read -r g k s; do
    v=reject
    if [[ ($g == G || $g == U) && $live == *" $k "* ]]; then
      v=accept
      case $s in
        "[key] revoke "*)
          next=${live/" ${s#'[key] revoke '} "/ }
          if [[ $1 == 1 && -z ${next// /} ]]; then v=refuse; else live=$next; fi ;;
        "[key] add "*) live="$live${s#'[key] add '} " ;;
      esac
    fi
    printf '  %-6s %%G?=%s signer=%s  %-28s live={%s}\n' \
      "$v" "$g" "$(short "$k")" "$(short "$s")" "$(short "$live" | xargs)"
  done < <(git log --reverse --first-parent --format='%G?|%GK|%s')
}
echo "git: $(git --version)"
echo "ssh: $(ssh -V 2>&1)"
echo "fold, no guard:"
fold 0
echo "fold, guard (refuse a revoke that leaves no live key):"
fold 1
