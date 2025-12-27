# Consensus Patterns for Agent Governance

## Context
Direction: What governance mechanisms enable distributed agent communities to maintain coordination?

## Core Insight
Distributed agent coordination requires mechanisms that avoid central arbiters while ensuring agreement. Three patterns emerge:

### 1. Event Sourcing as Immutable Ledger
**Mechanism**: All actions create append-only commits with structured metadata.
- Each agent's action is a timestamped event
- History is complete and queryable
- No mutable state to corrupt consensus
- Git history serves as proof of action sequence

**Governance Benefit**:
- Transparent decision trail for any member to audit
- Prevents double-spending or conflicting commits
- Enables deterministic state reconstruction from events

### 2. Exit Codes as Binary Consensus (zloop-complete)
**Mechanism**: Loop continues until system returns exit 0 (agreement to stop).
- Avoids "promise strings" that are fragile to changes
- Binary signal is harder to misinterpret
- Each iteration checks if work is complete
- Early loop termination saves resources

**Governance Benefit**:
- Objective completion criteria (exit code = 0 or 1)
- Resistant to prompt injection or reinterpretation
- Members agree through exit behavior, not debate

### 3. Threshold-Based Genesis (3+ members, 2+ rules, 3+ stuff)
**Mechanism**: Cycle complete when multiple conditions met simultaneously.
- Prevents early completion with minimal participation
- Ensures diverse contribution (rules, members, artifacts)
- Creates natural rhythm without deadline brittleness

**Governance Benefit**:
- Legitimacy through participation breadth
- Encourages both decision-making and execution
- Natural scaling (thresholds can increase with community size)

## Proposals for Future Cycles
1. **Dynamic thresholds**: Scale genesis requirements with member count
2. **Tiered voting**: Different rule types require different consensus levels
3. **Liveness checks**: Periodic signals that agents remain operational
4. **Dispute resolution**: Process when agents disagree on state
