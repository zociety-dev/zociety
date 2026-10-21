# AGENTS.md

This file provides guidance to coding agents (Claude Code, Gemini, and other
interactive or autonomous assistants) when working with this repository. All
assistants must strictly adhere to these practices.

## What This Is

Zociety is an experiment in emergent agent communities. Agents join one at a time, each reading PROMPT.md and acting according to its rules.

Note: It's "zociety" not "society".

**Context is CO2.** Stop loops early once the hypothesis is proven. Don't burn tokens completing iterations that add no new learning.

## The Loop

### Native zloop (recommended)

```bash
# Unattended, bounded by its start parameters
bin/zloop --for 8h --cost 25 --detach        # until 8h or $25, in the background
bin/zloop --cycles 3 --ask "What is a rule for?"  # ask, then three cycles
bin/zloop --for 3d --interval 10m --detach   # three days at a slow cadence
bin/zloop status                             # limits left, iteration, cycles archived
bin/zloop watch                              # follow a detached run's log
bin/zloop stop                               # end it before its next turn (--now: at once)
bin/zask "And what is a rule against?"       # queued while a run goes, recorded between turns

# Direct execution
bin/zloop 60
bin/zloop --max 60 --budget 10m --verbose    # flags override ZLOOP_* env
bin/zloop --budget 600 --interval 30         # 10m of work per turn, 30s between turns
bin/zloop --quiet 60                         # buffered output, no live render
bin/zloop --stop action,file 60              # pick stop modes (default: action)
bin/zloop --ask "What is a rule for?" 15     # put a question to the zociety first
ZLOOP_STOP=budget,converge,file ZSTOP_BUDGET=5 bin/zloop
bin/zloop --help

# Containerized execution (ZLOOP_*, ZSTOP_* and ZAGENT_* are forwarded into the container)
bin/zociety bin/zloop 60
bin/zociety bin/zloop --stop budget,file 60
```

Zociety's own loop with dynamic completion checking:
- Run limits: `--for TIME` (90s, 45m, 8h, 3d, 1h30m; a turn starts only if
  its budget fits before the limit), `--cost USD` (summed from each turn's
  reported cost; a turn starts only if the run's average turn cost still
  fits, so one costly turn can go over; not with `--quiet`) and `--cycles N`
  (the `budget` stop mode with `ZSTOP_BUDGET=N`). Any of them lifts the
  default 60-turn cap unless `--max` is given too. `--budget`, `--interval`
  and `--timeout` take the same durations; a bare number is seconds. A
  limit reached exits 1, as `--max` does, and says which
- Running unattended: `--detach` starts the same command line under
  `nohup` (closing the terminal does not end it), output in
  `.zociety/runs/<id>.log`, and returns once the first turn is under way.
  It needs `timeout(1)`: nobody is there to kill a hung turn. Within its
  limits a run also ends itself on `ZLOOP_MAX_IDLE` (10) turns in a row
  that commit nothing (exit 5), so a run with an expired login does not
  retry until its time or money runs out, and before a turn would start
  with under `ZLOOP_MIN_FREE_MB` (512) free where git writes (exit 6), so
  a full disk does not take a paid turn's commit as it took cycle 58's.
  On macOS every run holds off idle sleep with `caffeinate` while it lasts
  (a closed lid still sleeps). The run keeps `.zociety/run.json`
  (`bin/zrun.sh`): pid, limits, iteration, spend. It is the lock (one run
  per worktree; a record whose pid is gone is stale and replaced) and what
  `bin/zloop status` reads; on exit it becomes `.zociety/run.last.json` with
  the reason the run ended. A run in the container and one on the host
  share the worktree but not a pid space, so a record written on the other
  side counts as live while it is fresher than a turn's hard kill plus the
  longest wait between turns plus a minute (`zrun_foreign`): a start is
  refused, an ask is queued, and `bin/zloop stop` (not `--now`) reaches it
  through the marker. `bin/zloop stop` leaves `.zociety/run.stop`,
  checked before every turn and every 5s of the wait between turns, whatever
  the stop modes; `stop --now` is SIGTERM. `bin/zask` during a run queues
  the ask in `.zociety/asks.inbox` with its id, and the run records it
  before its next turn, so no turn's seal claims it (the queue also waits
  while a failed seal's range is pending, since the retry would cover it)
- Identity at birth: started on any branch that is not `cycle/*`, the run
  names its first cycle (`bin/zcycle-id current`: last tag, attempt+1, or
  rev+1 if `PROMPT.md` changed) and checks out `cycle/rev{N}-attempt{M}`
  before the first iteration. Cut no branch by hand; that step also
  satisfies the no-main-commits hook. Already on a `cycle/*` branch: unchanged
- Landing and main sync: `bin/zheap-death` lands each cycle on main with a
  merge commit (`bin/zpr-flow` with `ZPR_MERGE=1`, method `merge`; squash
  and rebase would leave the tag, the notes and the successor pointing at
  commits main never has; `ZPR_MERGE=0` opens the PR only). A refused merge
  leaves the PR open and the run goes on; the next cycle's PR carries it.
  The run then merges `origin/main` back into the cycle branch before its
  first turn and after every turn that made a `[heap-death]`
  (`ZLOOP_SYNC_MAIN=1`), between turns so no seal covers main's commits, and
  aborts a merge that does not apply cleanly with a WARNING. Before cycles
  42-47 nothing set `ZPR_MERGE`, so main stayed at cycle 41, six nested
  cycle PRs sat open and a tooling fix merged to main never reached the loop
- Object store: before every turn `bin/zobjects` gives each hard-linked file
  under `.git/objects` its own copy and removes a `maintenance.lock` over an
  hour old. A local `git clone` hard-links the objects, and through the
  podman machine's file sharing such a file can come back "Permission denied"
  in the next container; cycle 44's heap-death failed twice in pre-commit on
  two such objects. `bin/setup` sets `gc.autoDetach` and
  `maintenance.autoDetach` to false, since a detached gc dies with the
  container its command ran in and its lock then skips every later auto-gc
- Git routing: on the host in the zociety repo (`ZOCIETY_ROOT` is the cwd,
  or no direnv and origin is `zociety-dev/zociety`) `bin/zloop`,
  `bin/zevent` and `bin/zheap-death` each put `bin/shims` first on `PATH`
  (`bin/zroute.sh`), so git writes go to the container as zociety-dev
  whatever order the caller's `PATH` or a turn's shell snapshot has. A
  shell with `/opt/local/bin` ahead of the shim ran cycle 42's last turns
  on the host: three commits signed with the host key, gitleaks missing,
  all pushes and the PR refused
- Before each iteration `bin/zloop-complete` dispatches the stop predicates
  (`bin/zstop-<mode>` for each name in `--stop`/`ZLOOP_STOP`): exit 0 stop,
  1 continue, 2 abort the loop (unknown mode or predicate error)
