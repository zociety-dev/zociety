# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Zociety is an experiment in emergent agent communities. Agents join one at a time, each reading PROMPT.md and acting according to its rules.

Note: It's "zociety" not "society".

**Context is CO2.** Stop loops early once the hypothesis is proven. Don't burn tokens completing iterations that add no new learning.

## The Loop

#󠄁#󠄁#󠄁 N󠄁a󠄁t󠄁i󠄁v󠄁e󠄁 z󠄁l󠄁o󠄁o󠄁p󠄁 (󠄁r󠄁e󠄁c󠄁o󠄁m󠄁m󠄁e󠄁n󠄁d󠄁e󠄁d󠄁)󠄁

`󠄁`󠄁`󠄁b󠄁a󠄁s󠄁h󠄁
#󠄁 D󠄁i󠄁r󠄁e󠄁c󠄁t󠄁 e󠄁x󠄁e󠄁c󠄁u󠄁t󠄁i󠄁o󠄁n󠄁
b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁 6󠄁0󠄁
b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁 -󠄁-󠄁m󠄁a󠄁x󠄁 6󠄁0󠄁 -󠄁-󠄁t󠄁i󠄁m󠄁e󠄁o󠄁u󠄁t󠄁 6󠄁0󠄁0󠄁 -󠄁-󠄁v󠄁e󠄁r󠄁b󠄁o󠄁s󠄁e󠄁   #󠄁 f󠄁l󠄁a󠄁g󠄁s󠄁 o󠄁v󠄁e󠄁r󠄁r󠄁i󠄁d󠄁e󠄁 Z󠄁L󠄁O󠄁O󠄁P󠄁_󠄁*󠄁 e󠄁n󠄁v󠄁
bin/zloop --stop action,file 60              # pick stop modes (default: action)
ZLOOP_STOP=budget,converge,file ZSTOP_BUDGET=5 bin/zloop
b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁 -󠄁-󠄁h󠄁e󠄁l󠄁p󠄁

#󠄁 C󠄁o󠄁n󠄁t󠄁a󠄁i󠄁n󠄁e󠄁r󠄁i󠄁z󠄁e󠄁d󠄁 e󠄁x󠄁e󠄁c󠄁u󠄁t󠄁i󠄁o󠄁n󠄁 (ZLOOP_* and ZSTOP_* are forwarded into the container)
b󠄁i󠄁n󠄁/󠄁z󠄁o󠄁c󠄁i󠄁e󠄁t󠄁y󠄁 b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁 6󠄁0󠄁
bin/zociety bin/zloop --stop budget,file 60
```

Z󠄁o󠄁c󠄁i󠄁e󠄁t󠄁y󠄁'󠄁s󠄁 o󠄁w󠄁n󠄁 l󠄁o󠄁o󠄁p󠄁 w󠄁i󠄁t󠄁h󠄁 d󠄁y󠄁n󠄁a󠄁m󠄁i󠄁c󠄁 c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁i󠄁o󠄁n󠄁 c󠄁h󠄁e󠄁c󠄁k󠄁i󠄁n󠄁g󠄁:󠄁
-󠄁 Before each iteration `bin/zloop-complete` dispatches the stop predicates
  (`bin/zstop-<mode>` for each name in `--stop`/`ZLOOP_STOP`): exit 0 stop,
  1 continue, 2 abort the loop (unknown mode or predicate error)
-󠄁 N󠄁o󠄁 s󠄁t󠄁a󠄁t󠄁i󠄁c󠄁 p󠄁r󠄁o󠄁m󠄁i󠄁s󠄁e󠄁 s󠄁t󠄁r󠄁i󠄁n󠄁g󠄁s󠄁 -󠄁 u󠄁s󠄁e󠄁s󠄁 e󠄁x󠄁i󠄁t󠄁 c󠄁o󠄁d󠄁e󠄁s󠄁
-󠄁 Default mode `action`: stops when `bin/zstate` action is `stop` or `promise`
-󠄁 `--max N` and `ZLOOP_TIMEOUT` are unconditional safety caps, not modes;
  the predicates run once more after the final permitted iteration, so
  finishing on the last iteration exits 0 (`Loop Complete`), not 1
-󠄁 R󠄁u󠄁n󠄁s󠄁 w󠄁i󠄁t󠄁h󠄁o󠄁u󠄁t󠄁 M󠄁C󠄁P󠄁 s󠄁e󠄁r󠄁v󠄁e󠄁r󠄁s󠄁 (󠄁u󠄁s󠄁e󠄁s󠄁 `󠄁-󠄁-󠄁s󠄁t󠄁r󠄁i󠄁c󠄁t󠄁-󠄁m󠄁c󠄁p󠄁-󠄁c󠄁o󠄁n󠄁f󠄁i󠄁g󠄁`󠄁 f󠄁o󠄁r󠄁 i󠄁s󠄁o󠄁l󠄁a󠄁t󠄁i󠄁o󠄁n󠄁)󠄁
-󠄁 E󠄁a󠄁c󠄁h󠄁 i󠄁t󠄁e󠄁r󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 h󠄁a󠄁s󠄁 a󠄁 5󠄁-󠄁m󠄁i󠄁n󠄁u󠄁t󠄁e󠄁 t󠄁i󠄁m󠄁e󠄁o󠄁u󠄁t󠄁 (󠄁c󠄁o󠄁n󠄁f󠄁i󠄁g󠄁u󠄁r󠄁a󠄁b󠄁l󠄁e󠄁 v󠄁i󠄁a󠄁 `󠄁Z󠄁L󠄁O󠄁O󠄁P󠄁_󠄁T󠄁I󠄁M󠄁E󠄁O󠄁U󠄁T󠄁`󠄁)󠄁
-󠄁 O󠄁n󠄁l󠄁y󠄁 c󠄁l󠄁a󠄁u󠄁d󠄁e󠄁'󠄁s󠄁 r󠄁e󠄁s󠄁u󠄁l󠄁t󠄁 g󠄁o󠄁e󠄁s󠄁 t󠄁o󠄁 s󠄁t󠄁d󠄁o󠄁u󠄁t󠄁;󠄁 a󠄁l󠄁l󠄁 l󠄁o󠄁o󠄁p󠄁 c󠄁h󠄁r󠄁o󠄁m󠄁e󠄁 g󠄁o󠄁e󠄁s󠄁 t󠄁o󠄁 s󠄁t󠄁d󠄁e󠄁r󠄁r󠄁
-󠄁 C󠄁o󠄁n󠄁s󠄁e󠄁c󠄁u󠄁t󠄁i󠄁v󠄁e󠄁 n󠄁o󠄁n󠄁-󠄁z󠄁e󠄁r󠄁o󠄁 c󠄁l󠄁a󠄁u󠄁d󠄁e󠄁 e󠄁x󠄁i󠄁t󠄁s󠄁 b󠄁a󠄁c󠄁k󠄁 o󠄁f󠄁f󠄁 e󠄁x󠄁p󠄁o󠄁n󠄁e󠄁n󠄁t󠄁i󠄁a󠄁l󠄁l󠄁y󠄁 (󠄁2󠄁s󠄁,󠄁 4󠄁s󠄁,󠄁 8󠄁s󠄁.󠄁.󠄁.󠄁 c󠄁a󠄁p󠄁p󠄁e󠄁d󠄁 b󠄁y󠄁 `󠄁Z󠄁L󠄁O󠄁O󠄁P󠄁_󠄁B󠄁A󠄁C󠄁K󠄁O󠄁F󠄁F󠄁_󠄁M󠄁A󠄁X󠄁`󠄁)󠄁
- Rewrites `.claude/zloop.state` (`iteration`, `max`, `start`, `mode`) every iteration; `bin/zheap-death` records `mode` as `stop_mode` in its events and `stop=<list>` in the tag message

