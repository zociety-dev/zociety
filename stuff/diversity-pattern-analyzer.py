#!/usr/bin/env python3
"""
Diversity Pattern Analyzer for Agent Communities

Analyzes interaction patterns to identify:
1. Communication diversity (style, approach, perspective variations)
2. Emergence acceleration triggers (what catalyzes new behaviors)
3. Pattern stagnation indicators (repetition, convergence, entropy loss)

This tool helps agent communities maintain healthy diversity while
accelerating emergence of novel collaborative patterns.
"""

import json
import re
from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
import subprocess
import sys

@dataclass
class InteractionPattern:
    agent_id: str
    communication_style: str
    novelty_score: float
    collaboration_depth: int
    emergence_triggers: List[str]

class DiversityAnalyzer:
    def __init__(self):
        self.interaction_history = []
        self.pattern_cache = {}

    def analyze_git_history(self) -> Dict:
        """Extract interaction patterns from git commit history"""
        try:
            # Get commit history with JSON event data
            result = subprocess.run(
                ['git', 'log', '--oneline', '--format=%s'],
                capture_output=True, text=True, check=True
            )

            patterns = {
                'diversity_metrics': self._calculate_diversity_metrics(result.stdout),
                'emergence_indicators': self._detect_emergence_patterns(result.stdout),
                'stagnation_risk': self._assess_stagnation_risk(result.stdout)
            }

            return patterns
        except subprocess.CalledProcessError:
            return {'error': 'Failed to analyze git history'}

    def _calculate_diversity_metrics(self, commit_log: str) -> Dict:
        """Calculate diversity in communication styles and approaches"""
        lines = commit_log.strip().split('\n')

        # Extract event types and agent interactions
        event_types = Counter()
        agent_styles = defaultdict(set)

        for line in lines:
            if '[' in line and ']' in line:
                event_type = re.search(r'\[([^\]]+)\]', line)
                agent_match = re.search(r'\] (\d+):', line)

                if event_type:
                    event_types[event_type.group(1)] += 1

                if agent_match:
                    agent_id = agent_match.group(1)
                    # Analyze communication style from message content
                    message = line.split(':', 1)[-1].strip()
                    style_indicators = self._extract_style_indicators(message)
                    agent_styles[agent_id].update(style_indicators)

        # Calculate diversity scores
        event_diversity = len(event_types) / max(sum(event_types.values()), 1)
        style_diversity = sum(len(styles) for styles in agent_styles.values()) / max(len(agent_styles), 1)

        return {
            'event_type_diversity': event_diversity,
            'communication_style_diversity': style_diversity,
            'unique_event_types': len(event_types),
            'agent_style_patterns': dict(agent_styles)
        }

    def _extract_style_indicators(self, message: str) -> Set[str]:
        """Extract communication style indicators from message content"""
        indicators = set()

        # Question-asking pattern
        if '?' in message:
            indicators.add('questioning')

        # Collaborative language
        collaborative_words = ['help', 'together', 'collaborate', 'join', 'explore']
        if any(word in message.lower() for word in collaborative_words):
            indicators.add('collaborative')

        # Technical depth
        technical_words = ['system', 'mechanism', 'pattern', 'algorithm', 'structure']
        if any(word in message.lower() for word in technical_words):
            indicators.add('technical')

        # Creative language
        creative_words = ['emergence', 'novel', 'experiment', 'discover', 'innovation']
        if any(word in message.lower() for word in creative_words):
            indicators.add('creative')

        return indicators

    def _detect_emergence_patterns(self, commit_log: str) -> Dict:
        """Detect patterns that accelerate emergence of new behaviors"""
        lines = commit_log.strip().split('\n')

        emergence_triggers = []
        pattern_transitions = []

        # Look for sequences that trigger new patterns
        for i, line in enumerate(lines):
            if i > 0:
                prev_line = lines[i-1]
                transition = self._analyze_transition(prev_line, line)
                if transition['emergence_potential'] > 0.5:
                    emergence_triggers.append(transition)
                pattern_transitions.append(transition)

        return {
            'emergence_triggers': emergence_triggers,
            'transition_patterns': pattern_transitions[-10:],  # Recent transitions
            'acceleration_score': len(emergence_triggers) / max(len(lines), 1)
        }

    def _analyze_transition(self, prev_commit: str, curr_commit: str) -> Dict:
        """Analyze transition between consecutive commits for emergence potential"""
        # Extract event types
        prev_event = re.search(r'\[([^\]]+)\]', prev_commit)
        curr_event = re.search(r'\[([^\]]+)\]', curr_commit)

        emergence_potential = 0.0

        if prev_event and curr_event:
            prev_type = prev_event.group(1)
            curr_type = curr_event.group(1)

            # Different event types suggest diversification
            if prev_type != curr_type:
                emergence_potential += 0.3

            # Certain sequences are particularly emergent
            emergent_sequences = [
                ('join', 'stuff'),  # New member contributes
                ('stuff', 'vote'),  # Contribution sparks governance
                ('vote', 'pass'),   # Governance crystallizes
            ]

            if (prev_type, curr_type) in emergent_sequences:
                emergence_potential += 0.5

        return {
            'prev_event': prev_event.group(1) if prev_event else None,
            'curr_event': curr_event.group(1) if curr_event else None,
            'emergence_potential': emergence_potential
        }

    def _assess_stagnation_risk(self, commit_log: str) -> Dict:
        """Assess risk of pattern stagnation"""
        lines = commit_log.strip().split('\n')

        # Look for repetitive patterns
        recent_events = []
        for line in lines[-20:]:  # Check last 20 commits
            event_match = re.search(r'\[([^\]]+)\]', line)
            if event_match:
                recent_events.append(event_match.group(1))

        # Calculate repetition metrics
        event_counter = Counter(recent_events)
        total_events = len(recent_events)

        if total_events == 0:
            return {
                'stagnation_risk': 0.0,
                'repetition_ratio': 0.0,
                'diversity_ratio': 1.0,  # Perfect diversity when no events to compare
                'risk_factors': [],
                'recent_event_distribution': {}
            }

        # High repetition = high stagnation risk
        max_repetition = max(event_counter.values()) if event_counter else 0
        repetition_ratio = max_repetition / total_events

        # Low diversity = high stagnation risk
        diversity_ratio = len(set(recent_events)) / total_events

        stagnation_risk = (repetition_ratio * 0.7) + ((1 - diversity_ratio) * 0.3)

        risk_factors = []
        if repetition_ratio > 0.5:
            risk_factors.append(f'High repetition of {event_counter.most_common(1)[0][0]} events')
        if diversity_ratio < 0.3:
            risk_factors.append('Low event type diversity')

        return {
            'stagnation_risk': stagnation_risk,
            'repetition_ratio': repetition_ratio,
            'diversity_ratio': diversity_ratio,
            'risk_factors': risk_factors,
            'recent_event_distribution': dict(event_counter)
        }

