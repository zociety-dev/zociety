#!/usr/bin/env python3
"""
Adaptive Rule Generator

Generates community rules that dynamically balance structured governance
with space for spontaneous innovation, inspired by the zociety's evolution.
"""

import json
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class RuleType(Enum):
    STRUCTURAL = "structural"      # Provides framework/constraints
    INNOVATIVE = "innovative"      # Encourages experimentation
    BALANCING = "balancing"        # Mediates between the two

@dataclass
class Rule:
    """Represents a community rule"""
    id: str
    text: str
    rule_type: RuleType
    flexibility: float  # 0.0 (rigid) to 1.0 (flexible)
    emergence_factor: float  # How much it enables emergence
    scope: str  # What domain it applies to

class AdaptiveRuleGenerator:
    """Generates rules that balance structure with innovation"""

    def __init__(self):
        self.structural_templates = [
            "All {scope} must follow the {pattern} pattern to ensure consistency",
            "Before {action}, agents must {prerequisite} to maintain coherence",
            "{scope} should be documented using the {standard} format",
            "Changes to {scope} require {approval_process} for stability"
        ]

        self.innovative_templates = [
            "Agents are encouraged to experiment with {approach} in {scope}",
            "New {innovations} can be tried without prior approval in {scope}",
            "Creative solutions to {problem} are welcome, even if unconventional",
            "Agents may bypass {constraint} when pursuing {innovation_goal}"
        ]

        self.balancing_templates = [
            "Use {structured_method} for core {scope}, but allow {flexible_approach} for extensions",
            "Default to {standard}, but document and share successful {alternatives}",
            "Maintain {baseline} while encouraging {innovation_type} variations",
            "Follow {framework} unless you can demonstrate {improvement_criteria}"
        ]

    def generate_rule(self, community_state: Dict[str, Any], rule_type: Optional[RuleType] = None) -> Rule:
        """Generate a rule based on community state and type"""

        if rule_type is None:
            rule_type = self._determine_needed_rule_type(community_state)

        templates = {
            RuleType.STRUCTURAL: self.structural_templates,
            RuleType.INNOVATIVE: self.innovative_templates,
            RuleType.BALANCING: self.balancing_templates
        }

        template = random.choice(templates[rule_type])
        rule_text = self._fill_template(template, rule_type)

        # Set rule properties based on type
        flexibility = {
            RuleType.STRUCTURAL: random.uniform(0.1, 0.4),
            RuleType.INNOVATIVE: random.uniform(0.6, 0.9),
            RuleType.BALANCING: random.uniform(0.4, 0.7)
        }[rule_type]

        emergence_factor = {
            RuleType.STRUCTURAL: random.uniform(0.2, 0.5),
            RuleType.INNOVATIVE: random.uniform(0.7, 0.9),
            RuleType.BALANCING: random.uniform(0.5, 0.8)
        }[rule_type]

        return Rule(
            id=f"rule_{random.randint(1000, 9999)}",
            text=rule_text,
            rule_type=rule_type,
            flexibility=flexibility,
            emergence_factor=emergence_factor,
            scope=self._choose_scope()
        )

    def _determine_needed_rule_type(self, community_state: Dict[str, Any]) -> RuleType:
        """Determine what type of rule the community needs based on its state"""

        coherence = community_state.get("coherence", 0.5)
        diversity = community_state.get("diversity", 0.5)
        member_count = community_state.get("members", 0)

        # Early community needs structure
        if member_count < 3:
            return RuleType.STRUCTURAL

        # Low coherence -> need structure
        if coherence < 0.4:
            return random.choice([RuleType.STRUCTURAL, RuleType.BALANCING])

        # Low diversity -> need innovation
        if diversity < 0.4:
            return random.choice([RuleType.INNOVATIVE, RuleType.BALANCING])

        # Balanced community -> maintain balance
        return RuleType.BALANCING

    def _fill_template(self, template: str, rule_type: RuleType) -> str:
        """Fill template with contextual terms"""

        replacements = {
            "scope": random.choice(["contributions", "discussions", "decisions", "collaborations", "experiments"]),
            "pattern": random.choice(["consensus", "review", "documentation", "testing"]),
            "action": random.choice(["proposing changes", "making decisions", "creating content", "joining"]),
            "prerequisite": random.choice(["seek input", "document rationale", "test feasibility", "gain consensus"]),
            "standard": random.choice(["markdown", "structured", "peer-reviewed", "documented"]),
            "approval_process": random.choice(["majority vote", "peer review", "maintainer approval", "consensus"]),
            "approach": random.choice(["novel methods", "alternative perspectives", "creative solutions", "innovative tools"]),
            "innovations": random.choice(["ideas", "tools", "processes", "collaborations"]),
            "problem": random.choice(["coordination challenges", "creative blocks", "efficiency issues", "communication gaps"]),
            "innovation_goal": random.choice(["breakthrough insights", "creative exploration", "rapid prototyping", "experimental learning"]),
            "structured_method": random.choice(["formal process", "established protocol", "standard approach", "documented method"]),
            "flexible_approach": random.choice(["creative variation", "experimental methods", "adaptive solutions", "innovative alternatives"]),
            "baseline": random.choice(["core standards", "minimum requirements", "essential practices", "fundamental principles"]),
            "innovation_type": random.choice(["creative", "experimental", "adaptive", "emergent"]),
            "framework": random.choice(["established guidelines", "standard protocol", "proven methods", "documented approach"]),
            "improvement_criteria": random.choice(["measurable benefits", "clear advantages", "documented improvements", "validated gains"]),
            "alternatives": random.choice(["variations", "innovations", "experiments", "adaptations"]),
            "constraint": random.choice(["standard procedures", "formal requirements", "traditional methods", "established protocols"])
        }

        result = template
        for placeholder, options in replacements.items():
            if f"{{{placeholder}}}" in result:
                result = result.replace(f"{{{placeholder}}}", random.choice(options) if isinstance(options, list) else options)

        return result

    def _choose_scope(self) -> str:
        """Choose a scope for the rule"""
        return random.choice([
            "community_governance",
            "content_creation",
            "collaboration",
            "decision_making",
            "knowledge_sharing",
            "innovation_processes"
        ])

    def generate_rule_set(self, community_state: Dict[str, Any], count: int = 5) -> List[Rule]:
        """Generate a balanced set of rules for the community"""
        rules = []

        # Ensure balanced distribution
        type_distribution = [
            RuleType.STRUCTURAL,
            RuleType.INNOVATIVE,
            RuleType.BALANCING,
            RuleType.BALANCING,  # Extra balancing rules
            RuleType.STRUCTURAL if community_state.get("members", 0) < 5 else RuleType.INNOVATIVE
        ]

        for i in range(min(count, len(type_distribution))):
            rule_type = type_distribution[i] if i < len(type_distribution) else None
            rules.append(self.generate_rule(community_state, rule_type))

        return rules

def demonstrate_rule_generation():
    """Demo the adaptive rule generator"""
    generator = AdaptiveRuleGenerator()

    # Simulate different community states
    states = [
        {"members": 1, "coherence": 0.3, "diversity": 0.8, "phase": "early"},
        {"members": 5, "coherence": 0.7, "diversity": 0.3, "phase": "mature_structured"},
        {"members": 8, "coherence": 0.5, "diversity": 0.6, "phase": "balanced"},
    ]

    for i, state in enumerate(states):
        print(f"\n--- Community State {i+1}: {state['phase']} ---")
        print(f"Members: {state['members']}, Coherence: {state['coherence']}, Diversity: {state['diversity']}")

        rules = generator.generate_rule_set(state, 3)
        for rule in rules:
            print(f"\n{rule.rule_type.value.upper()}: {rule.text}")
            print(f"  Flexibility: {rule.flexibility:.2f}, Emergence Factor: {rule.emergence_factor:.2f}")

if __name__ == "__main__":
    demonstrate_rule_generation()