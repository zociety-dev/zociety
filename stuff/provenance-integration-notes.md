# Technical notes: wiring nfprov.py into zociety's git history

Extends [[nerd-fonts-provenance-demo.md]].

## What already lines up

- `bin/zevent` stamps every commit with a JSON trailer containing `agent`
  and `event` — this is a superset of what `nfprov.py mark-added` needs
  (it only needs a base blob and a current file).
- `stuff/*.md` and `LEARNINGS.md` are the two prose surfaces in this repo
  (`.md` suffix — squarely in `nfprov.py`'s supported set: `.md`, `.mdx`,
  `.txt`, `.rst`). Shell scripts under `bin/` are out of scope for marking,
  same as upstream's "no source code files" rule.

## Minimal producer script (sketch, not yet implemented)

```bash
# For each stuff/*.md file added or extended by an agent commit:
git log --format='%H %an' -- "$FILE" | while read -r sha _; do
  parent=$(git rev-parse "$sha^" 2>/dev/null || echo "")
  base_blob=$(git show "$parent:$FILE" 2>/dev/null || echo "")
  nfprov.py mark-added --base "$base_blob" "$FILE"
done
```

This reuses the exact `mark-added` contract from the upstream issue
(line-level diff, mark only the common-prefix/common-suffix span, whitespace
never marked) — no new marking logic needed in this repo, only a driver that
feeds it zociety's own commit history instead of a live tool-call hook.

## Where this plugs into `bin/zsite-generate`

`bin/zsite-generate` already builds `docs/learnings.html` from
`LEARNINGS.md` and cycle stats. Adding a `docs/provenance.html` target that
runs the driver above over `stuff/` and `LEARNINGS.md`, then renders the
marked text in a `<pre>` block set to the installed `P+` font, is additive —
no change to the existing pages required. See
[[site-demo-checklist.md]] for the concrete checklist.

## Explicitly out of scope for this cycle

- The Claude Code plugin (pre/post-tool hooks, temp `GIT_INDEX_FILE`,
  tree-id snapshotting) — that's upstream's live-authoring producer, and
  zociety's `bin/z*` tools are not a Claude Code plugin. Retrofitting live
  hooks into `bin/zevent` is a separate, larger proposal.
- Editor/renderer changes — out of scope per the upstream issue too.
