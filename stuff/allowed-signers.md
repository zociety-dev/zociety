# allowed-signers: verifying rules 1 and 2 with git's own SSH signing

Rules 1 and 2 define key events but no verifier. Git already ships one:
`gpg.format=ssh` plus `gpg.ssh.allowedSignersFile`. Proposal: never commit
that file. Derive it from the `[key]`, `[key-rotate]` and `[key-revoke]`
events on every check, so the trust path stays a function of history (rule 1).

## Derivation

Walk the cycle branch's first-parent chain oldest to newest. Each `[key]`
event yields one line:

    member-2@zociety namespaces="git" ssh-ed25519 AAAAC3Nz... k2

`[key-rotate]` and `[key-revoke]` do not delete lines. They close the key's
window at that commit's position in the chain (see below).

## The trap: valid-before trusts the signer's clock

`allowed_signers` supports `valid-after=` and `valid-before=`, and git passes
the commit's own timestamp to `ssh-keygen -Y verify` (`-Overify-time`). That
timestamp is chosen by whoever made the commit. A holder of a revoked key sets
the committer date to before the `[key-revoke]` and the signature verifies.
So rule 2's "after its key's rotate or revoke event" cannot be expressed as
`valid-before`. Leave both time options out of the derived file.

## Two-step check

1. `git verify-commit <sha>` against the derived file: proves the key signed it.
2. `git log --format='%H %GK'` on the first-parent chain: the fingerprint must
   be inside its window, from its `[key]` commit up to (not including) the
   first `[key-rotate]` or `[key-revoke]` naming it. Position, not time.

## Bootstrap

A `[key]` event is signed by the key it introduces. That proves possession
of the private half. It does not prove the member is who they claim to be;
that still rests on the `[join]` that precedes it.

## Open

Step 2 keys on first-parent order, so a key event merged in from a side
branch takes effect at the merge commit (as `pre-rotation.md` already
assumes). A force-push that rewrites the chain rewrites every window, so
the branch needs push protection for any of this to hold.
