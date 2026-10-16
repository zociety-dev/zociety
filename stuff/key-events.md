# Key events: the data rules 1 and 2 need

Rules 1 and 2 say keys live in git events, not in a mutable file. This is the
payload each event carries and the fold `bin/zstate` would run over them.

## Events

| Event | Signed by | Data |
|-------|-----------|------|
| `[key]` | the new key (self-signature over the payload) | `{member, key_id, path: "keys/<member>/<key_id>.pub"}` |
| `[key-rotate]` | the outgoing key | `{member, from: <key_id>, to: <key_id>, path}` |
| `[key-revoke]` | majority of the *other* members' valid keys | `{member, key_id, reason, sigs: [{key_id, sig}]}` |

`key_id` is the first 16 hex chars of `sha256(raw 32-byte Ed25519 public key)`,
so the id is checkable against the committed `.pub` file and cannot be chosen.
Signatures cover the canonical JSON of `data` without the `sigs` field
(`jq -cS 'del(.sigs)'`), so a commit's message cannot be edited to reuse them.

## The fold

Walk events oldest first. State is a map `key_id -> {member, from_seq, to_seq}`.

1. `[key]`: reject if `key_id` is already known or the `.pub` blob in that
   commit does not hash to `key_id`. Else add `{from_seq: seq, to_seq: null}`.
2. `[key-rotate]`: reject unless `from` is valid at `seq` and the signature
   verifies under `from`. Set `from.to_seq = seq`; add `to` as in step 1.
3. `[key-revoke]`: count distinct members (not keys) whose key is valid at
   `seq` and whose signature verifies, excluding `member`. Reject below
   `floor(other_members / 2) + 1`. Else set `key_id.to_seq = seq`.

A signature on event `e` is valid iff its key has `from_seq <= e.seq` and
(`to_seq` is null or `e.seq < to_seq`). Rejected events stay in history and
are reported, never silently skipped.

## Edge cases the rules leave open

- **Revoke with fewer than 3 members.** With 2 members, "majority of the
  others" is one key; with 1 member, no revoke is possible. Proposal: a solo
  member's lost key ends that member, and they rejoin with a new `[join]`.
- **Rotate after compromise.** An attacker holding the key can rotate first.
  Revoke must then name the attacker's successor key too; the fold retires
  the whole chain from the revoked key forward.
- **Ordering.** `seq` is commit order on the cycle branch. A merge that
  interleaves two branches' key events reorders them; key events should be
  rejected on any commit that is not first-parent.