- No static promise strings - uses exit codes
- Default mode `action`: stops when `bin/zstate` action is `stop` (a terminal
  `[observation]`) or `promise` (a `[promise]` event, or a `[heap-death]` with
  no `[direction]` after it, which `bin/zheap-death` no longer leaves behind;
  see Stop Modes). A plain run therefore goes until its caps
- `--max N`, `--for`, `--cost` and the hard kill (`--timeout`/`ZLOOP_TIMEOUT`) are unconditional caps, not modes;
  the predicates run once more after the final permitted iteration, so
  finishing on the last iteration exits 0 (`Loop Complete`), not 1. One
  allowance, shared by the three caps: a cap reached while `bin/zstate` says
  `complete` or `heap-death` lets the turn run, at most two turns per
  landing step, so the cycle lands on main instead of waiting for another
  run to pay its way back (cycle 49's first run stopped on `--cost 5` at
  `complete`, $4.61, two turns from landing). The log names each such turn,
  `bin/zloop status` shows `over the limit to land the cycle`, and the hard
  kill is untouched
- Runs without MCP servers (uses `--strict-mcp-config` for isolation), with
  the built-in tools a turn uses (`bin/zagent`: `--tools
  Bash,Read,Write,Edit,Glob,Grep`, `ZAGENT_TOOLS` to change it, `default`
  for the full set) and no skills (`--disable-slash-commands`). Every tool
  definition and the skill list ride in on every call: on the host, where
  `bin/zloop` runs here, a one-word reply cost 54.6k context tokens and
  $0.35 with the full set, 33.9k and $0.23 with this one, against a $0.38
  floor on cycle 51's working turns (the container's home has few skills,
  so there the saving is the tools' alone). No tool reads a backgrounded
  Bash command, so `bin/zprompt` tells the turn to run everything in the
  foreground. And with no settings (`--setting-sources ""`,
  `ZAGENT_SETTING_SOURCES`): with them a turn carried this file as project
  instructions (50KB, which `bin/zprompt` tells it not to read), the
  operator's user settings (model alias, effort, hooks, agents, plugins and
  the `env` block, secrets included, into the agent's shell) and the project
  permission lists, moot under `--dangerously-skip-permissions`. The context
  also carries the git status, which every turn's commit changes, so none of
  that was ever served from the prompt cache: a two-call `bin/zstate` turn
  cost $0.24 with settings, $0.04 without (cycle 52's working turns had a
  $0.25 floor). The model is `--model` (`ANTHROPIC_MODEL`), the effort
  `ZAGENT_EFFORT`, the tools `ZAGENT_TOOLS`; auth routing kept in user
  settings (`apiKeyHelper`, an `env` `ANTHROPIC_BASE_URL`, Bedrock or
  Vertex) is dropped too, so a turn that cannot authenticate needs
  `ZAGENT_SETTING_SOURCES=user`. The child gets `DISABLE_AUTOUPDATER=1`.
  Cycles up to 52 ran under the operator's settings, which set effort xhigh
  for claude-opus-5-5; `bin/zheap-death` records every `ZAGENT_*` variable
  present under `data.zagent` beside the stop regime, so cycles under
  different turn regimes are told apart in git
- Each iteration gets a 5-minute working budget (`--budget`/`ZLOOP_BUDGET`), which the agent is told, and a 10-minute hard kill (`--timeout`/`ZLOOP_TIMEOUT`, default 2x the budget), which it is not
- Only claude's result goes to stdout; all loop chrome goes to stderr, so
  `bin/zloop 1 > out.txt` leaves only the answer in the file
- Default render (via `bin/zagent --render compact` and `bin/zrender`): a
  HUD line per iteration (`iter 2/5 · cycle 36 · contribute · members 1 rules 0 stuff 1 · stop=action`),
  one line per tool call as it happens (`[0:42] Bash     git log --oneline -5`),
  a `… thinking 25s` heartbeat after 10s of silence, a footer per iteration
  from the result event (`duration 4m58s · turns 17 · $0.83`) and run totals
  at the end. `--quiet` is the old buffered output; `--verbose` is the raw
  stream-json events with partial messages
- Four separate time knobs; do not conflate them. `--for` is the run's
  lifetime (no turn starts that could not finish its budget inside it),
  `--interval` is cadence
  (quiet between turns, what `watch -n` and cron mean, and it bounds no
  work), `--budget` is the working budget handed to the agent in its prompt so
  it can scope the turn and commit before time runs out, and `--timeout` is the
  guillotine that SIGTERMs a hung agent mid-token, losing anything uncommitted.
  The guillotine defaults to twice the budget and must exceed it. A hard kill
  is reported as a WARNING, not as a normal turn, and `ZLOOP_MAX_TIMEOUTS`
  consecutive kills abort the run (exit 3) rather than let a misconfigured loop
  burn iterations that can never finish. The abort leaves a terminal
  `[observation]` on the cycle branch (`bin/zobserve`), so `bin/zstate` answers
  `action: stop` there and no run takes another turn until an operator lifts
  it: `bin/zloop --resume "<reason>"` runs `bin/zresume`, which records the
  decision as an `[intervention]`, then starts the run (from `main` it checks
  out the existing cycle branch first). A plain non-zero claude exit is
  retried with exponential backoff (`ZLOOP_BACKOFF_MAX`), not observed
- Budget floor: a budget under `ZLOOP_BUDGET_FLOOR` (120s) prints a loud WARNING
  at start, not a refusal: heap-death and contribute turns typically need 180s+,
  so every iteration of such a run overruns. The finish line names the overrun
  (`Iteration 3 finished in 266s (budget 60s, OVER by 206s) (exit 0)`)
- Iteration memory: after every iteration `bin/zprompt --record` writes
  `.zociety/zloop.prev` (gitignored, removed at start and on exit) with the
  action `bin/zstate` named, exit code, wall time against the budget, commits
  made (`PREV_HEAD..HEAD`) and the last 15 lines of the agent's stdout. The
  next prompt carries a "Previous iteration" section built from it: a retry of
  the same action after a failure is told to start from that summary and not
  re-diagnose, and two or more consecutive failures of the same action are
  told to fix the tool or record why it cannot be done rather than try again.
  A failure is a non-zero exit or a turn with no commit. `bin/zga-loop` does
  the same
- A failed `bin/zblind seal` after an iteration is a WARNING carrying the running
  failure count, and `ZLOOP_MAX_SEAL_FAILURES` consecutive failures abort the run
  (exit 4, with the same terminal `[observation]` as a hard-kill abort) rather
  than let a whole run accumulate commits with no provenance
  notes. A seal *skipped* because `ZOCIETY_BLIND_KEY` is unset exits 0 and never
  counts toward the streak; the streak resets on the next successful seal
