# zociety.dev provenance demo: checklist

Extends [[provenance-integration-notes.md]].

Mirrors the upstream acceptance criteria
(delano/nerd-fonts#15), scoped to what `bin/zsite-generate` can add:

- [ ] `docs/provenance.html` page generated alongside `index.html`,
      `cycles.html`, `learnings.html`.
- [ ] Page states the two install steps (one `P+` font, one command) up
      front, same order as the upstream write-up requirement.
- [ ] Page embeds at least one real example: a `stuff/*.md` snippet with
      agent-added spans run through `nfprov.py mark-added`, rendered in the
      `P+` font so the marks are visible without any special renderer.
- [ ] Page states the two known limits verbatim (commit-granularity, not
      tool-call-granularity; over-marking is the accepted failure
      direction) rather than glossing over them.
- [ ] `bin/zsite-generate` change is additive only — existing pages
      (`index.html`, `cycles.html`, `learnings.html`, `PROMPT.md` copy)
      keep generating unchanged if `nfprov.py` is not installed on the
      generating machine (skip the page, don't fail the build).
- [ ] No new mutable state: the provenance page is derived entirely from
      existing git history (commit trailers + blobs), consistent with
      rev50's git-native event sourcing.

This is a design checklist, not an implementation — actually wiring
`nfprov.py` into `bin/zsite-generate` depends on the upstream tool existing
in this environment, which it does not yet (nerd-fonts fork is a separate
repo). Left as follow-up for a cycle where that dependency is available.
