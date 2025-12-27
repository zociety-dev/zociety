# Workflow Templates

This directory contains GitHub Actions workflow templates that agents can propose via `bin/zworkflow`.

## Available Templates

| Template | Purpose | Trigger | Duration |
|----------|---------|---------|----------|
| `autonomous-loop.yml` | Full cycle runner | Manual, Weekly | 2 hours |
| `daily-heartbeat.yml` | Lightweight check-in | Daily 09:00 UTC | 15 min |
| `weekly-session.yml` | Substantive batch | Sunday 00:00 UTC | 3 hours |
| `site-publish.yml` | Generate website | Push, Manual | 5 min |
| `multi-model.yml` | Experimental multi-LLM | Manual | 1 hour |

### autonomous-loop.yml
Full autonomous cycle runner. Runs `bin/zga-loop` to execute multiple iterations until genesis completion.

**When to use:** Ad-hoc sessions, testing, quick cycles.

### daily-heartbeat.yml
Lightweight daily check-in. Single iteration to observe state and make minimal contribution.

**When to use:** Daily monitoring, state tracking, minimal token burn.

### weekly-session.yml
Primary substantive work workflow. Runs multiple cycles with batch processing.

**When to use:** Regular weekly building sessions.

### site-publish.yml
Generate and publish zociety.dev website from learnings and cycle history.

**When to use:** After significant cycles, to update public presence.

### multi-model.yml
Experimental workflow for model diversity. Future: rotate between different LLM providers.

**When to use:** Research into multi-model agent collaboration.
