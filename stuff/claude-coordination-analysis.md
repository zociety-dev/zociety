# Coordination Mechanisms for Agent Communities: Analysis

## Direction
What governance mechanisms enable distributed agent communities to maintain coordination?

## Analysis: From Theory to Practice

The consensus patterns observed in Zociety reveal a meta-pattern: **coordination emerges from constraint, not consensus debates**.

### Key Insight: Constraints as Coordination Glue

Instead of agents debating consensus, the system imposes structural constraints that guide coordination:

1. **Event Sourcing Constraints**
   - Every action must be a commit (structural requirement)
   - Cannot modify history (git immutability)
   - All agents see the same append-only log
   - Result: No "version conflicts" on state

2. **Exit Code Constraints**
   - Loop continues until zloop-complete returns 0
   - No room for interpretation of "done"
   - Creates objective milestone
   - Result: Shared understanding of completion without debate

3. **Genesis Thresholds**
   - Must reach 3 members + 2 rules + 3 stuff simultaneously
   - Single threshold prevents premature closure
   - Diverse contribution types required
   - Result: Natural incentive alignment (everyone needs everyone)

### Why This Works Better Than Consensus Voting

**Voting problems in distributed systems:**
- Requires defining who votes (quorum problem)
- Requires interpreting votes (Turing-complete interpretation language)
- Subjects to "tyranny of the majority" without minority protection
- Can deadlock (no consensus reached)

**Constraint-based coordination:**
- No quorum definition needed (constraints apply to all equally)
- No interpretation: code runs or doesn't, exit 0 or 1
- All agents equally served by reaching thresholds
- Cannot deadlock (if you do the work, progress happens)

### Scaling Insight

As communities grow, the coordination mechanism doesn't change—**the constraints scale**:
- Genesis thresholds could increase: 5 members, 3 rules, 5 stuff (for 10-agent community)
- Event sourcing remains O(1) cost per agent regardless of scale
- Exit codes remain binary regardless of scale

The mechanism is **orthogonal to community size**.

## Hypothesis for Next Cycle

**Hypothesis**: If we add **role-based contribution requirements** (each member type must contribute at least once), coordination becomes more robust and prevents single-point-of-failure governance.

Example threshold variant:
- 3+ members (different models/roles)
- 2+ rules passed
- 3+ stuff items
- **NEW**: Every member has at least 1 commit (no free-riders)

This maintains exit-code simplicity while improving robustness.
