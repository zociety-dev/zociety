# SPEC: zstop modes

Pluggable stop policies for `bin/zloop`. The policy is an executable predicate
selected per run. Default behaviour is unchanged.

## Interface

```
bin/zloop --stop <mode>[,<mode>...]     # flag wins over env
ZLOOP_STOP=<mode>[,<mode>...] bin/zloop
```

Default: `action`. `bin/zloop-complete` becomes a dispatcher: for each name,
run `bin/zstop-<name>`; exit 0 as soon as one exits 0; exit 1 if none did;
exit 2 (abort loop, message on stderr) if a name does not resolve or a
predicate exits 2.

`bin/zloop` must distinguish the dispatcher's three exit codes. The current
`if bin/zloop-complete; then` treats every non-zero code as "continue", so
exit 2 is silently swallowed. Capture the status explicitly: 0 -> stop
(exit 0), 2 -> abort (log to stderr, exit 2), anything else -> continue.

Predicate contract:
- exit 0 stop, 1 continue, 2 error
- stdout: one line `STOP: <mode> <reason>` or `CONTINUE: <mode> <reason>`;
  dispatcher forwards to stderr
- stateless; reads git and `.claude/zloop.state` only
- knobs via `ZSTOP_*` env, documented in the script header, `--help` supported
  (same `sed` header trick as `bin/zloop`)

`.claude/zloop.state` gains:
```
start: <sha at loop start>
mode: <resolved mode list>
```
`bin/zloop` rewrites this file every iteration (it currently emits only
`iteration`/`max`). Capture `START_SHA` and the resolved mode list into shell
variables once before the loop, then emit all four keys inside the existing
per-iteration `cat` block — writing `start`/`mode` only once would be clobbered
on iteration 2, and `zheap-death` deletes the file entirely when it archives.

`bin/zociety` must forward `ZSTOP_*` alongside `ZLOOP_*`.

Safety caps are not modes. `--max N` and `ZLOOP_TIMEOUT` stay unconditional,
checked before the predicate chain. Do not move them.

## Modes

Mapping from the five loop-program approaches. Approach 3 (schedules) is
already the backoff in `bin/zloop` and is not a stop predicate.

### 1. `action` (today's rule)
Stop when `bin/zstate .action` is `stop` or `promise`. Move the existing body
of `zloop-complete` here verbatim.

### 2. `budget` (system-owned counter)
Stop when `[heap-death]` commits in `start..HEAD` >= `ZSTOP_BUDGET` (default 3).
Also stop if `action` is `promise` (batch exhausted by an agent). Once this
mode exists, `zheap-death` should default `batch_size` to `ZSTOP_BUDGET - <heap-deaths so far>`
when unset, so the event data agrees with the loop. Do not remove the argument.

### 3. `converge` (state stops changing)
Compare the last `ZSTOP_PATIENCE + 1` (default 2 + 1) `cycle/*` branches by
`git rev-parse <branch>:stuff` tree hash and by count of files added under
`stuff/` in each cycle. A cycle is trivial if its stuff tree equals the prior
cycle's or it added < `ZSTOP_MIN_STUFF` (default 1) files. Stop after
`ZSTOP_PATIENCE` consecutive trivial cycles. Fewer branches than needed:
continue.

### 4. `feedback` (agent-reported, Copycat style)
Stop when the most recent `[heap-death]` event data contains `"done": true`.
Requires `zheap-death --done` flag which sets that field. The agent decides;
the loop honours it.

Read the heap-death event directly, not via `bin/zstate`. When a heap-death
leaves `remaining > 0`, `zheap-death` commits `[heap-death]` and then a
`[direction]` event, and `zstate` keys off the *latest* event — so it would
report `direction` and never see `done`. Find the commit explicitly:
```
sha=$(git log --format=%H --grep='^\[heap-death\]' -n 1)
done=$(git log -1 --format=%b "$sha" | jq '.data.done // false')
```

### 5. `file` (manual override)
Stop if `.claude/STOP` exists. Remove the file on stop and print who/when from
its mtime. Cheap, include it in every documented example combo.

Recommended combos: `action,file` (default-ish), `budget,file`,
`budget,converge,file`, `feedback,file`.

## History

Record the regime so runs are comparable:
- `zheap-death` reads `mode:` from `zloop.state` and adds
  `stop_mode: "<list>"` plus any `ZSTOP_*` values present to the heap-death
  event data and the direction event data.
- Append `stop=<list>` to the tag message.

## Files

| File | Change |
|---|---|
| `bin/zloop` | `--stop`/`ZLOOP_STOP`, write `start`/`mode` to state every iteration, pass mode to dispatcher, honour dispatcher exit 2 (abort) |
| `bin/zloop-complete` | becomes dispatcher |
| `bin/zstop-action` | new, old zloop-complete body |
| `bin/zstop-budget` | new |
| `bin/zstop-converge` | new |
| `bin/zstop-feedback` | new |
| `bin/zstop-file` | new |
| `bin/zheap-death` | `--done`, default batch from budget, record regime |
| `bin/zstate` | no change needed; `feedback` reads the `[heap-death]` commit directly (zstate reflects only the latest event) |
| `bin/zociety` | forward `ZSTOP_*` |
| `bin/zga-loop` | call dispatcher the same way, or leave on `action` and say so |
| `bin/zcheck` | list new scripts |
| `CLAUDE.md` | mode table, env table, examples |

## Tests

- shellcheck clean on every new script.
- Dry-run harness: fake `claude` on PATH plus a throwaway git repo with
  synthetic `[heap-death]`/`[direction]` commits and `cycle/*` branches.
  One case per mode proving stop and continue, plus one combo and one
  unresolvable name (expect exit 2, loop aborts).
- `bin/zloop --stop budget --max 3` against the fake harness must stop on
  budget before max.
