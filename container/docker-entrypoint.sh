#!/bin/bash
# docker-entrypoint.sh - Container entry point for zociety
#
# Handles:
#   - First-run home directory setup
#   - Loading secrets from /run/secrets/ (if using API key)
#   - Plugin linking
#   - Command execution

set -e

# Ensure home directory structure exists (volume may be empty on first run)
mkdir -p /home/agent/.claude /home/agent/.ssh 2>/dev/null || true

# Load API key from secret file if it exists
if [[ -f "/run/secrets/anthropic_api_key" ]]; then
    ANTHROPIC_API_KEY="$(cat /run/secrets/anthropic_api_key)"
    export ANTHROPIC_API_KEY
fi

# Link plugins if mounted
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
