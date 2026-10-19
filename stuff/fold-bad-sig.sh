#!/usr/bin/env bash
# Throwaway repo (rule 2): one SSH key, an EMPTY allowedSignersFile, three
# commits: signed (good), the same signature over a tampered message (bad),
# and unsigned (none). Prints %G? and %GK for each, then applies the fold
# from the direction: accept iff %G? is G or U AND %GK is in the live set.
# Run: bash stuff/fold-bad-sig.sh
set -euo pipefail
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
cd "$T"
ssh-keygen -q -t ed25519 -N '' -C k1 -f k1
: > allowed
git init -q r
cd r
git config user.name t
git config user.email t@example.invalid
git config gpg.format ssh
git config user.signingkey "$T/k1"
git config gpg.ssh.allowedSignersFile "$T/allowed"
git commit -q --allow-empty -S -m good
good=$(git rev-parse HEAD)
# Same gpgsig header, changed message: the signature no longer covers the payload.
bad=$(git cat-file commit "$good" | sed 's/^good$/tampered/' | git hash-object -t commit -w --stdin)
git commit -q --allow-empty --no-gpg-sign -m none
none=$(git rev-parse HEAD)
live=$(ssh-keygen -lf "$T/k1.pub" | awk '{print $2}')
echo "git: $(git --version)"
echo "ssh: $(ssh -V 2>&1)"
echo "live set: $live"
for c in "good:$good" "bad:$bad" "none:$none"; do
  name=${c%%:*}
  read -r g k < <(git log -1 --format='%G? %GK' "${c#*:}")
  verdict=reject
  if [[ ($g == G || $g == U) && ${k:-} == "$live" ]]; then verdict=accept; fi
  # what a fold reading %GK alone (no %G? check) would do
  gk_only=reject
  if [[ ${k:-} == "$live" ]]; then gk_only=accept; fi
  printf '%-5s %%G?=%s %%GK=%-50s fold=%s gk-only=%s\n' "$name" "$g" "${k:--}" "$verdict" "$gk_only"
done
