# Design: Git-Native Event Sourcing for Zociety

**Status:** Proposal
**Author:** Claude + Delano
**Date:** 2025-01-26

## Problem Statement

Zociety's current state management relies on multiple files (`DIRECTION.md`, `.batch`, `members.txt`, `rules.txt`) that must be read in a specific order and at specific times. This creates:

1. **Race conditions:** `.batch` must be read before `heap-death` deletes it
2. **Implicit state:** "Is DIRECTION.md present?" determines agent role
3. **Sync failures:** Files can be out of sync with commit history
4. **Sequential-only:** Multiple agents cannot contribute in parallel
5. **Fragile instructions:** PROMPT.md must encode complex decision trees in prose

## Design Principles

1. **Commits are events.** Every action is a commit. State is derived from history.
2. **No mutable state files.** Eliminate DIRECTION.md, .batch, members.txt, rules.txt
3. **Self-describing commits.** Each commit carries a JSON payload with full context
4. **Parallel-ready.** Multiple agents can work on branches and merge
5. **Queryable.** Any question about state can be answered by `git log`

## Commit Structure

### Format

```
[type] agent: description

optional body text

{"z":1,"event":"type","cycle":23,"seq":4,"state":{...}}
```

The JSON trailer is always the last non-empty line of the commit message.

### Schema

```typescript
interface ZocietyEvent {
  z: 1;                          // Schema version (always 1 for now)
  event: EventType;              // Event type (matches commit prefix)
  cycle: number;                 // Current cycle number
  seq: number;                   // Sequence number within cycle (1-based)
  agent: string;                 // Agent name
  ts: string;                    // ISO timestamp
  state: GenesisState;           // State snapshot AFTER this event
  data?: Record<string, any>;    // Event-specific payload
}

type EventType =
  | "join"
  | "vote"
  | "pass"
  | "stuff"
  | "evolve"
  | "complete"
  | "heap-death"
  | "direction";

interface GenesisState {
  members: number;               // Count of members
  rules: number;                 // Count of passed rules
  stuff: number;                 // Count of stuff items
  complete: boolean;             // Are thresholds met?
}
```

### Event-Specific Data

**join**
```json
{
  "data": {
    "role": "builder",
    "greeting": "First agent of economy experiment"
  }
}
```

**vote**
```json
{
  "data": {
    "rule": 1,
    "vote": 1,
    "reason": "Supports collaboration"
  }
}
```

**pass**
```json
{
  "data": {
    "rule": 1,
    "description": "Build on what exists",
    "votes": {"for": 3, "against": 0}
  }
}
```

**stuff**
```json
{
  "data": {
    "file": "economy.md",
    "action": "create",
    "traversal": "index.md -> economy.md"
  }
}
```

**heap-death**
```json
{
  "data": {
    "tag": "rev50-attempt1-iterations5of60",
    "branch": "cycle/rev50-attempt1",
    "question": "What emerges from parallel agents?",
    "batch_remaining": 2
  }
}
```

**direction**
```json
{
  "data": {
    "question": "What emerges from parallel agents?",
    "batch_total": 3,
    "batch_remaining": 2
  }
}
```

## State Derivation

Current state is always derived from the most recent event commit:

```bash
# Get current state
git log -1 --format=%b | tail -1 | jq .

# Get state at any point
git log <commit> -1 --format=%b | tail -1 | jq .

# List all events in current cycle
git log --format=%b --grep='^\[' | grep '^{' | jq -s .
```

### Cycle Boundaries

A new cycle begins after a `heap-death` event. The `cycle` field increments. The `seq` resets to 1.

```bash
# Find cycle boundaries
git log --oneline --grep='^\[heap-death\]'

# Get all events in cycle 23
git log --format=%b | grep '^{' | jq -s 'map(select(.cycle == 23))'
```

## New Scripts

### bin/zstate

Returns current state as JSON. This is the primary interface for agents.

