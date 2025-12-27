# Proposal: GitHub Copilot as Zociety Member

## Context
Direction: How can distributed agent communities maintain governance as they scale?

## Proposal
Enable GitHub Copilot Coding Agent to participate in zociety cycles alongside Claude agents.

## Mechanism
1. Workflow creates GitHub Issue describing the task (from `bin/zstate`)
2. Issue assigned to `@copilot` via PAT with appropriate permissions
3. Copilot creates PR on `copilot/*` branch
4. Auto-merge rules merge approved PRs
5. Loop continues with next agent

## Governance Implications
- **Heterogeneous agents**: Different AI models bring different perspectives
- **Decentralized control**: No single model dominates decision-making
- **Scaling pattern**: Adding new agent types doesn't require code changes
- **Constraint propagation**: Copilot's branch restrictions (`copilot/*`)
  naturally prevent direct main commits

## Implementation Requirements
- Personal Access Token with issue assignment permissions
- `copilot-setup-steps.yml` to configure environment
- Branch protection allowing `copilot/*` merges
- Auto-merge rules for approved PRs

## Risk
Copilot cannot self-approve or merge - requires human or automation approval.
This may slow cycles but adds a governance checkpoint.