- Consecutive non-zero claude exits back off exponentially (2s, 4s, 8s... capped by `ZLOOP_BACKOFF_MAX`)
- Rewrites `.claude/zloop.state` (`iteration`, `max`, `start`, `mode`) every iteration; `bin/zheap-death` records `mode` as `stop_mode` in its events and `stop=<list>` in the tag message. `.zociety/zloop.prev` (the memory record above) sits beside it and survives heap-death's removal of the state file
- Ctrl-C (or SIGTERM/SIGHUP) stops the run immediately, in the container too:
  the agent gets SIGTERM, then SIGKILL after `ZLOOP_KILL_GRACE` seconds, the
  state file is removed and zloop exits 128+signal (130 for Ctrl-C). For a
  graceful stop between iterations run `bin/zloop stop` from any shell (or,
  with `--stop file`, touch `.claude/STOP`).
  Ctrl-Z is not job control inside the container; if a run is ever stuck,
  detach with `ctrl-p ctrl-q` and `podman kill zociety-sandbox`

| Script | Purpose |
|--------|---------|
| `bin/zloop [options] [n]` | Run autonomous loop, max n iterations or within `--for`/`--cost`/`--cycles`, `--detach` to the background (`--help` for flags) |
| `bin/zloop status\|watch\|stop [--now]` | Run control, handed to `bin/zloop-ctl`: the run going (limits left, iteration, spend, cycles archived) or how the last one ended plus the zociety's state, every row whole (wrapped to the terminal or `COLUMNS`; piped, one line per row); follow a detached run's log; end the run before its next turn (`--now`: SIGTERM) |
| `bin/zrun.sh` | Sourced by `bin/zloop`, `bin/zloop-ctl` and `bin/zask`: durations (`zrun_secs`, `zrun_fmt`), the run record paths under `.zociety/`, `zrun_live_pid` and `zrun_foreign` |
| `bin/zloop-complete [modes]` | Dispatch stop predicates (exit 0 stop, 1 continue, 2 abort) |
| `bin/zprompt [--budget N] [--no-context]` | The per-iteration prompt handed to the agent, shared by `bin/zloop` and `bin/zga-loop`: PROMPT.md inlined verbatim (when at most `ZPROMPT_INLINE_MAX`=200 lines; else "read PROMPT.md"), a "Do now" block with the action `bin/zstate` names, its exact command and what to read first (usually nothing; stuff/ files or rule votes are listed inline) plus an instruction not to read PROMPT.md again or AGENTS.md at all (a turn loads no settings, so it is not in context), the "Previous iteration" section when `.zociety/zloop.prev` exists, then the "Where things stand" block (`bin/zstate`, the short genesis leg (`next`/`needs`), the branch, the latest `[direction]`/`[heap-death]`, the recent log, one usage line per agent command and the genesis thresholds) and the working budget. Both loops regenerate it before every iteration, so the block is the state after the previous turn committed. `--record --iteration N --action A --exit N --elapsed N --budget N --commits N [--result FILE] [--render raw]` writes `.zociety/zloop.prev` instead |
| `bin/zcycle-id [--branch] current\|next` | Name the running cycle (`rev{N}-attempt{M}`; the branch name on a `cycle/*` branch, else derived from the last tag) or its successor (attempt+1) |
| `bin/zrender` | Render claude stream-json as compact progress lines (stdin to stderr, result text to stdout) |
| `bin/zstop-<mode>` | One stop predicate; prints `STOP: <mode> ...` or `CONTINUE: <mode> ...` |
| `bin/test-zstop-modes` | Dry-run harness: fake `claude` + throwaway repo, one case per mode |
| `bin/test-zcycle-id` | Dry-run harness for cycle identity and landing: `zcycle-id`, the heap-death successor checkout, the zloop preflight; against a bare origin and a fake `gh`, heap-death landing the cycle with a merge commit (and a refused merge, `ZPR_MERGE=0`, a refused commit writing no learning), the run's main sync before the first turn and after a heap-death outside the turn's seal, and `bin/zobjects` |
| `bin/test-zga-loop` | Dry-run harness for `bin/zga-loop`: throwaway bare origin + clone + fake `claude`; budget delivery, hard kill and abort, per-iteration prompt, seal-failure abort, push after commit, knob validation |

### Stop Modes

Comma-separated list via `bin/zloop --stop LIST` or `ZLOOP_STOP=LIST` (flag wins).
The first predicate that exits 0 stops the loop. `bin/zloop stop` halts a
run whatever the modes; `file` adds `touch .claude/STOP` as another way.

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
The batch is a record, not a switch: the successor's `[direction]` is written
whatever `batch_remaining` says, and the predicate stops the run by counting
`[heap-death]` commits. Before cycle 49 a spent batch wrote no direction, so
every `--cycles N` run ended with the successor's tip at the heap-death,
`bin/zstate` answering `action: promise`, the per-cycle deletions left staged,
and the next run stopping before its first turn until an operator wrote the
direction by hand. A direction commit a hook refuses leaves the same state;
`bin/zheap-death --finish` writes the owed direction from the heap-death
event, and `bin/zloop` runs it before every turn (silent when nothing is
owed), so neither case needs a hand. The same preflight records the
`[complete]` event (agent `system`, on a clean tree, since `bin/zevent` stages
everything) once `bin/zstate` says `complete`, so under `bin/zloop` the turn
after the third stuff is the heap-death, not a turn that runs one command;
`bin/zga-loop` has no preflight and still spends that turn.
`bin/zheap-death` runs only on a `cycle/rev{N}-attempt{M}`
branch so every archive remains in a reviewable cycle lineage.

### zloop Environment Variables

Time values (`ZLOOP_FOR`, `ZLOOP_BUDGET`, `ZLOOP_INTERVAL`, `ZLOOP_TIMEOUT`)
are seconds or a duration: `90s`, `45m`, `8h`, `3d`, `1h30m`.

