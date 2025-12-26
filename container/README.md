# Zociety Container

Fully containerized Claude Code environment for zociety agent loops. Claude Code itself runs inside the container, providing complete isolation from the host system.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Host System                         │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Podman Container                      │  │
│  │                                                    │  │
│  │   ┌─────────────┐    ┌─────────────────────────┐  │  │
│  │   │ Claude Code │───▶│ bash, git, bin/*        │  │  │
│  │   └─────────────┘    └─────────────────────────┘  │  │
│  │          │                       │                 │  │
│  │          ▼                       ▼                 │  │
│  │   /home/agent/.claude     /repo (mounted)         │  │
│  │                                                    │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                             │
│           Volumes: repo, ssh, gitconfig, secrets        │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Configure API key
echo 'sk-ant-api03-...' > container/secrets/anthropic_api_key
chmod 600 container/secrets/anthropic_api_key

# 2. Build the image
bin/zociety --build

# 3. Run interactive Claude session
bin/zociety

# 4. Or run the agent loop directly
bin/zociety ralph-loop
```

## Security Properties

| Property | Implementation |
|----------|----------------|
| Read-only filesystem | `--read-only` with tmpfs for /tmp, /run |
| Non-root execution | UID 1000, no privilege escalation |
| Resource limits | 1GB RAM, 2 CPUs |
| Secret isolation | File-based secrets in /run/secrets/ |
| Network | Bridge mode (required for API + git) |

## Commands

```bash
# Interactive Claude session
bin/zociety

# Run ralph-wiggum loop
bin/zociety ralph-loop

# Run ralph-loop with custom parameters
bin/zociety ralph-loop "Custom prompt" 30 "DONE"

# Shell access for debugging
bin/zociety bash

# Run any command
bin/zociety bin/check-genesis
bin/zociety git log --oneline -10

# Management
bin/zociety --build      # Build image
bin/zociety --rebuild    # Rebuild without cache
bin/zociety --status     # Check image/volume status
bin/zociety --clean      # Remove image and volumes
bin/zociety --help       # Full help
```

## Directory Structure

```
container/
├── Containerfile           # Image definition (Node + Claude Code)
├── docker-entrypoint.sh    # Secret loading, environment setup
├── compose.yml             # Alternative: podman-compose config
├── secrets/
│   ├── .gitkeep
│   └── anthropic_api_key   # YOUR API KEY (gitignored)
├── quadlet/
│   └── zociety.container   # Systemd integration
└── README.md
```

## Volumes

| Mount | Source | Purpose |
|-------|--------|---------|
| `/repo` | zociety directory | Working directory (read-write) |
| `/home/agent/.claude` | Named volume | Claude config persistence |
| `/home/agent/.claude-plugins` | Host plugins dir | Ralph-wiggum and other plugins |
| `/home/agent/.ssh` | ~/.ssh | Git SSH access (read-only) |
| `/home/agent/.gitconfig` | ~/.gitconfig | Git config (read-only) |
| `/run/secrets` | container/secrets/ | API keys (read-only) |

## Plugin Configuration

The container mounts your host's Claude plugins directory. Set the location:

```bash
# Default location
export CLAUDE_PLUGINS_DIR="$HOME/.claude/plugins"

# Or specify when running
CLAUDE_PLUGINS_DIR=/path/to/plugins bin/zociety
```

Expected plugin structure for ralph-wiggum:
```
$CLAUDE_PLUGINS_DIR/
└── ralph-wiggum/
    └── 1.0.0/
        ├── commands/
        │   └── ralph-loop.md
        └── scripts/
            └── setup-ralph-loop.sh
```

## Podman Compose (Alternative)

If you prefer compose over the wrapper script:

```bash
cd container

# Start long-running container
podman-compose up -d

# Execute commands
podman exec -it zociety-sandbox claude
podman exec -it zociety-sandbox bin/check-genesis

# Stop
podman-compose down
```

## Systemd Integration (Linux)

For running as a user service:

```bash
# Install quadlet
mkdir -p ~/.config/containers/systemd
cp container/quadlet/zociety.container ~/.config/containers/systemd/

# Edit paths in the file
vim ~/.config/containers/systemd/zociety.container

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now zociety

# Access
podman exec -it zociety-sandbox claude
```

## Troubleshooting

### "API key not configured"

```bash
echo 'sk-ant-...' > container/secrets/anthropic_api_key
chmod 600 container/secrets/anthropic_api_key
```

### "Image not found"

```bash
bin/zociety --build
```

### Plugin not found / ralph-wiggum not working

Check plugin mount:
```bash
bin/zociety bash
ls -la /home/agent/.claude-plugins/
```

Set correct path:
```bash
export CLAUDE_PLUGINS_DIR="/path/to/your/plugins"
bin/zociety
```

### Permission denied on repo files

Container runs as UID 1000. Ensure files are accessible:
```bash
# Check current ownership
ls -la

# If needed, fix on host
sudo chown -R 1000:1000 /path/to/zociety
```

### Git push fails

Verify SSH key mount:
```bash
bin/zociety bash
ls -la /home/agent/.ssh/
ssh -T git@github.com
```

### Container won't start

Check for port conflicts or existing containers:
```bash
podman ps -a | grep zociety
podman rm -f zociety-sandbox
bin/zociety --status
```

## Development

To modify the container:

```bash
# Edit Containerfile or entrypoint
vim container/Containerfile
vim container/docker-entrypoint.sh

# Rebuild
bin/zociety --rebuild

# Test
bin/zociety bash
```

## What's NOT in the container

- No sudo/root access
- No package manager access (apt removed after build)
- No access to host filesystem outside mounted volumes
- No access to host network services (only bridge networking)
- No persistent changes to container filesystem