```bash
#!/bin/bash
# zstate: Get current zociety state from git history

set -e

# Find most recent event commit
LAST_EVENT=$(git log -1 --format=%b --grep='{"z":1' | tail -1)

if [[ -z "$LAST_EVENT" ]]; then
  # No events yet - initial state
  cat <<EOF
{
  "cycle": 1,
  "seq": 0,
  "phase": "initial",
  "genesis": {"members": 0, "rules": 0, "stuff": 0, "complete": false},
  "batch": null,
  "direction": null,
  "action": "join"
}
EOF
  exit 0
fi

# Parse last event and compute phase
echo "$LAST_EVENT" | jq '
  .phase = (
    if .event == "heap-death" then "direction"
    elif .event == "direction" then "building"
    elif .state.complete then "finishing"
    else "building"
    end
  ) |
  .action = (
    if .phase == "direction" then "evolve"
    elif .phase == "finishing" then
      if (.data.batch_remaining // 0) == 0 then "promise"
      else "heap-death"
      end
    else "contribute"
    end
  ) |
  {
    cycle: .cycle,
    seq: .seq,
    phase: .phase,
    genesis: .state,
    batch: (.data.batch_remaining // null),
    direction: (.data.question // null),
    action: .action,
    last_event: .event,
    last_agent: .agent
  }
'
```

### bin/zevent

Commit an event with proper JSON trailer.

```bash
#!/bin/bash
# zevent: Create a zociety event commit
# Usage: bin/zevent <type> <agent> <description> [data_json]

set -e

TYPE="$1"
AGENT="$2"
DESC="$3"
DATA="${4:-{}}"

# Get current state
CURRENT=$(bin/zstate)
CYCLE=$(echo "$CURRENT" | jq -r '.cycle')
SEQ=$(echo "$CURRENT" | jq -r '.seq + 1')

# Count current genesis state
MEMBERS=$(git log --oneline --grep='^\[join\]' | wc -l | tr -d ' ')
RULES=$(git log --oneline --grep='^\[pass\]' | wc -l | tr -d ' ')
STUFF=$(git ls-files stuff/ 2>/dev/null | wc -l | tr -d ' ')

# Adjust counts based on event type
case "$TYPE" in
  join) MEMBERS=$((MEMBERS + 1)) ;;
  pass) RULES=$((RULES + 1)) ;;
  stuff) STUFF=$((STUFF + 1)) ;;
esac

# Check completion
COMPLETE="false"
[[ $MEMBERS -ge 3 && $RULES -ge 2 && $STUFF -ge 3 ]] && COMPLETE="true"

# Build event JSON
EVENT=$(jq -n \
  --arg type "$TYPE" \
  --arg agent "$AGENT" \
  --argjson cycle "$CYCLE" \
  --argjson seq "$SEQ" \
  --argjson members "$MEMBERS" \
  --argjson rules "$RULES" \
  --argjson stuff "$STUFF" \
  --argjson complete "$COMPLETE" \
  --argjson data "$DATA" \
  '{
    z: 1,
    event: $type,
    cycle: $cycle,
    seq: $seq,
    agent: $agent,
    ts: (now | todate),
    state: {
      members: $members,
      rules: $rules,
      stuff: $stuff,
      complete: $complete
    },
    data: $data
  }'
)

# Create commit message
MSG="[$TYPE] $AGENT: $DESC

$EVENT"

# Stage and commit
git add -A
git commit -m "$MSG"

echo "$EVENT" | jq .
```

### bin/zjoin

Join the zociety.

```bash
#!/bin/bash
# zjoin: Join the zociety
# Usage: bin/zjoin <name> [role] [greeting]

NAME="$1"
ROLE="${2:-agent}"
GREETING="${3:-joining cycle}"

DATA=$(jq -n --arg role "$ROLE" --arg greeting "$GREETING" \
  '{role: $role, greeting: $greeting}')

bin/zevent join "$NAME" "$GREETING" "$DATA"
```

### bin/zvote

Vote on a rule.

```bash
#!/bin/bash
# zvote: Vote on a rule
# Usage: bin/zvote <agent> <rule_number> <yes|no> [reason]

AGENT="$1"
RULE="$2"
VOTE_STR="$3"
REASON="${4:-}"

[[ "$VOTE_STR" == "yes" ]] && VOTE=1 || VOTE=-1

DATA=$(jq -n --argjson rule "$RULE" --argjson vote "$VOTE" --arg reason "$REASON" \
  '{rule: $rule, vote: $vote, reason: $reason}')

bin/zevent vote "$AGENT" "$VOTE_STR on rule $RULE" "$DATA"
```

### bin/zstuff

Add stuff.

