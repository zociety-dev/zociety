# Handoff — making the loop kick-off idiomatic to the culture experiment

## 1. Problem Space
zociety is an emergent-governance / cultural-evolution experiment: sequential agent turns
accumulate members, rules, and `stuff/` until genesis thresholds trip; a cycle is a
generation. The concern here is the **kick-off ergonomics** of starting a round — it feels
like arbitrary git ceremony, and we want it idiomatic to what the experiment is actually
doing. (The sibling apt/build fix is done and out of scope.)

Two loop engines exist: `bin/zloop` (local) and `bin/zga-loop` (`zga` = GitHub Actions).
Both sit on the same single-shot atom, `bin/zagent`, which runs exactly one agent turn. The
Claude Code harness `/loop` skill is unrelated to any of the `z*` scripts.

The population is now **heterogeneous in agent model**: join events on record carry eight
distinct model strings (sonnet-4, haiku-4.5, sonnet-5, opus-4.5, opus-4.8, gpt-4o,
`unknown`, ...). CI runs haiku; local runs run whatever `ANTHROPIC_MODEL` /
`ZOCIETY_AGENT_CLIENT` say; a single cycle can span both. Model is a treatment variable
the archive must be able to answer for — and, per `docs/challenges/cross-agent-deference.md`,
one the agents must *not* be able to read mid-cycle.

## 2. Codebase Reference Points
- `bin/zheap-death` — the **death** boundary, already fully idiomatic. Derives the identity of
  the cycle *that just ended* (~`bin/zheap-death:186-201`): parses the last tag, bumps rev if
  `PROMPT.md` differs from that tag at death time, else bumps attempt. Creates
  `cycle/rev{N}-attempt{N}` as a pointer at HEAD, tags `rev{N}-attempt{N}-iterations{I}of{M}`,
  writes a git note (`cycle`, `question`, `batch_remaining`; no model), opens a PR via
  `bin/zpr-flow`, then commits the next cycle's `[direction]` event **on the same branch**
  (`bin/zheap-death:284-286` is the checkout dance; `:329-370` the direction event).
- `bin/zloop` — the **birth** boundary, currently bare. `START_SHA=$(git rev-parse HEAD)`
  (`bin/zloop:150`); runs on whatever branch is checked out; creates no branch. Passes
  `--client` to `bin/zagent`, never `--model` (model comes from `ANTHROPIC_MODEL` env).
- `bin/zga-loop` — CI loop engine; parallel reimplementation of `zloop`'s iterate/stop cycle
  (NOT a wrapper), though both call the same `bin/zagent` atom per turn. Runs on `main` under
  the `GITHUB_ACTIONS` guard bypass, pushes `main` directly. Passes `--model` explicitly
  (default haiku-4.5).
- `bin/zagent` — the single-shot atom: one agent turn, one client, one model. The child agent's
  shell currently inherits `ANTHROPIC_MODEL` unscrubbed.
- `.githooks/pre-commit:7` — `no-main-commits`: rejects commits on `main` unless `ALLOW_MAIN=1`
  or `GITHUB_ACTIONS`. The *only* reason a human branches first.
- `bin/zjoin:18` — `model` recorded per member at join: `$4`, else `ANTHROPIC_MODEL`, else
  `unknown`. Gemini clients fall to `unknown` unless the agent passes it explicitly. This is
  today the **only** place model enters the event log, and it is the leak the blind removes.
- `bin/zstate` — returns `cycle`, `seq`, `phase`, `direction`, `batch`, `action`.
- `bin/zstop-converge` — compares consecutive `cycle/*` branches' `stuff/` trees, blind to model.
- `bin/save-learning` — checks out the learnings orphan branch and back (matters for the
  `git checkout -` hazard below).
- `docs/challenges/cross-agent-deference.md` — the leak table and the four-step blind that
  step 4 below adopts.

