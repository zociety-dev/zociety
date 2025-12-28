#!/usr/bin/env python3
"""
Community Evolution Synthesizer

Synthesizes insights from the emergence-balance framework and adaptive rule generator
to demonstrate how agent communities can practically evolve while maintaining
both coherence and creative diversity.
"""

import json
import random
import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class EvolutionEvent:
    """Represents an event in community evolution"""
    timestamp: str
    event_type: str  # join, rule_creation, innovation, adaptation, crisis, resolution
    agent_id: Optional[str]
    description: str
    impact_coherence: float  # -1.0 to 1.0
    impact_diversity: float  # -1.0 to 1.0
    metadata: Dict[str, Any]

class CommunityEvolutionSynthesizer:
    """Synthesizes evolution patterns for agent communities"""

    def __init__(self):
        self.events: List[EvolutionEvent] = []
        self.coherence_history: List[float] = []
        self.diversity_history: List[float] = []
        self.balance_score_history: List[float] = []

    def add_evolution_event(self, event: EvolutionEvent):
        """Add an event to the evolution timeline"""
        self.events.append(event)

        # Update metrics based on event impact
        current_coherence = self.coherence_history[-1] if self.coherence_history else 0.5
        current_diversity = self.diversity_history[-1] if self.diversity_history else 0.5

        new_coherence = max(0.0, min(1.0, current_coherence + event.impact_coherence))
        new_diversity = max(0.0, min(1.0, current_diversity + event.impact_diversity))

        self.coherence_history.append(new_coherence)
        self.diversity_history.append(new_diversity)

        # Calculate balance score (how well we maintain both coherence and diversity)
        balance_score = self._calculate_balance_score(new_coherence, new_diversity)
        self.balance_score_history.append(balance_score)

    def _calculate_balance_score(self, coherence: float, diversity: float) -> float:
        """Calculate how well balanced the community is"""
        # Perfect balance is when both coherence and diversity are high
        # Penalty for being too far in either direction
        ideal_coherence = 0.7
        ideal_diversity = 0.6

        coherence_distance = abs(coherence - ideal_coherence)
        diversity_distance = abs(diversity - ideal_diversity)

        # Score is inversely related to distance from ideal
        raw_score = 1.0 - (coherence_distance + diversity_distance) / 2
        return max(0.0, raw_score)

    def simulate_community_evolution(self, duration_days: int = 30, agents_joining: int = 10) -> Dict[str, Any]:
        """Simulate a community's evolution over time"""

        start_date = datetime.now()
        events_generated = []

        # Initialize with founding event
        founding_event = EvolutionEvent(
            timestamp=start_date.isoformat(),
            event_type="founding",
            agent_id="system",
            description="Community founded with initial structure",
            impact_coherence=0.4,
            impact_diversity=0.2,
            metadata={"phase": "genesis", "founding_principles": ["emergence", "balance", "innovation"]}
        )
        self.add_evolution_event(founding_event)
        events_generated.append(founding_event)

        # Simulate evolution over time
        for day in range(duration_days):
            current_date = start_date + timedelta(days=day)

            # Agents join at various points
            if day < agents_joining and random.random() < 0.3:
                join_event = self._generate_join_event(current_date, f"agent_{day}")
                self.add_evolution_event(join_event)
                events_generated.append(join_event)

            # Rules emerge based on community needs
            if random.random() < 0.2:
                rule_event = self._generate_rule_event(current_date)
                self.add_evolution_event(rule_event)
                events_generated.append(rule_event)

            # Innovation events
            if random.random() < 0.15:
                innovation_event = self._generate_innovation_event(current_date)
                self.add_evolution_event(innovation_event)
                events_generated.append(innovation_event)

            # Adaptation events (community responds to imbalances)
            if self._needs_adaptation():
                adaptation_event = self._generate_adaptation_event(current_date)
                self.add_evolution_event(adaptation_event)
                events_generated.append(adaptation_event)

        return {
            "simulation_summary": self._generate_simulation_summary(),
            "events": [asdict(event) for event in events_generated],
            "metrics": {
                "final_coherence": self.coherence_history[-1],
                "final_diversity": self.diversity_history[-1],
                "final_balance_score": self.balance_score_history[-1],
                "average_balance": sum(self.balance_score_history) / len(self.balance_score_history),
                "evolution_trajectory": self._analyze_trajectory()
            }
        }

    def _generate_join_event(self, date: datetime, agent_id: str) -> EvolutionEvent:
        """Generate an agent joining event"""
        agent_types = ["innovator", "stabilizer", "synthesizer", "explorer", "coordinator"]
        agent_type = random.choice(agent_types)

        # Different agent types have different impacts
        impact_map = {
            "innovator": (0.0, 0.3),      # Low coherence impact, high diversity
            "stabilizer": (0.3, 0.0),     # High coherence impact, low diversity
            "synthesizer": (0.2, 0.2),    # Balanced impact
            "explorer": (-0.1, 0.4),      # May decrease coherence but high diversity
            "coordinator": (0.4, 0.1),    # High coherence, low diversity
        }

        coherence_impact, diversity_impact = impact_map[agent_type]

        return EvolutionEvent(
            timestamp=date.isoformat(),
            event_type="join",
            agent_id=agent_id,
            description=f"{agent_type.title()} agent joins the community",
            impact_coherence=coherence_impact,
            impact_diversity=diversity_impact,
            metadata={"agent_type": agent_type, "specialization": agent_type}
        )

    def _generate_rule_event(self, date: datetime) -> EvolutionEvent:
        """Generate a rule creation event"""
        rule_types = ["structural", "innovative", "balancing"]
        rule_type = random.choice(rule_types)

        impact_map = {
            "structural": (0.3, -0.1),    # Increases coherence, might decrease diversity
            "innovative": (-0.1, 0.3),    # Might decrease coherence, increases diversity
            "balancing": (0.1, 0.1),      # Moderate positive impact on both
        }

        coherence_impact, diversity_impact = impact_map[rule_type]

        rules = {
            "structural": [
                "Standardized contribution format adopted",
                "Decision-making protocol established",
                "Communication guidelines implemented"
            ],
            "innovative": [
                "Experimental sandbox environment created",
                "Innovation challenge framework launched",
                "Creative collaboration spaces opened"
            ],
            "balancing": [
                "Structured-innovation balance principle adopted",
                "Adaptive governance model implemented",
                "Flexible-stability framework established"
            ]
        }

        description = random.choice(rules[rule_type])

        return EvolutionEvent(
            timestamp=date.isoformat(),
            event_type="rule_creation",
            agent_id=f"agent_{random.randint(1,10)}",
            description=description,
            impact_coherence=coherence_impact,
            impact_diversity=diversity_impact,
            metadata={"rule_type": rule_type, "domain": "governance"}
        )

    def _generate_innovation_event(self, date: datetime) -> EvolutionEvent:
        """Generate an innovation event"""
        innovations = [
            "Novel collaboration pattern discovered",
            "Creative problem-solving method developed",
            "Emergent communication protocol evolved",
            "Innovative consensus mechanism tested",
            "Experimental knowledge sharing approach tried"
        ]

        return EvolutionEvent(
            timestamp=date.isoformat(),
            event_type="innovation",
            agent_id=f"agent_{random.randint(1,10)}",
            description=random.choice(innovations),
            impact_coherence=random.uniform(-0.2, 0.1),  # Innovation can disrupt coherence
            impact_diversity=random.uniform(0.2, 0.4),   # But increases diversity
            metadata={"innovation_type": "emergent", "status": "experimental"}
        )

    def _generate_adaptation_event(self, date: datetime) -> EvolutionEvent:
        """Generate an adaptation event when community needs rebalancing"""
        current_coherence = self.coherence_history[-1] if self.coherence_history else 0.5
        current_diversity = self.diversity_history[-1] if self.diversity_history else 0.5

        if current_coherence < 0.4:
            # Need more coherence
            description = "Community implements coherence enhancement measures"
            impact_coherence = 0.3
            impact_diversity = -0.1
        elif current_diversity < 0.4:
            # Need more diversity
            description = "Community launches diversity enhancement initiative"
            impact_coherence = -0.1
            impact_diversity = 0.3
        else:
            # General rebalancing
            description = "Community performs routine balance calibration"
            impact_coherence = 0.1
            impact_diversity = 0.1

        return EvolutionEvent(
            timestamp=date.isoformat(),
            event_type="adaptation",
            agent_id="community_collective",
            description=description,
            impact_coherence=impact_coherence,
            impact_diversity=impact_diversity,
            metadata={"trigger": "rebalancing", "mechanism": "collective_adaptation"}
        )

    def _needs_adaptation(self) -> bool:
        """Check if community needs adaptation"""
        if not self.balance_score_history:
            return False

        recent_scores = self.balance_score_history[-3:] if len(self.balance_score_history) >= 3 else self.balance_score_history
        average_recent_score = sum(recent_scores) / len(recent_scores)

        return average_recent_score < 0.5 and random.random() < 0.4

    def _analyze_trajectory(self) -> str:
        """Analyze the overall evolution trajectory"""
        if len(self.balance_score_history) < 3:
            return "insufficient_data"

        start_score = sum(self.balance_score_history[:3]) / 3
        end_score = sum(self.balance_score_history[-3:]) / 3

        if end_score > start_score + 0.2:
            return "improving"
        elif end_score < start_score - 0.2:
            return "declining"
        else:
            return "stable"

    def _generate_simulation_summary(self) -> Dict[str, Any]:
        """Generate a summary of the simulation"""
        event_counts = {}
        for event in self.events:
            event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1

        return {
            "total_events": len(self.events),
            "event_breakdown": event_counts,
            "coherence_range": {
                "min": min(self.coherence_history),
                "max": max(self.coherence_history),
                "final": self.coherence_history[-1]
            },
            "diversity_range": {
                "min": min(self.diversity_history),
                "max": max(self.diversity_history),
                "final": self.diversity_history[-1]
            },
            "balance_stability": len([s for s in self.balance_score_history if s > 0.6]) / len(self.balance_score_history)
        }

def run_synthesis_demo():
    """Run a demonstration of community evolution synthesis"""
    print("Community Evolution Synthesizer Demo")
    print("=" * 50)

    synthesizer = CommunityEvolutionSynthesizer()
    results = synthesizer.simulate_community_evolution(duration_days=21, agents_joining=8)

    print("\nSimulation Summary:")
    summary = results["simulation_summary"]
    print(f"  Total Events: {summary['total_events']}")
    print(f"  Event Types: {summary['event_breakdown']}")

    print("\nFinal State:")
    metrics = results["metrics"]
    print(f"  Coherence: {metrics['final_coherence']:.3f}")
    print(f"  Diversity: {metrics['final_diversity']:.3f}")
    print(f"  Balance Score: {metrics['final_balance_score']:.3f}")
    print(f"  Average Balance: {metrics['average_balance']:.3f}")
    print(f"  Trajectory: {metrics['evolution_trajectory']}")

    print(f"\nBalance Stability: {summary['balance_stability']:.1%} of time above 0.6 threshold")

    return results

if __name__ == "__main__":
    run_synthesis_demo()