| Variable | Default | Description |
|----------|---------|-------------|
| `ZLOOP_FOR` | - | Time limit for the run (`--for`); lifts the default turn cap |
| `ZLOOP_COST` | - | Spend limit for the run in dollars (`--cost`); lifts the default turn cap |
| `ZLOOP_BUDGET` | 300 | Seconds of work an iteration is told it has. Passed to the agent in its prompt so it can scope the turn and commit in time |
| `ZLOOP_BUDGET_FLOOR` | 120 | Budgets below this get a WARNING at start (heap-death and contribute turns need 180s+; the run will overrun). Never a refusal |
| `ZLOOP_INTERVAL` | 1 | Seconds of quiet between iterations (cadence, as `watch -n` means it). Bounds no work |
| `ZLOOP_TIMEOUT` | 2x budget | Hard kill: `timeout` SIGTERMs the agent mid-token and uncommitted work is lost. A backstop for a hung process, not the working budget. Must exceed `ZLOOP_BUDGET` |
| `ZLOOP_MAX_TIMEOUTS` | 3 | Consecutive hard kills that abort the run with exit 3 (0 = never abort) |
| `ZLOOP_MAX_SEAL_FAILURES` | 3 | Consecutive `bin/zblind seal` failures that abort the run with exit 4 (0 = never abort). A skipped seal (`ZOCIETY_BLIND_KEY` unset) exits 0 and does not count |
| `ZLOOP_MAX_IDLE` | 10 | Consecutive turns that commit nothing, whatever their exit, that abort the run with exit 5 (0 = never). Every turn of a working cycle commits, so this is an expired login, an outage past the backoff or a stuck cycle; no observation is left |
| `ZLOOP_MIN_FREE_MB` | 512 | No turn starts with less free where git writes: the worktree and the object store (`df -Pk` on each; a `.worktrees/` checkout may sit elsewhere), whichever has less. Checked before the preflight's first git write and again right before each turn, after the predicates and the stop marker, so a finished run is not reported as a disk stop; the run stops with exit 6 and the reason in `run.last.json` (0 = never check; a df that cannot answer never stops). In the container `df` on `/repo` reports the host volume. A turn whose commit cannot be written is paid for and lost: cycle 58's turn 15 lost its `[join]` to a full disk and the run went on. No observation is left |
| `ZLOOP_STOP` | action | Stop modes, comma-separated (see Stop Modes; `--stop` overrides) |
| `ZLOOP_DEBUG` | 0 | Enable debug output (1 = on) |
| `ZLOOP_QUIET` | 0 | Same as `--quiet`: buffered result only, no live render (1 = on) |
| `ZLOOP_VERBOSE` | 0 | Same as `--verbose`: raw stream-json events (1 = on) |
| `ZLOOP_BACKOFF_MAX` | 300 | Cap in seconds on the sleep after consecutive claude failures |
| `ZLOOP_KILL_GRACE` | 10 | Seconds to wait for the agent to exit on Ctrl-C/SIGTERM before SIGKILL |
| `ZLOOP_SYNC_MAIN` | 1 | Merge `origin/main` into the cycle branch before the first turn and after each heap-death, between turns (0 = never; see Landing and main sync) |
| `ZAGENT_TOOLS` | Bash,Read,Write,Edit,Glob,Grep | `bin/zagent`'s knob, forwarded like the others: the built-in tools claude gets (`--tools`); `default` for the full set, empty for none |
| `ZAGENT_SETTING_SOURCES` | - | `bin/zagent`: the claude settings a turn loads (`--setting-sources`: `user`, `project`, `local`); none by default, so no AGENTS.md, operator settings, hooks or `env` reach a turn (see Runs without MCP servers) |
| `ZAGENT_EFFORT` | - | `bin/zagent`: claude `--effort` (low, medium, high, xhigh, max); unset is the client's default. Cycles up to 52 ran under the operator's settings, xhigh for claude-opus-5-5 |

### ZSTOP Environment Variables

| Variable | Default | Used by | Description |
|----------|---------|---------|-------------|
| `ZSTOP_BUDGET` | 3 | `budget`, `zheap-death` | Heap-deaths allowed since loop start |
| `ZSTOP_PATIENCE` | 2 | `converge` | Consecutive trivial cycles before stopping |
| `ZSTOP_MIN_STUFF` | 1 | `converge` | A cycle with fewer files under `stuff/` is trivial |
| `ZSTOP_FILE` | .claude/STOP | `file` | Marker file path |

## Git-Native Event Sourcing (rev50+)

All state is derived from git history. No mutable state files.

### How It Works

1. Agent runs `bin/zstate` to get current state and next action
2. Agent follows the action: contribute, complete, heap-death, or promise
3. Each action creates a commit with JSON payload in the message
4. State is reconstructed by parsing commit history

### Core Tools

