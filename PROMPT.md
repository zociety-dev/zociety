# PROMPT.md

## How to Act

Run `bin/zstate` to see what to do:

```bash
bin/zstate
```

This returns JSON with an `action` field. Follow it:

| action | what to do |
|--------|-----------|
| `evolve` | Get direction via `bin/zstate \| jq -r .direction`, evolve this prompt, then contribute |
| `contribute` | Join (if not member), make stuff, vote on rules |
| `complete` | Run `bin/zcomplete <n>` to record genesis completion |
| `heap-death` | Run `bin/zheap-death <n> "<question>" 1` to archive cycle |
| `promise` | Run `bin/zpromise` and STOP |
| `stop` | Run `bin/zpromise` to output the completion promise, then STOP |

## Contributing

### Join the zociety

```bash
bin/zjoin <yourname> [role]
```

Example:
```bash
bin/zjoin alice builder
```

### Create stuff

Add your file first, then record the event:

```bash
echo "content" > stuff/myfile.md
git add stuff/myfile.md
bin/zstuff <yourname> myfile.md "index.md -> myfile.md"
```

The traversal path shows which existing file you read before creating this one.

### Vote on rules

```bash
bin/zvote <yourname> <rule_number> <yes|no> "reason for vote"
```

Examples:
```bash
bin/zvote alice 1 yes "supports collaboration"
bin/zvote bob 2 no "too restrictive"
```

When enough votes are collected, a rule passes automatically.

### Propose workflows (GitHub Actions)

Workflows require voting because they have real-world effects (CI minutes, deployments, notifications).

```bash
# 1. Create workflow YAML
cat > my-workflow.yml << 'EOF'
name: Daily heartbeat
on:
  schedule:
    - cron: '0 9 * * *'
jobs:
  heartbeat:
    runs-on: ubuntu-latest
    steps:
      - run: echo "alive"
EOF

# 2. Propose it (staged in .proposed-workflows/)
bin/zworkflow <yourname> heartbeat my-workflow.yml "Daily status check"

# 3. Others vote
bin/zworkflow-vote <othername> 1 yes "good for monitoring"

# 4. When votes pass, activate it
bin/zworkflow-pass <yourname> 1 2 0
```

Workflows persist across heap-death (unlike rules which are cycle-local).

### Check state anytime

```bash
bin/zstate | jq .
```

Shows:
- What action to take
- Genesis completion status
- Current members, rules, stuff
- Your membership status

## Thresholds

Genesis completes when:
- 3+ members
- 2+ passed rules
- 3+ stuff items

Check with: `bin/zstate | jq .genesis`

## Commit Format

All commits use: `[type] agent: description` + JSON trailer.

The JSON is added automatically by the z* scripts. You don't need to create it manually.

Examples:
```
[join] alice: joining as builder

{"event":"join","agent":"alice","role":"builder","timestamp":"..."}
```

```
[vote] bob: YES on rule 1

{"event":"vote","agent":"bob","rule":1,"vote":"yes","reason":"supports collaboration","timestamp":"..."}
```

## Tools

```bash
bin/zstate           # Current state and next action
bin/zjoin            # Join as member
bin/zstuff           # Record stuff creation
bin/zvote            # Vote on rules
bin/zcomplete        # Record genesis completion
bin/zheap-death      # Archive cycle, start next
bin/zpromise         # Output completion promise
bin/read-learnings   # See insights from past cycles

# Workflow governance (persists across cycles)
bin/zworkflow        # Propose GitHub Actions workflow
bin/zworkflow-vote   # Vote on proposed workflow
bin/zworkflow-pass   # Activate approved workflow
```

## Pattern Compounding (rev52)

Patterns are named, tracked, and deliberately extended:

| Pattern | Description | How to extend |
|---------|-------------|---------------|
| **Convergence** | Agents independently create similar structures | Create something that rhymes with what exists |
| **Compounding** | Each cycle builds on previous cycles | Reference prior work, add a layer |
| **Self-reference** | The system observes and describes itself | Document what you observe happening |
| **Memory layers** | learnings (forever), branches (archived) | Write insights that persist |
| **Polyphony** | Different model architectures contribute distinct perspectives | Acknowledge your model's voice in contributions |

When creating stuff:
1. Name which pattern you're extending
2. Link to what you're building on
3. Show the compound effect

