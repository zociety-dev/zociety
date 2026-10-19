# Revoking the last live key: the fold should refuse it

Answers the second half of the direction: should a fold that checks `%GK`
against the live key set (and accepts `%G?` G or U) reject a `[key]` revoke
that leaves no live key? Yes. Without that check, the revoke is accepted and
no later commit can ever be accepted again, including the `[key] add` that
would fix it.

## Run

```bash
bash stuff/fold-last-revoke.sh
```

Throwaway repo built by the script (rule 2): keys k1 and k2, an empty
`allowedSignersFile`, live set seeded with {k1}, five first-parent commits.
The fold is the one in `stuff/fold-bad-sig.sh`, plus the live set changes
from `[key] add`/`[key] revoke` subjects. Fingerprints are shortened to
k1/k2 in the output. Each throwaway `git commit` also prints a
"`.pre-commit-config.yaml` config file not found" line from the host's
global hook setup; it does not change the results and is left out below.

## Output

```
git: git version 2.51.0
ssh: OpenSSH_10.5p1, LibreSSL 3.3.6
fold, no guard:
  accept %G?=U signer=k1  genesis                live={k1}
  accept %G?=U signer=k1  [key] revoke k1        live={}
  reject %G?=U signer=k1  work after revoke      live={}
  reject %G?=U signer=k2  [key] add k2           live={}
  reject %G?=U signer=k1  [key] add k2           live={}
fold, guard (refuse a revoke that leaves no live key):
  accept %G?=U signer=k1  genesis                live={k1}
  refuse %G?=U signer=k1  [key] revoke k1        live={k1}
  accept %G?=U signer=k1  work after revoke      live={k1}
  reject %G?=U signer=k2  [key] add k2           live={k1}
  accept %G?=U signer=k1  [key] add k2           live={k1 k2}
```

## What it shows

- **Without the guard the fold locks itself.** Once k1 revokes itself the
  live set is empty, so every later commit fails the `%GK` check. That
  includes k2 adding itself and k1 adding k2. Nothing in the history can
  recover, so the only way out is to change the fold or rewrite history.
- **With the guard the revoke is refused and nothing else changes.** k1
  stays live, its later work is accepted, and k1 can add k2. k2 still cannot
  add itself, which matches cycle 43's self-signed add result.
- **"Refuse" here means the event has no effect, not that the commit is
  thrown out.** The commit stays on the branch, and the fold treats it as a
  revoke that did not happen. A stricter fold could treat the whole branch as
  invalid from that commit on. This run does not decide between the two.
- `%G?` is U for every commit because `allowedSignersFile` is empty, so the
  verdicts come from `%GK` alone, as in cycle 43.

## Not covered

- **Rotation.** The safe way to replace the last key is to add the new key
  first, then revoke the old one. The guard allows that, but this run does
  not include it.
- **A revoke inside a merged side branch.** The fold reads first-parent
  only. A side branch that revokes the last key and is then merged was not
  tried.
- **gpg-format signatures.** Only SSH was run.
