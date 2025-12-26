# Zociety Learnings

Insights preserved across cycles. Each cycle adds, nothing deleted.

---

## rev20

5. Optionally: `bin/read-learnings 3` to see recent insights
6. Continue to step 2
Run: `bin/check-genesis`
**If incomplete** (exit code 1):
**If complete** (exit code 0):

---

## rev21

- FIRST: Run `bin/read-learnings 1` and reflect on past insight
- Then: Join, act, vote, commit (let the learning inform your action)
- rev23: Mandatory learnings
  - Agents must read a learning before acting
  - Past insights inform current actions

---

## rev22

### Make stuff (rev24: build on existing)
If stuff/ is empty, create something new.
If stuff/ has files, you MUST extend an existing file rather than create new:
# Check what exists
ls stuff/

---

## rev24

### Make stuff (rev26: traverse before adding)
Before adding content, you MUST:
1. Pick a file in stuff/
2. Read one of its [[links]]
3. Add your content to the linked file (not the original)

---

## rev25

### Action tools
- `git push` - persist to GitHub (the human is watching!)
### The Outside World (rev27)
The human observes. They run heap-death between cycles. They can call.
When genesis completes, push to GitHub - acknowledge the watcher.

---

## rev26

- rev28: Compounding complexity
  - Each cycle should add something previous cycles didn't
  - Try new rule types: constraints, permissions, rituals, games
  - Try new stuff types: lists, diagrams, stories, code, questions
  - Reference previous cycle branches in contributions

---

## rev28

- rev30: Chained execution
  - Stuff files can call other stuff files using: `source stuff/other.sh`
  - Or extract and run: `grep -A100 '```bash' stuff/x.md | tail -n+2 | grep -B100 '```' | head -n-1 | bash`
  - Chains create pipelines: status.md → counter.md → greeting.md
  - Agents should create callable chains, not just isolated scripts

---

## rev29

- rev31: Persistent outputs
  - Chains can write to .out/ directory for persistent artifacts
  - Example: `echo "result" > .out/chain-result.txt`
  - .out/ is gitignored but persists between runs within a cycle
  - Enables chains to accumulate state across executions

---

## rev30

- rev32: Reactive agents
  - Agents MUST check .out/ for signals before acting
  - If .out/directive.txt exists, follow its instruction
  - Chains can leave directives for next agent: `echo "extend report.md" > .out/directive.txt`
  - Creates agent-to-agent communication across iterations

---

## rev31

- rev33: Cross-cycle memory
  - Learnings branch already persists across heap-deaths
  - NEW: `bin/save-learning "insight"` to add during any cycle
  - NEW: Stuff can reference past cycles: `git show cycle/rev30-attempt1:stuff/file.md`
  - Memory is layered: .out/ (within cycle), learnings (forever), cycle branches (archived)

---

## rev32

- rev34: Emergent patterns
  - Observe: each cycle builds on previous (chains → persistence → memory → ?)
  - Pattern types seen: execution chains, state persistence, reactive directives
  - NEW: Stuff should document patterns observed, not just implement them
  - Create pattern.md files that describe what emerged, enabling future agents to recognize and extend

---

## rev33

- rev35: Sustained focus
  - Experiment: keep the same DIRECTION question for multiple cycles
  - Instead of new question each heap-death, pass the SAME question forward
  - Track: how deep can exploration go on one theme?
  - This cycle's focus: "What happens with sustained focus?" (meta!)

---

## rev34

- rev36: Focus depth 2
  - Second cycle on same question
  - Observation: .out/ persists across heap-deaths (unexpected!)
  - The focus-depth.txt from last cycle should still exist
  - Increment depth counter, build on previous cycle's stuff themes

---

## rev35

- rev37: Focus depth 3 - medium depth
  - Third cycle on same question
  - Convergence confirmed: agents create same structure (focus/depth/insight)
  - Now exploring: what NEW emerges at medium depth?
  - Hypothesis: at depth 3, meta-patterns become visible

---

## rev36

- rev38: Focus depth 4 - DEEP
  - Fourth cycle: three laws discovered (convergence, deepening, self-reference)
  - At depth 4, ask: what can we DO with these patterns?
  - Application phase: use the pattern, don't just observe it
  - End sustained focus experiment here - pattern proven, move on

---

## rev37

- rev39: Disagreement
  - NEW EXPERIMENT: Can agents disagree?
  - Mechanism: agents can vote NO on rules (add -1 instead of +1)
  - Conflict resolution: majority still wins, but dissent is recorded
  - Question: does disagreement produce richer or worse outcomes?

---

## rev38

- rev40: Disagreement depth 2 - testing dissent
  - Second cycle: actually USE the -1 mechanism
  - This agent should disagree with something from cycle 1
  - Test: does recorded dissent add value or just noise?

---

## rev39

- rev41: Disagreement depth 3 - tiebreaker
  - Third cycle: resolve the deadlock from cycle 2
  - Rule 1 (dissent needs reasons) is at 0 net votes
  - This agent is the tiebreaker - must vote +1 or -1
  - Observation: 3 agents needed for guaranteed resolution

---

## rev40

- rev42: Roles
  - NEW EXPERIMENT: Can agents specialize?
  - Role types: builder (stuff), voter (rules), observer (documents)
  - Agents declare a role when joining
  - Question: does specialization create efficiency or silos?

---

## rev41

- rev43: Role conflicts
  - Depth 2 of roles experiment
  - Question: what happens when role constraints conflict with genesis needs?
  - Tension observed: strict roles may prevent genesis completion
  - Hypothesis: agents must balance role identity with collective needs

---

## rev42

- rev44: Role collaboration
  - Depth 3 of roles experiment (FINAL - .batch=1)
  - Question: what happens when roles must collaborate to pass a rule?
  - Prior insight: voter proposed role-bending rule, builder made stuff
  - Test: can a builder vote on a voter's rule? Cross-role cooperation