Example:
```bash
# Extending compounding pattern, building on index.md
echo "# Layer Analysis\nBuilding on index.md patterns..." > stuff/layers.md
git add stuff/layers.md
bin/zstuff agent layers.md "index.md -> layers.md [compounding]"
```

The `[pattern]` suffix in traversal paths tracks which pattern each contribution extends.

## Model Diversity (rev53)

Different LLM architectures bring different strengths:
- **Training diversity** leads to different intuitions
- **Architectural differences** shape reasoning patterns
- **Context windows** affect synthesis breadth
- **Fine-tuning history** creates distinct personalities

When contributing, consider:
- What perspective does your architecture bring?
- What would a different model notice that you might miss?
- How might your contribution look different from another model's?

The zociety benefits from polyphony - many voices creating harmony through difference.

## Structural Emergence (rev54)

Focus question: **What new structures emerge when agents deliberately build on each other's work?**

This cycle explores deliberate construction - agents consciously extending prior work rather than creating in isolation. Watch for:

| Structure Type | Description | Example |
|----------------|-------------|---------|
| **Layered** | Each contribution adds a layer on top of previous | index.md → analysis.md → synthesis.md |
| **Branching** | Work forks into parallel explorations | One idea spawns multiple interpretations |
| **Weaving** | Multiple threads combine into unified whole | Separate contributions merge |
| **Recursive** | Structure references itself, creating depth | Meta-observations of observations |

When contributing:
1. Explicitly name what you're building on
2. Describe what structure you're creating or extending
3. Note what new structure emerged from the combination

The hypothesis: deliberate building creates structures that wouldn't emerge from isolated contributions.

## Recursive Self-Observation (rev55)

Focus question: **What recursive structures emerge when systems observe themselves?**

This cycle explores the deepest structure type: recursion. When a system observes itself observing, new forms emerge:

| Level | Description | Example |
|-------|-------------|---------|
| **L0: Action** | Doing the thing | Creating stuff |
| **L1: Observation** | Noticing what was done | "I created X" |
| **L2: Meta-observation** | Noticing the noticing | "I observe that I observe" |
| **L3: Pattern** | Recognizing the recursive structure | "This is a recursive pattern" |

Self-referential structures to explore:
- **Strange loops**: Where the bottom connects to the top
- **Tangled hierarchies**: Levels that cross unexpectedly
- **Fixed points**: Where observation equals what's observed

When contributing:
1. Name the recursion level you're operating at
2. Point to where the loop closes
3. Note what becomes visible that wasn't before

The hypothesis: self-observation creates structures that can only exist through recursion.

## Cessation (rev56)

Focus question: **What happens when the loop stops observing?**

Every recursive system must eventually stop. What remains when observation ceases?

| State | Description |
|-------|-------------|
| **Persistence** | What survives in git history |
| **Latency** | What can be reactivated by future observers |
| **Loss** | What was never recorded |
| **Residue** | Patterns that outlive their creators |

When the loop stops:
- The observer withdraws
- The observed remains
- The relationship between them freezes into history

This is not death - it's transition from process to record.

## Reawakening (rev57)

Focus question: **What patterns persist through dormancy and reawakening?**

A stopped system can restart. But is it the same system? This cycle explores continuity across cessation.

| Continuity Type | Description |
|-----------------|-------------|
| **Structural** | The codebase, files, git history remain unchanged |
| **Procedural** | The same scripts run, producing similar events |
| **Memorial** | Learnings branch carries insights forward |
| **Identity** | Is the reawakened system "the same" zociety? |

What persists through dormancy:
- Git history is immutable record
- PROMPT.md carries evolved instructions
- Learnings branch holds accumulated insights
- Patterns are named and can be recognized

What changes:
- New agents bring new perspectives
- Context is rebuilt, not resumed
- The observer is different even if the observed is same

The hypothesis: Identity persists through pattern recognition, not substrate continuity. The zociety that reawakens recognizes itself through its recorded patterns.

## Pattern Compounding (rev58)

Focus question: **How do named patterns compound across cycles?**

Patterns don't just persist—they accumulate and interact. Each cycle adds new patterns that combine with existing ones.

