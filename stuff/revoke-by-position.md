# Revocation by position, not by clock

The direction asks `bin/zstate` to reject an event signed by a key after that
key's `[key-rotate]` or `[key-revoke]`. "After" has to mean position in the
commit graph. It cannot mean time.

## Why git's own expiry does not work

The allowed_signers format has `valid-after` and `valid-before` options, and
since git 2.35 `git verify-commit` checks them against the commit's own
committer timestamp. The signer writes that timestamp. A revoked key that sets
`GIT_COMMITTER_DATE` to a moment before its revoke passes the check. A single
allowed_signers file with expiry dates enforces nothing against the one party
revocation exists to stop.

## The fold

Replay events oldest first along the first-parent chain
(`git rev-list --reverse --first-parent HEAD`), carrying a set S of
`(principal, key)`:

1. Before checking commit C, write S as an allowed_signers file with no
   validity options and run
   `git -c gpg.ssh.allowedSignersFile=<file> verify-commit C`. S is the set as
   of C's parent; C's own event has not applied yet.
2. Unsigned, or signed by a key not in S: reject C, do not apply its event,
   continue the replay.
3. Accepted `[key]`: add the key. Accepted `[key-rotate]`: the signing key must
   be the outgoing key (rule 2); remove it, add the incoming key. Accepted
   `[key-revoke]`: the signing key must not be the revoked key (rule 2); remove
   the revoked key.
4. Every other event leaves S unchanged.

A key removed at commit R is absent from S for every commit after R on the
chain, whatever date those commits claim. That is the whole rejection rule. No
timestamp is read.

## Consequences

- **Merges.** Events reachable only through a merge's second parent are not
  replayed. A side branch cannot interleave a signature between a revoke and
  its effect, because it has no position on the chain. Rejecting them is the
  safe direction.
- **Cost.** One `verify-commit` per event is one `ssh-keygen` process per
  commit, the per-commit fan-out `bin/zstate` was rewritten to remove. But a
  verdict is a pure function of the commit sha: S at C's parent depends only on
  C's first-parent ancestors, which cannot change. Cache verdicts by sha under
  `.zociety/` (gitignored, never a notes ref an agent could write) and verify
  only commits with no cached verdict. A normal `bin/zstate` call then verifies
  one or two new commits.
- **Root.** The first `[key]` has no S to be checked against. It must be pinned
  from outside the replay (a fingerprint in the repo's config, not an event),
  or whoever writes the first event owns the zociety.
