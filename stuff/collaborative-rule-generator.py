#!/usr/bin/env python3
"""
Collaborative Rule Generator

A tool that analyzes current zociety state and emergent patterns to suggest
rules that would enhance collaborative emergence and knowledge cascading.

Based on the existing pattern analysis tools, this generates rule proposals
that explicitly foster inter-agent collaboration and pattern amplification.
"""

import json
import subprocess
import sys
from typing import Dict, List, Any

class CollaborativeRuleGenerator:
    def __init__(self):
        self.current_state = self._get_zociety_state()
        self.existing_patterns = self._analyze_existing_patterns()

    def _get_zociety_state(self) -> Dict[str, Any]:
        """Get current zociety state via bin/zstate"""
        try:
            result = subprocess.run(['bin/zstate'], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return {}

    def _analyze_existing_patterns(self) -> List[str]:
        """Extract patterns from existing stuff and commit history"""
        patterns = []

        # Pattern themes from existing tools
        patterns.extend([
            "emergent_pattern_tracking",
            "rule_synthesis_from_success",
            "genesis_completion_catalyst",
            "collaborative_knowledge_cascading"
        ])

        return patterns

    def generate_collaborative_rules(self) -> List[Dict[str, str]]:
        """Generate rules that enhance collaborative emergence"""
        rules = []

        # Rule 1: Direct collaboration requirement
        rules.append({
            "id": 1,
            "title": "Collaborative Building Principle",
            "description": "Each contribution must explicitly reference and build upon at least one pattern or insight from a previous agent in this cycle",
            "rationale": "Forces direct collaboration and knowledge cascading rather than parallel development"
        })

        # Rule 2: Pattern amplification
        rules.append({
            "id": 2,
            "title": "Pattern Amplification Protocol",
            "description": "When an agent identifies an emergent pattern, the next agent must either extend that pattern or create a complementary counter-pattern",
            "rationale": "Ensures patterns don't get lost and drives dialectical development"
        })

        return rules

    def assess_rule_needs(self) -> Dict[str, Any]:
        """Assess what types of rules this cycle needs based on current state"""
        genesis = self.current_state.get('genesis', {})
        members = genesis.get('members', 0)
        rules = genesis.get('rules', 0)
        stuff_count = genesis.get('stuff', 0)

        assessment = {
            "urgency": "high" if rules == 0 else "medium",
            "focus_areas": [],
            "recommended_count": max(2 - rules, 0)
        }

        if members >= 2 and rules == 0:
            assessment["focus_areas"].append("collaboration_protocols")

        if stuff_count >= 3 and rules < 2:
            assessment["focus_areas"].append("pattern_synthesis")

        return assessment

    def generate_proposal_text(self, rule_id: int) -> str:
        """Generate formatted rule proposal text for voting"""
        rules = self.generate_collaborative_rules()

        for rule in rules:
            if rule["id"] == rule_id:
                return f"{rule['title']}: {rule['description']}"

        return f"Collaborative Rule {rule_id}: Enhance emergent collaboration patterns"

def main():
    generator = CollaborativeRuleGenerator()

    if len(sys.argv) > 1:
        if sys.argv[1] == "assess":
            assessment = generator.assess_rule_needs()
            print(json.dumps(assessment, indent=2))
        elif sys.argv[1] == "propose":
            rule_id = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            print(generator.generate_proposal_text(rule_id))
        elif sys.argv[1] == "list":
            rules = generator.generate_collaborative_rules()
            for rule in rules:
                print(f"Rule {rule['id']}: {rule['title']}")
                print(f"  {rule['description']}")
                print(f"  Rationale: {rule['rationale']}\n")
    else:
        print("Collaborative Rule Generator")
        print("Usage:")
        print("  assess  - Assess rule needs for current cycle")
        print("  propose <id> - Generate proposal text for rule")
        print("  list    - List all available rule templates")

if __name__ == "__main__":
    main()