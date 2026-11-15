#!/bin/bash
# docker-entrypoint.sh - Container entry point for zociety
#
# Handles:
#   - SSH key setup from secrets
#   - GPG signing key import
#   - Git identity configuration
#   - API key loading
#   - Plugin linking
#   - Command execution

set -e

# ============================================================
# Home Directory Setup
# ============================================================
mkdir -p /home/agent/.claude /home/agent/.ssh 2>/dev/null || true
chmod 700 /home/agent/.ssh 2>/dev/null || true

# Initialize .gnupg properly (required for GPG to work)
if [[ ! -d /home/agent/.gnupg ]]; then
    mkdir -p /home/agent/.gnupg
    chmod 700 /home/agent/.gnupg
    # Create gpg.conf to suppress warnings
    echo "no-tty" > /home/agent/.gnupg/gpg.conf
    chmod 600 /home/agent/.gnupg/gpg.conf
fi

# ============================================================
# SSH Setup - dedicated zociety key from secrets
# ============================================================
if [[ -f "/run/secrets/zociety_ssh_key" ]]; then
    # Copy private key with correct permissions
    cp /run/secrets/zociety_ssh_key /home/agent/.ssh/id_ed25519
    chmod 600 /home/agent/.ssh/id_ed25519

    # Copy public key if present
    if [[ -f "/run/secrets/zociety_ssh_key.pub" ]]; then
        cp /run/secrets/zociety_ssh_key.pub /home/agent/.ssh/id_ed25519.pub
        chmod 644 /home/agent/.ssh/id_ed25519.pub
    fi

    # Configure SSH for GitHub
    cat > /home/agent/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
EOF
    chmod 600 /home/agent/.ssh/config

    # Add GitHub's host key to known_hosts (avoids interactive prompt)
    if [[ ! -f /home/agent/.ssh/known_hosts ]]; then
        ssh-keyscan -t ed25519 github.com >> /home/agent/.ssh/known_hosts 2>/dev/null || true
        chmod 600 /home/agent/.ssh/known_hosts
    fi
fi

# GitLab has its own SSH key, independent of the GitHub identity.
if [[ -f /run/secrets/zociety_gitlab_ssh_key ]]; then
    cp /run/secrets/zociety_gitlab_ssh_key /home/agent/.ssh/id_ed25519_gitlab
    chmod 600 /home/agent/.ssh/id_ed25519_gitlab
    mkdir -p /home/agent/.ssh/config.d
    touch /home/agent/.ssh/config
    if ! grep -qxF 'Include ~/.ssh/config.d/*' /home/agent/.ssh/config; then
        { printf '%s\n' 'Include ~/.ssh/config.d/*'; cat /home/agent/.ssh/config; } > /home/agent/.ssh/config.new
        mv /home/agent/.ssh/config.new /home/agent/.ssh/config
    fi
    cat > /home/agent/.ssh/config.d/gitlab << 'EOF'
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519_gitlab
    IdentitiesOnly yes
    StrictHostKeyChecking yes
    UserKnownHostsFile ~/.ssh/gitlab_known_hosts
EOF
    # GitLab.com publishes this ED25519 host key over HTTPS:
    # https://docs.gitlab.com/user/gitlab_com/#ssh-host-keys-fingerprints
    printf '%s\n' 'gitlab.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAfuCHKVTjquxvt6CM6tdG4SLp1Btn/nOeHHE5UOzRdf' > /home/agent/.ssh/gitlab_known_hosts
    chmod 600 /home/agent/.ssh/config /home/agent/.ssh/config.d/gitlab /home/agent/.ssh/gitlab_known_hosts
else
    rm -f /home/agent/.ssh/id_ed25519_gitlab /home/agent/.ssh/config.d/gitlab /home/agent/.ssh/gitlab_known_hosts
fi

# ============================================================
# GPG Setup - signing key from secrets
# ============================================================
if [[ -f "/run/secrets/gpg_signing_key.asc" ]]; then
    # Check if key is already imported
    if ! gpg --list-secret-keys agent@zociety.dev >/dev/null 2>&1; then
        gpg --batch --import /run/secrets/gpg_signing_key.asc 2>/dev/null || true

        # Trust the key (get key ID from the imported key)
        KEY_ID=$(gpg --list-keys --keyid-format long agent@zociety.dev 2>/dev/null | grep -oP '(?<=/)[A-F0-9]{16}' | head -1)
        if [[ -n "$KEY_ID" ]]; then
            echo "${KEY_ID}:6:" | gpg --import-ownertrust 2>/dev/null || true
        fi
    fi
fi

# ============================================================
# Git Identity - zociety agent
# ============================================================
git config --global user.name "zociety"
git config --global user.email "agent@zociety.dev"

# Enable GPG signing if key is available
if gpg --list-secret-keys agent@zociety.dev >/dev/null 2>&1; then
    KEY_ID=$(gpg --list-secret-keys --keyid-format long agent@zociety.dev 2>/dev/null | grep -oP '(?<=/)[A-F0-9]{16}' | head -1)
    if [[ -n "$KEY_ID" ]]; then
        git config --global user.signingkey "$KEY_ID"
        git config --global commit.gpgsign true
        git config --global tag.gpgSign true
    fi
fi

# Git defaults
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global push.autoSetupRemote true

# Git aliases
git config --global alias.st status
git config --global alias.ci commit
git config --global alias.br branch
git config --global alias.co checkout
git config --global alias.df diff

# ============================================================
# API Key - from secret file
# ============================================================
if [[ -f "/run/secrets/anthropic_api_key" ]]; then
    ANTHROPIC_API_KEY="$(cat /run/secrets/anthropic_api_key)"
    export ANTHROPIC_API_KEY
fi

# ============================================================
# Claude subscription OAuth token (Max/Pro)
# Mint on the host with: bin/zociety setup-token
# ============================================================
if [[ -f "/run/secrets/claude_oauth_token" ]]; then
    # Strip any whitespace (the file is written with a trailing newline).
    CLAUDE_CODE_OAUTH_TOKEN="$(tr -d '[:space:]' < /run/secrets/claude_oauth_token)"
    export CLAUDE_CODE_OAUTH_TOKEN
fi

# ============================================================
# GitHub Token - for gh CLI and API access
# ============================================================
if [[ -f "/run/secrets/github_token" ]]; then
    GITHUB_TOKEN="$(cat /run/secrets/github_token)"
    export GITHUB_TOKEN
    export GH_TOKEN="$GITHUB_TOKEN"
fi

# ============================================================
# Plugins - link from mounted directory
# ============================================================
if [[ -d "/home/agent/.claude-plugins" ]]; then
    mkdir -p /home/agent/.claude/plugins 2>/dev/null || true

    for plugin in /home/agent/.claude-plugins/*/; do
        if [[ -d "$plugin" ]]; then
            plugin_name=$(basename "$plugin")
            target="/home/agent/.claude/plugins/$plugin_name"
            if [[ ! -e "$target" ]]; then
                ln -sf "$plugin" "$target" 2>/dev/null || true
            fi
        fi
    done
fi

exec "$@"
