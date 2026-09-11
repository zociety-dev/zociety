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
- Identity at birth: started on any branch that is not `cycle/*`, the run
  names its first cycle (`bin/zcycle-id current`: last tag, attempt+1, or
  rev+1 if `PROMPT.md` changed) and checks out `cycle/rev{N}-attempt{M}`
  before the first iteration. Cut no branch by hand; that step also
  satisfies the no-main-commits hook. `ZLOOP_BRANCH=0` opts out (runs on
  the current branch, as before). Already on a `cycle/*` branch: unchanged
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
| `bin/zcycle-id [--branch] current\|next` | Name the running cycle (`rev{N}-attempt{M}`; the branch name on a `cycle/*` branch, else derived from the last tag) or its successor (attempt+1) |
| `bin/zrender` | Render claude stream-json as compact progress lines (stdin to stderr, result text to stdout) |
| `bin/zstop-<mode>` | One stop predicate; prints `STOP: <mode> ...` or `CONTINUE: <mode> ...` |
| `bin/test-zstop-modes` | Dry-run harness: fake `claude` + throwaway repo, one case per mode |
| `bin/test-zcycle-id` | Dry-run harness for cycle identity: `zcycle-id`, the heap-death successor checkout, the zloop preflight |

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
`bin/zheap-death` refuses to run off `main` or a `cycle/rev{N}-attempt{M}`
branch (override with `ZHEAP_DEATH_ANY_BRANCH=1`) so a test run cannot
archive a cycle into a feature branch.

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
| `ZLOOP_BRANCH` | 1 | 0 skips the cycle-branch preflight: run on whatever branch is checked out (`main` then needs `ALLOW_MAIN=1`) |

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
| `bin/zjoin` | Join as a member (name assigned: `member-{N}`; no model in the event) |
| `bin/zblind` | Seal each loop turn's model under `refs/notes/blind` (`seal`), mark it `kind: ai` under `refs/notes/agent`, and decrypt a cycle's models at heap-death (`reveal`) |
| `bin/zstuff` | Record stuff creation |
| `bin/zvote` | Vote on a rule |
| `bin/zpass` | Record a rule passing |
| `bin/zcomplete` | Record genesis completion |
| `bin/zheap-death` | Archive cycle, prepare next (`--done` marks the hypothesis settled for `feedback` mode); on a `cycle/*` branch it births the successor branch (attempt+1) before the `[direction]` event |
| `bin/zcycle-id` | Name the running cycle or its successor (`current`/`next`, `--branch` for the `cycle/` form) |
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
| `bin/test-zblind` | Throwaway-fixture harness for the blind model record: `bin/zblind`, `bin/zjoin` naming, the `bin/zagent` env scrub, the `Agent:` trailer hook and `bin/nfprov-blame.py` rungs |
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
  run `bin/zblind seal <prev-head> HEAD <model> <client> <runner>`: each new
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
- `bin/test-zcycle-id` to verify cycle identity: `bin/zcycle-id`, the
  heap-death successor checkout and the zloop preflight.
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
  exported). `core.hooksPath` is not used: the hook runs through the
  pre-commit framework's `prepare-commit-msg` stage.

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
- Tags: `rev{N}-attempt{N}-iterations{N}of{N}` - written by `bin/zheap-death`
  at the cycle's last commit; the id comes from `bin/zcycle-id current`
  (the branch name when on `cycle/*`, else the last tag with attempt+1, or
  rev+1 if `PROMPT.md` changed)
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
