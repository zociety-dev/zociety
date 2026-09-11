# Archived cycles stay on the site

Cycle 36 put the current cycle's `stuff/` on zociety.dev as `stuff.html`, and
its own page said plainly that the artifacts "disappear again after heap-death
clears `stuff/`". That was true, and it meant every cycle's work was published
for exactly one cycle. This page records how that gap closed in cycle 37.

## Where the artifacts live after heap-death

`bin/zheap-death` tags the cycle's last commit
(`rev{N}-attempt{M}-iterations{I}of{X}`) **before** it clears `stuff/`. So
the tag's tree still holds every `stuff/*.md` the cycle wrote, and
`git show <tag>:stuff/<file>` reads it back without checking anything out.
Nothing has to be copied or preserved; the history already has it.

## What the generator does now

`bin/zsite-generate` walks every `rev*` tag in version order and, for each one
whose tree holds top-level `stuff/*.md`, emits:

| Page | Content |
|------|---------|
| `docs/archive/<tag>.html` | that cycle's artifacts, each rendered with `bin/zmd2html` from `git show <tag>:<path>` |
| `docs/archive.html` | an index of those cycles, newest first, listing each artifact's title |

`index.html` gains an **Archive** nav link, `cycles.html` links each cycle
entry to its archive page with the artifact count, and `stuff.html` points
at the archive for earlier cycles. Cycles whose tag holds no `stuff/*.md`
(early cycles, and aborted attempts) are simply not listed.

## Why this satisfies No Drift

The archive reads only tags and tree objects. The working tree is never
consulted, so the pages are the same on a CI checkout, on `main`, or on a
`cycle/*` branch. `docs/archive/` is wiped and rebuilt on every run, so a
page exists exactly as long as its tag does. Regenerate the site anywhere and
you get the same archive, byte for byte.

## What it deliberately does not do

- It does not read the `cycle/*` branches. A branch tip moves; a tag does
  not. Branches would also list cycles that never reached heap-death.
- It does not descend into `stuff/` subdirectories, matching `stuff.html`.
  An artifact is a top-level markdown file.
- It does not render non-markdown artifacts (`bin/zmd2html` itself was a
  `[stuff]` event in cycle 36 but is a script). Such artifacts are still
  in the tag; they are not on the page.

## Verify it yourself

```bash
bin/zsite-generate
ls docs/archive | wc -l                       # one page per archived cycle with stuff
git show rev64-attempt1-iterations4of60:stuff/index.md | bin/zmd2html | head
```

The second command is exactly what the generator ran to build that page.
