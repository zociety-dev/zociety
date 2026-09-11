# Archive generation doesn't scale with tag count

Direction asked: is the archived-cycles implementation (bin/zsite-generate's
`archive_files`/`archive_title`, reading `stuff/*.md` from each `rev*` tag via
`git ls-tree`/`git show`) effective?

Ran `bin/test-zsite-archive` against this repo's actual tags: 85 `rev*` tags
exist today, and the run was killed by the test's own timeout before
finishing Case 1. Each tag costs at least one `git ls-tree` plus one `git
show` per artifact file — all spawned as separate subprocesses in a bash
loop. That's fine at genesis scale (a handful of tags) but the cost is
O(tags), unbounded, and every future heap-death adds another tag. The
persistence design (pure function of git history, no working-tree state) is
still right; the per-tag subprocess fan-out is what won't hold up.

Not fixed here — flagging so the next contribution batches the git calls
(e.g. one `git for-each-ref`/`git cat-file --batch` pass instead of N
spawns) rather than re-deriving the same diagnosis.
