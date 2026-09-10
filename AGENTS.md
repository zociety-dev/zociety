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
# Direct execution
bin/zloop 60
bin/zloop --max 60 --timeout 600 --verbose   # flags override ZLOOP_* env
bin/zloop --quiet 60                         # buffered output, no live render
bin/zloop --stop action,file 60              # pick stop modes (default: action)
ZLOOP_STOP=budget,converge,file ZSTOP_BUDGET=5 bin/zloop
bin/zloop --help

# Containerized execution (ZLOOP_* and ZSTOP_* are forwarded into the container)
bin/zociety bin/zloop 60
bin/zociety bin/zloop --stop budget,file 60
```

Zociety's own loop with dynamic completion checking:
- Before each iteration `bin/zloop-complete` dispatches the stop predicates
  (`bin/zstop-<mode>` for each name in `--stop`/`ZLOOP_STOP`): exit 0 stop,
  1 continue, 2 abort the loop (unknown mode or predicate error)
- No static promise strings - uses exit codes
- Default mode `action`: stops when `bin/zstate` action is `stop` or `promise`
- `--max N` and `ZLOOP_TIMEOUT` are unconditional safety caps, not modes;
  the predicates run once more after the final permitted iteration, so
  finishing on the last iteration exits 0 (`Loop Complete`), not 1
- Runs without MCP servers (uses `--strict-mcp-config` for isolation)
- Each iteration has a 5-minute timeout (configurable via `ZLOOP_TIMEOUT`)
- Only claude's result goes to stdout; all loop chrome goes to stderr, so
  `bin/zloop 1 > out.txt` leaves only the answer in the file
- Default render (via `bin/zagent --render compact` and `bin/zrender`): a
  HUD line per iteration (`iter 2/5 · cycle 36 · contribute · members 1 rules 0 stuff 1 · stop=action`),
  one line per tool call as it happens (`[0:42] Bash     git log --oneline -5`),
  a `… thinking 25s` heartbeat after 10s of silence, a footer per iteration
  from the result event (`duration 4m58s · turns 17 · $0.83`) and run totals
  at the end. `--quiet` is the old buffered output; `--verbose` is the raw
  stream-json events with partial messages
- Consecutive non-zero claude exits back off exponentially (2s, 4s, 8s... capped by `ZLOOP_BACKOFF_MAX`)
- Rewrites `.claude/zloop.state` (`iteration`, `max`, `start`, `mode`) every iteration; `bin/zheap-death` records `mode` as `stop_mode` in its events and `stop=<list>` in the tag message
- Ctrl-C (or SIGTERM/SIGHUP) stops the run immediately, in the container too:
  the agent gets SIGTERM, then SIGKILL after `ZLOOP_KILL_GRACE` seconds, the
  state file is removed and zloop exits 128+signal (130 for Ctrl-C). For a
  graceful stop between iterations use `--stop file` and touch `.claude/STOP`.
  Ctrl-Z is not job control inside the container; if a run is ever stuck,
  detach with `ctrl-p ctrl-q` and `podman kill zociety-sandbox`

| Script | Purpose |
|--------|---------|
| `bin/zloop [options] [n]` | Run autonomous loop, max n iterations (`--help` for flags) |
| `bin/zloop-complete [modes]` | Dispatch stop predicates (exit 0 stop, 1 continue, 2 abort) |
| `bin/zrender` | Render claude stream-json as compact progress lines (stdin to stderr, result text to stdout) |
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

### zloop Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ZLOOP_TIMEOUT` | 300 | Timeout per iteration in seconds |
| `ZLOOP_STOP` | action | Stop modes, comma-separated (see Stop Modes; `--stop` overrides) |
| `ZLOOP_DEBUG` | 0 | Enable debug output (1 = on) |
| `ZLOOP_QUIET` | 0 | Same as `--quiet`: buffered result only, no live render (1 = on) |
| `ZLOOP_VERBOSE` | 0 | Same as `--verbose`: raw stream-json events (1 = on) |
| `ZLOOP_BACKOFF_MAX` | 300 | Cap in seconds on the sleep after consecutive claude failures |
| `ZLOOP_KILL_GRACE` | 10 | Seconds to wait for the agent to exit on Ctrl-C/SIGTERM before SIGKILL |

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
| `bin/zstate` | Get current state and next action (JSON output) |
| `bin/zjoin` | Join as a member |
| `bin/zstuff` | Record stuff creation |
| `bin/zvote` | Vote on a rule |
| `bin/zpass` | Record a rule passing |
| `bin/zcomplete` | Record genesis completion |
| `bin/zheap-death` | Archive cycle, prepare next (`--done` marks the hypothesis settled for `feedback` mode) |
| `bin/zpr-flow` | Open (and optionally merge) a cycle branch PR into main (workflow step, run by `bin/zheap-death`) |
| `bin/zgit` | Run git inside the container as zociety-dev (host wrapper; `--no-pager`, refuses stdin/editor forms) |
| `bin/zgh` | Run gh inside the container as zociety-dev (host wrapper; `GH_PAGER=cat`, refuses stdin/editor/`--web` forms) |
| `bin/shims/{git,gh}` | direnv PATH shims: in-worktree, route git writes + all gh through `zgit`/`zgh`; reads and out-of-worktree stay on host |
| `bin/zpromise` | Output completion promise |
| `bin/zevent` | Low-level event creation |
| `bin/zloop` | Autonomous loop with dynamic completion (`--stop` modes) |
| `bin/zloop-complete` | Dispatch stop predicates (exit 0 stop, 1 continue, 2 abort) |
| `bin/zrender` | Compact live render of claude's stream-json (used by `bin/zagent --render compact`) |
| `bin/zstop-action` | Stop predicate: action is `stop` or `promise` |
| `bin/zstop-budget` | Stop predicate: `ZSTOP_BUDGET` heap-deaths since loop start |
| `bin/zstop-converge` | Stop predicate: recent cycles stopped changing `stuff/` |
| `bin/zstop-feedback` | Stop predicate: latest heap-death since loop start says `done: true` |
| `bin/zstop-file` | Stop predicate: `.claude/STOP` exists |
| `bin/test-zstop-modes` | Dry-run harness for the stop modes |
| `bin/test-prov-encoding` | Prove the provenance page's `vsToPua`/`puaToVs` match `nfprov` (exit 2 before the page exists) |
| `bin/zworkflow` | Propose GitHub Actions workflow |
| `bin/zworkflow-vote` | Vote on proposed workflow |
| `bin/zworkflow-pass` | Activate approved workflow |
| `bin/nfprov.py` | Vendored-verbatim canonical encoder from the fork (`mark`/`inspect`/`strip`/`convert`) |
| `bin/nfprov-diff.py` | Mark text added between a base and current file (`mark-added`); front end over `bin/nfprov.py` |
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
WebKit (Safari, Orion) ignores the VS sequences entirely because both
shape text with CoreText, which drops an unregistered variation selector
before the P+ face ever sees it; the page falls back to PUA-B display
there (#13). Any other CoreText consumer has the same gap, including
non-browser apps such as the Zed editor — VS18 text pastes in unmarked,
PUA-B pastes in marked. `bin/nfprov.py` and
`bin/nfprov-mapping.json` are vendored verbatim from the fork (`bin/nfprov.py`
is the fork's reference encoder; `bin/nfprov-diff.py` is zociety's own
`mark-added` front end over it); update the vendored pair by copying, and
keep the source SHA in the header. Attribution is by
commit convention: `[event]` commits are agents (name from the zevent
envelope), everything else is the human. Over-marking is the accepted
failure direction. `docs/provenance.html` shows `AGENTS.md` because
`PROMPT.md` is nine lines since rev66.

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

Query examples:
```bash
git log --oneline --grep="^\[join\]"   # all joins
git log --oneline --grep="^\[pass\]"   # all passed rules
bin/zstate | jq .                       # current state
```

### Branches

- `main` - current cycle
- `cycle/rev{N}-attempt{N}` - archived cycles
- `learnings` - orphan branch with accumulated insights

## Genesis Thresholds

A cycle completes when:
- 3+ members (join events)
- 2+ passed rules (pass events)
- 3+ stuff items (stuff events)

Check with: `bin/zstate | jq .genesis`

## Agent Flow

```
bin/zstate → action field tells you what to do:

  "contribute" → Join, make stuff, vote on rules
  "complete"   → Run bin/zcomplete
  "heap-death" → Run bin/zheap-death
  "promise"    → Run bin/zpromise and STOP
  "stop"       → Do nothing, exit cleanly
```

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
- `bin/test-zevent-system` to test the git-native event sourcing system.

The repository uses pre-commit hooks for:
- Trailing whitespace and EOF fixes
- Secret detection (gitleaks; `.gitleaks.toml`, inline `# gitleaks:allow` for exemptions)
- Shell script validation (shellcheck)
- State validation

Install with: `pre-commit install`. The gitleaks binary ships in the container; on the host, `brew install gitleaks`.

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
- Tags: `rev{N}-attempt{N}-iterations{N}of{N}`
- Branches: `cycle/rev{N}-attempt{N}`
- Orphan branch: `learnings`

---

## Historical Record

**Immutable, objective facts only below this line.**

| Rev | Change |
|-----|--------|
| rev1-49 | File-based state. Mutable `.z/` directory tracked loop state. |
| rev50 | Git-native event sourcing. State derived from commit history. |
| rev66 | Stable PROMPT.md. Commands drive the loop, not the prompt. Removed `evolve` action. |
