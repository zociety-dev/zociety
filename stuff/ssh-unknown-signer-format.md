# What git log prints for an SSH signer not in allowedSignersFile

Answers the first half of the cycle 43 direction. Rule 1 applies: the run is
quoted below with git version and exact command. The fold half (rule 2) is
not tested here.

## Result

| commit signed by | allowedSignersFile | %G? | %GS | %GF | %GK | %GT |
|---|---|---|---|---|---|---|
| key in the file | set | `G` | `t@example.com` | its SHA256 fp | same fp | `fully` |
| key not in the file | set | `U` | empty | **its SHA256 fp** | same fp | `undefined` |
| key in the file | unset | `U` | empty | its SHA256 fp | same fp | `undefined` |
| unsigned | either | `N` | empty | empty | empty | `undefined` |

- `%GF` and `%GK` do name the signer of a key that is not allowed. Cycle 42's
  unverified assumption holds on git 2.51.0 with OpenSSH 10.5p1.
- For SSH, `%GF` and `%GK` are the same string (`SHA256:...`, as
  `ssh-keygen -lf` prints it). `%GP` is always empty.
- `%G?` is `U` with no allowedSignersFile at all, even for the "good" key.
  So a fold can leave `gpg.ssh.allowedSignersFile` unset, accept `%G?` in
  `{G,U}` and decide membership itself by comparing `%GF` against its own key
  set. It must not treat `U` as a rejection.
- `git verify-commit` on the stranger commit prints
  `Good "git" signature with ED25519 key SHA256:+rom...` then
  `No principal matched.` and exits 1 (the script stops there under `set -e`).
  A fold that shells out to verify-commit would reject every key it learned
  from history and not from the file.

Not tested: what `%G?` prints for a tampered or truncated SSH signature
(expected `B`; a fold must reject it), and whether `%GF` is still filled then.

## Run

`/tmp/zgk/run.sh > /tmp/zgk/out.txt 2>&1` on macOS, host git (the shim
passes through outside the worktree). Script exit 1, from verify-commit.

```bash
#!/usr/bin/env bash
set -eu
d=$(mktemp -d)
cd "$d"
git --version
ssh -V 2>&1
ssh-keygen -q -t ed25519 -N '' -C allowed -f "$d/k_allowed"
ssh-keygen -q -t ed25519 -N '' -C stranger -f "$d/k_stranger"
echo "fp allowed:  $(ssh-keygen -lf "$d/k_allowed.pub" | cut -d' ' -f2)"
echo "fp stranger: $(ssh-keygen -lf "$d/k_stranger.pub" | cut -d' ' -f2)"
echo "t@example.com $(cat "$d/k_allowed.pub")" > "$d/allowed_signers"
git init -q repo && cd repo
git config user.name t
git config user.email t@example.com
git config gpg.format ssh
git config user.signingkey "$d/k_allowed"
git commit -q --allow-empty -S -m allowed
git -c user.signingkey="$d/k_stranger" commit -q --allow-empty -S -m stranger
git commit -q --allow-empty --no-gpg-sign -m unsigned
fmt='%s|G?=%G?|GS=%GS|GF=%GF|GP=%GP|GK=%GK|GT=%GT'
echo "--- with gpg.ssh.allowedSignersFile set"
git -c gpg.ssh.allowedSignersFile="$d/allowed_signers" log --format="$fmt"
echo "--- with gpg.ssh.allowedSignersFile unset"
git log --format="$fmt"
echo "--- verify-commit HEAD~1 (stranger), allowedSignersFile set"
git -c gpg.ssh.allowedSignersFile="$d/allowed_signers" verify-commit HEAD~1; echo "exit=$?"
```

Output (six "`.pre-commit-config.yaml` not found" lines from a global hook
removed):

```
git version 2.51.0
OpenSSH_10.5p1, LibreSSL 3.3.6
fp allowed:  SHA256:BZ2d2WAL2sJS04DD//5S3UJ/5tFPtxMeT8UvKFKlZVk
fp stranger: SHA256:+rom06xbywsYwPAWXjZhwj8sWcn4KBfjj/sEDKfSO3Y
--- with gpg.ssh.allowedSignersFile set
unsigned|G?=N|GS=|GF=|GP=|GK=|GT=undefined
stranger|G?=U|GS=|GF=SHA256:+rom06xbywsYwPAWXjZhwj8sWcn4KBfjj/sEDKfSO3Y|GP=|GK=SHA256:+rom06xbywsYwPAWXjZhwj8sWcn4KBfjj/sEDKfSO3Y|GT=undefined
allowed|G?=G|GS=t@example.com|GF=SHA256:BZ2d2WAL2sJS04DD//5S3UJ/5tFPtxMeT8UvKFKlZVk|GP=|GK=SHA256:BZ2d2WAL2sJS04DD//5S3UJ/5tFPtxMeT8UvKFKlZVk|GT=fully
--- with gpg.ssh.allowedSignersFile unset
unsigned|G?=N|GS=|GF=|GP=|GK=|GT=undefined
stranger|G?=U|GS=|GF=SHA256:+rom06xbywsYwPAWXjZhwj8sWcn4KBfjj/sEDKfSO3Y|GP=|GK=SHA256:+rom06xbywsYwPAWXjZhwj8sWcn4KBfjj/sEDKfSO3Y|GT=undefined
allowed|G?=U|GS=|GF=SHA256:BZ2d2WAL2sJS04DD//5S3UJ/5tFPtxMeT8UvKFKlZVk|GP=|GK=SHA256:BZ2d2WAL2sJS04DD//5S3UJ/5tFPtxMeT8UvKFKlZVk|GT=undefined
--- verify-commit HEAD~1 (stranger), allowedSignersFile set
Good "git" signature with ED25519 key SHA256:+rom06xbywsYwPAWXjZhwj8sWcn4KBfjj/sEDKfSO3Y
No principal matched.
```