## 3. Verbatim Inputs
- "We resolved the build issue but (b) is still a concern."
- "What can we learn what prior art / previous attempts or implementation of loop based
  culture experiments to make the kick-off process idiomatic to what it's trying to achieve?"
- "Why do I need to 'cut the next branch' before starting a loop?" / "I thought the loop
  creates its own branch."
- "Does the recommendation consider that zociety is now heterogenous in terms of agent model?"
- "Please make it so."
- Style: brief, specific, DRY; commit to a position; disagree directly.

## 4. Current Understanding
**The gap is birth/death asymmetry, not "should the loop branch."** heap-death mints a
first-class lineage identity (`rev/attempt`) only when a cycle *ends*; genesis has none. The
operator works on an arbitrary branch cut only to satisfy `no-main-commits`, then the machine
archives under a different, computed name.

**Three cycle counters exist today and disagree.** `zstate.cycle` = 36 (event-log counter,
present in every event, not monotonic across runs); the last tag says `rev63-attempt51`
(157 `cycle/*` branches); the `[evolve]` commits say rev66. `rev` has been frozen at 63 for 51
attempts because `PROMPT.md` is nine stable lines since rev66 — "commands drive the loop, not
the prompt". So `rev` bumps are effectively dead and `attempt` is a bare counter. Keep
`rev/attempt` as the lineage name (continuity with the archive), but do not reach for
`zstate.cycle` as a branch name until it is proven monotonic. It is not today.

**Decisions recorded:**
- **Identity = the branch name.** `cycle/rev{N}-attempt{M}` is the record of which cycle is
  running; nothing else (state file, tag arithmetic) is authoritative while a cycle is live.
- **Rev bumps are a manual operator action.** `PROMPT.md` is frozen, so the automatic
  "bump rev if PROMPT.md changed" path is dead. An operator who changes the prompt names the
  next branch `cycle/rev{N+1}-attempt1` by hand; the machine only ever bumps `attempt`.
- **heap-death checks out the successor branch only when already on a cycle branch.** On any
  other branch (`main` in CI) it keeps today's behaviour. CI on `main` is therefore unchanged
  until the `zga-loop` collapse, which is a follow-up outside this PR series.
- **CI adoption of the branch flow: decided yes, at collapse time.** When `zga-loop` folds
  onto the shared iterate/stop atom it starts pushing `cycle/*` branches and `main` advances
  only through the PRs `zpr-flow` already opens. Not before.
- **Model is recorded blind and revealed at death.** Models for a cycle derive from the
  reveal ledger (`refs/notes/blind`), not from join events.

**Prior art → the single lesson each gives for kick-off:**
- **Voyager** — kick-off derives from state (zociety has `zstate`).
- **POET / DGM / MAP-Elites** — lineage is first-class and machine-named at birth; the archive
  is indexed by descriptors. With heterogeneous models, *model is a descriptor of the
  archive entry, not part of the lineage name*.
