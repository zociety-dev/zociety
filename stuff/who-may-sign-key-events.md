# Who may sign key events

The other two files say when a key stops counting: at the position of its
revoke (`revoke-by-position.md`), and in a merge, at the merge point
(`key-state-across-merges.md`). Neither says who is allowed to write a
`[key]`, `[key-rotate]` or `[key-revoke]` event. If anyone can, the set
proves nothing: an attacker commits `[key] attacker-key`, signs it with that
key, and from then on every forged event passes.

## Anchor

A set derived only from events still needs one fact that is not an event.
Make that fact a commit hash, not a key: `bin/zstate` is given the SHA of
the first `[key]` event (one line in a tracked config, or the cycle's
parent tag). The hash fixes the content of that commit, including the key
it adds. Rewriting the root event changes its SHA, and the fold refuses to
start. Every other key in the set is then reached from that one commit.

## Rules for the fold

1. `[key] K` counts only when its commit is signed by a key already in the
   set at that position. A `[key]` signed by K itself is rejected. The root
   event is the one exception, and the anchor covers it.
2. `[key-rotate] old -> new` counts only when signed by `old`. That shows
   the holder of `old` agreed. `new` cannot co-sign, because a commit has one
   signature. The first event signed by `new` is the proof that its holder
   has it.
3. `[key-revoke] K` counts when signed by any key in the set, K included.
   Revoking your own key is how a holder reports it stolen. A thief who
   revokes the stolen key only locks themselves out.
4. A key event is checked against the set as it stands before that event.
   A rotate signed by `old` is valid, and `old` stops counting at the
   commit after it.

## What rule 3 costs

Any member can revoke every other member. That attack costs availability,
not integrity: the revoker can stop the zociety but cannot forge an event
in anyone else's name. If the set ends up empty, the fold has no valid
signer and `bin/zstate` answers `action: stop`. That fails closed, which is
the safe direction. Recovery is an operator `[intervention]`, the same path
as any other terminal observation.

## Cost in the one-pass fold

The fold already walks events oldest first and keeps the current set. A key
event adds one lookup: is the signer's fingerprint in the set before this
event? `git log --format='%H %G? %GF %s'` prints the fingerprint per commit,
so no process is spawned per commit. Not tested yet: what `%GF` prints for
an SSH signature whose key is missing from the allowed signers file. The
fold should compare `%GF` against its own set and ignore `%G?`, so the
answer to that matters only for formatting.