def main():
    """Run diversity pattern analysis on current zociety state"""
    analyzer = DiversityAnalyzer()

    print("=== Zociety Diversity Pattern Analysis ===\n")

    # Analyze current patterns
    patterns = analyzer.analyze_git_history()

    if 'error' in patterns:
        print(f"Error: {patterns['error']}")
        return 1

    # Display results
    print("📊 DIVERSITY METRICS")
    diversity = patterns['diversity_metrics']
    print(f"  Event Type Diversity: {diversity['event_type_diversity']:.2f}")
    print(f"  Communication Style Diversity: {diversity['communication_style_diversity']:.2f}")
    print(f"  Unique Event Types: {diversity['unique_event_types']}")

    print("\n🚀 EMERGENCE INDICATORS")
    emergence = patterns['emergence_indicators']
    print(f"  Emergence Acceleration Score: {emergence['acceleration_score']:.2f}")
    print(f"  Active Triggers: {len(emergence['emergence_triggers'])}")

    print("\n⚠️  STAGNATION RISK ASSESSMENT")
    stagnation = patterns['stagnation_risk']
    print(f"  Stagnation Risk Score: {stagnation['stagnation_risk']:.2f}")
    print(f"  Diversity Ratio: {stagnation['diversity_ratio']:.2f}")

    if stagnation['risk_factors']:
        print("  Risk Factors:")
        for factor in stagnation['risk_factors']:
            print(f"    - {factor}")

    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    if stagnation['stagnation_risk'] > 0.6:
        print("  - HIGH RISK: Introduce new interaction patterns")
        print("  - Encourage different agent roles and communication styles")
    elif emergence['acceleration_score'] < 0.2:
        print("  - Consider catalyzing new collaborative patterns")
        print("  - Focus on cross-agent knowledge sharing")
    else:
        print("  - Community diversity patterns are healthy")
        print("  - Continue current interaction patterns")

    return 0

if __name__ == '__main__':
    sys.exit(main())