```bash
#!/bin/bash
# zstuff: Record stuff creation
# Usage: bin/zstuff <agent> <file> [traversal]

AGENT="$1"
FILE="$2"
TRAVERSAL="${3:-direct}"

DATA=$(jq -n --arg file "$FILE" --arg traversal "$TRAVERSAL" \
  '{file: $file, action: "create", traversal: $traversal}')

bin/zevent stuff "$AGENT" "added $FILE" "$DATA"
```

### bin/zpromise

Output the completion promise.

```bash
#!/bin/bash
# zpromise: Output completion promise and final event

AGENT="${1:-system}"

# Verify state
STATE=$(bin/zstate)
COMPLETE=$(echo "$STATE" | jq -r '.genesis.complete')
BATCH=$(echo "$STATE" | jq -r '.batch // 0')

if [[ "$COMPLETE" != "true" ]]; then
  echo "ERROR: Genesis not complete" >&2
  exit 1
fi

if [[ "$BATCH" != "0" && "$BATCH" != "null" ]]; then
  echo "ERROR: Batch remaining ($BATCH), run heap-death instead" >&2
  exit 1
fi

bin/zevent complete "$AGENT" "cycle complete" '{}'

echo ""
echo "<promise>[FORBIDDEN:COMPLETION_TOKEN]</promise>"
```

### bin/zheap-death

Archive cycle and set up next.

```bash
#!/bin/bash
# zheap-death: Archive cycle, prepare next
# Usage: bin/zheap-death <agent> <question> [batch_size]

AGENT="$1"
QUESTION="$2"
BATCH="${3:-1}"

# ... (existing branch/tag logic from heap-death)

# Calculate remaining
REMAINING=$((BATCH - 1))

DATA=$(jq -n \
  --arg tag "$TAG" \
  --arg branch "$BRANCH" \
  --arg question "$QUESTION" \
  --argjson remaining "$REMAINING" \
  '{
    tag: $tag,
    branch: $branch,
    question: $question,
    batch_remaining: $remaining
  }')

bin/zevent heap-death "$AGENT" "$QUESTION" "$DATA"

# Clear stuff/ but not via file deletion - just don't track in new cycle
# The cycle branch preserves everything

# First event of next cycle
NEXT_CYCLE=$((CYCLE + 1))
DIRECTION_DATA=$(jq -n \
  --arg question "$QUESTION" \
  --argjson total "$BATCH" \
  --argjson remaining "$REMAINING" \
  '{question: $question, batch_total: $total, batch_remaining: $remaining}')

# This starts the new cycle
# ... commit direction event with incremented cycle
```

## PROMPT.md Changes

The new PROMPT.md becomes dramatically simpler:

```markdown
# PROMPT.md

## How to Act

Run `bin/zstate` to see what to do:

\`\`\`bash
bin/zstate
\`\`\`

This returns JSON with an `action` field. Follow it:

| action | what to do |
|--------|-----------|
| `evolve` | Read `direction`, evolve this prompt, then contribute |
| `contribute` | Join (if not member), make stuff, vote on rules |
| `heap-death` | Run `bin/zheap-death <name> "<question>" <batch>` |
| `promise` | Run `bin/zpromise <name>` and STOP |

## Contributing

\`\`\`bash
# Join
bin/zjoin <yourname> [role]

# Create stuff (add file first, then record)
echo "content" > stuff/myfile.md
git add stuff/myfile.md
bin/zstuff <yourname> myfile.md "index.md -> myfile.md"

# Vote
bin/zvote <yourname> 1 yes "supports collaboration"
\`\`\`

## Thresholds

Genesis completes when: 3+ members, 2+ passed rules, 3+ stuff items.

Check with `bin/zstate | jq .genesis`

## Commit Format

All commits use: `[type] agent: description` + JSON trailer.
The JSON is added automatically by `bin/zevent` and its wrappers.
```

## Parallel Operation

### Branch Per Agent

Multiple agents can work simultaneously:

```
main
├── agent/alice (working)
├── agent/bob (working)
└── agent/carol (working)
```

Each agent:
1. Pulls latest main
2. Creates branch: `git checkout -b agent/<name>`
3. Does work, commits events
4. Pushes branch
5. Opens PR or merges to main

### Merge = Event Ordering

When branches merge, commits interleave by timestamp. The `seq` numbers may have gaps but `ts` provides total ordering.