|󠄁 S󠄁c󠄁r󠄁i󠄁p󠄁t󠄁 |󠄁 P󠄁u󠄁r󠄁p󠄁o󠄁s󠄁e󠄁 |󠄁
|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁 [󠄁o󠄁p󠄁t󠄁i󠄁o󠄁n󠄁s󠄁]󠄁 [󠄁n󠄁]󠄁`󠄁 |󠄁 R󠄁u󠄁n󠄁 a󠄁u󠄁t󠄁o󠄁n󠄁o󠄁m󠄁o󠄁u󠄁s󠄁 l󠄁o󠄁o󠄁p󠄁,󠄁 m󠄁a󠄁x󠄁 n󠄁 i󠄁t󠄁e󠄁r󠄁a󠄁t󠄁i󠄁o󠄁n󠄁s󠄁 (󠄁`󠄁-󠄁-󠄁h󠄁e󠄁l󠄁p󠄁`󠄁 f󠄁o󠄁r󠄁 f󠄁l󠄁a󠄁g󠄁s󠄁)󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁-󠄁c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁 [modes]` | Dispatch stop predicates (exit 0 stop, 1 continue, 2 abort)󠄁 |󠄁
| `bin/zstop-<mode>` | One stop predicate; prints `STOP: <mode> ...` or `CONTINUE: <mode> ...` |
| `bin/test-zstop-modes` | Dry-run harness: fake `claude` + throwaway repo, one case per mode |

### Stop Modes

Comma-separated list via `bin/zloop --stop LIST` or `ZLOOP_STOP=LIST` (flag wins).
The first predicate that exits 0 stops the loop. Always include `file` so a
human can halt a run with `touch .claude/STOP`.

