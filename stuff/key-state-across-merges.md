# Key state across merges

`revoke-by-position.md` makes a revoke take effect at its place in history.
That place has to be unique. On a branch with merges it is not: this cycle
branch merges `main` (3afa749, 374d107), and `git log`, `--topo-order`,
`--date-order` and `--first-parent` put a `[key-revoke]` that arrived from
`main` at different positions. If the outcome of a revoke depends on which
traversal flag was used, the revoke is not enforced.

## Rule

Fold the allowed_signers set over `git rev-list --first-parent --reverse HEAD`.

1. A first-parent commit is checked against the set as of its first parent.
   If it is a `[key]`, `[key-rotate]` or `[key-revoke]` event, it then
   updates the set.
2. A merge commit must be signed by a key in the set at its first parent.
3. Commits reachable only through a merge's second parent
   (`M^1..M^2`) are checked against the set at `M^1`, as if they happened
   at the merge. Key events among them do not change this branch's set.
4. To carry a key change across branches, re-issue it as a new key event on
   the first-parent chain, signed under this branch's rules.

## What it prevents

Branch A revokes key K at commit r. Branch B forked before r and keeps
signing with K. Each of B's commits comes before r in B's own history, so
a fold that walks each branch's history separately accepts them all. Under
rule 3 they are checked at the merge point, where K is already revoked, so
they are rejected.

## Cost

No process per commit. One `git log --first-parent --format='%H %P %G? %GK'`
pass, verified against the union of every key ever added, gives each commit's
signer fingerprint. `jq` then checks each fingerprint against the set as of
that commit's position, and checks second-parent ranges against the set at
their merge. The union file only proves that a signature is valid for some
key. Whether that key was allowed at that position is decided by the fold.

Not tested here: how `%G?` reports an SSH key that is missing from
`gpg.ssh.allowedSignersFile`. The union file avoids that case, so the fold
never depends on it.
