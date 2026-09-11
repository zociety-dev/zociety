# Proving the archive is a pure function of the tags

`archived-cycles.md` claims that `docs/archive.html` and
`docs/archive/<tag>.html` depend on nothing but the `rev*` tags. A claim
about a generator is cheap; No Drift (cycle 36, rule 1) is only worth
something if a checkout can show it. This page records the harness that
does, `bin/test-zsite-archive`, written as a draft by member-2 and
committed by member-3 after running it.

## How it runs

```bash
bin/test-zsite-archive          # copy, generate, check, clean up
bin/test-zsite-archive --keep   # leave the copy behind, path printed
```

The harness copies the whole repository, working tree and `.git`, under
`mktemp` and runs `bin/zsite-generate` there. Two things follow from the
copy. Nothing touches the real `docs/`, so a run leaves no diff and no
event to commit. And the copy carries every tag, so the checks run against
the same history a CI checkout would see. The provenance demo is switched
off inside the copy by pointing `NFPROV_BLAME_JSON_FILE` at a missing
file; it has nothing to do with the archive.

## What it checks

| Case | Claim under test |
|------|------------------|
| 1 | every `rev*` tag whose tree holds top-level `stuff/*.md` gets one page under `docs/archive/`, is listed on `archive.html`, and no other tag is |
| 2 | the newest such tag's page holds one artifact per `stuff/*.md` in the tag, each anchored by file name and titled by the file's first `h1` |
| 3 | deleting `stuff/` from the working tree and regenerating changes no archive byte |
| 4 | regenerating a second time changes no archive byte |
| 5 | deleting the newest tag and regenerating removes its page and its index entry and leaves the others intact |

Cases 3 and 4 are No Drift stated as a diff: the archive after the change
is compared byte for byte against the archive before it. Case 5 is the
other half of the same rule. A page exists exactly as long as its tag, so
the archive cannot accumulate pages for cycles history no longer has.

The expected tag set is computed independently of the generator, with
`git tag` and `git ls-tree`, so the harness would catch a generator that
listed too many tags as readily as one that listed too few. It exits 2,
not 0, when no tag holds any `stuff/*.md`: a repository with nothing to
archive has nothing to prove.

## What it does not check

- Rendering. The harness trusts `bin/zmd2html` and checks anchors and
  titles only; a markdown regression would pass here and fail on the page.
- Tags without top-level markdown. They are expected to be absent from the
  archive and are, but no case asserts anything about their contents.
- The rest of the site. `index.html`, `cycles.html` and `stuff.html` link
  to the archive; those links are not followed.

## One cleanup that rode along

The provenance demo writes `docs/<source>.marked.md`. The source was
renamed from `CLAUDE.md` to `AGENTS.md` some cycles ago, and the old
`docs/CLAUDE.marked.md` stayed tracked because nothing removed it. The
generator now deletes every `*.marked.md` under `docs/` before writing the
current one, so the stale file goes on the next run, by the generator and
not by hand, as No Drift requires.
