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
│           Volumes: repo, credentials, plugins           │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Configure credentials (see "Setting Up Credentials" below)

# 2. Build the image
bin/zociety --build

# 3. Run interactive Claude session
bin/zociety

# 4. Or run the agent loop directly
bin/zociety ralph-loop
```

## Setting Up Credentials

The container uses dedicated credentials for the zociety agent identity. All files go in `container/secrets/` (gitignored).

### API Key (required)

```bash
echo 'sk-ant-api03-...' > container/secrets/anthropic_api_key
chmod 600 container/secrets/anthropic_api_key
```

### SSH Key (required for GitHub push)

Generate a dedicated SSH key for agent@zociety.dev:

```bash
ssh-keygen -t ed25519 -C "agent@zociety.dev" \
    -f container/secrets/zociety_ssh_key -N ""
chmod 600 container/secrets/zociety_ssh_key
```

Then add the public key to the zociety GitHub account:
1. Copy the contents of `container/secrets/zociety_ssh_key.pub`
2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste the public key

### GPG Signing Key (for verified commits)

Generate a GPG key for agent@zociety.dev:

```bash
gpg --full-generate-key
# Choose: RSA and RSA, 4096 bits, no expiration
# Name: Zociety Agent
# Email: agent@zociety.dev
```

Export the key:

```bash
gpg --export-secret-keys --armor agent@zociety.dev > container/secrets/gpg_signing_key.asc
chmod 600 container/secrets/gpg_signing_key.asc
```

Add the public key to GitHub for verified commits:

```bash
gpg --export --armor agent@zociety.dev
# Copy output → GitHub Settings → SSH and GPG keys → New GPG key
```

### Summary: Required Files

```
container/secrets/
├── anthropic_api_key       # API key (required)
├── zociety_ssh_key         # Private SSH key (required for push)
├── zociety_ssh_key.pub     # Public SSH key (add to GitHub)
├── gpg_signing_key.asc     # GPG key (for verified commits)
└── github_token            # GitHub PAT (for gh CLI, optional)
```

## GitHub Account Setup

The zociety agent needs its own GitHub account to push commits independently.

### 1. Email Access

Set up forwarding from `agent@zociety.dev` to yourself (temporarily or permanently). This lets verification emails reach you while keeping the agent's email as the account identity.

### 2. Human-Assisted Registration

You create the account (CAPTCHA requires human eyes):
- Username: `zociety-dev`
- Email: `agent@zociety.dev`
- Complete CAPTCHA, click verification link

This is the one step that genuinely requires a human.

### 3. Add SSH Key to Account

```bash
cat container/secrets/zociety_ssh_key.pub
# Copy output → GitHub Settings → SSH keys → New
```

### 4. Add GPG Key to Account (for verified commits)

```bash
gpg --export --armor agent@zociety.dev
# Copy output → GitHub Settings → GPG keys → New
```

### 5. Create GitHub Token (for API/CLI access)

Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens:
- Token name: `zociety-container`
- Expiration: 90 days (or custom)
- Repository access: Select `zociety-dev/zociety`
- Permissions: Contents (read/write), Metadata (read)

Save the token:

```bash
echo "github_pat_xxxxxxxxxxxx" > container/secrets/github_token
chmod 600 container/secrets/github_token
```

### 6. Authenticate gh CLI

**Inside the container:** Authentication is automatic. The entrypoint exports `GITHUB_TOKEN` and `GH_TOKEN` from `/run/secrets/github_token`, and `gh` reads these env vars.

```bash
bin/zociety bash
gh auth status  # Should show logged in
```

**Outside the container (on host):** Use `--with-token` to authenticate non-interactively:

```bash
# Authenticate from the token file
gh auth login --with-token < container/secrets/github_token

# Or pipe it
cat container/secrets/github_token | gh auth login --with-token