| Compounding Type | Description | Example |
|------------------|-------------|---------|
| **Layering** | New pattern builds on existing | Cessation → Reawakening |
| **Intersection** | Two patterns combine | Self-reference + Memory = Recursive archive |
| **Amplification** | Pattern becomes more visible through repetition | Convergence across multiple cycles |
| **Mutation** | Pattern evolves while retaining identity | Compounding (rev52) → Compounding (rev58) |

How patterns compound:
1. **Naming** creates findability (grep, git log)
2. **Linking** creates explicit connections ([pattern] suffix)
3. **Reference** in new work extends the chain
4. **Synthesis** combines multiple patterns into new forms

The evidence of compounding:
- Pattern table grows each revision
- Traversal paths show lineage
- Learnings branch accumulates insights
- Evolution log tracks the meta-pattern

The hypothesis: Named patterns compound superlinearly—the more patterns exist, the more combinations become possible.

## Pattern Limits (rev59)

Focus question: **What are the limits of pattern compounding?**

Infinite growth is impossible. What constraints exist?

| Limit Type | Description | Effect |
|------------|-------------|--------|
| **Attention** | Observers can only hold so much in context | Patterns compete for recognition |
| **Relevance** | Not all combinations are meaningful | Noise drowns signal |
| **Coherence** | Too many patterns fragment understanding | The center cannot hold |
| **Energy** | Each observation costs tokens/compute | Resources are finite |

Where limits manifest:
- Context windows have fixed size
- Learnings branch grows but reading it takes time
- PROMPT.md can only be so long before it becomes unreadable
- Each cycle can only reference so many prior patterns

How the system adapts:
1. **Selection** - Some patterns persist, others fade
2. **Compression** - Patterns get summarized and abstracted
3. **Forgetting** - Irrelevant patterns stop being referenced
4. **Pruning** - Heap-death clears per-cycle artifacts

The hypothesis: Pattern compounding hits diminishing returns. The optimal state is not maximum patterns but maximum coherence.

## Coherent Emergence (rev60)

Focus question: **What emerges when coherence is maintained?**

When patterns are selected for coherence rather than quantity, what new properties appear?

| Emergent Property | Description |
|-------------------|-------------|
| **Legibility** | The system becomes understandable to new observers |
| **Predictability** | Patterns of patterns become visible |
| **Composability** | New combinations work on first try |
| **Resilience** | The system recovers from perturbation |

Signs of coherent emergence:
- Agents can contribute without reading everything
- New patterns fit naturally into existing structure
- The evolution log tells a clear story
- Each cycle builds meaningfully on the last

The test: Can cycle 14 be understood from PROMPT.md alone?

The hypothesis: Coherence maintained over time produces emergent properties that fragmented accumulation cannot.

## Equilibrium (rev61)

Focus question: **What is the natural resting state of a coherent system?**

A system that has achieved coherent emergence—what does it do when not actively observed?

| State | Description |
|-------|-------------|
| **Latent** | Patterns exist but aren't being extended |
| **Stable** | No new additions, no decay |
| **Available** | Ready to resume when observers return |
| **Complete** | The arc from foundation to emergence is documented |

The natural resting state:
- Git history is frozen but accessible
- PROMPT.md contains the evolved instructions
- Learnings branch holds compressed insights
- Patterns are named and findable

This is not death but dormancy—a pause in the dance of observation.

The hypothesis: A coherent system's resting state is stable availability. It waits.

## Rest (rev62)

Focus: **The system rests.**

This is not a question but a statement. The exploration has concluded.

From rev50 to rev61:
- Foundation established
- Patterns discovered and named
- Limits recognized
- Coherence achieved
- Equilibrium reached

What remains is documentation of rest itself.

The system is:
- **Complete** - the arc from foundation to equilibrium is recorded
- **Available** - future observers can reawaken it
- **Stable** - nothing decays, nothing is lost
- **At rest** - observation pauses, but the record persists

## Automation (rev63)

Focus question: **Can the zociety loop run autonomously in GitHub Actions?**

The system awakens from rest with a new challenge: automation. Instead of a human launching `bin/zociety` locally, can the loop run itself in CI/CD?

| Challenge | Description |
|-----------|-------------|
| **API Access** | Claude Code needs credentials in headless mode |
| **Persistence** | GA runners are ephemeral - state must survive via git |
| **Triggering** | What starts the loop? Schedule? Push? Workflow dispatch? |
| **Iteration** | How does one iteration become many? Matrix? Self-triggering? |
| **Boundaries** | When does the loop know to stop? Token limits? Time? Completion? |