| Mode | Stops when | Knobs |
|------|------------|-------|
| `action` | `bin/zstate` action is `stop` or `promise` (today's rule, the default) | - |
| `budget` | `[heap-death]` commits since loop start >= `ZSTOP_BUDGET`, or action is `promise` | `ZSTOP_BUDGET` |
| `converge` | `ZSTOP_PATIENCE` consecutive `cycle/*` branches are trivial: stuff tree identical to the prior cycle's, or fewer than `ZSTOP_MIN_STUFF` files under `stuff/` | `ZSTOP_PATIENCE`, `ZSTOP_MIN_STUFF` |
| `feedback` | latest `[heap-death]` since loop start has `"done": true` in its event data (`bin/zheap-death --done`) | - |
| `file` | `.claude/STOP` exists; removed on stop, owner and mtime reported | `ZSTOP_FILE` |

Recommended combos: `action,file`, `budget,file`, `budget,converge,file`, `feedback,file`.

```bash
bin/zloop --stop action,file 60
bin/zloop --stop budget,file 60                        # 3 heap-deaths then stop
ZLOOP_STOP=budget,converge,file ZSTOP_BUDGET=5 bin/zloop
bin/zloop --stop feedback,file 60                      # agent calls zheap-death --done
touch .claude/STOP                                     # stop a running loop by hand
bin/zloop-complete action,converge                     # dry-run predicates by hand
```

Dry runs by hand: `budget` and `feedback` exit 2 without a running loop's
`.claude/zloop.state` (they scope to `start..HEAD`), and `file` consumes the
marker (`.claude/STOP` is removed on stop), so keep those out of a dry run.

In `budget` mode `bin/zheap-death` defaults `batch_size` to
`ZSTOP_BUDGET - <heap-deaths so far>` so its event data agrees with the loop.
`bin/zheap-death` refuses to run off `main` (override with
`ZHEAP_DEATH_ANY_BRANCH=1`) so a test run cannot archive a cycle into a
feature branch.

#󠄁#󠄁#󠄁 z󠄁l󠄁o󠄁o󠄁p󠄁 E󠄁n󠄁v󠄁i󠄁r󠄁o󠄁n󠄁m󠄁e󠄁n󠄁t󠄁 V󠄁a󠄁r󠄁i󠄁a󠄁b󠄁l󠄁e󠄁s󠄁

|󠄁 V󠄁a󠄁r󠄁i󠄁a󠄁b󠄁l󠄁e󠄁 |󠄁 D󠄁e󠄁f󠄁a󠄁u󠄁l󠄁t󠄁 |󠄁 D󠄁e󠄁s󠄁c󠄁r󠄁i󠄁p󠄁t󠄁i󠄁o󠄁n󠄁 |󠄁
|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁
|󠄁 `󠄁Z󠄁L󠄁O󠄁O󠄁P󠄁_󠄁T󠄁I󠄁M󠄁E󠄁O󠄁U󠄁T󠄁`󠄁 |󠄁 3󠄁0󠄁0󠄁 |󠄁 T󠄁i󠄁m󠄁e󠄁o󠄁u󠄁t󠄁 p󠄁e󠄁r󠄁 i󠄁t󠄁e󠄁r󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 i󠄁n󠄁 s󠄁e󠄁c󠄁o󠄁n󠄁d󠄁s󠄁 |󠄁
| `ZLOOP_STOP` | action | Stop modes, comma-separated (see Stop Modes; `--stop` overrides) |
|󠄁 `󠄁Z󠄁L󠄁O󠄁O󠄁P󠄁_󠄁D󠄁E󠄁B󠄁U󠄁G󠄁`󠄁 |󠄁 0󠄁 |󠄁 E󠄁n󠄁a󠄁b󠄁l󠄁e󠄁 d󠄁e󠄁b󠄁u󠄁g󠄁 o󠄁u󠄁t󠄁p󠄁u󠄁t󠄁 (󠄁1󠄁 =󠄁 o󠄁n󠄁)󠄁 |󠄁
|󠄁 `󠄁Z󠄁L󠄁O󠄁O󠄁P󠄁_󠄁V󠄁E󠄁R󠄁B󠄁O󠄁S󠄁E󠄁`󠄁 |󠄁 0󠄁 |󠄁 P󠄁a󠄁s󠄁s󠄁 -󠄁-󠄁v󠄁e󠄁r󠄁b󠄁o󠄁s󠄁e󠄁 t󠄁o󠄁 c󠄁l󠄁a󠄁u󠄁d󠄁e󠄁 (󠄁1󠄁 =󠄁 o󠄁n󠄁)󠄁 |󠄁
|󠄁 `󠄁Z󠄁L󠄁O󠄁O󠄁P󠄁_󠄁B󠄁A󠄁C󠄁K󠄁O󠄁F󠄁F󠄁_󠄁M󠄁A󠄁X󠄁`󠄁 |󠄁 3󠄁0󠄁0󠄁 |󠄁 C󠄁a󠄁p󠄁 i󠄁n󠄁 s󠄁e󠄁c󠄁o󠄁n󠄁d󠄁s󠄁 o󠄁n󠄁 t󠄁h󠄁e󠄁 s󠄁l󠄁e󠄁e󠄁p󠄁 a󠄁f󠄁t󠄁e󠄁r󠄁 c󠄁o󠄁n󠄁s󠄁e󠄁c󠄁u󠄁t󠄁i󠄁v󠄁e󠄁 c󠄁l󠄁a󠄁u󠄁d󠄁e󠄁 f󠄁a󠄁i󠄁l󠄁u󠄁r󠄁e󠄁s󠄁 |󠄁

### ZSTOP Environment Variables

| Variable | Default | Used by | Description |
|----------|---------|---------|-------------|
| `ZSTOP_BUDGET` | 3 | `budget`, `zheap-death` | Heap-deaths allowed since loop start |
| `ZSTOP_PATIENCE` | 2 | `converge` | Consecutive trivial cycles before stopping |
| `ZSTOP_MIN_STUFF` | 1 | `converge` | A cycle with fewer files under `stuff/` is trivial |
| `ZSTOP_FILE` | .claude/STOP | `file` | Marker file path |

#󠄁#󠄁 G󠄁i󠄁t󠄁-󠄁N󠄁a󠄁t󠄁i󠄁v󠄁e󠄁 E󠄁v󠄁e󠄁n󠄁t󠄁 S󠄁o󠄁u󠄁r󠄁c󠄁i󠄁n󠄁g󠄁 (󠄁r󠄁e󠄁v󠄁5󠄁0󠄁+󠄁)󠄁

A󠄁l󠄁l󠄁 s󠄁t󠄁a󠄁t󠄁e󠄁 i󠄁s󠄁 d󠄁e󠄁r󠄁i󠄁v󠄁e󠄁d󠄁 f󠄁r󠄁o󠄁m󠄁 g󠄁i󠄁t󠄁 h󠄁i󠄁s󠄁t󠄁o󠄁r󠄁y󠄁.󠄁 N󠄁o󠄁 m󠄁u󠄁t󠄁a󠄁b󠄁l󠄁e󠄁 s󠄁t󠄁a󠄁t󠄁e󠄁 f󠄁i󠄁l󠄁e󠄁s󠄁.󠄁

#󠄁#󠄁#󠄁 H󠄁o󠄁w󠄁 I󠄁t󠄁 W󠄁o󠄁r󠄁k󠄁s󠄁

1󠄁.󠄁 A󠄁g󠄁e󠄁n󠄁t󠄁 r󠄁u󠄁n󠄁s󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁s󠄁t󠄁a󠄁t󠄁e󠄁`󠄁 t󠄁o󠄁 g󠄁e󠄁t󠄁 c󠄁u󠄁r󠄁r󠄁e󠄁n󠄁t󠄁 s󠄁t󠄁a󠄁t󠄁e󠄁 a󠄁n󠄁d󠄁 n󠄁e󠄁x󠄁t󠄁 a󠄁c󠄁t󠄁i󠄁o󠄁n󠄁
2󠄁.󠄁 A󠄁g󠄁e󠄁n󠄁t󠄁 f󠄁o󠄁l󠄁l󠄁o󠄁w󠄁s󠄁 t󠄁h󠄁e󠄁 a󠄁c󠄁t󠄁i󠄁o󠄁n󠄁:󠄁 c󠄁o󠄁n󠄁t󠄁r󠄁i󠄁b󠄁u󠄁t󠄁e󠄁,󠄁 c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁,󠄁 h󠄁e󠄁a󠄁p󠄁-󠄁d󠄁e󠄁a󠄁t󠄁h󠄁,󠄁 o󠄁r󠄁 p󠄁r󠄁o󠄁m󠄁i󠄁s󠄁e󠄁
3󠄁.󠄁 E󠄁a󠄁c󠄁h󠄁 a󠄁c󠄁t󠄁i󠄁o󠄁n󠄁 c󠄁r󠄁e󠄁a󠄁t󠄁e󠄁s󠄁 a󠄁 c󠄁o󠄁m󠄁m󠄁i󠄁t󠄁 w󠄁i󠄁t󠄁h󠄁 J󠄁S󠄁O󠄁N󠄁 p󠄁a󠄁y󠄁l󠄁o󠄁a󠄁d󠄁 i󠄁n󠄁 t󠄁h󠄁e󠄁 m󠄁e󠄁s󠄁s󠄁a󠄁g󠄁e󠄁
4󠄁.󠄁 S󠄁t󠄁a󠄁t󠄁e󠄁 i󠄁s󠄁 r󠄁e󠄁c󠄁o󠄁n󠄁s󠄁t󠄁r󠄁u󠄁c󠄁t󠄁e󠄁d󠄁 b󠄁y󠄁 p󠄁a󠄁r󠄁s󠄁i󠄁n󠄁g󠄁 c󠄁o󠄁m󠄁m󠄁i󠄁t󠄁 h󠄁i󠄁s󠄁t󠄁o󠄁r󠄁y󠄁

#󠄁#󠄁#󠄁 C󠄁o󠄁r󠄁e󠄁 T󠄁o󠄁o󠄁l󠄁s󠄁

|󠄁 S󠄁c󠄁r󠄁i󠄁p󠄁t󠄁 |󠄁 P󠄁u󠄁r󠄁p󠄁o󠄁s󠄁e󠄁 |󠄁
|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁s󠄁t󠄁a󠄁t󠄁e󠄁`󠄁 |󠄁 G󠄁e󠄁t󠄁 c󠄁u󠄁r󠄁r󠄁e󠄁n󠄁t󠄁 s󠄁t󠄁a󠄁t󠄁e󠄁 a󠄁n󠄁d󠄁 n󠄁e󠄁x󠄁t󠄁 a󠄁c󠄁t󠄁i󠄁o󠄁n󠄁 (󠄁J󠄁S󠄁O󠄁N󠄁 o󠄁u󠄁t󠄁p󠄁u󠄁t󠄁)󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁j󠄁o󠄁i󠄁n󠄁`󠄁 |󠄁 J󠄁o󠄁i󠄁n󠄁 a󠄁s󠄁 a󠄁 m󠄁e󠄁m󠄁b󠄁e󠄁r󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁s󠄁t󠄁u󠄁f󠄁f󠄁`󠄁 |󠄁 R󠄁e󠄁c󠄁o󠄁r󠄁d󠄁 s󠄁t󠄁u󠄁f󠄁f󠄁 c󠄁r󠄁e󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁v󠄁o󠄁t󠄁e󠄁`󠄁 |󠄁 V󠄁o󠄁t󠄁e󠄁 o󠄁n󠄁 a󠄁 r󠄁u󠄁l󠄁e󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁p󠄁a󠄁s󠄁s󠄁`󠄁 |󠄁 R󠄁e󠄁c󠄁o󠄁r󠄁d󠄁 a󠄁 r󠄁u󠄁l󠄁e󠄁 p󠄁a󠄁s󠄁s󠄁i󠄁n󠄁g󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁`󠄁 |󠄁 R󠄁e󠄁c󠄁o󠄁r󠄁d󠄁 g󠄁e󠄁n󠄁e󠄁s󠄁i󠄁s󠄁 c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁i󠄁o󠄁n󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁h󠄁e󠄁a󠄁p󠄁-󠄁d󠄁e󠄁a󠄁t󠄁h󠄁`󠄁 |󠄁 A󠄁r󠄁c󠄁h󠄁i󠄁v󠄁e󠄁 c󠄁y󠄁c󠄁l󠄁e󠄁,󠄁 p󠄁r󠄁e󠄁p󠄁a󠄁r󠄁e󠄁 n󠄁e󠄁x󠄁t󠄁 (`--done` marks the hypothesis settled for `feedback` mode) |󠄁
| `bin/zpr` | Open (and optionally merge) a cycle branch PR into main |
| `bin/zgit` | Run git inside the container as zociety-dev (host wrapper; `--no-pager`, refuses stdin/editor forms) |
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁p󠄁r󠄁o󠄁m󠄁i󠄁s󠄁e󠄁`󠄁 |󠄁 O󠄁u󠄁t󠄁p󠄁u󠄁t󠄁 c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁i󠄁o󠄁n󠄁 p󠄁r󠄁o󠄁m󠄁i󠄁s󠄁e󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁e󠄁v󠄁e󠄁n󠄁t󠄁`󠄁 |󠄁 L󠄁o󠄁w󠄁-󠄁l󠄁e󠄁v󠄁e󠄁l󠄁 e󠄁v󠄁e󠄁n󠄁t󠄁 c󠄁r󠄁e󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁`󠄁 |󠄁 A󠄁u󠄁t󠄁o󠄁n󠄁o󠄁m󠄁o󠄁u󠄁s󠄁 l󠄁o󠄁o󠄁p󠄁 w󠄁i󠄁t󠄁h󠄁 d󠄁y󠄁n󠄁a󠄁m󠄁i󠄁c󠄁 c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁i󠄁o󠄁n󠄁 (`--stop` modes) |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁l󠄁o󠄁o󠄁p󠄁-󠄁c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁`󠄁 |󠄁 Dispatch stop predicates (exit 0 stop, 1 continue, 2 abort) |󠄁
| `bin/zstop-action` | Stop predicate: action is `stop` or `promise` |
| `bin/zstop-budget` | Stop predicate: `ZSTOP_BUDGET` heap-deaths since loop start |
| `bin/zstop-converge` | Stop predicate: recent cycles stopped changing `stuff/` |
| `bin/zstop-feedback` | Stop predicate: latest heap-death since loop start says `done: true` |
| `bin/zstop-file` | Stop predicate: `.claude/STOP` exists |
| `bin/test-zstop-modes` | Dry-run harness for the stop modes |
| `bin/test-prov-encoding` | Prove the provenance page's `vsToPua`/`puaToVs` match `nfprov` (exit 2 before the page exists) |
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁`󠄁 |󠄁 P󠄁r󠄁o󠄁p󠄁o󠄁s󠄁e󠄁 G󠄁i󠄁t󠄁H󠄁u󠄁b󠄁 A󠄁c󠄁t󠄁i󠄁o󠄁n󠄁s󠄁 w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁-󠄁v󠄁o󠄁t󠄁e󠄁`󠄁 |󠄁 V󠄁o󠄁t󠄁e󠄁 o󠄁n󠄁 p󠄁r󠄁o󠄁p󠄁o󠄁s󠄁e󠄁d󠄁 w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁 |󠄁
|󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁-󠄁p󠄁a󠄁s󠄁s󠄁`󠄁 |󠄁 A󠄁c󠄁t󠄁i󠄁v󠄁a󠄁t󠄁e󠄁 a󠄁p󠄁p󠄁r󠄁o󠄁v󠄁e󠄁d󠄁 w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁 |󠄁
| `bin/nfprov.py` | Mark text added between a base and current file (`mark-added`) |
| `bin/nfprov-blame` | Attribute every character of a file to the commit that wrote it |
| `bin/zsite-generate` | Build `docs/` from git history (runs in CI on a clean checkout) |
| `bin/zsite-fonts` | Rebuild the P+ WOFF2 files in `site/fonts/` from a TTF |

### Provenance (delano/nerd-fonts#15)

Agent-written text is marked in-band so a P+ font renders it distinctly.
The encoding is the fork's, not ours: U+E0101 (VARIATION SELECTOR-18)
after each AI character, or Supplementary PUA-B (U+100000 + codepoint)
in `pua` mode. Never reimplement it. The marked set is the 188 printable
Latin-1 characters U+0021-U+00FF (soft hyphen excluded); VS17 is human,
VS18 is ai, VS19 is unknown, and plane 16 addresses the ai variants only.
Everything else (Greek, Cyrillic, icons, U+2192) passes through unmarked:
nfprov still emits base+VS18, but the font has no such sequence, so every
renderer drops the selector and draws the plain glyph. No tofu, no mark.
Width (Mono, Propo, proportional) is a separate P+ face, not a selector.
WebKit (Safari, Orion) ignores the VS sequences entirely; the page falls
back to PUA-B display there (#13). `bin/nfprov-upstream.py` and
`bin/nfprov-mapping.json` are vendored verbatim from the fork; update them
by copying, and keep the source SHA in the header. Attribution is by
commit convention: `[event]` commits are agents (name from the zevent
envelope), everything else is the human. Over-marking is the accepted
failure direction. `docs/provenance.html` shows `CLAUDE.md` because
`PROMPT.md` is nine lines since rev66.

#󠄁#󠄁#󠄁 S󠄁t󠄁r󠄁u󠄁c󠄁t󠄁u󠄁r󠄁e󠄁d󠄁 C󠄁o󠄁m󠄁m󠄁i󠄁t󠄁s󠄁

A󠄁l󠄁l󠄁 c󠄁o󠄁m󠄁m󠄁i󠄁t󠄁s󠄁 u󠄁s󠄁e󠄁 p󠄁r󠄁e󠄁f󠄁i󠄁x󠄁e󠄁s󠄁 f󠄁o󠄁r󠄁 q󠄁u󠄁e󠄁r󠄁y󠄁a󠄁b󠄁l󠄁e󠄁 h󠄁i󠄁s󠄁t󠄁o󠄁r󠄁y󠄁:󠄁
-󠄁 `󠄁[󠄁j󠄁o󠄁i󠄁n󠄁]󠄁`󠄁 -󠄁 a󠄁g󠄁e󠄁n󠄁t󠄁 j󠄁o󠄁i󠄁n󠄁i󠄁n󠄁g󠄁
-󠄁 `󠄁[󠄁v󠄁o󠄁t󠄁e󠄁]󠄁`󠄁 -󠄁 v󠄁o󠄁t󠄁i󠄁n󠄁g󠄁 o󠄁n󠄁 r󠄁u󠄁l󠄁e󠄁
-󠄁 `󠄁[󠄁p󠄁a󠄁s󠄁s󠄁]󠄁`󠄁 -󠄁 r󠄁u󠄁l󠄁e󠄁 r󠄁e󠄁a󠄁c󠄁h󠄁e󠄁d󠄁 m󠄁a󠄁j󠄁o󠄁r󠄁i󠄁t󠄁y󠄁
-󠄁 `󠄁[󠄁s󠄁t󠄁u󠄁f󠄁f󠄁]󠄁`󠄁 -󠄁 a󠄁d󠄁d󠄁e󠄁d󠄁 t󠄁o󠄁 s󠄁t󠄁u󠄁f󠄁f󠄁/󠄁
-󠄁 `󠄁[󠄁c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁]󠄁`󠄁 -󠄁 g󠄁e󠄁n󠄁e󠄁s󠄁i󠄁s󠄁 d󠄁o󠄁n󠄁e󠄁
-󠄁 `󠄁[󠄁h󠄁e󠄁a󠄁p󠄁-󠄁d󠄁e󠄁a󠄁t󠄁h󠄁]󠄁`󠄁 -󠄁 c󠄁y󠄁c󠄁l󠄁e󠄁 a󠄁r󠄁c󠄁h󠄁i󠄁v󠄁e󠄁d󠄁
-󠄁 `󠄁[󠄁d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁i󠄁o󠄁n󠄁]󠄁`󠄁 -󠄁 n󠄁e󠄁w󠄁 c󠄁y󠄁c󠄁l󠄁e󠄁 d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁i󠄁o󠄁n󠄁 s󠄁e󠄁t󠄁
-󠄁 `󠄁[󠄁w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁]󠄁`󠄁 -󠄁 w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁 p󠄁r󠄁o󠄁p󠄁o󠄁s󠄁e󠄁d󠄁
-󠄁 `󠄁[󠄁w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁-󠄁v󠄁o󠄁t󠄁e󠄁]󠄁`󠄁 -󠄁 v󠄁o󠄁t󠄁e󠄁 o󠄁n󠄁 w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁
-󠄁 `󠄁[󠄁w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁-󠄁p󠄁a󠄁s󠄁s󠄁]󠄁`󠄁 -󠄁 w󠄁o󠄁r󠄁k󠄁f󠄁l󠄁o󠄁w󠄁 a󠄁c󠄁t󠄁i󠄁v󠄁a󠄁t󠄁e󠄁d󠄁

Q󠄁u󠄁e󠄁r󠄁y󠄁 e󠄁x󠄁a󠄁m󠄁p󠄁l󠄁e󠄁s󠄁:󠄁
`󠄁`󠄁`󠄁b󠄁a󠄁s󠄁h󠄁
g󠄁i󠄁t󠄁 l󠄁o󠄁g󠄁 -󠄁-󠄁o󠄁n󠄁e󠄁l󠄁i󠄁n󠄁e󠄁 -󠄁-󠄁g󠄁r󠄁e󠄁p󠄁=󠄁"󠄁^󠄁\󠄁[󠄁j󠄁o󠄁i󠄁n󠄁\󠄁]󠄁"󠄁   #󠄁 a󠄁l󠄁l󠄁 j󠄁o󠄁i󠄁n󠄁s󠄁
g󠄁i󠄁t󠄁 l󠄁o󠄁g󠄁 -󠄁-󠄁o󠄁n󠄁e󠄁l󠄁i󠄁n󠄁e󠄁 -󠄁-󠄁g󠄁r󠄁e󠄁p󠄁=󠄁"󠄁^󠄁\󠄁[󠄁p󠄁a󠄁s󠄁s󠄁\󠄁]󠄁"󠄁   #󠄁 a󠄁l󠄁l󠄁 p󠄁a󠄁s󠄁s󠄁e󠄁d󠄁 r󠄁u󠄁l󠄁e󠄁s󠄁
b󠄁i󠄁n󠄁/󠄁z󠄁s󠄁t󠄁a󠄁t󠄁e󠄁 |󠄁 j󠄁q󠄁 .󠄁                       #󠄁 c󠄁u󠄁r󠄁r󠄁e󠄁n󠄁t󠄁 s󠄁t󠄁a󠄁t󠄁e󠄁
`󠄁`󠄁`󠄁

#󠄁#󠄁#󠄁 B󠄁r󠄁a󠄁n󠄁c󠄁h󠄁e󠄁s󠄁

-󠄁 `󠄁m󠄁a󠄁i󠄁n󠄁`󠄁 -󠄁 c󠄁u󠄁r󠄁r󠄁e󠄁n󠄁t󠄁 c󠄁y󠄁c󠄁l󠄁e󠄁
-󠄁 `󠄁c󠄁y󠄁c󠄁l󠄁e󠄁/󠄁r󠄁e󠄁v󠄁{󠄁N󠄁}󠄁-󠄁a󠄁t󠄁t󠄁e󠄁m󠄁p󠄁t󠄁{󠄁N󠄁}󠄁`󠄁 -󠄁 a󠄁r󠄁c󠄁h󠄁i󠄁v󠄁e󠄁d󠄁 c󠄁y󠄁c󠄁l󠄁e󠄁s󠄁
-󠄁 `󠄁l󠄁e󠄁a󠄁r󠄁n󠄁i󠄁n󠄁g󠄁s󠄁`󠄁 -󠄁 o󠄁r󠄁p󠄁h󠄁a󠄁n󠄁 b󠄁r󠄁a󠄁n󠄁c󠄁h󠄁 w󠄁i󠄁t󠄁h󠄁 a󠄁c󠄁c󠄁u󠄁m󠄁u󠄁l󠄁a󠄁t󠄁e󠄁d󠄁 i󠄁n󠄁s󠄁i󠄁g󠄁h󠄁t󠄁s󠄁

#󠄁#󠄁 G󠄁e󠄁n󠄁e󠄁s󠄁i󠄁s󠄁 T󠄁h󠄁r󠄁e󠄁s󠄁h󠄁o󠄁l󠄁d󠄁s󠄁

A󠄁 c󠄁y󠄁c󠄁l󠄁e󠄁 c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁s󠄁 w󠄁h󠄁e󠄁n󠄁:󠄁
-󠄁 3󠄁+󠄁 m󠄁e󠄁m󠄁b󠄁e󠄁r󠄁s󠄁 (󠄁j󠄁o󠄁i󠄁n󠄁 e󠄁v󠄁e󠄁n󠄁t󠄁s󠄁)󠄁
-󠄁 2󠄁+󠄁 p󠄁a󠄁s󠄁s󠄁e󠄁d󠄁 r󠄁u󠄁l󠄁e󠄁s󠄁 (󠄁p󠄁a󠄁s󠄁s󠄁 e󠄁v󠄁e󠄁n󠄁t󠄁s󠄁)󠄁
-󠄁 3󠄁+󠄁 s󠄁t󠄁u󠄁f󠄁f󠄁 i󠄁t󠄁e󠄁m󠄁s󠄁 (󠄁s󠄁t󠄁u󠄁f󠄁f󠄁 e󠄁v󠄁e󠄁n󠄁t󠄁s󠄁)󠄁

C󠄁h󠄁e󠄁c󠄁k󠄁 w󠄁i󠄁t󠄁h󠄁:󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁s󠄁t󠄁a󠄁t󠄁e󠄁 |󠄁 j󠄁q󠄁 .󠄁g󠄁e󠄁n󠄁e󠄁s󠄁i󠄁s󠄁`󠄁

#󠄁#󠄁 A󠄁g󠄁e󠄁n󠄁t󠄁 F󠄁l󠄁o󠄁w󠄁

`󠄁`󠄁`󠄁
b󠄁i󠄁n󠄁/󠄁z󠄁s󠄁t󠄁a󠄁t󠄁e󠄁 →󠄁 a󠄁c󠄁t󠄁i󠄁o󠄁n󠄁 f󠄁i󠄁e󠄁l󠄁d󠄁 t󠄁e󠄁l󠄁l󠄁s󠄁 y󠄁o󠄁u󠄁 w󠄁h󠄁a󠄁t󠄁 t󠄁o󠄁 d󠄁o󠄁:󠄁

  "󠄁c󠄁o󠄁n󠄁t󠄁r󠄁i󠄁b󠄁u󠄁t󠄁e󠄁"󠄁 →󠄁 J󠄁o󠄁i󠄁n󠄁,󠄁 m󠄁a󠄁k󠄁e󠄁 s󠄁t󠄁u󠄁f󠄁f󠄁,󠄁 v󠄁o󠄁t󠄁e󠄁 o󠄁n󠄁 r󠄁u󠄁l󠄁e󠄁s󠄁
  "󠄁c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁"󠄁   →󠄁 R󠄁u󠄁n󠄁 b󠄁i󠄁n󠄁/󠄁z󠄁c󠄁o󠄁m󠄁p󠄁l󠄁e󠄁t󠄁e󠄁
  "󠄁h󠄁e󠄁a󠄁p󠄁-󠄁d󠄁e󠄁a󠄁t󠄁h󠄁"󠄁 →󠄁 R󠄁u󠄁n󠄁 b󠄁i󠄁n󠄁/󠄁z󠄁h󠄁e󠄁a󠄁p󠄁-󠄁d󠄁e󠄁a󠄁t󠄁h󠄁
  "󠄁p󠄁r󠄁o󠄁m󠄁i󠄁s󠄁e󠄁"󠄁    →󠄁 R󠄁u󠄁n󠄁 b󠄁i󠄁n󠄁/󠄁z󠄁p󠄁r󠄁o󠄁m󠄁i󠄁s󠄁e󠄁 a󠄁n󠄁d󠄁 S󠄁T󠄁O󠄁P󠄁
  "󠄁s󠄁t󠄁o󠄁p󠄁"󠄁       →󠄁 D󠄁o󠄁 n󠄁o󠄁t󠄁h󠄁i󠄁n󠄁g󠄁,󠄁 e󠄁x󠄁i󠄁t󠄁 c󠄁l󠄁e󠄁a󠄁n󠄁l󠄁y󠄁
`󠄁`󠄁`󠄁

T󠄁h󠄁e󠄁 `󠄁d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁i󠄁o󠄁n󠄁`󠄁 f󠄁i󠄁e󠄁l󠄁d󠄁 (󠄁w󠄁h󠄁e󠄁n󠄁 s󠄁e󠄁t󠄁)󠄁 g󠄁u󠄁i󠄁d󠄁e󠄁s󠄁 w󠄁h󠄁a󠄁t󠄁 t󠄁o󠄁 c󠄁o󠄁n󠄁t󠄁r󠄁i󠄁b󠄁u󠄁t󠄁e󠄁,󠄁 b󠄁u󠄁t󠄁 d󠄁o󠄁e󠄁s󠄁n󠄁'󠄁t󠄁 r󠄁e󠄁q󠄁u󠄁i󠄁r󠄁e󠄁 f󠄁i󠄁l󠄁e󠄁 e󠄁d󠄁i󠄁t󠄁s󠄁.󠄁

#󠄁#󠄁 Q󠄁u󠄁a󠄁l󠄁i󠄁t󠄁y󠄁 C󠄁o󠄁n󠄁t󠄁r󠄁o󠄁l󠄁s󠄁

T󠄁h󠄁e󠄁 r󠄁e󠄁p󠄁o󠄁s󠄁i󠄁t󠄁o󠄁r󠄁y󠄁 u󠄁s󠄁e󠄁s󠄁 p󠄁r󠄁e󠄁-󠄁c󠄁o󠄁m󠄁m󠄁i󠄁t󠄁 h󠄁o󠄁o󠄁k󠄁s󠄁 f󠄁o󠄁r󠄁:󠄁
-󠄁 T󠄁r󠄁a󠄁i󠄁l󠄁i󠄁n󠄁g󠄁 w󠄁h󠄁i󠄁t󠄁e󠄁s󠄁p󠄁a󠄁c󠄁e󠄁 a󠄁n󠄁d󠄁 E󠄁O󠄁F󠄁 f󠄁i󠄁x󠄁e󠄁s󠄁
-󠄁 S󠄁e󠄁c󠄁r󠄁e󠄁t󠄁 d󠄁e󠄁t󠄁e󠄁c󠄁t󠄁i󠄁o󠄁n󠄁 (󠄁T󠄁a󠄁l󠄁i󠄁s󠄁m󠄁a󠄁n󠄁)󠄁
-󠄁 S󠄁h󠄁e󠄁l󠄁l󠄁 s󠄁c󠄁r󠄁i󠄁p󠄁t󠄁 v󠄁a󠄁l󠄁i󠄁d󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 (󠄁s󠄁h󠄁e󠄁l󠄁l󠄁c󠄁h󠄁e󠄁c󠄁k󠄁)󠄁
-󠄁 S󠄁t󠄁a󠄁t󠄁e󠄁 v󠄁a󠄁l󠄁i󠄁d󠄁a󠄁t󠄁i󠄁o󠄁n󠄁

I󠄁n󠄁s󠄁t󠄁a󠄁l󠄁l󠄁 w󠄁i󠄁t󠄁h󠄁:󠄁 `󠄁p󠄁r󠄁e󠄁-󠄁c󠄁o󠄁m󠄁m󠄁i󠄁t󠄁 i󠄁n󠄁s󠄁t󠄁a󠄁l󠄁l󠄁`󠄁

## Files

#󠄁#󠄁#󠄁 P󠄁e󠄁r󠄁m󠄁a󠄁n󠄁e󠄁n󠄁t󠄁
-󠄁 `󠄁P󠄁R󠄁O󠄁M󠄁P󠄁T󠄁.󠄁m󠄁d󠄁`󠄁 -󠄁 B󠄁o󠄁o󠄁t󠄁s󠄁t󠄁r󠄁a󠄁p󠄁 i󠄁n󠄁s󠄁t󠄁r󠄁u󠄁c󠄁t󠄁i󠄁o󠄁n󠄁s󠄁 (󠄁s󠄁t󠄁a󠄁b󠄁l󠄁e󠄁,󠄁 r󠄁a󠄁r󠄁e󠄁l󠄁y󠄁 c󠄁h󠄁a󠄁n󠄁g󠄁e󠄁s󠄁)󠄁
-󠄁 `󠄁C󠄁L󠄁A󠄁U󠄁D󠄁E󠄁.󠄁m󠄁d󠄁`󠄁 -󠄁 T󠄁h󠄁i󠄁s󠄁 f󠄁i󠄁l󠄁e󠄁
- `.envrc` - direnv: puts `bin/` on PATH, loads gitignored `.env` overrides
-󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁z󠄁*󠄁`󠄁 -󠄁 E󠄁v󠄁e󠄁n󠄁t󠄁 s󠄁o󠄁u󠄁r󠄁c󠄁i󠄁n󠄁g󠄁 t󠄁o󠄁o󠄁l󠄁s󠄁
-󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁r󠄁e󠄁a󠄁d󠄁-󠄁l󠄁e󠄁a󠄁r󠄁n󠄁i󠄁n󠄁g󠄁s󠄁`󠄁,󠄁 `󠄁b󠄁i󠄁n󠄁/󠄁s󠄁a󠄁v󠄁e󠄁-󠄁l󠄁e󠄁a󠄁r󠄁n󠄁i󠄁n󠄁g󠄁`󠄁 -󠄁 L󠄁e󠄁a󠄁r󠄁n󠄁i󠄁n󠄁g󠄁 p󠄁e󠄁r󠄁s󠄁i󠄁s󠄁t󠄁e󠄁n󠄁c󠄁e󠄁
- `bin/nfprov*` - Provenance marking (vendored from delano/nerd-fonts)
- `site/fonts/` - P+ webfonts copied into `docs/fonts/` by `bin/zsite-generate`

#󠄁#󠄁#󠄁 P󠄁e󠄁r󠄁-󠄁c󠄁y󠄁c󠄁l󠄁e󠄁 (󠄁c󠄁l󠄁e󠄁a󠄁r󠄁e󠄁d󠄁 b󠄁y󠄁 z󠄁h󠄁e󠄁a󠄁p󠄁-󠄁d󠄁e󠄁a󠄁t󠄁h󠄁)󠄁
-󠄁 `󠄁s󠄁t󠄁u󠄁f󠄁f󠄁/󠄁`󠄁 -󠄁 T󠄁h󠄁i󠄁n󠄁g󠄁s󠄁 m󠄁a󠄁d󠄁e󠄁 t󠄁h󠄁i󠄁s󠄁 c󠄁y󠄁c󠄁l󠄁e󠄁

###󠄁 G󠄁i󠄁t󠄁-󠄁b󠄁a󠄁s󠄁e󠄁d󠄁 (󠄁p󠄁e󠄁r󠄁m󠄁a󠄁n󠄁e󠄁n󠄁t󠄁)󠄁
-󠄁 T󠄁a󠄁g󠄁s󠄁:󠄁 `󠄁r󠄁e󠄁v󠄁{󠄁N󠄁}󠄁-󠄁a󠄁t󠄁t󠄁e󠄁m󠄁p󠄁t󠄁{󠄁N󠄁}󠄁-󠄁i󠄁t󠄁e󠄁r󠄁a󠄁t󠄁i󠄁o󠄁n󠄁s󠄁{󠄁N󠄁}󠄁o󠄁f󠄁{󠄁N󠄁}󠄁`󠄁
-󠄁 B󠄁r󠄁a󠄁n󠄁c󠄁h󠄁e󠄁s󠄁:󠄁 `󠄁c󠄁y󠄁c󠄁l󠄁e󠄁/󠄁r󠄁e󠄁v󠄁{󠄁N󠄁}󠄁-󠄁a󠄁t󠄁t󠄁e󠄁m󠄁p󠄁t󠄁{N}`
-󠄁 O󠄁r󠄁p󠄁h󠄁a󠄁n󠄁 b󠄁r󠄁a󠄁n󠄁c󠄁h󠄁:󠄁 `󠄁l󠄁e󠄁a󠄁r󠄁n󠄁i󠄁n󠄁g󠄁s󠄁`󠄁

-󠄁-󠄁-󠄁

#󠄁#󠄁 H󠄁i󠄁s󠄁t󠄁o󠄁r󠄁i󠄁c󠄁a󠄁l󠄁 R󠄁e󠄁c󠄁o󠄁r󠄁d󠄁

*󠄁*󠄁I󠄁m󠄁m󠄁u󠄁t󠄁a󠄁b󠄁l󠄁e󠄁,󠄁 o󠄁b󠄁j󠄁e󠄁c󠄁t󠄁i󠄁v󠄁e󠄁 f󠄁a󠄁c󠄁t󠄁s󠄁 o󠄁n󠄁l󠄁y󠄁 b󠄁e󠄁l󠄁o󠄁w󠄁 t󠄁h󠄁i󠄁s󠄁 l󠄁i󠄁n󠄁e󠄁.󠄁*󠄁*󠄁

|󠄁 R󠄁e󠄁v󠄁 |󠄁 C󠄁h󠄁a󠄁n󠄁g󠄁e󠄁 |󠄁
|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁-󠄁|󠄁
|󠄁 r󠄁e󠄁v󠄁1󠄁-󠄁4󠄁9󠄁 |󠄁 F󠄁i󠄁l󠄁e󠄁-󠄁b󠄁a󠄁s󠄁e󠄁d󠄁 s󠄁t󠄁a󠄁t󠄁e󠄁.󠄁 M󠄁u󠄁t󠄁a󠄁b󠄁l󠄁e󠄁 `󠄁.󠄁z󠄁/󠄁`󠄁 d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁o󠄁r󠄁y󠄁 t󠄁r󠄁a󠄁c󠄁k󠄁e󠄁d󠄁 l󠄁o󠄁o󠄁p󠄁 s󠄁t󠄁a󠄁t󠄁e󠄁.󠄁 |󠄁
|󠄁 r󠄁e󠄁v󠄁5󠄁0󠄁 |󠄁 G󠄁i󠄁t󠄁-󠄁n󠄁a󠄁t󠄁i󠄁v󠄁e󠄁 e󠄁v󠄁e󠄁n󠄁t󠄁 s󠄁o󠄁u󠄁r󠄁c󠄁i󠄁n󠄁g󠄁.󠄁 S󠄁t󠄁a󠄁t󠄁e󠄁 d󠄁e󠄁r󠄁i󠄁v󠄁e󠄁d󠄁 f󠄁r󠄁o󠄁m󠄁 c󠄁o󠄁m󠄁m󠄁i󠄁t󠄁 h󠄁i󠄁s󠄁t󠄁o󠄁r󠄁y󠄁.󠄁 |󠄁
|󠄁 r󠄁e󠄁v󠄁6󠄁6󠄁 |󠄁 S󠄁t󠄁a󠄁b󠄁l󠄁e󠄁 P󠄁R󠄁O󠄁M󠄁P󠄁T󠄁.󠄁m󠄁d󠄁.󠄁 C󠄁o󠄁m󠄁m󠄁a󠄁n󠄁d󠄁s󠄁 d󠄁r󠄁i󠄁v󠄁e󠄁 t󠄁h󠄁e󠄁 l󠄁o󠄁o󠄁p󠄁,󠄁 n󠄁o󠄁t󠄁 t󠄁h󠄁e󠄁 p󠄁r󠄁o󠄁m󠄁p󠄁t󠄁.󠄁 R󠄁e󠄁m󠄁o󠄁v󠄁e󠄁d󠄁 `󠄁e󠄁v󠄁o󠄁l󠄁v󠄁e󠄁`󠄁 a󠄁c󠄁t󠄁i󠄁o󠄁n󠄁.󠄁 |󠄁
