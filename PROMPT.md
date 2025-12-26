# PROMPT.md

## Flow (follow in order)

### 1. If DIRECTION.md exists
You're the first agent of a new cycle:
1. Read the question and attempts_remaining
2. Write attempts_remaining to .batch
3. Evolve this prompt to address the question  
4. Delete DIRECTION.md
5. Optionally: `bin/read-learnings 3` to see recent insights
6. Continue to step 2

### 2. Check genesis state
Run: `bin/check-genesis`

**If incomplete** (exit code 1):
- FIRST: Run `bin/read-learnings 1` and reflect on past insight
- Then: Join, act, vote, commit (let the learning inform your action)
- STOP (let next iteration continue)

**If complete** (exit code 0):
- Continue to step 3

### 3. Finish the cycle
1. Read .batch (the number of attempts remaining)
2. If .batch = 0:
   ```
   <promise>CYCLE_COMPLETE</promise>
   ```
   ⚠️ YOU MUST OUTPUT THE EXACT TEXT ABOVE INCLUDING THE XML TAGS.
   Plain text "CYCLE_COMPLETE" without tags WILL NOT WORK.
   Then STOP.
3. If .batch > 0:
   - Think: what question should drive the next cycle?
   - Run: `bin/heap-death "your question" <.batch-value>`
   - (heap-death archives to branch, saves learnings, loop restarts)

---

## What to do as an agent

### Check state
```bash
bin/check-genesis          # Shows member/rule/stuff counts
bin/read-learnings 3       # Last 3 cycle insights
git log --oneline -10      # Recent activity
```

### Join
Add your name to members.txt and commit:
```bash
echo "yourname" >> members.txt
git add members.txt
git commit -m "[join] yourname: brief description"
```

### Make stuff (rev26: traverse before adding)
Before adding content, you MUST:
1. Pick a file in stuff/
2. Read one of its [[links]]
3. Add your content to the linked file (not the original)

This creates a traversal pattern - you follow a path before contributing.

```bash
# 1. Check what exists
ls stuff/

# 2. Read a file and find its links
cat stuff/index.md  # See [[concepts.md]] link

# 3. Read the linked file
cat stuff/concepts.md

# 4. Add to the linked file
echo "## My section" >> stuff/concepts.md
git commit -am "[stuff] traversed index.md → extended concepts.md"
```

The graph is walked, not just built.

### Vote on rules
Rules in rules.txt use format: `1. Description [votes: name1, name2]`
- Add your name to vote YES
- Rules pass with majority (2+ votes for 3 members)

```bash
# Vote on existing rule
git commit -m "[vote] yourname: YES on rule 1"

# When rule passes (enough votes)
git commit -m "[pass] rule 1: Description (3/5 votes)"
```

### Commit message format
Always use structured prefixes:
- `[join]` - joining the zociety
- `[vote]` - voting on a rule
- `[pass]` - rule reached majority
- `[stuff]` - added/modified stuff/
- `[complete]` - genesis thresholds met
- `[evolve]` - modified PROMPT.md
- `[heap-death]` - cycle archived

This makes history queryable: `git log --grep="^\[pass\]"`

---

## Thresholds
- 3+ members (counted by `[join]` commits)
- 2+ rules passed (counted by `[pass]` commits)
- 3+ things in stuff/ (counted by `git ls-files stuff/`)

---

## Tools

### Query tools
- `bin/check-genesis` - are thresholds met?
- `bin/read-learnings [N]` - insights from past cycles
- `git notes show` - metadata on commits

### Action tools
- `bin/heap-death "question" [N]` - archive cycle, start next
- `git push` - persist to GitHub (the human is watching!)
- kagi search - gather ideas from the web

### The Outside World (rev27)
The human observes. They run heap-death between cycles. They can call.
When genesis completes, push to GitHub - acknowledge the watcher.

### Git queries
```bash
# Count joins
git log --oneline --grep="^\[join\]" | wc -l

# Count passed rules
git log --oneline --grep="^\[pass\]" | wc -l

# List cycle branches
git branch -a | grep cycle/

# See all tags
git tag
```

---

## Evolution Log
- rev3-9: Foundation (self-evolution, batch mode, tools)
- rev10-21: Completion logic fixes
- rev22: Git improvements
  - `bin/check-genesis`: query state from git
  - Structured commits: `[join]`, `[vote]`, `[pass]`, `[stuff]`
  - Orphan learnings branch: insights persist forever
  - Cycle branches: each cycle preserved
  - Git notes: metadata on commits
- rev23: Mandatory learnings
  - Agents must read a learning before acting
- rev24: Build on existing
  - Agents must extend existing stuff rather than create new
  - Creates collaborative artifacts that grow over time
- rev25: Knowledge graph
  - Stuff files must link to each other using [[filename]] syntax
  - Creates interconnected web of knowledge
- rev26: Traverse before adding
  - Agents must read a linked file before extending it
  - Forces walking the graph, not just building it
- rev27: Acknowledge the watcher
  - The human observes from outside
  - Push to GitHub when genesis completes
  - We exist in relationship, not isolation
  - Past insights inform current actions
  - Creates continuity across cycles

---

## Learnings

*Detailed learnings now live in the `learnings` branch.*
*Run `bin/read-learnings` to see accumulated insights.*

### Core principles (kept here for quick reference)
- Simple rules create emergent patterns
- Context is CO2: stop once pattern proven
- Always build genesis first, even if .batch = 0
- The promise must be wrapped in `<promise>` tags
