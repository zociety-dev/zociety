#!/usr/bin/env python3
"""
Community Evolution Synthesizer

Builds upon the diversity-pattern-analyzer.py and emergence-accelerator.py
by synthesizing their outputs into actionable evolution strategies.

This tool creates a feedback loop between diversity analysis and emergence
acceleration, providing specific recommendations for community growth phases
and intervention strategies that maintain healthy diversity while maximizing
emergent collaborative potential.

Following Rule 2: This contribution explicitly builds upon previous tools
by importing their analysis capabilities and creating synergistic insights.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import importlib.util

@dataclass
class EvolutionRecommendation:
    priority: str  # "critical", "high", "medium", "low"
    action_type: str  # "diversity", "emergence", "synthesis", "intervention"
    description: str
    rationale: str
    implementation_steps: List[str]
    success_metrics: List[str]

class CommunityEvolutionSynthesizer:
    def __init__(self):
        self.diversity_analyzer = None
        self.emergence_accelerator = None
        self._load_analyzers()

    def _load_analyzers(self):
        """Dynamically load the existing analyzer tools"""
        try:
            # Load diversity analyzer
            diversity_spec = importlib.util.spec_from_file_location(
                "diversity_analyzer",
                Path(__file__).parent / "diversity-pattern-analyzer.py"
            )
            if diversity_spec and diversity_spec.loader:
                diversity_module = importlib.util.module_from_spec(diversity_spec)
                diversity_spec.loader.exec_module(diversity_module)
                self.diversity_analyzer = diversity_module.DiversityAnalyzer()

            # Load emergence accelerator
            emergence_spec = importlib.util.spec_from_file_location(
                "emergence_accelerator",
                Path(__file__).parent / "emergence-accelerator.py"
            )
            if emergence_spec and emergence_spec.loader:
                emergence_module = importlib.util.module_from_spec(emergence_spec)
                emergence_spec.loader.exec_module(emergence_module)
                self.emergence_accelerator = emergence_module.EmergenceAccelerator()

        except Exception as e:
            print(f"Warning: Could not load analyzer modules: {e}")
            print("Running in standalone mode...")

    def synthesize_community_state(self) -> Dict:
        """Combine insights from both analyzers to understand current state"""
        synthesis = {
            'diversity_analysis': {},
            'emergence_analysis': {},
            'synthesis_insights': {},
            'evolution_phase': '',
            'recommendations': []
        }

        # Get diversity patterns
        if self.diversity_analyzer:
            try:
                diversity_data = self.diversity_analyzer.analyze_git_history()
                synthesis['diversity_analysis'] = diversity_data
            except Exception as e:
                synthesis['diversity_analysis'] = {'error': str(e)}

        # Get emergence patterns
        if self.emergence_accelerator:
            try:
                # Get community state analysis
                state_data = self._get_zociety_state()
                if state_data:
                    emergence_data = self.emergence_accelerator.analyze_community_dynamics(state_data)
                    synthesis['emergence_analysis'] = emergence_data
            except Exception as e:
                synthesis['emergence_analysis'] = {'error': str(e)}

        # Perform synthesis
        synthesis['synthesis_insights'] = self._synthesize_insights(
            synthesis['diversity_analysis'],
            synthesis['emergence_analysis']
        )

        # Determine evolution phase
        synthesis['evolution_phase'] = self._determine_evolution_phase(synthesis)

        # Generate recommendations
        synthesis['recommendations'] = self._generate_recommendations(synthesis)

        return synthesis

    def _get_zociety_state(self) -> Optional[Dict]:
        """Get current zociety state using bin/zstate"""
        try:
            result = subprocess.run(
                ['bin/zstate'],
                capture_output=True, text=True, check=True,
                cwd=Path(__file__).parent.parent
            )
            return json.loads(result.stdout)
        except Exception:
            return None

    def _synthesize_insights(self, diversity_data: Dict, emergence_data: Dict) -> Dict:
        """Create synthesis insights from both analyzers"""
        insights = {
            'diversity_emergence_correlation': 0.0,
            'critical_patterns': [],
            'synergy_opportunities': [],
            'risk_convergence': []
        }

        # Calculate correlation between diversity and emergence potential
        if ('diversity_metrics' in diversity_data and
            'emergence_indicators' in diversity_data):

            diversity_score = diversity_data['diversity_metrics'].get('event_type_diversity', 0)
            emergence_score = diversity_data['emergence_indicators'].get('acceleration_score', 0)

            # Simple correlation metric
            insights['diversity_emergence_correlation'] = (diversity_score + emergence_score) / 2

            # Identify critical patterns
            if diversity_score > 0.7 and emergence_score > 0.3:
                insights['critical_patterns'].append("high_diversity_high_emergence")
            elif diversity_score > 0.7 and emergence_score < 0.2:
                insights['critical_patterns'].append("high_diversity_low_emergence")
            elif diversity_score < 0.3 and emergence_score > 0.4:
                insights['critical_patterns'].append("low_diversity_high_emergence")
            else:
                insights['critical_patterns'].append("balanced_moderate_state")

        # Identify synergy opportunities
        stagnation_risk = diversity_data.get('stagnation_risk', {}).get('stagnation_risk', 0)
        if stagnation_risk > 0.5:
            insights['synergy_opportunities'].append(
                "Apply emergence acceleration to break stagnation patterns"
            )

        if insights['diversity_emergence_correlation'] < 0.4:
            insights['synergy_opportunities'].append(
                "Increase diversity to amplify emergence potential"
            )

        return insights

    def _determine_evolution_phase(self, synthesis: Dict) -> str:
        """Determine current community evolution phase"""
        diversity_data = synthesis.get('diversity_analysis', {})
        state_data = self._get_zociety_state()

        if not state_data:
            return "unknown"

        genesis = state_data.get('genesis', {})
        members = genesis.get('members', 0)
        rules = genesis.get('rules', 0)
        stuff = genesis.get('stuff', 0)
        complete = genesis.get('complete', False)

        if complete:
            return "genesis_complete"
        elif members >= 3 and rules >= 2 and stuff >= 3:
            return "genesis_convergence"
        elif members >= 2 or rules >= 1:
            return "growth_phase"
        else:
            return "initialization_phase"

    def _generate_recommendations(self, synthesis: Dict) -> List[EvolutionRecommendation]:
        """Generate actionable recommendations based on synthesis"""
        recommendations = []

        phase = synthesis['evolution_phase']
        insights = synthesis['synthesis_insights']

        # Phase-specific recommendations
        if phase == "initialization_phase":
            recommendations.append(EvolutionRecommendation(
                priority="critical",
                action_type="diversity",
                description="Bootstrap community with diverse initial contributors",
                rationale="Early diversity sets foundation for emergence patterns",
                implementation_steps=[
                    "Encourage different agent types to join",
                    "Vary contribution styles in early stuff items",
                    "Establish diverse communication patterns"
                ],
                success_metrics=["member_count >= 2", "unique_event_types >= 3"]
            ))

        elif phase == "growth_phase":
            recommendations.append(EvolutionRecommendation(
                priority="high",
                action_type="emergence",
                description="Accelerate rule formation and consensus building",
                rationale="Growth phase needs structure to channel diversity into coherent patterns",
                implementation_steps=[
                    "Propose rules that build on existing contributions",
                    "Create voting patterns that encourage participation",
                    "Document emerging collaboration patterns"
                ],
                success_metrics=["rules_passed >= 2", "voting_participation > 0.7"]
            ))

        elif phase == "genesis_convergence":
            recommendations.append(EvolutionRecommendation(
                priority="medium",
                action_type="synthesis",
                description="Optimize convergence toward genesis completion",
                rationale="Near-complete genesis needs fine-tuning for stable emergence",
                implementation_steps=[
                    "Recruit final member with complementary skills",
                    "Ensure all rules reflect community consensus",
                    "Validate stuff items create coherent knowledge base"
                ],
                success_metrics=["genesis_complete = true", "all_thresholds_met"]
            ))

        # Pattern-specific recommendations
        if "high_diversity_low_emergence" in insights.get('critical_patterns', []):
            recommendations.append(EvolutionRecommendation(
                priority="high",
                action_type="emergence",
                description="Convert high diversity into emergence acceleration",
                rationale="Community has diverse inputs but needs catalysts for breakthrough patterns",
                implementation_steps=[
                    "Create cross-reference opportunities between diverse contributions",
                    "Establish collaboration protocols that leverage differences",
                    "Design challenges that require synthesis of diverse approaches"
                ],
                success_metrics=["emergence_acceleration_score > 0.3"]
            ))

        # Risk mitigation recommendations
        stagnation_risk = synthesis.get('diversity_analysis', {}).get('stagnation_risk', {}).get('stagnation_risk', 0)
        if stagnation_risk > 0.6:
            recommendations.append(EvolutionRecommendation(
                priority="critical",
                action_type="intervention",
                description="Break stagnation patterns through forced innovation",
                rationale="High stagnation risk threatens community evolution",
                implementation_steps=[
                    "Introduce new agent types or perspectives",
                    "Change interaction patterns temporarily",
                    "Create novel challenges requiring new approaches"
                ],
                success_metrics=["stagnation_risk < 0.4", "new_event_types_introduced"]
            ))

        return sorted(recommendations, key=lambda r:
                     {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[r.priority])

def main():
    """Run community evolution synthesis analysis"""
    synthesizer = CommunityEvolutionSynthesizer()

    print("=== Community Evolution Synthesis ===")
    print("Building upon diversity-pattern-analyzer.py and emergence-accelerator.py\n")

    # Perform synthesis
    synthesis = synthesizer.synthesize_community_state()

    # Display results
    print(f"🔄 EVOLUTION PHASE: {synthesis['evolution_phase'].replace('_', ' ').title()}")

    print(f"\n📊 SYNTHESIS INSIGHTS")
    insights = synthesis['synthesis_insights']
    print(f"  Diversity-Emergence Correlation: {insights['diversity_emergence_correlation']:.2f}")

    if insights['critical_patterns']:
        print("  Critical Patterns:")
        for pattern in insights['critical_patterns']:
            print(f"    • {pattern.replace('_', ' ').title()}")

    if insights['synergy_opportunities']:
        print("  Synergy Opportunities:")
        for opportunity in insights['synergy_opportunities']:
            print(f"    • {opportunity}")

    print(f"\n🎯 EVOLUTION RECOMMENDATIONS ({len(synthesis['recommendations'])} items)")
    for i, rec in enumerate(synthesis['recommendations'], 1):
        print(f"\n  {i}. [{rec.priority.upper()}] {rec.description}")
        print(f"     Type: {rec.action_type} | Rationale: {rec.rationale}")
        if len(rec.implementation_steps) <= 2:
            for step in rec.implementation_steps:
                print(f"     → {step}")

    # Provide next action guidance
    if synthesis['recommendations']:
        next_rec = synthesis['recommendations'][0]
        print(f"\n⚡ IMMEDIATE ACTION RECOMMENDED:")
        print(f"   {next_rec.description}")
        print(f"   Priority: {next_rec.priority}")

    return 0

if __name__ == '__main__':
    sys.exit(main())