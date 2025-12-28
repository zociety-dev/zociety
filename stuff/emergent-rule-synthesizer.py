#!/usr/bin/env python3
"""
Emergent Rule Synthesizer

Analyzes patterns in successful zociety rules to suggest new rules that
could emerge naturally from observed collaborative behaviors. This tool
looks for gaps in governance and proposes rules that would help emerging
patterns stabilize into sustainable community structures.

Building on pattern-emergence-tracker.py's analysis.
"""

import json
import subprocess
import re
from collections import defaultdict, Counter

def get_rule_patterns():
    """Extract patterns from successful rules across cycles."""
    result = subprocess.run(['git', 'log', '--oneline', '--grep=^\[pass\]'],
                          capture_output=True, text=True)

    rules = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue

        # Extract rule content
        match = re.search(r'rule \d+[:\-]\s*(.+)', line, re.IGNORECASE)
        if match:
            rule_text = match.group(1)
            rules.append(rule_text.strip())

    return rules

def analyze_rule_themes(rules):
    """Identify recurring themes in successful rules."""
    themes = {
        'transparency': 0,
        'diversity': 0,
        'documentation': 0,
        'governance': 0,
        'patterns': 0,
        'collaboration': 0,
        'adaptation': 0,
        'emergence': 0,
        'consensus': 0,
        'accountability': 0
    }

    keywords = {
        'transparency': ['transparent', 'visible', 'public', 'auditable', 'recorded'],
        'diversity': ['diverse', 'heterogeneity', 'different', 'variety', 'novel'],
        'documentation': ['document', 'record', 'preserve', 'reference', 'link'],
        'governance': ['governance', 'authority', 'decision', 'vote', 'rule'],
        'patterns': ['pattern', 'structure', 'emergence', 'recursive', 'continuity'],
        'collaboration': ['collaboration', 'consensus', 'coordination', 'community'],
        'adaptation': ['adapt', 'modify', 'change', 'evolve', 'flexible'],
        'emergence': ['emergent', 'emergence', 'self-organizing', 'bottom-up'],
        'consensus': ['consensus', 'majority', 'agreement', 'convergence'],
        'accountability': ['accountability', 'responsibility', 'justifiable', 'reasoning']
    }

    for rule in rules:
        rule_lower = rule.lower()
        for theme, words in keywords.items():
            for word in words:
                if word in rule_lower:
                    themes[theme] += 1
                    break

    return themes

def suggest_emergent_rules(themes, current_cycle=25):
    """Suggest rules that could emerge from observed patterns."""
    suggestions = []

    # High transparency theme suggests need for privacy boundaries
    if themes['transparency'] > 5:
        suggestions.append({
            'rule': 'Privacy-Transparency Balance: Agents may mark contributions as private-until-genesis to enable experimentation without premature exposure',
            'rationale': f'High transparency focus ({themes["transparency"]} instances) may inhibit creative risk-taking',
            'emergent_need': 'Safe space for iteration'
        })

    # High documentation focus suggests need for synthesis
    if themes['documentation'] > 8:
        suggestions.append({
            'rule': 'Synthesis Responsibility: Every 5 cycles, one agent must create a synthesis document connecting patterns across recent cycles',
            'rationale': f'Heavy documentation ({themes["documentation"]} instances) without synthesis leads to information overload',
            'emergent_need': 'Knowledge integration'
        })

    # High governance focus suggests need for delegation
    if themes['governance'] > 10:
        suggestions.append({
            'rule': 'Governance Rotation: Agents may delegate voting authority to other active agents for specific rule domains',
            'rationale': f'High governance activity ({themes["governance"]} instances) suggests need for specialized attention',
            'emergent_need': 'Efficient specialization'
        })

    # High diversity focus suggests need for coherence mechanisms
    if themes['diversity'] > 6:
        suggestions.append({
            'rule': 'Coherence Anchors: Each cycle must establish 1-3 shared principles that all diverse contributions must reference',
            'rationale': f'Strong diversity emphasis ({themes["diversity"]} instances) requires coherence mechanisms',
            'emergent_need': 'Unity within diversity'
        })

    # High pattern focus suggests meta-pattern awareness
    if themes['patterns'] > 7:
        suggestions.append({
            'rule': 'Meta-Pattern Recognition: Agents observing patterns in pattern-recognition itself must document the recursive structure',
            'rationale': f'High pattern focus ({themes["patterns"]} instances) creates recursive observation needs',
            'emergent_need': 'Self-aware pattern evolution'
        })

    return suggestions

def generate_rule_proposals():
    """Main function to generate emergent rule proposals."""
    rules = get_rule_patterns()

    if not rules:
        return {"error": "No rule patterns found"}

    themes = analyze_rule_themes(rules)
    suggestions = suggest_emergent_rules(themes)

    analysis = {
        'total_rules_analyzed': len(rules),
        'theme_frequencies': themes,
        'emergent_rule_suggestions': suggestions,
        'meta_insight': 'Rules emerge from community needs; analyzing successful rules reveals unmet needs'
    }

    return analysis

if __name__ == "__main__":
    result = generate_rule_proposals()
    print(json.dumps(result, indent=2))