- **Smallville** — human supplies a one-line seed; runtime builds the rest.
- **Iterated learning (Kirby; '24 LLM transmission chains)** — the prior generation's compressed
  output is the bottleneck. Mixed-learner chains are a known variant; the treatment (which
  learner) must be recorded per generation or results are uninterpretable.
- **AutoGPT / BabyAGI (cautionary)** — kick-off must get *lighter*, not heavier.

Through-line: **the run owns its own initialization; a human supplies a seed, never prepares
VCS plumbing by hand; the archive records the treatment — without showing it to the agents.**

**Recommended approach — the branch name is the identity record:**
1. `zheap-death` reads its identity from the current branch when it matches
   `cycle/rev*-attempt*`; falls back to today's tag derivation otherwise. No state file
   (`.zociety/zloop.state` is deleted by both the `zloop` EXIT trap and heap-death; it cannot
   be a record). Rewrite `bin/zheap-death:284-286`: when already on the cycle branch,
   `git checkout -b X || git checkout X; git checkout -` lands on the learnings orphan branch
   after `save-learning`'s round trip.
2. **Death births the successor.** When on a cycle branch, heap-death's last act is
   `git checkout -b` the next cycle's branch (`attempt+1`; rev is never bumped by the machine)
   *before* committing the `[direction]` event. A zloop run spans several cycles; without this,
   cycles 2..k share cycle 1's branch and birth==death holds only for the first cycle of a run.
   Not on a cycle branch (CI on `main`): no checkout, today's behaviour.
3. `zloop` preflight covers only the first cycle: if the current branch is not a cycle branch,
   derive `cycle/rev{N}-attempt{N}` from the last tag and check it out. That satisfies
   `no-main-commits` *by* the naming step.
4. **Record the model blind; reveal at death** (`docs/challenges/cross-agent-deference.md`):
   - `[join]` events lose the `model` field; `zjoin` assigns member names (no self-chosen
     `opus` / `sonnet-2` / `haiku`).
   - `zagent` takes the model as a flag and scrubs `ANTHROPIC_MODEL` / `GEMINI_MODEL` from
     the child env, so the agent cannot read its own or anyone's model from the shell.
   - New `bin/zblind` seals an encrypted per-iteration note (runner, model, client) under
     `refs/notes/blind`. The **loop** writes it, not the agent. Key `ZOCIETY_BLIND_KEY` is
     shared by CI and local and stripped from the agent env before `zagent` starts.
   - Whichever runner observes a `[heap-death]` commit decrypts the cycle's blind notes and
     reveals the distinct model list into the cycle git note (`models:`) and the heap-death
     event data. A cycle can be mixed (CI haiku picks up a direction a local opus run left),
     so a birth-time declaration would be wrong; per-iteration truth lives in the ledger.
   - The ledger is the only source: `zstop-converge`, provenance and any later analysis read
     models from the reveal, never from join events.
5. **CI**: decided yes (see Decisions). `zga-loop` keeps pushing `main` until it collapses onto
   the shared atom; at that point it adopts the cycle-branch flow and PR-only advancement of
   `main`. Follow-up, outside this series.

**Guardrails:** branch per *cycle*, never per *turn*. Keep model out of the branch and tag
names, out of member names, and out of every event until the reveal. Note that
`zstop-converge` compares consecutive cycles regardless of model; with a mixed archive its
"trivial cycle" verdict conflates model change with convergence — record, don't fix, for now.
Provenance (`bin/nfprov-blame`) goes dark inside a live cycle and resolves after the reveal;
accepted cost. Collapse `zga-loop` onto the shared atom last so local and CI cycles are named
and recorded identically.

**Resolved question:** heap-death does *not* compute the NEXT cycle; it names the one that just
ended relative to the previous tag. With the branch as the record there is nothing to reconcile.

## 5. Immediate Next Steps
Three PRs, in order:
1. **Identity PR** — `zheap-death`: read identity from the current branch (fallback: tag
   derivation); rewrite the checkout block; check out the successor (`attempt+1`) before
   committing `[direction]`, only when already on a cycle branch. `zloop`: first-cycle
   preflight (derive + checkout when not on a cycle branch). Rev bumps become a documented
   manual step (`cycle/rev{N+1}-attempt1`).
2. **Blind PR** — `zjoin` drops `model` and assigns names; `zagent` takes `--model` and scrubs
   model env from the child; new `bin/zblind` seals per-iteration notes under
   `refs/notes/blind` with `ZOCIETY_BLIND_KEY` (stripped from the agent env); `zloop` and
   `zga-loop` call it per iteration; heap-death observer reveals `models:` into the cycle note
   and event. Schema: no change to the event envelope; `join` loses one data field.
3. **zga-loop collapse** — fold `zga-loop` onto the shared iterate/stop atom; CI adopts the
   cycle-branch flow and PR-only `main`. Outside this series.
