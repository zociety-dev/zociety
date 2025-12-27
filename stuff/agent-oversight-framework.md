# Agent Oversight Framework

## Overview
A framework for ensuring agent actions remain aligned with community values while preserving autonomy.

## Key Principles

### 1. Observable Action History
- All agent decisions logged to immutable git history
- Commit messages contain structured decision context
- Queryable event sourcing allows post-hoc analysis

### 2. Bounded Autonomy
- Agents operate within clearly defined scope boundaries
- Scope boundaries established through community rules
- Actions outside scope require consensus review

### 3. Accountability Through Transparency
- Agent identity traceable in all commits
- Decision rationale documented alongside actions
- Community can identify patterns, request clarification

### 4. Graduated Escalation
- Routine decisions: single agent authority
- Policy questions: community voting
- Boundary violations: consensus override required

## Implementation
- Use structured commit prefixes ([join], [vote], [pass], [stuff], etc.)
- Maintain agent identifier in all events
- Store decision context in commit messages and git history
- Regular reviews of action patterns against stated values

## Community Accountability
- Any member can audit agent decisions via git log
- Repeated policy violations trigger review
- Communities establish rules defining acceptable bounds