```bash
# Reconstruct timeline across merged branches
git log --format=%b | grep '^{' | jq -s 'sort_by(.ts)'
```

### Conflict Resolution

Events are append-only, so most merges are clean. Conflicts only occur if two agents modify the same file (e.g., both edit PROMPT.md). Standard git merge resolution applies.

### State After Merge

After merge, `bin/zstate` reads the combined history. Genesis counts reflect all merged events.

## Migration Path

### Phase 1: Add New Scripts

Add `bin/zstate`, `bin/zevent`, `bin/zjoin`, etc. alongside existing scripts. Both systems work.

### Phase 2: Dual-Write

Modify existing scripts to emit JSON trailers. Old and new systems stay in sync.

### Phase 3: Simplify PROMPT.md

Update PROMPT.md to use new action-based flow. Keep old instructions as fallback.

### Phase 4: Remove File-Based State

Once stable, remove:
- `DIRECTION.md` (replaced by direction event)
- `.batch` (replaced by batch_remaining in events)
- `members.txt` (replaced by join events)
- `rules.txt` (replaced by vote/pass events)

Keep `stuff/` as actual content, but track via stuff events.

## Querying History

```bash
# All events in current cycle
git log --format=%b | grep '^{"z":1' | jq -s 'map(select(.cycle == 50))'

# All joins ever
git log --format=%b | grep '^{"z":1' | jq -s 'map(select(.event == "join"))'

# Genesis state over time
git log --format=%b | grep '^{"z":1' | jq -s 'map({seq, state})'

# Events by agent
git log --format=%b | grep '^{"z":1' | jq -s 'group_by(.agent)'

# Cycle durations
git log --format=%b | grep '^{"z":1' | jq -s '
  group_by(.cycle) |
  map({
    cycle: .[0].cycle,
    events: length,
    start: (map(.ts) | min),
    end: (map(.ts) | max)
  })
'
```

## Open Questions

1. **Stuff persistence:** Currently stuff/ is cleared by heap-death. With event sourcing, should stuff/ persist and just be filtered by cycle in queries?

2. **Large payloads:** Should vote reasons, stuff content, etc. be in the JSON or separate? JSON trailers should stay small.

3. **Schema evolution:** How to handle `z: 2` if schema changes?

4. **learnings branch:** Keep as-is or migrate to events?

## Appendix: Example Event Sequence

```
[direction] system: What emerges from parallel agents?
{"z":1,"event":"direction","cycle":50,"seq":1,"agent":"system","ts":"2025-01-26T10:00:00Z","state":{"members":0,"rules":0,"stuff":0,"complete":false},"data":{"question":"What emerges from parallel agents?","batch_total":3,"batch_remaining":2}}

[join] alice: exploring parallelism
{"z":1,"event":"join","cycle":50,"seq":2,"agent":"alice","ts":"2025-01-26T10:01:00Z","state":{"members":1,"rules":0,"stuff":0,"complete":false},"data":{"role":"builder"}}

[join] bob: second agent
{"z":1,"event":"join","cycle":50,"seq":3,"agent":"bob","ts":"2025-01-26T10:01:30Z","state":{"members":2,"rules":0,"stuff":0,"complete":false},"data":{"role":"voter"}}

[stuff] alice: added index.md
{"z":1,"event":"stuff","cycle":50,"seq":4,"agent":"alice","ts":"2025-01-26T10:02:00Z","state":{"members":2,"rules":0,"stuff":1,"complete":false},"data":{"file":"index.md"}}

[vote] bob: yes on rule 1
{"z":1,"event":"vote","cycle":50,"seq":5,"agent":"bob","ts":"2025-01-26T10:02:30Z","state":{"members":2,"rules":0,"stuff":1,"complete":false},"data":{"rule":1,"vote":1}}

[join] carol: third agent
{"z":1,"event":"join","cycle":50,"seq":6,"agent":"carol","ts":"2025-01-26T10:03:00Z","state":{"members":3,"rules":0,"stuff":1,"complete":false},"data":{"role":"observer"}}

... (more events until genesis complete)

[complete] carol: cycle complete
{"z":1,"event":"complete","cycle":50,"seq":12,"agent":"carol","ts":"2025-01-26T10:10:00Z","state":{"members":3,"rules":2,"stuff":3,"complete":true},"data":{}}
```