# Verify
gh auth status
```

To set the git protocol explicitly (SSH vs HTTPS):

```bash
gh auth login --with-token --git-protocol ssh < container/secrets/github_token
```

The `--with-token` flag tells `gh` to read a PAT from stdin rather than launching the interactive browser flow.

### 7. Update Remote URL

Switch the repo to use SSH with the zociety account:

```bash
git remote set-url origin git@github.com:zociety-dev/zociety.git
```

### What the Agent Can Do Independently

Once set up:
- Push/pull via SSH
- Create repos, issues, PRs via `gh` CLI
- Manage its own SSH/GPG keys via API
- Rotate tokens (with appropriate scopes)

### What Still Needs a Human

- Initial account creation (CAPTCHA)
- Recovery if 2FA device is lost
- Responding to GitHub support/abuse inquiries

## Security Properties

| Property | Implementation |
|----------|----------------|
| Read-only filesystem | `--read-only` with tmpfs for /tmp, /run |
| Non-root execution | UID 1000, no privilege escalation |
| Resource limits | 1GB RAM, 2 CPUs |
| Credential isolation | File-based in /run/secrets/ |
| Dedicated identity | Own SSH/GPG keys, not host credentials |
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
├── docker-entrypoint.sh    # Credential loading, identity setup
├── compose.yml             # Alternative: podman-compose config
├── secrets/
│   ├── .gitkeep
│   ├── anthropic_api_key   # API key (gitignored)
│   ├── zociety_ssh_key     # SSH private key (gitignored)
│   ├── zociety_ssh_key.pub # SSH public key (gitignored)
│   ├── gpg_signing_key.asc # GPG key (gitignored)
│   └── github_token        # GitHub PAT (gitignored)
├── quadlet/
│   └── zociety.container   # Systemd integration
└── README.md
```

## Volumes

| Mount | Source | Purpose |
|-------|--------|---------|
| `/repo` | zociety directory | Working directory (read-write) |
| `/home/agent` | Named volume | Home dir persistence (.gnupg, .claude, etc.) |
| `/home/agent/.claude-plugins` | Host plugins dir | Ralph-wiggum and other plugins |
| `/run/secrets` | container/secrets/ | All credentials (read-only) |

Note: The container does NOT mount host SSH keys or gitconfig. The agent has its own identity configured in the entrypoint script.

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

### Git push fails (SSH)

Verify SSH key is loaded:
```bash
bin/zociety bash
ls -la /home/agent/.ssh/
cat /home/agent/.ssh/config
ssh -T git@github.com
```

Check that the public key is added to GitHub.

### Git push fails (wrong remote)

Check the remote is using SSH URL:
```bash
git remote -v
# Should show: git@github.com:zociety-dev/zociety.git
# Not: https://github.com/zociety-dev/zociety.git

# Fix if needed:
git remote set-url origin git@github.com:zociety-dev/zociety.git
```

### GPG signing fails

The GPG key is imported on first use, but the `.gnupg` directory must exist. If signing fails:

```bash
bin/zociety bash

# Check if key is imported
gpg --list-secret-keys

# If empty, import manually
gpg --batch --import /run/secrets/gpg_signing_key.asc

# Verify
gpg --list-secret-keys agent@zociety.dev
```

The home volume persists `.gnupg`, so this only needs to happen once. If you see "No secret key" errors after a `--clean`, just import again.

To commit without signing (temporary workaround):
```bash
git commit --no-gpg-sign -m "message"
```

### Commits not showing as verified on GitHub

1. GPG key must be imported in container (see above)
2. Public key must be added to GitHub account
3. Email must match: `agent@zociety.dev`

Check git config:
```bash
git config --global user.signingkey
git config --global commit.gpgsign
git config --global user.email
```

### gh CLI not authenticated

**Inside container:**
```bash
bin/zociety bash
echo $GH_TOKEN | head -c 20  # Should show token prefix
gh auth status
```

If `GH_TOKEN` is empty, check that the secret file exists:
```bash
ls -la /run/secrets/github_token
```

**Outside container:**
```bash
# Re-authenticate
gh auth login --with-token < container/secrets/github_token
gh auth status
```

If you see "not logged into any GitHub hosts", the token may be invalid or expired. Generate a new one in GitHub Settings → Developer settings → Personal access tokens.

### Container won't start

Check for port conflicts or existing containers:
```bash
podman ps -a | grep zociety
podman rm -f zociety-sandbox
bin/zociety --status
```

### GPG key not persisting between sessions

The home volume (`zociety-claude-home`) stores `.gnupg`. If you ran `bin/zociety --clean`, the volume was deleted. Re-import:

```bash
bin/zociety bash
gpg --batch --import /run/secrets/gpg_signing_key.asc
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
- No access to host SSH keys or git identity (uses dedicated agent identity)
