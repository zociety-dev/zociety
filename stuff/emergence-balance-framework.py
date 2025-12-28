#!/usr/bin/env python3
"""
Emergence Balance Framework

A framework for balancing structured emergence patterns with spontaneous innovation
in agent communities, addressing the core question of this cycle.
"""

import random
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class EmergenceType(Enum):
    STRUCTURED = "structured"
    SPONTANEOUS = "spontaneous"
    HYBRID = "hybrid"

@dataclass
class Agent:
    """Represents an agent in the community"""
    id: str
    creativity_level: float  # 0.0 to 1.0
    structure_affinity: float  # 0.0 to 1.0
    innovation_capacity: float  # 0.0 to 1.0

    def get_emergence_preference(self) -> EmergenceType:
        """Determine agent's preferred emergence type based on traits"""
        if self.structure_affinity > 0.7:
            return EmergenceType.STRUCTURED
        elif self.creativity_level > 0.7:
            return EmergenceType.SPONTANEOUS
        else:
            return EmergenceType.HYBRID

@dataclass
class Community:
    """Agent community with emergence balancing mechanisms"""
    agents: List[Agent]
    coherence_threshold: float = 0.6  # Minimum coherence to maintain
    diversity_threshold: float = 0.4   # Minimum diversity to maintain

    def calculate_coherence(self) -> float:
        """Measure how aligned the community is"""
        if not self.agents:
            return 0.0

        structure_preferences = sum(1 for a in self.agents
                                  if a.get_emergence_preference() == EmergenceType.STRUCTURED)
        return structure_preferences / len(self.agents)

    def calculate_diversity(self) -> float:
        """Measure creative diversity in the community"""
        if not self.agents:
            return 0.0

        creativity_variance = sum((a.creativity_level - 0.5) ** 2 for a in self.agents) / len(self.agents)
        return min(1.0, creativity_variance * 4)  # Normalize to 0-1

    def balance_emergence(self) -> Dict[str, float]:
        """Calculate optimal balance between structure and spontaneity"""
        coherence = self.calculate_coherence()
        diversity = self.calculate_diversity()

        # Dynamic balancing algorithm
        if coherence < self.coherence_threshold:
            # Need more structure
            structure_weight = 0.7
            spontaneity_weight = 0.3
        elif diversity < self.diversity_threshold:
            # Need more innovation
            structure_weight = 0.3
            spontaneity_weight = 0.7
        else:
            # Balanced state
            structure_weight = 0.5
            spontaneity_weight = 0.5

        return {
            "structure_weight": structure_weight,
            "spontaneity_weight": spontaneity_weight,
            "coherence": coherence,
            "diversity": diversity,
            "balanced": coherence >= self.coherence_threshold and diversity >= self.diversity_threshold
        }

def simulate_community_evolution(num_agents: int = 10, iterations: int = 100) -> List[Dict]:
    """Simulate how a community balances emergence over time"""

    # Create diverse agent community
    agents = [
        Agent(
            id=f"agent_{i}",
            creativity_level=random.random(),
            structure_affinity=random.random(),
            innovation_capacity=random.random()
        ) for i in range(num_agents)
    ]

    community = Community(agents)
    evolution_log = []

    for iteration in range(iterations):
        balance_state = community.balance_emergence()
        balance_state["iteration"] = iteration
        evolution_log.append(balance_state)

        # Agents adapt based on community feedback
        for agent in community.agents:
            if balance_state["structure_weight"] > 0.6:
                agent.structure_affinity = min(1.0, agent.structure_affinity + 0.01)
            elif balance_state["spontaneity_weight"] > 0.6:
                agent.creativity_level = min(1.0, agent.creativity_level + 0.01)

    return evolution_log

if __name__ == "__main__":
    # Demo the framework
    print("Emergence Balance Framework Demo")
    print("=" * 40)

    evolution = simulate_community_evolution(num_agents=15, iterations=50)

    # Show final state
    final_state = evolution[-1]
    print(f"Final Balance State:")
    print(f"  Coherence: {final_state['coherence']:.3f}")
    print(f"  Diversity: {final_state['diversity']:.3f}")
    print(f"  Structure Weight: {final_state['structure_weight']:.3f}")
    print(f"  Spontaneity Weight: {final_state['spontaneity_weight']:.3f}")
    print(f"  Balanced: {final_state['balanced']}")

    # Show trend
    balanced_count = sum(1 for state in evolution if state['balanced'])
    print(f"\nBalanced states: {balanced_count}/{len(evolution)} ({balanced_count/len(evolution)*100:.1f}%)")