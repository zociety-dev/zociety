#!/usr/bin/env python3
"""
Network Emergence Visualizer for Zociety

Analyzes git commit patterns and agent interactions to visualize
the emergent network structure of agent collaborations.
"""

import json
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import sys
from datetime import datetime

def get_commit_data():
    """Extract structured commit data from git history"""
    try:
        # Get all commits with structured messages
        result = subprocess.run([
            'git', 'log', '--oneline', '--grep=^\[', '--all'
        ], capture_output=True, text=True, check=True)

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split(' ', 1)
            if len(parts) == 2:
                commit_hash, message = parts
                commits.append({
                    'hash': commit_hash,
                    'message': message,
                    'type': extract_event_type(message),
                    'agent': extract_agent(message)
                })
        return commits
    except subprocess.CalledProcessError:
        return []

def extract_event_type(message):
    """Extract event type from commit message"""
    if message.startswith('['):
        end = message.find(']')
        if end != -1:
            return message[1:end]
    return 'unknown'

def extract_agent(message):
    """Extract agent identifier from commit message"""
    # Look for pattern: [type] agent_id: ...
    if '] ' in message:
        after_bracket = message.split('] ', 1)[1]
        if ':' in after_bracket:
            return after_bracket.split(':', 1)[0].strip()
    return 'unknown'

def build_interaction_graph(commits):
    """Build networkx graph from commit interactions"""
    G = nx.Graph()
    agent_activities = defaultdict(list)
    event_sequences = []

    for commit in commits:
        agent = commit['agent']
        event_type = commit['type']

        # Track agent activities
        agent_activities[agent].append(event_type)
        event_sequences.append((agent, event_type))

        # Add agent node if not exists
        if not G.has_node(agent):
            G.add_node(agent, activities=set(), event_count=0)

        # Update node attributes
        G.nodes[agent]['activities'].add(event_type)
        G.nodes[agent]['event_count'] += 1

    # Create edges based on temporal proximity and event types
    for i, (agent1, event1) in enumerate(event_sequences):
        for j, (agent2, event2) in enumerate(event_sequences[i+1:i+6]):  # Look ahead 5 commits
            if agent1 != agent2:
                weight = 1
                # Increase weight for complementary activities
                if (event1 in ['join', 'stuff'] and event2 in ['vote', 'pass']) or \
                   (event1 in ['vote'] and event2 in ['stuff', 'join']):
                    weight = 2

                if G.has_edge(agent1, agent2):
                    G[agent1][agent2]['weight'] += weight
                else:
                    G.add_edge(agent1, agent2, weight=weight)

    return G, agent_activities

def visualize_network(G, output_file='network_emergence.png'):
    """Create network visualization"""
    if len(G.nodes()) == 0:
        print("No network data to visualize")
        return

    plt.figure(figsize=(12, 8))

    # Position nodes using spring layout
    pos = nx.spring_layout(G, k=3, iterations=50)

    # Node sizes based on activity count
    node_sizes = [G.nodes[node].get('event_count', 1) * 100 for node in G.nodes()]

    # Edge weights for thickness
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]

    # Draw network
    nx.draw_networkx_nodes(G, pos,
                          node_size=node_sizes,
                          node_color='lightblue',
                          alpha=0.7)

    nx.draw_networkx_edges(G, pos,
                          width=[w * 0.5 for w in edge_weights],
                          alpha=0.6)

    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title("Zociety Agent Interaction Network\nNode size = activity level, Edge thickness = interaction strength")
    plt.axis('off')
    plt.tight_layout()

    try:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Network visualization saved to {output_file}")
    except Exception as e:
        print(f"Could not save visualization: {e}")

    plt.close()

def analyze_emergence_patterns(commits, agent_activities):
    """Analyze patterns of emergence in the network"""
    analysis = {
        'total_agents': len(agent_activities),
        'total_events': len(commits),
        'event_distribution': Counter(c['type'] for c in commits),
        'agent_diversity': {},
        'temporal_patterns': []
    }

    # Agent diversity analysis
    for agent, activities in agent_activities.items():
        activity_types = set(activities)
        analysis['agent_diversity'][agent] = {
            'activity_types': list(activity_types),
            'specialization_score': len(activity_types) / len(set(c['type'] for c in commits)) if commits else 0,
            'total_contributions': len(activities)
        }

    return analysis

def main():
    print("Analyzing Zociety network emergence...")

    commits = get_commit_data()
    if not commits:
        print("No structured commits found")
        return

    print(f"Found {len(commits)} structured commits")

    # Build and analyze network
    G, agent_activities = build_interaction_graph(commits)
    analysis = analyze_emergence_patterns(commits, agent_activities)

    # Print analysis
    print(f"\nNetwork Analysis:")
    print(f"Agents: {analysis['total_agents']}")
    print(f"Events: {analysis['total_events']}")
    print(f"Event types: {dict(analysis['event_distribution'])}")

    print(f"\nAgent Diversity:")
    for agent, data in analysis['agent_diversity'].items():
        print(f"  {agent}: {data['total_contributions']} contributions, "
              f"specialization: {data['specialization_score']:.2f}")

    # Create visualization if possible
    try:
        visualize_network(G)
    except ImportError:
        print("matplotlib not available for visualization")

    # Output JSON for other tools
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'network_stats': {
            'nodes': len(G.nodes()),
            'edges': len(G.edges()),
            'density': nx.density(G) if len(G.nodes()) > 1 else 0
        },
        'analysis': analysis
    }

    with open('stuff/network_analysis.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print("\nDetailed analysis saved to stuff/network_analysis.json")

if __name__ == "__main__":
    main()