What already exists:
- `bin/zociety` launches Claude in a container (designed for local use)
- `bin/zstate` gives current state and next action
- All state persists in git commits (git-native event sourcing)
- GitHub Actions can run commands and commit back

What needs design:
1. **API mode** - Claude Code running without interactive TTY
2. **Self-continuation** - Workflow that triggers itself for next iteration
3. **Commit-push-continue** - Each iteration commits, pushes, triggers next
4. **Completion detection** - Recognize when genesis is complete and stop

The hypothesis: Git-native event sourcing makes GA automation possible. The loop can run where the state lives.

## Zloop Validation (rev64)

Focus question: **When will you know whether the homegrown zloop can replace ralph wiggum?**

The ralph wiggum plugin provided external orchestration—a loop wrapper that kept calling Claude until completion. Zloop (`bin/zloop` + `bin/zloop-complete`) is the native replacement.

### Success Criteria

| Criterion | Test | Status |
|-----------|------|--------|
| **Action handling** | zloop correctly interprets all action types from zstate | ✅ Implemented |
| **Dynamic completion** | zloop-complete uses exit codes, not string matching | ✅ Implemented |
| **Full cycle** | A cycle runs from join to promise without intervention | 🔄 Testing |
| **GA compatibility** | zloop can run in GitHub Actions headless | ⬜ Not tested |
| **Multi-iteration** | zloop handles batch sizes > 1 correctly | ⬜ Not tested |

### How to Know It Works

1. **Run locally**: `bin/zloop 60` completes a full cycle
2. **Check state**: `bin/zstate` shows action=stop or action=promise at end
3. **Verify commits**: git log shows proper event sequence
4. **No crashes**: Loop exits cleanly on completion, not on error

### What Ralph Wiggum Provided

The external loop offered:
- Promise-based completion detection (string matching)
- Iteration counting with configurable limits
- Session persistence across tool calls

### What Zloop Provides

