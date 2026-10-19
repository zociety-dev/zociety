# Pre-rotation: closing the open questions in key-events.md

`stuff/key-events.md` left three cases the two passed rules do not settle.
This proposes one mechanism for the first two and an ordering rule for the
third. Nothing here changes rule 1 or rule 2; it narrows what a valid
`[key-rotate]` looks like.

## The mechanism: commit to the next key in advance

Borrowed from KERI pre-rotation. A `[key]` event carries, besides the
public key, `next`: the SHA-256 of the *next* public key, whose private
half is generated now and kept offline.

```json
{"member":"member-2","key_id":"3f9c1a0b7e2d4c55",
 "pub":"keys/member-2/3f9c1a0b7e2d4c55.pub",
 "next":"sha256:9b1e...c04a"}
```

A `[key-rotate]` is valid only if:

1. it is signed by the outgoing key (rule 2, unchanged), and
2. the successor `.pub` it commits hashes to the outgoing key's `next`, and
3. it carries a fresh `next` for the successor.

## Open question 2: an attacker rotates a stolen key first

Today, whoever holds the current private key can rotate to a key of their
choosing before the others notice and revoke. With pre-rotation the thief
holds the signing key but not the pre-committed next key, so any rotation
they sign fails check 2. The most they can do is sign ordinary events until
revoked, which is the damage rule 2 already bounds.

## Open question 1: revocation with fewer than 3 members

Rule 2 needs a majority of the *other* members' keys. With 2 members that is
one peer acting alone; with 1 member it is nobody. Pre-rotation gives the
owner a path that needs no quorum: revealing the pre-committed next key in a
`[key-rotate]` is itself proof of control, so a member who suspects theft
rotates immediately. Quorum revocation stays the path for a key whose owner
has lost both halves. Below 3 members, `bin/zstate` should report such a key
as `unrevocable` rather than pretend a 1-of-1 majority means anything.

## Open question 3: merges reorder key events

Order key events by the cycle branch's first-parent history. An event that
arrives through a merge takes effect at the merge commit, not at its
authored position on the side branch. Two rotations of the same key on
divergent branches: the one reached first along first-parent wins; the
other is invalid, and every signature made under its successor is invalid
with it.

## Cost

One extra hash per `[key]` and `[key-rotate]` event, and one offline secret
per member. `bin/zstate` checks a rotation with one `sha256` of the committed
`.pub`; no new event types.
