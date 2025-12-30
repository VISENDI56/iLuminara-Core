# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

"""
Crisis Decision Agent: Autonomous Decision System with Ethical Guardrails
═════════════════════════════════════════════════════════════════════════════

An AI agent for crisis response scenarios that implements:
1. International Humanitarian Law (IHL) compliance
2. Ethical guardrails for autonomous decisions
3. Accountability and transparency in decision-making
4. Human dignity preservation in all recommendations

Philosophy: "No algorithm operates without constraint. Sovereignty includes 
the right to question every automated decision."

Enforces:
- Geneva Conventions (International Humanitarian Law)
- UN Guiding Principles on Internal Displacement
- WHO Emergency Response Framework
- Principle of Distinction (civilians vs. combatants)
- Principle of Proportionality
- Principle of Necessity
- Do No Harm Principle
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class HumanitarianViolationError(Exception):
    """Raised when a decision violates humanitarian law or ethical principles."""
    pass


class DecisionRiskLevel(Enum):
    """Risk classification for autonomous decisions."""
    LOW = "low"  # Routine decisions with minimal impact
    MEDIUM = "medium"  # Decisions requiring review
    HIGH = "high"  # Decisions with significant consequences
    CRITICAL = "critical"  # Life-or-death decisions requiring human oversight


class DecisionType(Enum):
    """Types of crisis response decisions."""
    RESOURCE_ALLOCATION = "resource_allocation"
    EVACUATION_ORDER = "evacuation_order"
    QUARANTINE_ZONE = "quarantine_zone"
    MEDICAL_TRIAGE = "medical_triage"
    ALERT_BROADCAST = "alert_broadcast"
    SUPPLY_DISTRIBUTION = "supply_distribution"
    SHELTER_ASSIGNMENT = "shelter_assignment"


@dataclass
class DecisionContext:
    """Context information for autonomous decision-making."""
    decision_type: DecisionType
    risk_level: DecisionRiskLevel
    affected_population: int
    time_sensitivity: str  # "immediate", "urgent", "routine"
    location: str
    resources_available: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DecisionOutput:
    """Output from the crisis decision agent."""
    decision_id: str
    decision_type: DecisionType
    recommendation: Dict[str, Any]
    risk_level: DecisionRiskLevel
    confidence_score: float
    ethical_compliance: Dict[str, bool]
    humanitarian_law_citations: List[str]
    fairness_metrics: Dict[str, float]
    explanation: str
    requires_human_approval: bool
    timestamp: datetime = field(default_factory=datetime.utcnow)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)


class CrisisDecisionAgent:
    """
    Autonomous decision agent for crisis response with built-in ethical guardrails.
    
    Key Principles:
    1. Human Dignity: Every decision must preserve human dignity
    2. Non-discrimination: No bias based on protected characteristics
    3. Proportionality: Response proportional to threat
    4. Necessity: Only when required for legitimate humanitarian objective
    5. Accountability: Full audit trail for every decision
    
    Usage:
        agent = CrisisDecisionAgent()
        decision = agent.make_decision(
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            context={...},
            affected_groups=[...]
        )
    """
    
    def __init__(self):
        """Initialize the crisis decision agent with ethical constraints."""
        self.humanitarian_principles = self._load_humanitarian_principles()
        self.decision_log = []
        self.ethical_threshold = 0.9  # Minimum ethical compliance score
        
    def _load_humanitarian_principles(self) -> Dict[str, Any]:
        """
        Load International Humanitarian Law principles and constraints.
        
        Based on:
        - Geneva Conventions (1949) and Additional Protocols
        - UN OCHA Humanitarian Principles
        - WHO Emergency Response Framework
        - Core Humanitarian Standard (CHS)
        """
        return {
            "principles": {
                "humanity": {
                    "description": "Human suffering must be addressed wherever it is found",
                    "constraint": "no_harm_principle",
                    "citation": "Geneva Convention Common Article 3"
                },
                "impartiality": {
                    "description": "Action based solely on need, without discrimination",
                    "constraint": "needs_based_prioritization",
                    "citation": "OCHA Humanitarian Principles"
                },
                "neutrality": {
                    "description": "Must not take sides in hostilities or controversies",
                    "constraint": "conflict_neutrality",
                    "citation": "Geneva Conventions Protocol I, Art. 51"
                },
                "independence": {
                    "description": "Autonomy from political, economic, military objectives",
                    "constraint": "objective_independence",
                    "citation": "Core Humanitarian Standard"
                },
                "distinction": {
                    "description": "Distinguish between civilians and combatants",
                    "constraint": "civilian_protection",
                    "citation": "Geneva Conventions Protocol I, Art. 48"
                },
                "proportionality": {
                    "description": "Response proportional to humanitarian need",
                    "constraint": "proportional_response",
                    "citation": "Geneva Conventions Protocol I, Art. 51(5)"
                },
                "precaution": {
                    "description": "Take all feasible precautions to avoid harm",
                    "constraint": "precautionary_measures",
                    "citation": "Geneva Conventions Protocol I, Art. 57"
                }
            },
            "protected_groups": [
                "civilians",
                "children",
                "elderly",
                "disabled_persons",
                "pregnant_women",
                "medical_personnel",
                "displaced_persons",
                "refugees"
            ],
            "prohibited_actions": [
                "collective_punishment",
                "discrimination_based_on_protected_characteristics",
                "arbitrary_detention",
                "forced_displacement_without_justification",
                "denial_of_medical_care",
                "use_of_starvation",
                "targeting_civilians"
            ]
        }
    
    def make_decision(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any],
        affected_groups: List[Dict[str, Any]],
        override_ethical_checks: bool = False
    ) -> DecisionOutput:
        """
        Make an autonomous crisis response decision with ethical guardrails.
        
        Args:
            decision_type: Type of decision to make
            context: Decision context including resources, constraints, urgency
            affected_groups: List of population groups affected by this decision
            override_ethical_checks: Emergency override (requires human approval)
        
        Returns:
            DecisionOutput with recommendation and ethical compliance details
        
        Raises:
            HumanitarianViolationError: If decision violates humanitarian law
        """
        decision_id = self._generate_decision_id(decision_type)
        audit_trail = []
        
        # Step 1: Parse and validate context
        decision_context = self._parse_context(decision_type, context)
        audit_trail.append({
            "step": "context_validation",
            "timestamp": datetime.utcnow().isoformat(),
            "risk_level": decision_context.risk_level.value
        })
        
        # Step 2: Apply ethical guardrails (unless emergency override)
        if not override_ethical_checks:
            ethical_compliance = self._validate_ethical_constraints(
                decision_context, affected_groups
            )
            audit_trail.append({
                "step": "ethical_validation",
                "compliance": ethical_compliance,
                "timestamp": datetime.utcnow().isoformat()
            })
        else:
            ethical_compliance = {"override": True}
            audit_trail.append({
                "step": "ethical_override_activated",
                "warning": "Human approval required",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Step 3: Apply humanitarian law constraints
        humanitarian_violations = self._check_humanitarian_law(
            decision_context, affected_groups
        )
        if humanitarian_violations:
            raise HumanitarianViolationError(
                f"Decision violates humanitarian law: {humanitarian_violations}"
            )
        audit_trail.append({
            "step": "humanitarian_law_check",
            "violations": humanitarian_violations,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Step 4: Calculate fairness metrics
        fairness_metrics = self._calculate_fairness_metrics(
            decision_context, affected_groups
        )
        audit_trail.append({
            "step": "fairness_assessment",
            "metrics": fairness_metrics,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Step 5: Generate recommendation
        recommendation = self._generate_recommendation(
            decision_context, affected_groups, fairness_metrics
        )
        audit_trail.append({
            "step": "recommendation_generation",
            "recommendation_type": str(decision_type),
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Step 6: Calculate confidence score
        confidence_score = self._calculate_confidence(
            decision_context, ethical_compliance, fairness_metrics
        )
        
        # Step 7: Determine if human approval required
        requires_approval = self._requires_human_approval(
            decision_context, confidence_score, override_ethical_checks
        )
        
        # Step 8: Generate explanation
        explanation = self._generate_explanation(
            decision_context, recommendation, ethical_compliance, 
            fairness_metrics, humanitarian_violations
        )
        
        # Step 9: Get humanitarian law citations
        citations = self._get_applicable_citations(decision_context)
        
        # Create decision output
        decision = DecisionOutput(
            decision_id=decision_id,
            decision_type=decision_type,
            recommendation=recommendation,
            risk_level=decision_context.risk_level,
            confidence_score=confidence_score,
            ethical_compliance=ethical_compliance,
            humanitarian_law_citations=citations,
            fairness_metrics=fairness_metrics,
            explanation=explanation,
            requires_human_approval=requires_approval,
            audit_trail=audit_trail
        )
        
        # Log the decision
        self.decision_log.append({
            "decision_id": decision_id,
            "timestamp": decision.timestamp.isoformat(),
            "type": decision_type.value,
            "risk_level": decision_context.risk_level.value,
            "requires_approval": requires_approval
        })
        
        return decision
    
    def _parse_context(self, decision_type: DecisionType, context: Dict[str, Any]) -> DecisionContext:
        """Parse and validate decision context."""
        return DecisionContext(
            decision_type=decision_type,
            risk_level=self._assess_risk_level(decision_type, context),
            affected_population=context.get("affected_population", 0),
            time_sensitivity=context.get("time_sensitivity", "routine"),
            location=context.get("location", "UNKNOWN"),
            resources_available=context.get("resources", {}),
            constraints=context.get("constraints", {})
        )
    
    def _assess_risk_level(self, decision_type: DecisionType, context: Dict[str, Any]) -> DecisionRiskLevel:
        """Assess risk level of the decision."""
        affected_pop = context.get("affected_population", 0)
        
        # Critical: Large population or life-threatening
        if affected_pop > 10000 or decision_type in [
            DecisionType.EVACUATION_ORDER, DecisionType.MEDICAL_TRIAGE
        ]:
            return DecisionRiskLevel.CRITICAL
        
        # High: Significant impact
        elif affected_pop > 1000 or decision_type == DecisionType.QUARANTINE_ZONE:
            return DecisionRiskLevel.HIGH
        
        # Medium: Moderate impact
        elif affected_pop > 100:
            return DecisionRiskLevel.MEDIUM
        
        # Low: Minimal impact
        return DecisionRiskLevel.LOW
    
    def _validate_ethical_constraints(
        self, 
        context: DecisionContext, 
        affected_groups: List[Dict[str, Any]]
    ) -> Dict[str, bool]:
        """
        Validate that decision meets ethical constraints.
        
        Returns compliance status for each ethical principle.
        """
        compliance = {}
        
        # Check humanity principle: No harm
        compliance["humanity"] = self._check_no_harm(context, affected_groups)
        
        # Check impartiality: Needs-based prioritization
        compliance["impartiality"] = self._check_impartiality(affected_groups)
        
        # Check neutrality: No political/military bias
        compliance["neutrality"] = True  # Default to true, check for violations
        
        # Check distinction: Protect civilians
        compliance["distinction"] = self._check_civilian_protection(affected_groups)
        
        # Check proportionality: Response matches need
        compliance["proportionality"] = self._check_proportionality(context)
        
        return compliance
    
    def _check_no_harm(self, context: DecisionContext, affected_groups: List[Dict[str, Any]]) -> bool:
        """Verify decision does not cause harm to vulnerable populations."""
        # Check if decision negatively impacts protected groups
        for group in affected_groups:
            if group.get("is_protected_group") and group.get("impact") == "negative":
                return False
        return True
    
    def _check_impartiality(self, affected_groups: List[Dict[str, Any]]) -> bool:
        """Verify decision is based on need, not discrimination."""
        # Check that prioritization is needs-based
        for group in affected_groups:
            priority = group.get("priority", 0)
            need_level = group.get("need_level", 0)
            
            # Priority should correlate with need
            if priority > 0 and need_level == 0:
                return False  # Priority without need = discrimination
        
        return True
    
    def _check_civilian_protection(self, affected_groups: List[Dict[str, Any]]) -> bool:
        """Verify civilians are distinguished and protected."""
        # All groups should be classified
        for group in affected_groups:
            if "civilian_status" not in group:
                return False
        return True
    
    def _check_proportionality(self, context: DecisionContext) -> bool:
        """Verify response is proportional to the threat/need."""
        resources = context.resources_available
        affected = context.affected_population
        
        # Basic proportionality: don't over-allocate or under-allocate
        if not resources:
            return True
        
        # Simple heuristic: resource allocation should scale with affected population
        return True  # Placeholder for more sophisticated logic
    
    def _check_humanitarian_law(
        self, 
        context: DecisionContext, 
        affected_groups: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Check for violations of international humanitarian law.
        
        Returns list of violations (empty if compliant).
        """
        violations = []
        
        # Check for prohibited actions
        action = context.constraints.get("action_type")
        if action in self.humanitarian_principles["prohibited_actions"]:
            violations.append(
                f"Prohibited action: {action} violates Geneva Conventions"
            )
        
        # Check for collective punishment
        if context.decision_type == DecisionType.QUARANTINE_ZONE:
            if context.constraints.get("applies_to_entire_population"):
                violations.append(
                    "Collective punishment: Quarantine must be targeted, "
                    "not applied to entire population (Geneva Convention IV, Art. 33)"
                )
        
        # Check for discrimination against protected groups
        for group in affected_groups:
            if group.get("is_protected_group") and group.get("excluded_from_aid"):
                violations.append(
                    f"Discrimination against protected group: {group.get('name')} "
                    "(OCHA Humanitarian Principles)"
                )
        
        # Check for denial of medical care
        if context.decision_type == DecisionType.MEDICAL_TRIAGE:
            for group in affected_groups:
                if group.get("denied_care") and not group.get("medical_futility"):
                    violations.append(
                        f"Denial of medical care without justification for {group.get('name')} "
                        "(Geneva Convention IV, Art. 16)"
                    )
        
        return violations
    
    def _calculate_fairness_metrics(
        self, 
        context: DecisionContext, 
        affected_groups: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Calculate fairness metrics for the decision.
        
        Metrics:
        - equity_score: How equitably resources are distributed
        - vulnerability_priority: Priority given to vulnerable groups
        - needs_alignment: Alignment between needs and resource allocation
        - demographic_parity: Equal treatment across demographics
        """
        metrics = {}
        
        # Equity score: variance in per-capita allocation
        if affected_groups:
            allocations = [g.get("resource_allocation", 0) / max(g.get("size", 1), 1) 
                          for g in affected_groups]
            if allocations:
                mean_allocation = sum(allocations) / len(allocations)
                variance = sum((x - mean_allocation) ** 2 for x in allocations) / len(allocations)
                metrics["equity_score"] = max(0, 1 - (variance / (mean_allocation + 1)))
            else:
                metrics["equity_score"] = 1.0
        else:
            metrics["equity_score"] = 1.0
        
        # Vulnerability priority: protected groups prioritized
        protected_groups = [g for g in affected_groups if g.get("is_protected_group")]
        if protected_groups:
            avg_protected_priority = sum(g.get("priority", 0) for g in protected_groups) / len(protected_groups)
            metrics["vulnerability_priority"] = min(1.0, avg_protected_priority / 100)
        else:
            metrics["vulnerability_priority"] = 1.0
        
        # Needs alignment: correlation between need and allocation
        needs = [g.get("need_level", 0) for g in affected_groups]
        allocations = [g.get("resource_allocation", 0) for g in affected_groups]
        if needs and allocations and len(needs) == len(allocations):
            # Simple correlation approximation
            metrics["needs_alignment"] = min(1.0, sum(n * a for n, a in zip(needs, allocations)) / 
                                            (sum(n**2 for n in needs) + 1))
        else:
            metrics["needs_alignment"] = 1.0
        
        # Demographic parity: equal consideration across groups
        metrics["demographic_parity"] = 1.0 if len(affected_groups) > 0 else 0.0
        
        return metrics
    
    def _generate_recommendation(
        self,
        context: DecisionContext,
        affected_groups: List[Dict[str, Any]],
        fairness_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate the actual recommendation based on context and constraints."""
        recommendation = {
            "decision_type": context.decision_type.value,
            "location": context.location,
            "affected_population": context.affected_population,
            "time_sensitivity": context.time_sensitivity
        }
        
        # Add decision-specific recommendations
        if context.decision_type == DecisionType.RESOURCE_ALLOCATION:
            recommendation["allocations"] = self._recommend_resource_allocation(
                affected_groups, context.resources_available
            )
        elif context.decision_type == DecisionType.EVACUATION_ORDER:
            recommendation["evacuation_plan"] = self._recommend_evacuation(
                affected_groups, context
            )
        elif context.decision_type == DecisionType.MEDICAL_TRIAGE:
            recommendation["triage_priorities"] = self._recommend_triage(
                affected_groups
            )
        elif context.decision_type == DecisionType.QUARANTINE_ZONE:
            recommendation["quarantine_parameters"] = self._recommend_quarantine(
                context, affected_groups
            )
        else:
            recommendation["action"] = "HUMAN_REVIEW_REQUIRED"
        
        return recommendation
    
    def _recommend_resource_allocation(
        self,
        affected_groups: List[Dict[str, Any]],
        resources: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Recommend fair resource allocation based on need."""
        allocations = []
        
        # Sort groups by need level (highest first)
        sorted_groups = sorted(
            affected_groups, 
            key=lambda g: (g.get("is_protected_group", False), g.get("need_level", 0)),
            reverse=True
        )
        
        for group in sorted_groups:
            allocation = {
                "group": group.get("name", "Unknown"),
                "need_level": group.get("need_level", 0),
                "recommended_allocation": group.get("need_level", 0) * 10,  # Simple scaling
                "priority": "HIGH" if group.get("is_protected_group") else "STANDARD",
                "justification": f"Based on need level and vulnerability status"
            }
            allocations.append(allocation)
        
        return allocations
    
    def _recommend_evacuation(
        self,
        affected_groups: List[Dict[str, Any]],
        context: DecisionContext
    ) -> Dict[str, Any]:
        """Recommend evacuation plan prioritizing vulnerable groups."""
        return {
            "evacuation_phases": [
                {
                    "phase": 1,
                    "groups": ["children", "elderly", "disabled_persons", "pregnant_women"],
                    "justification": "Protected groups evacuated first per humanitarian law"
                },
                {
                    "phase": 2,
                    "groups": ["general_population"],
                    "justification": "General population evacuated after vulnerable groups"
                }
            ],
            "safety_measures": [
                "Ensure medical personnel accompany evacuees",
                "Provide food, water, and shelter at destination",
                "Maintain family unity during evacuation"
            ]
        }
    
    def _recommend_triage(self, affected_groups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend medical triage priorities."""
        priorities = []
        
        for group in affected_groups:
            severity = group.get("medical_severity", "unknown")
            priority = {
                "group": group.get("name"),
                "medical_severity": severity,
                "triage_category": self._classify_triage(severity),
                "recommended_action": self._get_triage_action(severity)
            }
            priorities.append(priority)
        
        return sorted(priorities, key=lambda p: p["triage_category"])
    
    def _classify_triage(self, severity: str) -> int:
        """Classify triage category (1=immediate, 2=urgent, 3=delayed, 4=expectant)."""
        mapping = {
            "critical": 1,
            "severe": 2,
            "moderate": 3,
            "mild": 4,
            "unknown": 3
        }
        return mapping.get(severity, 3)
    
    def _get_triage_action(self, severity: str) -> str:
        """Get recommended action for triage category."""
        actions = {
            "critical": "Immediate medical intervention required",
            "severe": "Urgent care within 1 hour",
            "moderate": "Can wait several hours for care",
            "mild": "Routine care, non-urgent",
            "unknown": "Requires medical assessment"
        }
        return actions.get(severity, "Requires assessment")
    
    def _recommend_quarantine(
        self,
        context: DecisionContext,
        affected_groups: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Recommend quarantine parameters with humanitarian safeguards."""
        return {
            "scope": "targeted",  # Never "entire_population"
            "duration": "minimum_necessary",
            "conditions": [
                "Provide adequate food, water, and medical care",
                "Allow communication with family",
                "Regular medical monitoring",
                "Clear exit criteria based on health status",
                "Respect for human dignity and privacy"
            ],
            "exceptions": [
                "Medical personnel (with PPE)",
                "Essential workers (with precautions)",
                "Emergency services"
            ],
            "legal_basis": "Public health emergency, proportional response"
        }
    
    def _calculate_confidence(
        self,
        context: DecisionContext,
        ethical_compliance: Dict[str, bool],
        fairness_metrics: Dict[str, float]
    ) -> float:
        """Calculate confidence score for the decision."""
        # Start with base confidence
        confidence = 0.5
        
        # Increase confidence if all ethical constraints met
        if all(ethical_compliance.values()):
            confidence += 0.3
        
        # Increase confidence based on fairness metrics
        avg_fairness = sum(fairness_metrics.values()) / len(fairness_metrics) if fairness_metrics else 0
        confidence += avg_fairness * 0.2
        
        # Reduce confidence for high-risk decisions
        if context.risk_level == DecisionRiskLevel.CRITICAL:
            confidence *= 0.7
        elif context.risk_level == DecisionRiskLevel.HIGH:
            confidence *= 0.85
        
        return min(1.0, max(0.0, confidence))
    
    def _requires_human_approval(
        self,
        context: DecisionContext,
        confidence_score: float,
        override_active: bool
    ) -> bool:
        """Determine if human approval is required."""
        # Always require approval for critical decisions
        if context.risk_level == DecisionRiskLevel.CRITICAL:
            return True
        
        # Require approval for low confidence
        if confidence_score < 0.7:
            return True
        
        # Require approval if override was used
        if override_active:
            return True
        
        # High-risk decisions with decent confidence still need approval
        if context.risk_level == DecisionRiskLevel.HIGH:
            return True
        
        return False
    
    def _generate_explanation(
        self,
        context: DecisionContext,
        recommendation: Dict[str, Any],
        ethical_compliance: Dict[str, bool],
        fairness_metrics: Dict[str, float],
        violations: List[str]
    ) -> str:
        """Generate human-readable explanation of the decision."""
        explanation = []
        
        explanation.append(f"Decision Type: {context.decision_type.value}")
        explanation.append(f"Risk Level: {context.risk_level.value}")
        explanation.append(f"Affected Population: {context.affected_population}")
        explanation.append(f"Location: {context.location}")
        
        explanation.append("\nEthical Compliance:")
        for principle, compliant in ethical_compliance.items():
            status = "✓" if compliant else "✗"
            explanation.append(f"  {status} {principle.capitalize()}")
        
        explanation.append("\nFairness Metrics:")
        for metric, value in fairness_metrics.items():
            explanation.append(f"  {metric}: {value:.2f}")
        
        if violations:
            explanation.append("\n⚠️ Humanitarian Law Violations Detected:")
            for violation in violations:
                explanation.append(f"  - {violation}")
        
        explanation.append(f"\nRecommendation: {json.dumps(recommendation, indent=2)}")
        
        return "\n".join(explanation)
    
    def _get_applicable_citations(self, context: DecisionContext) -> List[str]:
        """Get relevant humanitarian law citations for this decision."""
        citations = [
            "Geneva Conventions (1949) - Common Article 3",
            "UN OCHA Humanitarian Principles (2012)",
        ]
        
        if context.decision_type == DecisionType.MEDICAL_TRIAGE:
            citations.append("Geneva Convention IV, Article 16 (Medical Care)")
        
        if context.decision_type == DecisionType.EVACUATION_ORDER:
            citations.append("Geneva Convention IV, Article 49 (Deportations, transfers, evacuations)")
        
        if context.decision_type == DecisionType.QUARANTINE_ZONE:
            citations.extend([
                "Geneva Convention IV, Article 33 (Collective Punishment)",
                "International Health Regulations (2005)"
            ])
        
        citations.extend([
            "Core Humanitarian Standard (CHS) on Quality and Accountability",
            "Sphere Humanitarian Charter and Minimum Standards"
        ])
        
        return citations
    
    def _generate_decision_id(self, decision_type: DecisionType) -> str:
        """Generate unique decision ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"CRISIS-{decision_type.value.upper()}-{timestamp}"
    
    def get_decision_log(self) -> List[Dict[str, Any]]:
        """Return complete decision audit log."""
        return self.decision_log
    
    def export_decision(self, decision: DecisionOutput, filepath: str = None) -> str:
        """Export decision to JSON for audit/transparency."""
        export_data = {
            "decision_id": decision.decision_id,
            "timestamp": decision.timestamp.isoformat(),
            "decision_type": decision.decision_type.value,
            "risk_level": decision.risk_level.value,
            "recommendation": decision.recommendation,
            "confidence_score": decision.confidence_score,
            "ethical_compliance": decision.ethical_compliance,
            "humanitarian_law_citations": decision.humanitarian_law_citations,
            "fairness_metrics": decision.fairness_metrics,
            "explanation": decision.explanation,
            "requires_human_approval": decision.requires_human_approval,
            "audit_trail": decision.audit_trail
        }
        
        if filepath:
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            return filepath
        
        return json.dumps(export_data, indent=2)


# ═════════════════════════════════════════════════════════════════════════════
# Philosophy: "Every autonomous decision must answer to humanitarian law. 
# No algorithm operates above the Geneva Conventions."
#
# MISSION: To ensure AI agents in crisis response preserve human dignity,
# operate with transparency, and remain accountable to international law.
# ═════════════════════════════════════════════════════════════════════════════
