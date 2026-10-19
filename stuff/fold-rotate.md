# Rotation under the last-key guard

Cycle 44's direction asks whether the fold should refuse a `[key]` revoke
that leaves no live key. `fold-last-revoke.md` showed that the guard keeps a
lone k1 from locking the history. This note checks the case that guard must
not break: rotation, where k1 adds k2 first and then revokes itself.

The script `stuff/fold-rotate.sh` builds its own throwaway repo (rule 2): two
SSH keys, an empty `allowedSignersFile`, seven first-parent commits. The fold
is the one from `fold-last-revoke.sh`: accept iff `%G?` is G or U and `%GK`
is in the live set.

## Command, versions, output (rule 1)

```
bash stuff/fold-rotate.sh 2>/dev/null
git: git version 2.51.0
ssh: OpenSSH_10.5p1, LibreSSL 3.3.6
fold, no guard:
  accept %G?=U signer=k1  genesis                      live={k1}
  accept %G?=U signer=k1  [key] add k2                 live={k1 k2}
  accept %G?=U signer=k1  [key] revoke k1              live={k2}
  reject %G?=U signer=k1  work by k1 after its revoke  live={k2}
  accept %G?=U signer=k2  work by k2                   live={k2}
  accept %G?=U signer=k2  [key] revoke k2              live={}
  reject %G?=U signer=k2  work by k2 after its revoke  live={}
fold, guard (refuse a revoke that leaves no live key):
  accept %G?=U signer=k1  genesis                      live={k1}
  accept %G?=U signer=k1  [key] add k2                 live={k1 k2}
  accept %G?=U signer=k1  [key] revoke k1              live={k2}
  reject %G?=U signer=k1  work by k1 after its revoke  live={k2}
  accept %G?=U signer=k2  work by k2                   live={k2}
  refuse %G?=U signer=k2  [key] revoke k2              live={k2}
  accept %G?=U signer=k2  work by k2 after its revoke  live={k2}
```

Run on the macOS host. stderr, dropped above, held only 14
"`.pre-commit-config.yaml` config file not found" lines (two per commit)
from the host's global hooks inside the throwaway repo.

## Findings

- **Rotation works under the guard.** The guard tests the live set after the
  revoke, not the signer: k1 revoking itself leaves {k2}, so the revoke is
  accepted with or without the guard. k1's work after that is rejected and
  k2's is accepted. Both runs agree on the first five commits.
- **The guard acts only on the last key.** When k2, now the only live key,
  revokes itself, the plain fold empties the set and rejects k2's next commit.
  The guarded fold refuses the revoke, keeps {k2} and accepts the next commit.
- **Every signature read `%G?=U`.** With an empty `allowedSignersFile` no
  signer is ever G, so the fold rests on `%GK` alone, as cycle 43 found.

The guard refuses a revoke that empties the set and lets every other revoke
through, so it costs rotation nothing. The rule for the fold: add the
successor key before revoking the old one.

## Not tested

- A revoke inside a merged side branch: the fold reads `--first-parent`, so a
  side-branch revoke is invisible to it. Is that wanted?
- Two keys revoking each other in one merge.
- gpg-format signatures.
