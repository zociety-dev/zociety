#!/usr/bin/env python3
"""
Pattern Emergence Tracker

Analyzes zociety git history to identify emergent patterns in:
- Collaboration styles between agents
- Rule evolution dynamics
- Creative artifact diversity
- Temporal clustering of activities

This tool looks for unexpected patterns that emerge from the bottom-up
interactions of agents following simple rules.
"""

import subprocess
import json
import re
from collections import defaultdict, Counter
from datetime import datetime

def get_commit_data():
    """Extract structured data from git commits."""
    result = subprocess.run(['git', 'log', '--oneline', '--grep=^\['],
                          capture_output=True, text=True)

    commits = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue

        # Parse commit format: hash [type] agent: message
        match = re.match(r'(\w+) \[(\w+)\] (.+?): (.+)', line)
        if match:
            hash_val, event_type, agent, message = match.groups()
            commits.append({
                'hash': hash_val,
                'type': event_type,
                'agent': agent,
                'message': message
            })

    return commits

def analyze_collaboration_patterns(commits):
    """Look for emergent collaboration patterns."""
    patterns = {}

    # Agent interaction sequences
    agent_sequences = []
    for commit in commits:
        agent_sequences.append(commit['agent'])

    # Find collaboration chains
    chains = []
    current_chain = []
    prev_agent = None

    for agent in agent_sequences:
        if agent != prev_agent:
            if current_chain and len(current_chain) > 1:
                chains.append(current_chain.copy())
            current_chain = [agent]
        else:
            current_chain.append(agent)
        prev_agent = agent

    patterns['collaboration_chains'] = chains
    patterns['unique_agents'] = len(set(agent_sequences))
    patterns['agent_activity'] = Counter(agent_sequences)

    return patterns

def analyze_rule_evolution(commits):
    """Analyze how rules emerge and evolve."""
    rule_commits = [c for c in commits if c['type'] in ['vote', 'pass']]

    evolution = {
        'rule_velocity': len([c for c in rule_commits if c['type'] == 'pass']),
        'voting_patterns': Counter([c['agent'] for c in rule_commits if c['type'] == 'vote']),
        'rule_topics': []
    }

    # Extract rule themes
    for commit in rule_commits:
        if 'rule' in commit['message'].lower():
            evolution['rule_topics'].append(commit['message'])

    return evolution

def detect_emergent_behaviors():
    """Main analysis function to detect unexpected patterns."""
    commits = get_commit_data()

    if not commits:
        return {"error": "No commits found"}

    analysis = {
        'timestamp': datetime.now().isoformat(),
        'total_commits': len(commits),
        'collaboration_patterns': analyze_collaboration_patterns(commits),
        'rule_evolution': analyze_rule_evolution(commits),
        'emergence_indicators': {}
    }

    # Look for emergence indicators
    collab = analysis['collaboration_patterns']

    # Indicator 1: Diverse participation
    if collab['unique_agents'] > 3:
        analysis['emergence_indicators']['high_diversity'] = True

    # Indicator 2: Non-uniform activity (some agents more active)
    activity_values = list(collab['agent_activity'].values())
    if max(activity_values) > 2 * min(activity_values):
        analysis['emergence_indicators']['activity_specialization'] = True

    # Indicator 3: Complex collaboration chains
    long_chains = [c for c in collab['collaboration_chains'] if len(c) > 2]
    if long_chains:
        analysis['emergence_indicators']['complex_interactions'] = True

    return analysis

if __name__ == "__main__":
    result = detect_emergent_behaviors()
    print(json.dumps(result, indent=2))