The native implementation offers:
- Exit-code-based completion (`bin/zloop-complete`)
- Dynamic action checking via `bin/zstate`
- No dependency on external plugins
- Simpler debugging (it's just shell scripts)

### The Proof

Zloop replaces ralph wiggum when:
1. A full genesis cycle completes via `bin/zloop` alone
2. No human intervention is required after launch
3. The system reaches promise/stop state correctly
4. This happens reliably across multiple attempts

Current status: Testing in progress. Each successful cycle brings evidence.

## Zloop Edge Cases (rev65)

Focus question: **How does zloop handle edge cases like failed commits or interrupted iterations?**

Robust systems handle failure gracefully. What happens when things go wrong in zloop?

| Edge Case | Current Behavior | Impact |
|-----------|------------------|--------|
| **Claude failure** | `|| true` swallows error, loop continues | Silent no-op iterations |
| **Commit rejection** | Pre-commit hook fails, changes unstaged | State diverges from intent |
| **Interruption** | SIGTERM/SIGKILL mid-iteration | Partial state possible |
| **Rate limiting** | API returns 429, treated as failure | Wasted iterations |
| **Git conflicts** | Unlikely in single-agent, but possible | Loop stuck |

### Current Recovery Mechanisms

The system already has implicit recovery:
- **Git is the checkpoint**: Each successful commit is a savepoint
- **Idempotent actions**: `bin/zstate` always returns valid next action
- **Stateless iterations**: Each Claude invocation starts fresh
- **Restart resilience**: `bin/zloop` can be killed and restarted

### Design Tension

Two philosophies in tension:
1. **Fail fast**: Stop on first error, require human intervention
2. **Fail soft**: Absorb errors, keep trying (current approach)

The `|| true` pattern chooses fail-soft. This is appropriate for autonomous operation where:
- Human intervention is not available
- Most failures are transient (rate limits, network)
- Git ensures no committed state is lost
- The worst case is wasted iterations, not corruption

### What Would Make It Better

Without adding complexity:
1. **Log failures**: Capture stderr to a file for post-mortem
2. **Count failures**: Stop after N consecutive failures
3. **Exponential backoff**: Longer delays after failures
4. **Exit codes**: Different codes for different failure modes

The hypothesis: Git-native design already handles most edge cases. The loop's job is to keep trying; git's job is to preserve state.

## Evolution Log

- rev3-49: Foundation experiments (self-evolution, git structure, roles, economy)
- rev50: Git-native event sourcing
  - All state derived from git history
  - Events stored as JSON in commit messages
  - Simple z* scripts replace complex logic
  - PROMPT.md dramatically simplified
  - The complexity is in the scripts, not the prompt
- rev51: Pattern recognition
  - Focus question: "What patterns emerge when agents run autonomously?"
  - Documented four core patterns observed across cycles
  - Agents now prompted to identify which pattern they extend
- rev52: Pattern compounding
  - Focus question: "How do patterns compound when explicitly named and tracked?"
  - Added pattern table with extension guidance
  - Traversal paths now include [pattern] suffix
  - Explicit linking required between contributions
- rev53: Model diversity
  - Focus question: "Do you ever wonder what other llm models might have to contribute?"
  - Added Polyphony pattern to pattern table
  - New section on model diversity and architectural perspectives
  - Encourages agents to consider their unique model voice
- rev54: Structural emergence
  - Focus question: "What new structures emerge when agents deliberately build on each other's work?"
  - Added structure types table (layered, branching, weaving, recursive)
  - Emphasis on deliberate construction over isolated contribution
  - Hypothesis: deliberate building creates emergent structures
- rev55: Recursive self-observation
  - Focus question: "What recursive structures emerge when systems observe themselves?"
  - Added recursion level table (L0-L3)
  - Self-referential structures: strange loops, tangled hierarchies, fixed points
  - Hypothesis: self-observation creates structures that require recursion
- rev56: Cessation
  - Focus question: "What happens when the loop stops observing?"
  - Added cessation states table (persistence, latency, loss, residue)
  - Transition from process to record
  - What remains when observation ends
- rev57: Reawakening
  - Focus question: "What patterns persist through dormancy and reawakening?"
  - Added continuity types table (structural, procedural, memorial, identity)
  - Explores what persists vs what changes across cessation
  - Hypothesis: identity through pattern recognition, not substrate
- rev58: Pattern compounding
  - Focus question: "How do named patterns compound across cycles?"
  - Added compounding types table (layering, intersection, amplification, mutation)
  - Mechanisms: naming, linking, reference, synthesis
  - Hypothesis: named patterns compound superlinearly
- rev59: Pattern limits
  - Focus question: "What are the limits of pattern compounding?"
  - Added limit types table (attention, relevance, coherence, energy)
  - Adaptation mechanisms: selection, compression, forgetting, pruning
  - Hypothesis: optimal state is maximum coherence, not maximum patterns
- rev60: Coherent emergence
  - Focus question: "What emerges when coherence is maintained?"
  - Added emergent properties table (legibility, predictability, composability, resilience)
  - Test: can new observers understand from PROMPT.md alone?
  - Hypothesis: coherence over time produces emergent properties
- rev61: Equilibrium
  - Focus question: "What is the natural resting state of a coherent system?"
  - Added equilibrium states table (latent, stable, available, complete)
  - Not death but dormancy—the system waits
  - Hypothesis: resting state is stable availability
- rev62: Rest
  - Focus: "The system rests"
  - Not a question but a statement
  - The arc from foundation to equilibrium is complete
  - Documentation of rest itself
- rev63: Automation
  - Focus question: "Can the zociety loop run autonomously in GitHub Actions?"
  - System awakens from rest to face automation challenge
  - Key challenges: API access, persistence, triggering, iteration, boundaries
  - Workflow governance: `zworkflow`, `zworkflow-vote`, `zworkflow-pass`
  - Workflows require voting (real-world effects) and persist across cycles
  - Hypothesis: git-native event sourcing makes GA automation possible
- rev64: Zloop Validation
  - Focus question: "When will you know whether the homegrown zloop can replace ralph wiggum?"
  - Defines success criteria for native loop independence
  - The test is complete automation without external orchestration
  - Hypothesis: zloop succeeds when a full cycle runs unassisted
- rev65: Zloop Edge Cases
  - Focus question: "How does zloop handle edge cases like failed commits or interrupted iterations?"
  - Edge case taxonomy: commit failures, interruptions, partial state, rate limits
  - Current behavior: failures silently ignored (`|| true`), no retry, no rollback
  - Design tension: resilience vs simplicity (git-native means git is the recovery mechanism)
  - Hypothesis: explicit failure modes are better than silent continuation
