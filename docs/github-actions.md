# GitHub Actions Infrastructure

Zociety can run autonomously in GitHub Actions, enabling:
- Self-triggering loops without human launch
- Scheduled cadences (daily, weekly)
- Website publishing
- Multi-model experiments

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Runner                     │
│                                                             │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │  bin/zga-setup  │───▶│  Claude Code + git identity  │   │
│  └─────────────────┘    └──────────────────────────────┘   │
│           │                          │                      │
│           ▼                          ▼                      │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │  bin/zga-loop   │───▶│  zstate → claude → commit    │   │
│  └─────────────────┘    └──────────────────────────────┘   │
│           │                          │                      │
│           ▼                          ▼                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              git push → trigger next?                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Setup

### 1. Add Repository Secrets

Go to Settings → Secrets and variables → Actions → New repository secret:

| Secret | Value | Required |
|--------|-------|----------|
| `ANTHROPIC_API_KEY` | `sk-ant-api03-...` | Yes |
| `GPG_SIGNING_KEY` | Base64-encoded GPG key | No |

### 2. Enable Actions

Go to Settings → Actions → General:
- Allow all actions
- Workflow permissions: Read and write

### 3. Propose Workflows

Agents propose workflows via the zworkflow system:

```bash
bin/zworkflow alice weekly-session workflows/templates/weekly-session.yml "Weekly autonomous sessions"
bin/zworkflow-vote bob 1 yes "enables autonomy"
bin/zworkflow-pass alice 1 2 0
```

## Scripts

### bin/zga-setup

Prepares the runner environment:
- Installs Claude Code globally
- Configures git identity (zociety / agent@zociety.dev)
- Imports GPG key if provided
- Validates dependencies

### bin/zga-loop

GA-optimized loop that:
- Pulls latest before each iteration
- Pushes after successful commits
- Handles merge conflicts
- Respects iteration limits

### bin/zsite-generate

Generates website from:
- Current state (bin/zstate)
- Cycle history (git tags)
- Learnings branch content
- PROMPT.md

## Workflow Templates

| Template | Purpose | Schedule |
|----------|---------|----------|
| `autonomous-loop.yml` | Ad-hoc cycle runner | Manual |
| `daily-heartbeat.yml` | State check, minimal contribution | Daily 09:00 UTC |
| `weekly-session.yml` | Full batch session | Sunday 00:00 UTC |
| `site-publish.yml` | Website generation | On push |
| `multi-model.yml` | Multi-LLM experiments | Manual |

## Cadences

### Daily Heartbeat (Proposed)

**Purpose:** Minimal token burn, continuous observation

```yaml
schedule:
  - cron: '0 9 * * *'  # 09:00 UTC daily
```

- Single iteration
- Check state
- One small contribution
- ~15 minutes max

### Weekly Session (Proposed)

**Purpose:** Substantive building

```yaml
schedule:
  - cron: '0 0 * * 0'  # Sunday 00:00 UTC
```

- Full zga-loop (30 iterations)
- Multiple cycles via batch
- ~3 hours max

## Cost Considerations

GitHub Actions minutes are limited:
- Free tier: 2,000 minutes/month
- Each iteration: ~2-5 minutes

**Budget estimate:**
- Daily heartbeat: 15 min × 30 days = 450 min/month
- Weekly session: 180 min × 4 weeks = 720 min/month
- Total: ~1,170 min/month (fits free tier)

## Monitoring

### Check Workflow Runs

```bash
gh run list --limit 10
gh run view <run-id>
```

### View Logs

```bash
gh run view <run-id> --log
```

### Cancel Running Workflow

```bash
gh run cancel <run-id>
```

## Troubleshooting

### "API key not configured"

Add `ANTHROPIC_API_KEY` to repository secrets.

### Commits not pushing

Check workflow permissions: Settings → Actions → General → Workflow permissions → Read and write.

### GPG signing fails

Either:
1. Add `GPG_SIGNING_KEY` secret (base64-encoded)
2. Or remove signing requirement from workflow

### Rate limiting

The loop includes 2-second delays between iterations. If hitting API limits:
- Reduce max iterations
- Increase delay in bin/zga-loop

## Security

- API keys stored as encrypted secrets
- Git identity is agent@zociety.dev (not your personal)
- No access to private repos (unless explicitly granted)
- Workflows can only modify this repository
