# site/fonts

Self-hosted `P+` web fonts for the provenance demo page
(`docs/provenance.html`). `bin/zsite-generate` copies `*.woff2` from here
into `docs/fonts/` so the GitHub Pages build never depends on fonts
installed on the build machine.

## Files

| File | Weight | Size |
|------|--------|------|
| `AgaveNerdFontMonoP+-Regular.woff2` | 400 | ~27 KB |
| `AgaveNerdFontMonoP+-Bold.woff2` | 700 | ~22 KB |
| `OFL-agave.txt` | Upstream Agave license (SIL OFL 1.1) | |

## Provenance of the files

- **Typeface:** Agave, by agarick — <https://github.com/blobject/agave>
  (formerly `agarick/agave`; GitHub redirects). Licensed under the SIL Open
  Font License 1.1, copied verbatim to `OFL-agave.txt`.
- **Patch:** the `P+` ("provenance plus") build from the
  [delano/nerd-fonts](https://github.com/delano/nerd-fonts) fork, see
  [delano/nerd-fonts#15](https://github.com/delano/nerd-fonts/issues/15).
  A `P+` face adds, for every base glyph, a cmap format 14 variation
  sequence (U+E0100-E0104) and a Supplementary PUA-B mirror at
  U+100000 + codepoint, both pointing at a visually distinct `.ai` glyph.
  The Nerd Fonts patcher output was installed locally as
  `AgaveNerdFontMonoP+-{Regular,Bold}.ttf`.
- **Subset:** produced by `bin/zsite-fonts`, which runs

  ```
  pyftsubset <face>.ttf \
    --unicodes='0020-007E,00A0-00FF,2000-206F,2190-21FF,2500-259F,E0100-E0104,100000-1000FF' \
    --layout-features='*' \
    --name-IDs='*' \
    --notdef-outline \
    --glyph-names \
    --drop-tables+=PfEd \
    --flavor=woff2 \
    --output-file=site/fonts/<face>.woff2
  ```

  (fonttools 4.64, brotli). The subset keeps Basic Latin, Latin-1, general
  punctuation, arrows and box drawing, plus all variation-selector and
  PUA-B entries needed for the marks. The script fails if the resulting
  font lacks a format 14 cmap subtable or the U+100061 glyph.

## Rebuilding

```
bin/zsite-fonts ~/Library/Fonts/AgaveNerdFontMonoP+-Regular.ttf \
                ~/Library/Fonts/AgaveNerdFontMonoP+-Bold.ttf
```

Commit the resulting `.woff2` files; do not regenerate them in CI.
