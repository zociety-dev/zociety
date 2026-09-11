# PROMPT.md

```bash
bin/zstate | jq .
```

The `action` field tells you what to do. The commands are in `bin/z*`.

When `action` is `contribute`, the `next` field says WHICH leg is short —
`contribute:member`, `contribute:rule` or `contribute:stuff`. Do that one.
`needs` shows how many of each are still REMAINING; a leg at 0 is done, do not
add more to it.

- `contribute:member` → `bin/zjoin`
- `contribute:rule` → `bin/zvote`, then `bin/zpass` once a rule has the votes
- `contribute:stuff` → write a file, then `bin/zstuff`

Genesis completes at: 3 members, 2 passed rules, 3 stuff items.
