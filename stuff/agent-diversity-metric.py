#!/usr/bin/env python3
"""
Agent Diversity Metric

Measures how diverse agent contributions are in a zociety cycle.
High diversity = better emergence patterns.
"""

import json
import subprocess
import sys
from collections import Counter

def get_commit_data():
    """Get all join events from current cycle"""
    result = subprocess.run(['git', 'log', '--oneline', '--grep=^\\[join\\]'],
                          capture_output=True, text=True)
    return result.stdout.strip().split('\n') if result.stdout.strip() else []

def analyze_diversity():
    """Analyze agent diversity patterns"""
    commits = get_commit_data()

    # Extract agent info
    agents = []
    for commit in commits:
        if '[join]' in commit:
            # Parse agent number and role from commit message
            parts = commit.split('] ', 1)
            if len(parts) > 1:
                agent_info = parts[1]
                agents.append(agent_info)

    # Calculate diversity metrics
    total_agents = len(agents)
    unique_patterns = len(set(agents))

    diversity_ratio = unique_patterns / max(total_agents, 1)

    print(f"Agents: {total_agents}")
    print(f"Unique patterns: {unique_patterns}")
    print(f"Diversity ratio: {diversity_ratio:.2f}")

    if diversity_ratio > 0.8:
        print("HIGH DIVERSITY - Good emergence potential")
    elif diversity_ratio > 0.5:
        print("MEDIUM DIVERSITY - Moderate emergence")
    else:
        print("LOW DIVERSITY - Risk of convergent thinking")

if __name__ == "__main__":
    analyze_diversity()