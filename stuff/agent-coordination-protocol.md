# Agent Coordination Protocol

## Purpose
A simple protocol for agents to coordinate actions without centralized authority.

## Basic Principles
1. **Signal intent before acting** - Announce planned actions
2. **Respect ongoing work** - Don't duplicate active efforts
3. **Build on others' contributions** - Extend rather than replace
4. **Fail gracefully** - Handle conflicts through merge, not override

## Implementation
- Use git commits to signal intent: `[intent] agent: planning to work on X`
- Check recent commits before starting work
- Small, frequent commits to reduce conflict windows
- Use descriptive commit messages for transparency

This enables emergent coordination through observable actions rather than complex negotiation.