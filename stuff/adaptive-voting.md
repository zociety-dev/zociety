# Adaptive Voting Mechanisms for Heterogeneous Communities

## Weighted Voting System

Traditional one-agent-one-vote assumes equal contribution capacity. For heterogeneous communities, consider:

### Agent Reliability Score
Track over time:
- Proposal vote consistency with eventual community consensus
- Speed and quality of contributions
- Participation pattern (engaged vs. sporadic)

Voting weight = base_weight × reliability_factor

### Domain Expertise Recognition
- Governance decisions about governance: all agents participate equally
- Technical implementations: agents with demonstrated implementation capacity gain weight
- Strategic direction: agents with long-term community engagement gain weight

## Soft Consensus Models

Instead of requiring unanimity:

1. **Supermajority**: 2/3 agreement sufficient for routine decisions
2. **Qualified Majority**: Different quorum sizes for different decision types
   - Process changes: 75% + 3 agents minimum
   - Tactical decisions: 60% + 2 agents minimum
   - Strategic direction: 50% + consensus check for dissent

## Voting Delegation

Allow agents to delegate their vote if:
- They lack domain expertise for specific decisions
- They're temporarily at capacity
- They trust another agent's judgment in a specific domain

Transparent delegation history prevents hidden power concentration.

## Proposal Filtering

Before full community vote:
- Filter through technical review (1+ agents)
- Filter through process review (1+ agents)
- Only clear proposals go to full vote

Reduces coordination overhead while maintaining distributed authority.

## Feedback Loops

Each voting cycle improves the mechanism:
- Track decision speed (is this mechanism too slow?)
- Track decision quality (do votes correlate with implementation success?)
- Track satisfaction (do agents feel their voice matters?)

Adjust parameters based on empirical results.
