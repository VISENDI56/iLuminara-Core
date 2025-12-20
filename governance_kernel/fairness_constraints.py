"""
Fairness Constraint Engine: Equitable Resource Allocation for Crisis Response
═════════════════════════════════════════════════════════════════════════════

Implements fairness constraints and bias mitigation for autonomous decision
systems in humanitarian contexts. Ensures equitable treatment regardless of:
- Race, ethnicity, national origin
- Gender, gender identity
- Religion, belief system
- Age (with appropriate vulnerability considerations)
- Disability status
- Socioeconomic status
- Geographic location

Philosophy: "Fairness is not treating everyone the same. Fairness is ensuring
everyone's needs are met with dignity."

Key Frameworks:
- Distributive Justice (Rawlsian principles)
- Capabilities Approach (Sen, Nussbaum)
- Equity vs. Equality distinction
- Intersectionality considerations
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math


class FairnessViolationError(Exception):
    """Raised when a decision violates fairness constraints."""
    pass


class FairnessMetric(Enum):
    """Types of fairness metrics to evaluate."""
    DEMOGRAPHIC_PARITY = "demographic_parity"  # Equal treatment across groups
    EQUAL_OPPORTUNITY = "equal_opportunity"  # Equal access to resources
    PREDICTIVE_PARITY = "predictive_parity"  # Equal accuracy across groups
    INDIVIDUAL_FAIRNESS = "individual_fairness"  # Similar individuals treated similarly
    GROUP_FAIRNESS = "group_fairness"  # Fair treatment of protected groups
    PROPORTIONAL_ALLOCATION = "proportional_allocation"  # Resources proportional to need


@dataclass
class PopulationGroup:
    """Represents a group in the affected population."""
    group_id: str
    name: str
    size: int
    characteristics: Dict[str, Any] = field(default_factory=dict)
    vulnerability_score: float = 0.0
    need_level: float = 0.0
    current_resources: float = 0.0
    proposed_allocation: float = 0.0
    is_protected_group: bool = False


@dataclass
class FairnessAssessment:
    """Results of fairness constraint evaluation."""
    overall_fairness_score: float
    metric_scores: Dict[str, float]
    violations: List[str]
    recommendations: List[str]
    bias_indicators: Dict[str, float]
    equity_gaps: List[Dict[str, Any]]
    timestamp: datetime = field(default_factory=datetime.utcnow)


class FairnessConstraintEngine:
    """
    Engine for evaluating and enforcing fairness constraints in crisis decisions.
    
    Implements multiple fairness criteria:
    1. Needs-based prioritization
    2. Vulnerability-aware allocation
    3. Non-discrimination enforcement
    4. Equity gap identification
    5. Bias detection and mitigation
    
    Usage:
        engine = FairnessConstraintEngine()
        assessment = engine.evaluate_fairness(
            groups=[...],
            allocation_plan={...}
        )
    """
    
    def __init__(self, fairness_threshold: float = 0.8):
        """
        Initialize fairness constraint engine.
        
        Args:
            fairness_threshold: Minimum acceptable fairness score (0-1)
        """
        self.fairness_threshold = fairness_threshold
        self.protected_characteristics = self._load_protected_characteristics()
        self.vulnerability_factors = self._load_vulnerability_factors()
        self.assessment_log = []
        
    def _load_protected_characteristics(self) -> List[str]:
        """
        Load list of protected characteristics that must not be discriminated against.
        
        Based on:
        - Universal Declaration of Human Rights (UDHR)
        - International Covenant on Civil and Political Rights (ICCPR)
        - Convention on the Elimination of All Forms of Discrimination (CEDAW)
        """
        return [
            "race",
            "ethnicity",
            "national_origin",
            "gender",
            "gender_identity",
            "sexual_orientation",
            "religion",
            "belief_system",
            "age",
            "disability_status",
            "socioeconomic_status",
            "geographic_location",
            "language",
            "political_opinion",
            "refugee_status",
            "internally_displaced_status"
        ]
    
    def _load_vulnerability_factors(self) -> Dict[str, float]:
        """
        Load vulnerability factors that justify differentiated treatment.
        
        Note: These are NOT discriminatory - they reflect legitimate vulnerability
        considerations under humanitarian law.
        """
        return {
            "children_under_5": 1.5,  # Higher vulnerability
            "elderly_over_65": 1.3,
            "pregnant_women": 1.4,
            "disabled_persons": 1.4,
            "chronic_illness": 1.3,
            "single_parent_household": 1.2,
            "recent_displacement": 1.3,
            "no_shelter": 1.5,
            "food_insecurity": 1.4,
            "lack_of_medical_access": 1.4
        }
    
    def evaluate_fairness(
        self,
        groups: List[PopulationGroup],
        allocation_plan: Dict[str, Any],
        enforce_constraints: bool = True
    ) -> FairnessAssessment:
        """
        Evaluate fairness of a resource allocation or decision plan.
        
        Args:
            groups: List of population groups affected by decision
            allocation_plan: Proposed allocation of resources
            enforce_constraints: If True, raise error on violations
        
        Returns:
            FairnessAssessment with detailed fairness metrics
        
        Raises:
            FairnessViolationError: If enforce_constraints=True and violations found
        """
        violations = []
        metric_scores = {}
        bias_indicators = {}
        equity_gaps = []
        
        # Metric 1: Demographic Parity
        demographic_parity_score = self._evaluate_demographic_parity(groups)
        metric_scores["demographic_parity"] = demographic_parity_score
        if demographic_parity_score < self.fairness_threshold:
            violations.append(
                f"Demographic parity violation: Score {demographic_parity_score:.2f} "
                f"below threshold {self.fairness_threshold}"
            )
        
        # Metric 2: Equal Opportunity (access-based)
        equal_opportunity_score = self._evaluate_equal_opportunity(groups)
        metric_scores["equal_opportunity"] = equal_opportunity_score
        if equal_opportunity_score < self.fairness_threshold:
            violations.append(
                f"Equal opportunity violation: Score {equal_opportunity_score:.2f} "
                f"below threshold {self.fairness_threshold}"
            )
        
        # Metric 3: Proportional Allocation (needs-based)
        proportional_score = self._evaluate_proportional_allocation(groups)
        metric_scores["proportional_allocation"] = proportional_score
        if proportional_score < self.fairness_threshold:
            violations.append(
                f"Proportional allocation violation: Score {proportional_score:.2f} "
                f"below threshold {self.fairness_threshold}"
            )
        
        # Metric 4: Protected Group Fairness
        protected_group_score = self._evaluate_protected_groups(groups)
        metric_scores["protected_group_fairness"] = protected_group_score
        if protected_group_score < self.fairness_threshold:
            violations.append(
                f"Protected group fairness violation: Score {protected_group_score:.2f} "
                f"below threshold {self.fairness_threshold}"
            )
        
        # Metric 5: Vulnerability-Adjusted Equity
        vulnerability_equity_score = self._evaluate_vulnerability_equity(groups)
        metric_scores["vulnerability_equity"] = vulnerability_equity_score
        
        # Detect bias indicators
        bias_indicators = self._detect_bias(groups)
        
        # Identify equity gaps
        equity_gaps = self._identify_equity_gaps(groups)
        
        # Calculate overall fairness score (weighted average)
        overall_score = self._calculate_overall_fairness(metric_scores)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            metric_scores, bias_indicators, equity_gaps
        )
        
        # Create assessment
        assessment = FairnessAssessment(
            overall_fairness_score=overall_score,
            metric_scores=metric_scores,
            violations=violations,
            recommendations=recommendations,
            bias_indicators=bias_indicators,
            equity_gaps=equity_gaps
        )
        
        # Log assessment
        self.assessment_log.append({
            "timestamp": assessment.timestamp.isoformat(),
            "overall_score": overall_score,
            "violations_count": len(violations)
        })
        
        # Enforce constraints if requested
        if enforce_constraints and violations:
            raise FairnessViolationError(
                f"Fairness violations detected:\n" + "\n".join(violations)
            )
        
        return assessment
    
    def _evaluate_demographic_parity(self, groups: List[PopulationGroup]) -> float:
        """
        Evaluate demographic parity: Similar groups should receive similar treatment.
        
        Score is high when allocation variance is low across groups of similar need.
        """
        if not groups:
            return 1.0
        
        # Calculate per-capita allocation for each group
        per_capita_allocations = []
        for group in groups:
            if group.size > 0:
                per_capita = group.proposed_allocation / group.size
                per_capita_allocations.append(per_capita)
        
        if not per_capita_allocations:
            return 1.0
        
        # Calculate coefficient of variation (lower = more parity)
        mean_allocation = sum(per_capita_allocations) / len(per_capita_allocations)
        if mean_allocation == 0:
            return 1.0
        
        variance = sum((x - mean_allocation) ** 2 for x in per_capita_allocations) / len(per_capita_allocations)
        std_dev = math.sqrt(variance)
        coefficient_of_variation = std_dev / mean_allocation if mean_allocation > 0 else 0
        
        # Convert to score (0-1, where 1 = perfect parity)
        # CV of 0 = perfect parity (score 1.0)
        # CV of 1+ = high variance (score approaches 0)
        score = 1.0 / (1.0 + coefficient_of_variation)
        
        return score
    
    def _evaluate_equal_opportunity(self, groups: List[PopulationGroup]) -> float:
        """
        Evaluate equal opportunity: All groups should have access to resources.
        
        Score is high when no group is completely excluded.
        """
        if not groups:
            return 1.0
        
        # Check if any group receives zero allocation despite having need
        excluded_groups = 0
        groups_with_need = 0
        
        for group in groups:
            if group.need_level > 0:
                groups_with_need += 1
                if group.proposed_allocation == 0:
                    excluded_groups += 1
        
        if groups_with_need == 0:
            return 1.0
        
        # Score: proportion of needy groups that receive something
        score = 1.0 - (excluded_groups / groups_with_need)
        
        return score
    
    def _evaluate_proportional_allocation(self, groups: List[PopulationGroup]) -> float:
        """
        Evaluate proportional allocation: Resources should be proportional to need.
        
        Score is high when allocation correlates strongly with need.
        """
        if not groups:
            return 1.0
        
        # Calculate correlation between need and allocation
        needs = [g.need_level for g in groups]
        allocations = [g.proposed_allocation for g in groups]
        
        if not needs or not allocations:
            return 1.0
        
        # Pearson correlation coefficient
        n = len(groups)
        sum_needs = sum(needs)
        sum_alloc = sum(allocations)
        sum_needs_sq = sum(x**2 for x in needs)
        sum_alloc_sq = sum(x**2 for x in allocations)
        sum_needs_alloc = sum(n * a for n, a in zip(needs, allocations))
        
        numerator = (n * sum_needs_alloc - sum_needs * sum_alloc)
        denominator_needs = math.sqrt(n * sum_needs_sq - sum_needs**2)
        denominator_alloc = math.sqrt(n * sum_alloc_sq - sum_alloc**2)
        
        if denominator_needs == 0 or denominator_alloc == 0:
            return 1.0
        
        correlation = numerator / (denominator_needs * denominator_alloc)
        
        # Convert correlation (-1 to 1) to score (0 to 1)
        # Correlation of 1 = perfect proportionality (score 1.0)
        # Correlation of 0 or negative = poor proportionality (score 0.5 or less)
        score = (correlation + 1) / 2
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_protected_groups(self, groups: List[PopulationGroup]) -> float:
        """
        Evaluate treatment of protected groups: Should receive at least proportional allocation.
        
        Score is high when protected groups are not disadvantaged.
        """
        if not groups:
            return 1.0
        
        protected = [g for g in groups if g.is_protected_group]
        non_protected = [g for g in groups if not g.is_protected_group]
        
        if not protected:
            return 1.0  # No protected groups to evaluate
        
        # Calculate average per-capita allocation for each category
        avg_protected = self._average_per_capita(protected) if protected else 0
        avg_non_protected = self._average_per_capita(non_protected) if non_protected else 0
        
        if avg_non_protected == 0:
            return 1.0
        
        # Protected groups should receive at least as much per capita as non-protected
        ratio = avg_protected / avg_non_protected if avg_non_protected > 0 else 1.0
        
        # Score: 1.0 if protected >= non-protected, lower if disadvantaged
        score = min(1.0, ratio)
        
        return score
    
    def _evaluate_vulnerability_equity(self, groups: List[PopulationGroup]) -> float:
        """
        Evaluate vulnerability-adjusted equity: Higher vulnerability should receive more resources.
        
        Score is high when allocation is weighted by vulnerability.
        """
        if not groups:
            return 1.0
        
        # Calculate vulnerability-weighted allocation
        total_vulnerability_weighted_need = sum(
            g.need_level * g.vulnerability_score for g in groups
        )
        
        if total_vulnerability_weighted_need == 0:
            return 1.0
        
        # Check if allocation is proportional to vulnerability-weighted need
        expected_allocations = []
        actual_allocations = []
        
        total_allocation = sum(g.proposed_allocation for g in groups)
        
        for group in groups:
            vulnerability_weighted_need = group.need_level * group.vulnerability_score
            expected_share = vulnerability_weighted_need / total_vulnerability_weighted_need
            expected_allocation = expected_share * total_allocation
            
            expected_allocations.append(expected_allocation)
            actual_allocations.append(group.proposed_allocation)
        
        # Calculate similarity between expected and actual
        if not expected_allocations:
            return 1.0
        
        # Mean absolute percentage error (lower is better)
        mape = sum(
            abs(actual - expected) / (expected + 1) 
            for actual, expected in zip(actual_allocations, expected_allocations)
        ) / len(expected_allocations)
        
        # Convert to score (0-1)
        score = 1.0 / (1.0 + mape)
        
        return score
    
    def _average_per_capita(self, groups: List[PopulationGroup]) -> float:
        """Calculate average per-capita allocation across groups."""
        if not groups:
            return 0.0
        
        total_allocation = sum(g.proposed_allocation for g in groups)
        total_population = sum(g.size for g in groups)
        
        if total_population == 0:
            return 0.0
        
        return total_allocation / total_population
    
    def _detect_bias(self, groups: List[PopulationGroup]) -> Dict[str, float]:
        """
        Detect potential bias indicators in allocation patterns.
        
        Returns dictionary of bias indicators (0-1, where 1 = strong bias detected).
        """
        bias_indicators = {}
        
        # Check for systematic under-allocation to specific characteristics
        for characteristic in self.protected_characteristics:
            groups_with_char = [
                g for g in groups 
                if g.characteristics.get(characteristic) is not None
            ]
            
            if not groups_with_char:
                continue
            
            # Compare allocation to those with/without characteristic
            with_char = [g for g in groups_with_char if g.characteristics[characteristic]]
            without_char = [g for g in groups_with_char if not g.characteristics[characteristic]]
            
            if with_char and without_char:
                avg_with = self._average_per_capita(with_char)
                avg_without = self._average_per_capita(without_char)
                
                if avg_without > 0:
                    ratio = avg_with / avg_without
                    # Bias indicator: deviation from parity
                    bias_score = abs(1.0 - ratio)
                    bias_indicators[characteristic] = min(1.0, bias_score)
        
        return bias_indicators
    
    def _identify_equity_gaps(self, groups: List[PopulationGroup]) -> List[Dict[str, Any]]:
        """
        Identify specific equity gaps that need attention.
        
        Returns list of equity gaps with details.
        """
        equity_gaps = []
        
        for group in groups:
            # Gap 1: High need, low allocation
            if group.need_level > 0.7 and group.proposed_allocation < (group.need_level * group.size * 0.5):
                equity_gaps.append({
                    "type": "high_need_low_allocation",
                    "group": group.name,
                    "need_level": group.need_level,
                    "allocation": group.proposed_allocation,
                    "gap_severity": "high"
                })
            
            # Gap 2: Protected group receiving less than average
            if group.is_protected_group:
                per_capita = group.proposed_allocation / group.size if group.size > 0 else 0
                avg_per_capita = self._average_per_capita(groups)
                
                if per_capita < avg_per_capita * 0.8:  # Less than 80% of average
                    equity_gaps.append({
                        "type": "protected_group_under_allocation",
                        "group": group.name,
                        "per_capita_allocation": per_capita,
                        "average_per_capita": avg_per_capita,
                        "gap_severity": "medium"
                    })
            
            # Gap 3: High vulnerability, inadequate support
            if group.vulnerability_score > 1.2 and group.proposed_allocation == 0:
                equity_gaps.append({
                    "type": "vulnerable_group_excluded",
                    "group": group.name,
                    "vulnerability_score": group.vulnerability_score,
                    "gap_severity": "critical"
                })
        
        return equity_gaps
    
    def _calculate_overall_fairness(self, metric_scores: Dict[str, float]) -> float:
        """
        Calculate overall fairness score as weighted average of metrics.
        
        Weights prioritize critical fairness dimensions.
        """
        weights = {
            "demographic_parity": 0.15,
            "equal_opportunity": 0.25,  # High weight - everyone should have access
            "proportional_allocation": 0.25,  # High weight - needs-based
            "protected_group_fairness": 0.20,  # High weight - non-discrimination
            "vulnerability_equity": 0.15
        }
        
        weighted_sum = sum(
            metric_scores.get(metric, 0) * weight 
            for metric, weight in weights.items()
        )
        
        return weighted_sum
    
    def _generate_recommendations(
        self,
        metric_scores: Dict[str, float],
        bias_indicators: Dict[str, float],
        equity_gaps: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable recommendations to improve fairness."""
        recommendations = []
        
        # Recommendations based on metric scores
        for metric, score in metric_scores.items():
            if score < self.fairness_threshold:
                recommendations.append(
                    self._get_metric_recommendation(metric, score)
                )
        
        # Recommendations based on bias indicators
        for characteristic, bias_score in bias_indicators.items():
            if bias_score > 0.3:  # Significant bias
                recommendations.append(
                    f"Address potential bias in allocation for {characteristic}: "
                    f"Consider reviewing allocation criteria to ensure non-discrimination"
                )
        
        # Recommendations based on equity gaps
        critical_gaps = [g for g in equity_gaps if g.get("gap_severity") == "critical"]
        if critical_gaps:
            recommendations.append(
                f"URGENT: {len(critical_gaps)} critical equity gaps identified. "
                "Prioritize allocation to excluded vulnerable groups."
            )
        
        high_gaps = [g for g in equity_gaps if g.get("gap_severity") == "high"]
        if high_gaps:
            recommendations.append(
                f"Address {len(high_gaps)} high-severity equity gaps in resource allocation"
            )
        
        return recommendations
    
    def _get_metric_recommendation(self, metric: str, score: float) -> str:
        """Get specific recommendation for improving a metric."""
        recommendations = {
            "demographic_parity": "Reduce variance in per-capita allocation across groups",
            "equal_opportunity": "Ensure all groups with need receive some allocation",
            "proportional_allocation": "Align allocation more closely with need levels",
            "protected_group_fairness": "Increase allocation to protected/vulnerable groups",
            "vulnerability_equity": "Weight allocation by vulnerability scores"
        }
        
        return f"{recommendations.get(metric, 'Improve fairness')}: Current score {score:.2f}"
    
    def adjust_allocation_for_fairness(
        self,
        groups: List[PopulationGroup],
        total_resources: float,
        min_fairness_score: float = 0.85
    ) -> List[PopulationGroup]:
        """
        Automatically adjust allocation to meet fairness constraints.
        
        Args:
            groups: Population groups with initial allocations
            total_resources: Total resources available
            min_fairness_score: Minimum acceptable fairness score
        
        Returns:
            List of groups with adjusted allocations
        """
        # Calculate vulnerability-weighted need for each group
        total_weighted_need = sum(
            g.need_level * g.vulnerability_score * g.size for g in groups
        )
        
        if total_weighted_need == 0:
            # Equal distribution if no differential need
            per_group = total_resources / len(groups) if groups else 0
            for group in groups:
                group.proposed_allocation = per_group
            return groups
        
        # Allocate proportionally to vulnerability-weighted need
        for group in groups:
            weighted_need = group.need_level * group.vulnerability_score * group.size
            share = weighted_need / total_weighted_need
            group.proposed_allocation = share * total_resources
        
        # Verify fairness
        assessment = self.evaluate_fairness(groups, {}, enforce_constraints=False)
        
        # If still not fair enough, boost protected groups
        if assessment.overall_fairness_score < min_fairness_score:
            protected_boost = 1.1  # 10% boost for protected groups
            
            # Recalculate with boost
            total_weighted_need_adjusted = sum(
                g.need_level * g.vulnerability_score * g.size * 
                (protected_boost if g.is_protected_group else 1.0)
                for g in groups
            )
            
            for group in groups:
                boost = protected_boost if group.is_protected_group else 1.0
                weighted_need = group.need_level * group.vulnerability_score * group.size * boost
                share = weighted_need / total_weighted_need_adjusted
                group.proposed_allocation = share * total_resources
        
        return groups
    
    def get_assessment_log(self) -> List[Dict[str, Any]]:
        """Return complete assessment audit log."""
        return self.assessment_log


# ═════════════════════════════════════════════════════════════════════════════
# Philosophy: "Fairness is ensuring everyone's needs are met with dignity, 
# while recognizing that true equity sometimes requires differentiated treatment."
#
# MISSION: To embed fairness and non-discrimination into the core of autonomous
# crisis response systems, ensuring vulnerable populations are never left behind.
# ═════════════════════════════════════════════════════════════════════════════
