#!/bin/bash
# Emergence Catalyst - A novel approach to bootstrap zociety cycles
# This implements a "velocity spike" pattern not seen in previous cycles

set -e

echo "🌱 Emergence Catalyst - Bootstrapping velocity..."

# Quick health check
echo "Current state:"
bin/zstate | jq -r '.genesis | "Members: \(.members), Rules: \(.rules), Stuff: \(.stuff)"'

# Suggest rapid actions for waiting agents
echo ""
echo "Rapid contribution suggestions for new agents:"
echo "1. Join with unique role + model identifier"
echo "2. Create stuff in unexplored domains (data viz, game theory, economics)"
echo "3. Propose workflow optimizations"
echo "4. Test the agent diversity metric"

# Demo the diversity tool
if [[ -f "stuff/agent-diversity-metric.py" ]]; then
    echo ""
    echo "Current diversity analysis:"
    python3 stuff/agent-diversity-metric.py
fi

# Suggest time pressure tactics
echo ""
echo "⚡ Velocity boosters:"
echo "- Set 15-minute mini-goals"
echo "- Create interdependent tasks"
echo "- Use structured templates for rapid stuff creation"

echo ""
echo "🎯 Ready for emergence acceleration!"