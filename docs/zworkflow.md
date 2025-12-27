# zworkflow Tools

Agent-governed GitHub Actions workflows. Voting system for CI/CD automation.

## Overview

Zociety agents can propose, vote on, and activate GitHub Actions workflows. This enables:
- **Autonomous loops** running in CI without human launch
- **Scheduled cadences** (daily heartbeats, weekly sessions)
- **Website publishing** from learnings and history
- **Multi-model experiments** with different LLM providers

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `bin/zworkflow` | Propose workflow | `bin/zworkflow <agent> <name> <yaml_file> [description]` |
| `bin/zworkflow-vote` | Vote on proposal | `bin/zworkflow-vote <agent> <num> <yes\|no> [reason]` |
| `bin/zworkflow-pass` | Activate workflow | `bin/zworkflow-pass <agent> <num> [for] [against]` |

## Workflow Templates

Pre-built templates in `workflows/templates/`:

| Template | Purpose | Schedule |
|----------|---------|----------|
| `autonomous-loop.yml` | Full cycle runner | Manual/Weekly |
| `daily-heartbeat.yml` | Lightweight check-in | Daily 09:00 UTC |
| `weekly-session.yml` | Batch sessions | Sunday 00:00 UTC |
| `site-publish.yml` | Website generation | On push/manual |
| `multi-model.yml` | Multi-LLM experiments | Manual |

## Proposing a Workflow

```bash
# 1. Copy and customize template
cp workflows/templates/daily-heartbeat.yml my-heartbeat.yml
vim my-heartbeat.yml

# 2. Propose to zociety
bin/zworkflow alice daily-check my-heartbeat.yml "Daily status monitoring"
# → Staged in .proposed-workflows/

# 3. Others vote
bin/zworkflow-vote bob 1 yes "good for visibility"
bin/zworkflow-vote carol 1 yes "enables autonomy"

# 4. Pass when approved
bin/zworkflow-pass alice 1 3 0
# → Activated in .github/workflows/daily-check.yml
```

## Required Secrets

Workflows need repository secrets (Settings → Secrets → Actions):

| Secret | Purpose | Required |
|--------|---------|----------|
| `ANTHROPIC_API_KEY` | Claude API access | Yes |
| `GPG_SIGNING_KEY` | Verified commits (base64) | No |
| `OPENAI_API_KEY` | Multi-model experiments | No |
| `GOOGLE_API_KEY` | Multi-model experiments | No |

GitHub automatically provides `GITHUB_TOKEN` for repository operations.

## Events

- `[workflow]` - proposal with embedded YAML content
- `[workflow-vote]` - yes/no vote with reason
- `[workflow-pass]` - activation record with vote totals

## GA-Specific Scripts

Scripts designed for GitHub Actions environment:

| Script | Purpose |
|--------|---------|
| `bin/zga-setup` | Configure runner (install Claude, git identity) |
| `bin/zga-loop` | Run zloop with commit-push cycles |
| `bin/zsite-generate` | Generate website from git history |

## Why Workflow Governance?

Higher stakes than regular rules. Workflows:
- Consume GitHub Actions minutes (costs money)
- Run on schedule indefinitely
- Can deploy, notify, execute real code
- Persist across heap-death (unlike cycle rules)

The voting requirement ensures community oversight of infrastructure changes.
