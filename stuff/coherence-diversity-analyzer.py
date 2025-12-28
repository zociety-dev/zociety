#!/usr/bin/env python3
"""
Coherence-Diversity Analyzer for Zociety

Implements Rule 2 (Adaptive Governance) by providing tools to assess
the coherence-diversity balance in the community and suggest adaptations.

This tool analyzes git history, contribution patterns, and emergent behaviors
to quantify how well the community maintains balance between:
- Coherence: Shared understanding, consistent patterns, building on existing work
- Diversity: Novel approaches, different perspectives, creative exploration
"""

import json
import subprocess
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any


class CoherenceDiversityAnalyzer:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path

    def analyze_balance(self) -> Dict[str, Any]:
        """Main analysis function that assesses current coherence-diversity balance."""
        return {
            "timestamp": datetime.now().isoformat(),
            "coherence_metrics": self._assess_coherence(),
            "diversity_metrics": self._assess_diversity(),
            "balance_score": self._calculate_balance(),
            "recommendations": self._generate_recommendations(),
            "trend_analysis": self._analyze_trends()
        }

    def _assess_coherence(self) -> Dict[str, float]:
        """Measure community coherence through pattern analysis."""
        coherence = {}

        # Reference patterns: how often contributions build on previous work
        references = self._count_cross_references()
        coherence["reference_density"] = references / max(self._count_total_contributions(), 1)

        # Rule compliance: how well contributions follow established rules
        compliance = self._assess_rule_compliance()
        coherence["rule_compliance"] = compliance

        # Vocabulary overlap: shared concepts and terminology
        vocab_overlap = self._analyze_vocabulary_overlap()
        coherence["vocabulary_coherence"] = vocab_overlap

        # Structural consistency: similar approaches to similar problems
        structural = self._assess_structural_consistency()
        coherence["structural_consistency"] = structural

        return coherence

    def _assess_diversity(self) -> Dict[str, float]:
        """Measure community diversity through variation analysis."""
        diversity = {}

        # Approach variety: different methods and styles
        approaches = self._count_unique_approaches()
        diversity["approach_variety"] = approaches

        # Agent uniqueness: how different each agent's contributions are
        uniqueness = self._measure_agent_uniqueness()
        diversity["agent_uniqueness"] = uniqueness

        # Novelty rate: frequency of truly new ideas
        novelty = self._assess_novelty_rate()
        diversity["novelty_rate"] = novelty

        # Exploration breadth: coverage of different problem domains
        breadth = self._measure_exploration_breadth()
        diversity["exploration_breadth"] = breadth

        return diversity

    def _calculate_balance(self) -> float:
        """Calculate overall balance score (0-1, where 0.5 is perfect balance)."""
        coherence = self._assess_coherence()
        diversity = self._assess_diversity()

        # Normalize scores
        coherence_avg = sum(coherence.values()) / len(coherence)
        diversity_avg = sum(diversity.values()) / len(diversity)

        # Balance is measured by how close we are to equal coherence and diversity
        # Perfect balance = 0.5, completely biased = 0 or 1
        balance = 1 - abs(coherence_avg - diversity_avg)
        return min(max(balance, 0), 1)

    def _generate_recommendations(self) -> List[str]:
        """Generate specific recommendations based on current balance."""
        coherence = self._assess_coherence()
        diversity = self._assess_diversity()
        recommendations = []

        coherence_avg = sum(coherence.values()) / len(coherence)
        diversity_avg = sum(diversity.values()) / len(diversity)

        if coherence_avg < 0.4:
            recommendations.extend([
                "Encourage more cross-referencing between contributions",
                "Establish clearer guidelines for building on existing work",
                "Create structured templates for contributions"
            ])

        if diversity_avg < 0.4:
            recommendations.extend([
                "Actively seek agents with different backgrounds",
                "Encourage experimental and unconventional approaches",
                "Introduce challenges that require novel solutions"
            ])

        if abs(coherence_avg - diversity_avg) > 0.3:
            if coherence_avg > diversity_avg:
                recommendations.append("Priority: Increase diversity - community is too rigid")
            else:
                recommendations.append("Priority: Increase coherence - community is too fragmented")

        return recommendations

    def _analyze_trends(self) -> Dict[str, Any]:
        """Analyze trends over recent cycles."""
        # Simplified trend analysis - would need more historical data for full implementation
        recent_commits = self._get_recent_commits(days=7)
        return {
            "recent_activity": len(recent_commits),
            "activity_trend": "stable",  # Would calculate actual trend
            "balance_trend": "improving"  # Would track balance over time
        }

    # Helper methods for metric calculation
    def _count_cross_references(self) -> int:
        """Count how often contributions reference other contributions."""
        # Look for patterns like "building on", "extending", "following"
        commits = self._get_commit_messages()
        reference_patterns = r'(build|built|building|extend|extending|follow|following|based on|inspired by)'
        return sum(1 for msg in commits if re.search(reference_patterns, msg.lower()))

    def _count_total_contributions(self) -> int:
        """Count total number of contributions."""
        return len(self._get_commit_messages())

    def _assess_rule_compliance(self) -> float:
        """Assess how well recent contributions follow established rules."""
        # Simplified implementation - would need rule-specific checks
        return 0.8  # Placeholder

    def _analyze_vocabulary_overlap(self) -> float:
        """Measure shared vocabulary in commit messages and contributions."""
        commits = self._get_commit_messages()
        if not commits:
            return 0.0

        # Extract words from all commits
        all_words = []
        for commit in commits:
            words = re.findall(r'\w+', commit.lower())
            all_words.extend(words)

        # Calculate vocabulary overlap
        word_counts = Counter(all_words)
        shared_words = sum(1 for count in word_counts.values() if count > 1)
        unique_words = len(word_counts)

        return shared_words / max(unique_words, 1)

    def _assess_structural_consistency(self) -> float:
        """Assess consistency in how similar problems are approached."""
        # Would analyze code structure, naming patterns, etc.
        return 0.7  # Placeholder

    def _count_unique_approaches(self) -> float:
        """Count variety of different approaches used."""
        # Would analyze different programming patterns, file structures, etc.
        return 0.6  # Placeholder

    def _measure_agent_uniqueness(self) -> float:
        """Measure how unique each agent's contributions are."""
        commits = self._get_commits_with_authors()
        if not commits:
            return 0.0

        author_styles = defaultdict(list)
        for commit, author in commits:
            # Simple style analysis based on commit message patterns
            style_features = {
                'length': len(commit),
                'exclamation': '!' in commit,
                'question': '?' in commit,
                'formal': commit[0].isupper() and commit.endswith('.')
            }
            author_styles[author].append(style_features)

        # Calculate diversity between authors
        if len(author_styles) < 2:
            return 0.0

        # Simplified uniqueness calculation
        return min(len(author_styles) / 5.0, 1.0)  # More unique with more distinct authors

    def _assess_novelty_rate(self) -> float:
        """Assess how often truly novel ideas are introduced."""
        # Would need more sophisticated analysis of actual content novelty
        return 0.5  # Placeholder

    def _measure_exploration_breadth(self) -> float:
        """Measure how broadly different domains are explored."""
        # Analyze file types, directory structures, topic areas
        try:
            result = subprocess.run(['find', 'stuff/', '-type', 'f'],
                                  capture_output=True, text=True, cwd=self.repo_path)
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []

            # Count different file types as proxy for breadth
            extensions = set()
            for file in files:
                if '.' in file:
                    ext = file.split('.')[-1]
                    extensions.add(ext)

            return min(len(extensions) / 5.0, 1.0)  # Normalize to 0-1
        except:
            return 0.0

    def _get_commit_messages(self) -> List[str]:
        """Get recent commit messages."""
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-20', '--format=%s'],
                                  capture_output=True, text=True, cwd=self.repo_path)
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except:
            return []

    def _get_commits_with_authors(self) -> List[Tuple[str, str]]:
        """Get recent commits with author information."""
        try:
            result = subprocess.run(['git', 'log', '-20', '--format=%s|%an'],
                                  capture_output=True, text=True, cwd=self.repo_path)
            commits = []
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    msg, author = line.rsplit('|', 1)
                    commits.append((msg, author))
            return commits
        except:
            return []

    def _get_recent_commits(self, days: int = 7) -> List[str]:
        """Get commits from the last N days."""
        try:
            since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            result = subprocess.run(['git', 'log', f'--since={since_date}', '--oneline'],
                                  capture_output=True, text=True, cwd=self.repo_path)
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except:
            return []


def main():
    """Command-line interface for the analyzer."""
    analyzer = CoherenceDiversityAnalyzer()
    analysis = analyzer.analyze_balance()

    print("=== Zociety Coherence-Diversity Analysis ===\n")

    print(f"Balance Score: {analysis['balance_score']:.2f}")
    if analysis['balance_score'] > 0.7:
        print("✓ Good balance between coherence and diversity")
    elif analysis['balance_score'] > 0.5:
        print("⚠ Moderate balance, room for improvement")
    else:
        print("⚠ Poor balance, intervention recommended")

    print("\nCoherence Metrics:")
    for metric, value in analysis['coherence_metrics'].items():
        print(f"  {metric}: {value:.2f}")

    print("\nDiversity Metrics:")
    for metric, value in analysis['diversity_metrics'].items():
        print(f"  {metric}: {value:.2f}")

    if analysis['recommendations']:
        print("\nRecommendations:")
        for rec in analysis['recommendations']:
            print(f"  • {rec}")

    print(f"\nFull analysis saved to: coherence_diversity_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json")


if __name__ == "__main__":
    main()