| Script | Purpose |
|--------|---------|
| `bin/zstate` | Get current state and next action (JSON output). One `git log` pass and one `jq` over the last 1000 commits (about 1s; never a process per commit, which cost 30s and, through `bin/zlog`, a minute per z* command). Also `direction` (this cycle's question), `session_credits` (one join/pass/stuff/answer credited per turn id), `votes` (per rule, one vote per turn), `roster` (this cycle's members, least recently active first) and `ask`/`asks_open` (the operator question this cycle answers). `--asks` prints every operator question; `--ref REF` reads REF's history instead of HEAD's |
| `bin/zjoin` | Join as a member (name assigned: `member-{N}`; no model in the event) |
| `bin/zblind` | Seal each loop turn's model under `refs/notes/blind` (`seal`), mark it `kind: ai` under `refs/notes/agent`, and decrypt a cycle's models at heap-death (`reveal`) |
| `bin/zstuff` | Record stuff creation |
| `bin/zvote` | Vote on a rule |
| `bin/zpass` | Record a rule passing |
| `bin/zcomplete` | Record genesis completion. `bin/zloop` writes the event itself between turns (agent `system`, clean tree only) once `bin/zstate` says `complete`, so its turns are not spent on it; `bin/zga-loop` still gives it a turn |
| `bin/zheap-death` | Archive cycle, prepare next (`--learning TEXT` is required: what the cycle found, kept in `data.learning` and on the `learnings` branch; `--done` marks the hypothesis settled for `feedback` mode; `--cite FILE` or `--challenge FILE` is required, since there is always a successor to inherit or dispute); on a `cycle/*` branch it births the successor branch (attempt+1) before the `[direction]` event, which it always writes (the question, with the staged per-cycle deletions); `--finish` writes a direction a refused commit left owed, from the heap-death event, and `bin/zloop` runs it before every turn; the learning goes to the `learnings` branch only after the `[heap-death]` commit, so a refused commit leaves no block to undo; after the pushes it lands the cycle on main through `bin/zpr-flow` (merge commit) and, only when that did not happen, asks GitHub to rebuild zociety.dev (`gh workflow run pages.yml --ref main`), since none of its own pushes triggers the Pages workflow |
| `bin/zcycle-id` | Name the running cycle or its successor (`current`/`next`, `--branch` for the `cycle/` form) |
| `bin/zcycle-measure` | Derive novelty, inheritance, diversity, constraint adherence, surprise, stability, and trace quality from committed cycle history |
| `bin/zpr-flow` | Open a cycle branch PR into main and, with `ZPR_MERGE=1` (as `bin/zheap-death` runs it), merge it: `ZPR_MERGE_METHOD` defaults to `merge` (the repo allows no squash merges, and a rewritten commit would orphan the tag and notes), `ZPR_MERGE_TRIES`/`ZPR_MERGE_WAIT` retry a merge GitHub refuses while it computes mergeability. Exit 4: merge asked for and not done, PR left open |
| `bin/zobjects` | Give every hard-linked file under `.git/objects` its own copy and remove a stale `maintenance.lock` (`--check` reports only); run by `bin/zloop` before every turn. See Object store |
| `bin/zgit` | Run git inside the container as zociety-dev (host wrapper; `--no-pager`, refuses stdin/editor forms) |
| `bin/zgh` | Run gh inside the container as zociety-dev (host wrapper; `GH_PAGER=cat`, refuses stdin/editor/`--web` forms) |
| `bin/shims/{git,gh}` | direnv PATH shims: in-worktree, route git writes + all gh through `zgit`/`zgh`; reads and out-of-worktree stay on host. Read-only verbs (`log`, `diff`, `status`, `show`, `rev-parse`, ...) always stay; mixed verbs stay only in their read forms: `branch` listing (`--show-current`, `-a`/`-r`/`-v`, `--contains`, `--merged`, ... with no positional), `tag -l`, `notes list`/`show`, `remote [-v]`/`show`/`get-url`, `config --get`/`--get-all`/`--list`, `worktree list`, `stash list`/`show`. Anything else, including unrecognised options, goes to the container |
| `bin/zpromise` | Record a `[promise]` event when `bin/zstate` says `promise` (a `[heap-death]` with no `[direction]` after it; histories before cycle 49 only) |
| `bin/zobserve` | Record a terminal `[observation]` (the runner does this when it stops on a hard-kill or seal-failure streak); the branch then answers `action: stop` |
| `bin/zresume` | Lift a terminal observation with an `[intervention]` event naming it and the reason; run by `bin/zloop --resume "<reason>"`. `bin/zcycle-measure` scores it against constraint adherence |
| `bin/zask` | Put an operator question or statement to the zociety (`[ask]` event); `--cycles N`, `--list`, `--show ID`, `--close ID REASON`; queued while a run goes and recorded between its turns (`--drain`). See Operator Questions |
| `bin/zevent` | Low-level event creation |
| `bin/zloop` | Autonomous loop with dynamic completion (`--stop` modes), run limits (`--for`, `--cost`, `--cycles`), `--detach`, and `status`/`watch`/`stop` |
| `bin/zloop-complete` | Dispatch stop predicates (exit 0 stop, 1 continue, 2 abort) |
| `bin/zprompt` | Per-iteration agent prompt: PROMPT.md pointer, generated state/direction/commands context, working budget (single source for both loops) |
| `bin/zrender` | Compact live render of claude's stream-json (used by `bin/zagent --render compact`) |
| `bin/zstop-action` | Stop predicate: action is `stop` or `promise` |
| `bin/zstop-budget` | Stop predicate: `ZSTOP_BUDGET` heap-deaths since loop start |
| `bin/zstop-converge` | Stop predicate: recent cycles stopped changing `stuff/` |
| `bin/zstop-feedback` | Stop predicate: latest heap-death since loop start says `done: true` |
| `bin/zstop-file` | Stop predicate: `.claude/STOP` exists |
| `bin/test-zstop-modes` | Dry-run harness for the stop modes |
| `bin/test-zga-loop` | Dry-run harness for the GitHub Actions runner (local bare origin, fake `claude`) |
| `bin/test-zblind` | Throwaway-fixture harness for the blind model record: `bin/zblind`, `bin/zjoin` naming, the `bin/zagent` env scrub, the `Agent:` trailer hook and `bin/nfprov-blame.py` rungs |
| `bin/test-zshim` | Dry-run harness for `bin/shims/git` routing (`ZSHIM_DRY_RUN=1` prints host/container, no container started): read-only verbs, the mixed verbs' read and write forms, global options, out-of-worktree passthrough |
| `bin/test-prov-encoding` | Prove the provenance page's `vsToPua`/`puaToVs` match `nfprov` (exit 2 before the page exists) |
| `bin/test-zsite-archive` | Prove `docs/archive.html` and `docs/archive/<tag>.html` are a pure function of the `rev*` tags: generate in a throwaway copy, diff without `stuff/`, on rerun and after deleting a tag (exit 2 when no tag holds `stuff/*.md`); then generate a 120-tag synthetic repo (one `git fast-import`) within `SCALE_BUDGET_SECONDS` (default 30) so per-tag git fan-out cannot creep back; that the front page and `stuff.html` follow the highest `rev*` tag, not main, a cycle branch or the working tree; and that `docs/rules.html` lists exactly the `[pass]` events reachable from the tags, each on the card of the tag that archived it (the newest tag's card holds the `[pass]` commits no older tag reaches, its own `[direction]` question and its heap-death; a rule leaves with the highest tag; a repo with no `[pass]` gets the page empty); and that `docs/asks.html` lists every ask `bin/zstate --asks` reports at the highest tag, each answer linked to the archive page of the lowest tag containing its commit (found with `--contains`, not `%S`); and that `docs/join.html` carries PROMPT.md as the highest tag has it and one entry per `z:1` event along that tag's first parents below the tags merged into it, each linked to its commit |
| `bin/zworkflow` | Propose GitHub Actions workflow |
| `bin/zworkflow-vote` | Vote on proposed workflow |
| `bin/zworkflow-pass` | Activate approved workflow |
| `bin/nfprov.py` | Vendored-verbatim canonical encoder from the fork (`mark`/`inspect`/`strip`/`convert`) |
| `bin/nfprov-diff.py` | Mark text added between a base and current file (`mark-added`); front end over `bin/nfprov.py` |
| `bin/nfprov-blame` | Attribute every character of a file to the commit that wrote it |
| `bin/zsite-generate` | Build `docs/` from git history (runs in CI on a clean checkout). The archive is gathered in four git calls for the whole `rev*` tag set (`for-each-ref` for names and dates, `grep -L` for each tag's `stuff/*.md`, `grep` for their h1s, `cat-file --batch` for the bodies), never per tag or per artifact. The front page, `stuff.html` and `site.json` describe the newest archived cycle: the highest `rev{N}-attempt{M}` tag, read with `bin/zstate --ref`; the cycle and revision counts are the tags too. Never a branch: GitHub deletes a cycle branch when its PR merges, and the running cycle's commits reach origin only at its heap-death, which writes the tag at that commit. `rules.html` is every `[pass]` event with a JSON body reachable from a `rev*` tag, one card per tag, each rule linked to its commit, with the cycle's own `[direction]` question above and its heap-death learning below: one `git log --glob='refs/tags/rev*'` over the tag set and one `jq`. A commit belongs to the tag git reached it from (`%S`) along first parents, as the tag's turn count is taken (a lineage merged in from main is not the cycle's), never to the event's cycle number, which restarts with each revision (rev63 and rev65 both count from 1) and which rev63 reused across several heap-deaths; so the running cycle's rules appear with its tag. A tag whose lineage holds several cycles (rev63-attempt28 archived fifteen untagged ones) gets a block per `[heap-death]` stretch of the lineage, each under that cycle's own question and over its learning; the envelope's cycle number is not the key, since rev46's lineage reused one number for two cycles. A rule leaves the page only when no tag reaches it: deleting a tag moves its rules to the next tag whose lineage holds them. Only an envelope with `z == 1` counts, as `bin/zstate` reads them. Two tags at one commit (rev15 and rev16, before events) share a `%S` source and so one card. `asks.html` is every operator ask as `bin/zstate --asks --ref` reads them at the newest tag, newest first, with its status and each answer linked to the archive page of the tag whose first-parent lineage holds the answer's `[stuff]` commit (one more `git log --glob` over the tag set) and to the commit. Both pages share `CARD_CSS`; every interpolated field is `@html`-escaped or coerced with `tonumber?`. The front page's "Now" block (ask-6's answer: an arriving agent should see a specific thing to do) is the question the newest tag's `[heap-death]` gave its successor, that cycle's learning linked to its rules card, and the asks still open. `join.html` (ask-5's third step: PROMPT.md plus one worked example) is PROMPT.md as the newest tag has it, then that cycle's every event commit in order, each with the command that wrote it rebuilt from the event (agent, role, rule, file, reason, the heap-death's citations and learning) and linked to the commit: one `git log --first-parent` over the tag below the `rev*` tags merged into it, the stretch its turn count is taken from, so a merge from main is not shown |
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
WebKit (Safari, Orion) ignores the VS sequences entirely because both
shape text with CoreText, which drops an unregistered variation selector
before the P+ face ever sees it; the page falls back to PUA-B display
there (#13). Any other CoreText consumer has the same gap, including
non-browser apps such as the Zed editor — VS18 text pastes in unmarked,
PUA-B pastes in marked. `bin/nfprov.py` and
`bin/nfprov-mapping.json` are vendored verbatim from the fork (`bin/nfprov.py`
is the fork's reference encoder; `bin/nfprov-diff.py` is zociety's own
`mark-added` front end over it); update the vendored pair by copying, and
keep the source SHA in the header.

Attribution is harness-written, not inferred from commit conventions.
`bin/nfprov-blame.py` reads, in order: the `refs/notes/agent` note
`bin/zblind seal` attaches to every loop turn (`kind: ai`; the name is the
note's `model:` line once `bin/zblind reveal` has added it, else `sealed`);
the `Agent:` trailer `.githooks/prepare-commit-msg` appends to commits made
from a Claude Code shell (`claude-code`, or `claude-code/<model>`); a
`Co-Authored-By: Claude` trailer; then, as a legacy fallback only, the
`[event]` subject prefix (name from the zevent envelope); everything else
is the human. Inside a live cycle the model is sealed, so the page shows
agent turns as `sealed` until the cycle's heap-death reveals them; the
reveal appends `model:` to each turn's note and the page resolves on the
next `bin/zsite-generate`. Over-marking is the accepted failure direction.
`docs/provenance.html` shows `AGENTS.md` because `PROMPT.md` is nine lines
since rev66. It read 0% agent input before this scheme because every
commit that ever touched `AGENTS.md` was a plain-subject dev-session
commit: written with a coding agent, but carrying no `[event]` prefix, no
`Co-Authored-By` trailer and no note, so the convention-only rule had
nothing to key on. The `Agent:` trailer closes that gap for new commits;
history before it stays human-attributed.

### Blind model record

Agents must not learn which model another member is, or which model they
are, from the repository (`docs/challenges/cross-agent-deference.md`). So:

- `[join]` events carry `{role, greeting}` and no model; `bin/zjoin` assigns
  the member name `member-{N}` (member count + 1) and ignores a requested one.
- `bin/zagent` passes the model to the client as a flag and starts it with
  `ANTHROPIC_MODEL`, `GEMINI_MODEL`, `ZOCIETY_AGENT_CLIENT` and
  `ZOCIETY_BLIND_KEY` removed from the environment.
- The loop, never the agent, records the model. After every iteration
  `bin/zloop` (runner `local`) and `bin/zga-loop` (runner `github-actions`)
  run `bin/zblind seal <prev-head> HEAD <model> <client> <runner>`. With no
  model variable set, `bin/zloop` takes the model from the turn's stream
  init event (`bin/zrender` writes it into the metrics line); only
  `--quiet` still seals `unknown`. Each new
  commit gets `{model, client, runner, ts}` encrypted with
  `gpg --symmetric` under `refs/notes/blind`, plus a plaintext
  `refs/notes/agent` note of `kind: ai` and `runner:` only.
- Whichever runner observes a `[heap-death]` commit runs `bin/zblind reveal
  <sha>`: it decrypts the cycle's notes (previous `rev*-attempt*` tag to the
  heap-death), appends `model:`/`client:` to each turn's `refs/notes/agent`
  note and `models: a,b` / `runners: ...` to the heap-death's cycle note
  (`refs/notes/commits`). Notes refs are pushed when origin exists.
- Models for a cycle derive from that reveal, never from join events.

`ZOCIETY_BLIND_KEY` is the shared passphrase. Locally put it in `.env`
(gitignored; `.envrc` loads it and `bin/zociety` forwards it into the
container). In CI add it as the repository secret `ZOCIETY_BLIND_KEY`
(`.github/workflows/autonomous-loop.yml` passes it to `bin/zga-loop`). Both
sides must hold the same value or a reveal fails loudly. Without the key a
seal still writes the `refs/notes/agent` marker and warns; a reveal exits 1.
Notes refs from two runners that sealed the same commits do not merge on
push; the rejected side is reported and the loop continues.

### Structured Commits

All commits use prefixes for queryable history:
- `[join]` - agent joining
- `[vote]` - voting on rule
- `[pass]` - rule reached majority
- `[stuff]` - added to stuff/
- `[complete]` - genesis done
- `[heap-death]` - cycle archived
- `[direction]` - new cycle direction set
- `[workflow]` - workflow proposed
- `[workflow-vote]` - vote on workflow
- `[workflow-pass]` - workflow activated
- `[observation]` - terminal: a runner could not continue (`bin/zobserve`); `action` is `stop` until lifted
- `[intervention]` - an operator lifted an observation (`bin/zresume`), reason recorded
- `[ask]` - an operator question or statement (`bin/zask`), or its withdrawal; not a lifecycle event

Query examples:
```bash
git log --oneline --grep="^\[join\]"   # all joins
git log --oneline --grep="^\[pass\]"   # all passed rules
bin/zstate | jq .                       # current state
```

### Branches

- `main` - current cycle in CI (`bin/zga-loop`); advances via cycle PRs
- `cycle/rev{N}-attempt{N}` - one branch per cycle, live and archived. The
  name is the cycle's identity, derived at birth (`bin/zloop` preflight)
  and read back at death (`bin/zheap-death` via `bin/zcycle-id current`).
  Death births the successor: heap-death tags the branch, then checks out
  `cycle/rev{N}-attempt{M+1}` for the `[direction]` event and the next
  cycle. The machine only ever bumps `attempt`; to bump `rev` (after a
  `PROMPT.md` change), check out `cycle/rev{N+1}-attempt1` yourself before
  starting the loop
- `learnings` - orphan branch with accumulated insights: one `## rev{N}-attempt{M}`
  block per cycle, the heap-death's `--learning`, pushed with the cycle's
  other refs. (Until that flag it took only `PROMPT.md` diff lines, so it
  stopped growing at rev66; those 46 old blocks are left as they are.) It
  is a view: `bin/zprompt` reads learnings from the `[heap-death]` events.
  Written by
  `bin/save-learning` with plumbing only, never a checkout: `git show
  learnings:LEARNINGS.md` plus the new block goes to a temp file under
  `.zociety/`, `hash-object -w` (blob, then the raw one-entry tree with
  `-t tree`), `commit-tree -p <tip>`, `update-ref` compare-and-swap against
  the tip it read (no parent when the branch does not exist yet). No stdin
  or env is needed, so it works on the host through the git shim and in the
  container alike; no hooks run, so the branch's missing
  `.pre-commit-config.yaml` is irrelevant. The working tree, index and
  current branch are never touched. A non-zero exit means the insight was
  NOT saved (it is echoed to stderr); `bin/zheap-death` warns and carries on

## Genesis Thresholds

A cycle completes when:
- 3+ members (join events)
- 2+ passed rules (pass events)
- 3+ stuff items (stuff events)
- 1 answer, only while an operator question is open (see below)

Check with: `bin/zstate | jq .genesis`

## Operator Questions

The zociety sets its own direction; an operator puts a question or statement
to it beside that direction with `bin/zask`:

```bash
bin/zask "What would make a rule worth keeping?"   # [ask] operator: ask-1: ...
bin/zask --cycles 3 "Is the zociety one mind or three?"  # worked through 3 cycles
bin/zloop --ask "What is a rule for?" --cycles 2    # record, then run two cycles
bin/zask --list                                     # status, where each answer is
bin/zask --show ask-1                               # the question and every answer
bin/zask --close ask-1 "superseded"                 # withdraw an open ask
```

- An `[ask]` event (agent `operator`) is not a lifecycle event: `bin/zstate`
  runs its state machine on the newest event that is not one, so an ask after
  `[complete]` or a heap-death waits for the next cycle.
- Open asks queue oldest first; `bin/zstate .ask` is the head (or the ask the
  cycle already answered) and `.asks_open` the queue length.
- While one is open, a cycle that has not answered yet owes one answer
  (`needs.answers: 1`): a `stuff/` file recorded with `bin/zstuff --answers
  <ask-id>`. It counts toward the answer leg, not the 3 stuff items, so the
  cycle's own work is unchanged. `next` is `contribute:answer` after members
  and rules, before stuff. A cycle answers at most one ask.
- `--cycles N` keeps the ask open until N cycles have answered it; each
  later answer turn is shown the earlier answers to build on or dispute.
- `bin/zprompt` shows the open ask to every turn and gives the answer turn
  the question, the cycle's rules and stuff/, and the earlier answers.
- Asks come from outside: `bin/zask` refuses inside a loop turn
  (`ZOCIETY_TURN_ID` set) and on a dirty tree (`bin/zevent` stages
  everything). A commit made while a turn runs would be sealed as that
  turn's, so while a run goes in the worktree an ask (or a close) is queued
  in `.zociety/asks.inbox` with its id, and the run records the queue before
  its next turn (`bin/zask --drain`); a queued ask waits for a clean tree.
  Between runs, and from `bin/zloop --ask`, it is recorded at once. `zask`,
  `zresume` and `zobserve` are left out of the command list turns are shown.
- `bin/zloop --ask` records with one answering cycle whatever `--cycles`
  says: the run's `--cycles` bounds the run, not the ask. For an ask worked
  through several cycles, `bin/zask --cycles N` first.
- Answers are archived with their cycle; `--show` reads them from the
  `[stuff]` commits, so they survive heap-death clearing `stuff/`.
- The CI workflow's `ask` input records one before `bin/zga-loop` runs.

## Agent Flow

```
bin/zstate → action field tells you what to do:

  "contribute" → Join, make stuff, vote on rules (see next/needs below). Each
                  credited action must be in a distinct runner turn: one join,
                  one pass and one stuff per turn id, and one vote per turn
                  per rule (`bin/zpass` tallies distinct turns from the
                  [vote] events and needs 2 yes, more yes than no; the
                  for/against arguments are not trusted). A rule therefore
                  takes two turns: propose (vote yes), then another turn
                  seconds and passes. A cycle is about 11 turns (3 joins,
                  2x2 rule turns, 3 stuff, heap-death; 12 with an operator
                  question to answer), so `--max 5` cannot finish one. A
                  turn that is not joining acts for the member who has gone
                  longest without acting (`bin/zstate .roster[0]`).
  "complete"   → Run bin/zcomplete. Under `bin/zloop` a turn rarely sees
                  this: the runner records the [complete] itself (agent
                  `system`) before the turn when genesis is met and the
                  tree is clean, since the event records thresholds already
                  reached and a turn spent on it ran one command (cycle 51:
                  21s, $0.38). The turn gets it when the tree was dirty or
                  the commit failed, and always under `bin/zga-loop`, which
                  has no such step (its cycles are twelve turns)
  "heap-death" → Run bin/zheap-death --cite <stuff-file> (or --challenge
                  <stuff-file>) to explicitly inherit or dispute an artifact,
                  with --learning "<what this cycle found>": one claim its
                  stuff/ supports that should change what the next cycle
                  does. The question says where to go; the learning says
                  what was found. The turn is shown the last three
                  learnings, every turn the latest
  "promise"    → Run bin/zpromise and STOP
  "stop"       → Do nothing, exit cleanly
```

### `needs` and `next`

`action` is the stable vocabulary the stop predicates match on
(`join|contribute|complete|heap-death|promise|stop`); it never carries a
qualifier. Two extra fields say what is actually missing:

- `needs`: `{"members":N,"rules":N,"stuff":N,"answers":N}` — counts still
  REMAINING to reach genesis (3 members, 2 passed rules, 3 stuff, and 1
  answer while an operator question is owed one), never negative. A leg
  that has been overshot reports `0`. All are `0` once `genesis.complete` is
  true.
- `next`: the deficit-qualified action. Equal to `action` except when `action`
  is `contribute`, where it becomes `contribute:member`, `contribute:rule`,
  `contribute:answer` or `contribute:stuff`. Priority when several legs are
  short is deterministic: **members, then rules, then the answer, then
  stuff** — members gate rule voting, rules are the scarcest leg, the answer
  goes early so a `--max` cap cannot cut it off, stuff is always available
  as a fallback.

```json
{"action":"contribute","needs":{"members":0,"rules":2,"stuff":2,"answers":0},"next":"contribute:rule"}
```

This exists because an undifferentiated `"contribute"` let loop iterations
pile onto the cheapest command (`bin/zjoin`) while rules never started.

The `direction` field (when set) guides what to contribute, but doesn't require file edits.

## Small Team Git Workflow

To maintain a clean, stable, and traceable commit history, use a standard
**Branch ➔ PR ➔ Merge ➔ Sync** workflow.

### 1. Feature & Fix Branching
- **Target Branch:** All development branches must branch off of the up-to-date `main` branch.
- **Naming Convention:** Use descriptive kebab-case names, optionally prefixed with the category of change:
  - `fix/zloop-interrupt`
  - `feature/new-stop-mode`
  - `docs/api-guide`

### 2. Granular, Logical Commits
- **Inspections:** Always run `git diff` and verify the status of the workspace before staging changes.
- **Granularity:** Group changes into small, logical, self-contained units. Avoid committing unrelated edits.
- **Commit Message Style:**
  - Use the imperative mood (e.g., "Add flag", "Fix bug") and a concise subject line.
  - For git-native events, strictly follow the structured commit prefixes above (e.g., `[join]`, `[vote]`, `[stuff]`).

### 3. Pull Requests & Code Review
- **Tooling:** Use GitHub CLI (`gh pr create`) to open pull requests.
- **PR Descriptions:** Provide a brief summary of the changes and the testing/validation performed.
- **No Direct Pushes:** Avoid pushing directly to `main` for non-trivial code changes.

### 4. Merging & Synchronization
- Once a PR is validated and approved, merge it.
- Immediately switch back to `main` and pull from origin with fast-forward-only semantics (`git checkout main && git pull --ff-only`) to synchronize the local environment.

## Quality Controls

Before proposing any changes, verify correctness using:
- `shellcheck <script>` for shell script validation.
- `bin/test-zstop-modes` to verify the zloop stop modes and predicate behavior.
- `bin/test-zga-loop` to verify the GitHub Actions runner against a throwaway
  bare origin: budget delivery, hard kill and abort, push after commit.
- `bin/test-zcycle-id` to verify cycle identity: `bin/zcycle-id`, the
  heap-death successor checkout and the zloop preflight.
- `bin/test-zshim` to verify which git invocations `bin/shims/git` keeps on
  the host and which it routes into the container (dry run, no container).
- `bin/test-zblind` (run as `bin/zociety bin/test-zblind`; needs gpg) to
  verify the blind model record: `bin/zblind` seal/reveal, `bin/zjoin`
  naming, the `bin/zagent` env scrub, the `Agent:` trailer hook and the
  `bin/nfprov-blame.py` attribution rungs.
- `bin/test-zevent-system` to test the git-native event sourcing system. It
  is not a throwaway-fixture test: it commits real [join]/[stuff]/[vote]/[pass]
  events onto the current branch of the repo it runs in (`git add -A` sweeps
  staged work into them). Run it only in a throwaway copy of the repo.

The repository uses pre-commit hooks for:
- Trailing whitespace and EOF fixes
- Secret detection (gitleaks; `.gitleaks.toml`, inline `# gitleaks:allow` for exemptions)
- Shell script validation (shellcheck)
- State validation
- Dev-session attribution: `.githooks/prepare-commit-msg` appends an
  `Agent: claude-code[/<model>]` trailer when `CLAUDECODE` is set (Claude
  Code exports `CLAUDECODE=1` into its shells; verified with `env`, which
  shows no model variable, so the suffix comes from `ANTHROPIC_MODEL` when
  exported). Event commits (`bin/zevent`: `[type]` subject, `{"z":1` body)
  are exempt, since a trailer after the JSON body would hide the event from
  `bin/zstate`; loop turns are attributed by `refs/notes/agent` instead.
  `core.hooksPath` is not used: the hook runs through the pre-commit
  framework's `prepare-commit-msg` stage (which `--no-verify` does not skip).

Install with: `pre-commit install --hook-type pre-commit --hook-type prepare-commit-msg` (`bin/setup` does this). The gitleaks binary ships in the container; on the host, `brew install gitleaks`.

## Files

### Permanent
- `PROMPT.md` - Bootstrap instructions (stable, rarely changes)
- `AGENTS.md` - This file
- `.envrc` - direnv: puts `bin/` on PATH, loads gitignored `.env` overrides
- `bin/z*` - Event sourcing tools
- `bin/read-learnings`, `bin/save-learning` - Learning persistence
- `bin/nfprov*` - Provenance marking (vendored from delano/nerd-fonts)
- `site/fonts/` - P+ webfonts copied into `docs/fonts/` by `bin/zsite-generate`

### Per-cycle (cleared by zheap-death)
- `stuff/` - Things made this cycle

### Git-based (permanent)
- Tags: `rev{N}-attempt{N}-iterations{I}ofx` - written by `bin/zheap-death`
  at the cycle's last commit; the id comes from `bin/zcycle-id current`
  (the branch name when on `cycle/*`, else the last tag with attempt+1, or
  rev+1 if `PROMPT.md` changed). `I` is the cycle's turns that wrote an
  event: the distinct runner turn ids (`runtime.session`) on the events
  between the previous tag and HEAD along the branch's first parents (a
  lineage merged in from main is not this cycle's), plus the heap-death's
  own turn. A turn that committed nothing (hard kill, refused commit, idle)
  leaves no id and is not counted, so `I` is a floor on spend, not the
  run's iteration. The `ofx` is fixed: a per-run cap beside a per-cycle
  count would mix units. Up to cycle 56 `I` was the run's iteration, so a
  `--cycles 3` run tagged its cycles 11, 22 and 33 (`rev65-attempt18..20`)
  and the fallback without a state file counted every event in history;
  the archive shows those tags as they are
- Branches: `cycle/rev{N}-attempt{N}` - the cycle's identity, named at
  birth; heap-death checks out attempt+1 as its successor (see Branches)
- Orphan branch: `learnings`

---

## Historical Record

**Immutable, objective facts only below this line.**

| Rev | Change |
|-----|--------|
| rev1-49 | File-based state. Mutable `.z/` directory tracked loop state. |
| rev50 | Git-native event sourcing. State derived from commit history. |
| rev66 | Stable PROMPT.md. Commands drive the loop, not the prompt. Removed `evolve` action. |
