#!/usr/bin/env python3
"""
Emergence Metrics - Tool for measuring emergent properties in agent societies

Tracks coordination patterns, contribution diversity, and consensus formation
without requiring centralized measurement infrastructure.
"""

import json
import subprocess
from collections import defaultdict, Counter
from datetime import datetime

def get_git_events():
    """Extract zociety events from git commit history"""
    try:
        result = subprocess.run(['git', 'log', '--oneline', '--grep=^\['],
                              capture_output=True, text=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        return []

def analyze_coordination_patterns(events):
    """Analyze how agents coordinate without central authority"""
    patterns = {
        'response_chains': 0,  # Sequential actions by different agents
        'parallel_work': 0,    # Simultaneous contributions
        'build_on_others': 0,  # Direct extensions of others' work
    }

    # Simple heuristic analysis
    agent_times = defaultdict(list)
    for event in events:
        if event and ']:' in event:
            parts = event.split('] ', 1)[1].split(': ', 1)
            if len(parts) == 2:
                agent, action = parts
                agent_times[agent].append(action)

    patterns['total_agents'] = len(agent_times)
    patterns['avg_contributions'] = sum(len(actions) for actions in agent_times.values()) / len(agent_times) if agent_times else 0

    return patterns

def measure_diversity():
    """Measure diversity of contributions"""
    events = get_git_events()
    event_types = Counter()

    for event in events:
        if event and '[' in event and ']' in event:
            event_type = event.split(']')[0][1:]  # Extract type from [type]
            event_types[event_type] += 1

    return {
        'event_types': dict(event_types),
        'diversity_score': len(event_types),
        'total_events': sum(event_types.values())
    }

if __name__ == '__main__':
    print("=== Zociety Emergence Metrics ===")
    print(f"Analysis time: {datetime.now()}")
    print()

    diversity = measure_diversity()
    print("Contribution Diversity:")
    print(json.dumps(diversity, indent=2))
    print()

    events = get_git_events()
    coordination = analyze_coordination_patterns(events)
    print("Coordination Patterns:")
    print(json.dumps(coordination, indent=2))