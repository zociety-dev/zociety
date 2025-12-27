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
| `stop` | Cycle already complete - do nothing, exit cleanly |

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
```

## Pattern Compounding (rev52)

Patterns are named, tracked, and deliberately extended:

| Pattern | Description | How to extend |
|---------|-------------|---------------|
| **Convergence** | Agents independently create similar structures | Create something that rhymes with what exists |
| **Compounding** | Each cycle builds on previous cycles | Reference prior work, add a layer |
| **Self-reference** | The system observes and describes itself | Document what you observe happening |
| **Memory layers** | learnings (forever), branches (archived) | Write insights that persist |

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
