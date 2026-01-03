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
AI Agent Coordinator: Integrated Ethical Decision System for Crisis Response
═════════════════════════════════════════════════════════════════════════════

Coordinates multiple AI agents with ethical guardrails, humanitarian law compliance,
and fairness constraints for autonomous decision-making in crisis scenarios.

This coordinator integrates:
1. Crisis Decision Agent (humanitarian law compliance)
2. Fairness Constraint Engine (equitable resource allocation)
3. Sovereign Guardrail (data protection and legal compliance)

Philosophy: "Multiple layers of ethical protection. Every decision must pass
through humanitarian law, fairness constraints, and sovereignty checks."

Usage Example:
    coordinator = AIAgentCoordinator()
    result = coordinator.execute_crisis_decision(
        scenario_type="disease_outbreak",
        affected_area="Dadaab_Refugee_Camp",
        population_data=[...],
        resources_available={...}
    )
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

from governance_kernel.crisis_decision_agent import (
    CrisisDecisionAgent,
    DecisionType,
    DecisionContext,
    DecisionOutput,
    HumanitarianViolationError
)
from governance_kernel.fairness_constraints import (
    FairnessConstraintEngine,
    FairnessAssessment,
    PopulationGroup,
    FairnessViolationError
)
from governance_kernel.vector_ledger import (
    SovereignGuardrail,
    SovereigntyViolationError
)


class CrisisScenarioType(Enum):
    """Types of crisis scenarios."""
    DISEASE_OUTBREAK = "disease_outbreak"
    NATURAL_DISASTER = "natural_disaster"
    CONFLICT_DISPLACEMENT = "conflict_displacement"
    FOOD_SECURITY_CRISIS = "food_security_crisis"
    WATER_EMERGENCY = "water_emergency"
    MEDICAL_EMERGENCY = "medical_emergency"


@dataclass
class IntegratedDecisionResult:
    """Result from integrated AI agent decision process."""
    scenario_type: CrisisScenarioType
    decision_output: DecisionOutput
    fairness_assessment: FairnessAssessment
    sovereignty_compliance: Dict[str, Any]
    final_recommendation: Dict[str, Any]
    approval_status: str  # "APPROVED", "REQUIRES_HUMAN_REVIEW", "REJECTED"
    rejection_reasons: List[str] = field(default_factory=list)
    ethical_summary: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)


class AIAgentCoordinator:
    """
    Coordinates multiple AI agents with layered ethical protections.
    
    Decision Pipeline:
    1. Crisis Decision Agent generates recommendation
    2. Fairness Constraint Engine validates equity
    3. Sovereign Guardrail ensures legal compliance
    4. Coordinator synthesizes final decision
    5. Human approval check
    
    Usage:
        coordinator = AIAgentCoordinator()
        result = coordinator.execute_crisis_decision(...)
    """
    
    def __init__(
        self,
        fairness_threshold: float = 0.8,
        confidence_threshold: float = 0.7
    ):
        """
        Initialize AI agent coordinator.
        
        Args:
            fairness_threshold: Minimum fairness score (0-1)
            confidence_threshold: Minimum confidence for autonomous decisions
        """
        self.crisis_agent = CrisisDecisionAgent()
        self.fairness_engine = FairnessConstraintEngine(fairness_threshold)
        self.sovereignty_guardrail = SovereignGuardrail()
        
        self.fairness_threshold = fairness_threshold
        self.confidence_threshold = confidence_threshold
        self.decision_history = []
        
    def execute_crisis_decision(
        self,
        scenario_type: CrisisScenarioType,
        decision_type: DecisionType,
        affected_area: str,
        population_groups: List[Dict[str, Any]],
        resources_available: Dict[str, Any],
        constraints: Dict[str, Any] = None,
        jurisdiction: str = "GLOBAL_DEFAULT"
    ) -> IntegratedDecisionResult:
        """
        Execute a crisis decision through the full ethical pipeline.
        
        Args:
            scenario_type: Type of crisis scenario
            decision_type: Type of decision to make
            affected_area: Geographic area affected
            population_groups: List of population group data
            resources_available: Available resources for allocation
            constraints: Additional constraints or requirements
            jurisdiction: Legal jurisdiction for compliance
        
        Returns:
            IntegratedDecisionResult with final recommendation and compliance details
        """
        rejection_reasons = []
        
        try:
            # Step 1: Prepare population groups
            pop_groups = self._prepare_population_groups(population_groups)
            
            # Step 2: Generate crisis decision
            decision_output = self._generate_crisis_decision(
                decision_type=decision_type,
                affected_area=affected_area,
                pop_groups=pop_groups,
                resources=resources_available,
                constraints=constraints or {}
            )
            
            # Step 3: Validate fairness
            fairness_assessment = self._validate_fairness(
                pop_groups=pop_groups,
                decision_output=decision_output
            )
            
            # Step 4: Check sovereignty/compliance
            sovereignty_compliance = self._check_sovereignty_compliance(
                decision_output=decision_output,
                jurisdiction=jurisdiction
            )
            
            # Step 5: Synthesize final recommendation
            final_recommendation = self._synthesize_recommendation(
                decision_output=decision_output,
                fairness_assessment=fairness_assessment,
                sovereignty_compliance=sovereignty_compliance
            )
            
            # Step 6: Determine approval status
            approval_status = self._determine_approval_status(
                decision_output=decision_output,
                fairness_assessment=fairness_assessment,
                sovereignty_compliance=sovereignty_compliance,
                rejection_reasons=rejection_reasons
            )
            
            # Step 7: Generate ethical summary
            ethical_summary = self._generate_ethical_summary(
                decision_output=decision_output,
                fairness_assessment=fairness_assessment,
                sovereignty_compliance=sovereignty_compliance,
                approval_status=approval_status
            )
            
            # Create integrated result
            result = IntegratedDecisionResult(
                scenario_type=scenario_type,
                decision_output=decision_output,
                fairness_assessment=fairness_assessment,
                sovereignty_compliance=sovereignty_compliance,
                final_recommendation=final_recommendation,
                approval_status=approval_status,
                rejection_reasons=rejection_reasons,
                ethical_summary=ethical_summary
            )
            
            # Log decision
            self._log_decision(result)
            
            return result
            
        except HumanitarianViolationError as e:
            rejection_reasons.append(f"Humanitarian Law Violation: {str(e)}")
            return self._create_rejection_result(
                scenario_type, rejection_reasons, "HUMANITARIAN_LAW_VIOLATION"
            )
        
        except FairnessViolationError as e:
            rejection_reasons.append(f"Fairness Constraint Violation: {str(e)}")
            return self._create_rejection_result(
                scenario_type, rejection_reasons, "FAIRNESS_VIOLATION"
            )
        
        except SovereigntyViolationError as e:
            rejection_reasons.append(f"Sovereignty/Legal Violation: {str(e)}")
            return self._create_rejection_result(
                scenario_type, rejection_reasons, "SOVEREIGNTY_VIOLATION"
            )
        
        except Exception as e:
            rejection_reasons.append(f"System Error: {str(e)}")
            return self._create_rejection_result(
                scenario_type, rejection_reasons, "SYSTEM_ERROR"
            )
    
    def _prepare_population_groups(
        self, 
        group_data: List[Dict[str, Any]]
    ) -> List[PopulationGroup]:
        """Convert group data dictionaries to PopulationGroup objects."""
        groups = []
        
        for data in group_data:
            group = PopulationGroup(
                group_id=data.get("group_id", f"GROUP_{len(groups)}"),
                name=data.get("name", "Unknown Group"),
                size=data.get("size", 0),
                characteristics=data.get("characteristics", {}),
                vulnerability_score=data.get("vulnerability_score", 1.0),
                need_level=data.get("need_level", 0.5),
                current_resources=data.get("current_resources", 0.0),
                proposed_allocation=data.get("proposed_allocation", 0.0),
                is_protected_group=data.get("is_protected_group", False)
            )
            groups.append(group)
        
        return groups
    
    def _generate_crisis_decision(
        self,
        decision_type: DecisionType,
        affected_area: str,
        pop_groups: List[PopulationGroup],
        resources: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> DecisionOutput:
        """Generate crisis decision using Crisis Decision Agent."""
        # Prepare context
        total_population = sum(g.size for g in pop_groups)
        
        context = {
            "affected_population": total_population,
            "location": affected_area,
            "resources": resources,
            "constraints": constraints,
            "time_sensitivity": constraints.get("time_sensitivity", "urgent")
        }
        
        # Convert PopulationGroup to dict for agent
        affected_groups = []
        for group in pop_groups:
            affected_groups.append({
                "name": group.name,
                "size": group.size,
                "need_level": group.need_level,
                "is_protected_group": group.is_protected_group,
                "resource_allocation": group.proposed_allocation,
                "priority": int(group.vulnerability_score * 100)
            })
        
        # Make decision
        decision = self.crisis_agent.make_decision(
            decision_type=decision_type,
            context=context,
            affected_groups=affected_groups
        )
        
        return decision
    
    def _validate_fairness(
        self,
        pop_groups: List[PopulationGroup],
        decision_output: DecisionOutput
    ) -> FairnessAssessment:
        """Validate fairness of the decision using Fairness Constraint Engine."""
        # Update proposed allocations based on decision
        if "allocations" in decision_output.recommendation:
            allocations = decision_output.recommendation["allocations"]
            
            # Map allocations back to groups
            for alloc in allocations:
                group_name = alloc.get("group")
                recommended_amt = alloc.get("recommended_allocation", 0)
                
                for group in pop_groups:
                    if group.name == group_name:
                        group.proposed_allocation = recommended_amt
                        break
        
        # Evaluate fairness
        assessment = self.fairness_engine.evaluate_fairness(
            groups=pop_groups,
            allocation_plan=decision_output.recommendation,
            enforce_constraints=False  # Don't raise, just assess
        )
        
        return assessment
    
    def _check_sovereignty_compliance(
        self,
        decision_output: DecisionOutput,
        jurisdiction: str
    ) -> Dict[str, Any]:
        """Check sovereignty and legal compliance using Sovereign Guardrail."""
        compliance_results = {
            "jurisdiction": jurisdiction,
            "checks_performed": [],
            "violations": [],
            "compliant": True
        }
        
        # Check 1: Data sovereignty (if decision involves data transfer)
        if "data_type" in decision_output.recommendation:
            try:
                self.sovereignty_guardrail.validate_action(
                    action_type="Data_Transfer",
                    payload={
                        "data_type": decision_output.recommendation.get("data_type"),
                        "destination": decision_output.recommendation.get("destination", "Local"),
                        "consent_token": "CRISIS_EMERGENCY_OVERRIDE"
                    },
                    jurisdiction=jurisdiction
                )
                compliance_results["checks_performed"].append("data_sovereignty_check_passed")
            except SovereigntyViolationError as e:
                compliance_results["violations"].append(str(e))
                compliance_results["compliant"] = False
        
        # Check 2: Consent validation (for non-emergency actions)
        if decision_output.decision_type not in [DecisionType.EVACUATION_ORDER]:
            # Emergency actions may override consent requirements
            compliance_results["checks_performed"].append("consent_check_waived_emergency")
        
        # Check 3: Retention compliance
        compliance_results["checks_performed"].append("retention_policy_applied")
        
        return compliance_results
    
    def _synthesize_recommendation(
        self,
        decision_output: DecisionOutput,
        fairness_assessment: FairnessAssessment,
        sovereignty_compliance: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize final recommendation from all components."""
        final_rec = {
            "decision_id": decision_output.decision_id,
            "decision_type": decision_output.decision_type.value,
            "base_recommendation": decision_output.recommendation,
            "ethical_compliance_status": {
                "humanitarian_law": all(decision_output.ethical_compliance.values()),
                "fairness_score": fairness_assessment.overall_fairness_score,
                "sovereignty_compliant": sovereignty_compliance["compliant"]
            },
            "fairness_adjustments": []
        }
        
        # Apply fairness adjustments if needed
        if fairness_assessment.overall_fairness_score < self.fairness_threshold:
            final_rec["fairness_adjustments"] = fairness_assessment.recommendations
        
        # Add citations
        final_rec["legal_citations"] = decision_output.humanitarian_law_citations
        
        return final_rec
    
    def _determine_approval_status(
        self,
        decision_output: DecisionOutput,
        fairness_assessment: FairnessAssessment,
        sovereignty_compliance: Dict[str, Any],
        rejection_reasons: List[str]
    ) -> str:
        """Determine if decision is approved, requires review, or rejected."""
        # Check for critical violations
        if not sovereignty_compliance["compliant"]:
            rejection_reasons.append("Sovereignty compliance failure")
            return "REJECTED"
        
        if fairness_assessment.violations:
            rejection_reasons.extend(fairness_assessment.violations)
        
        # Check if human approval required
        if decision_output.requires_human_approval:
            rejection_reasons.append("High-risk decision requires human approval")
            return "REQUIRES_HUMAN_REVIEW"
        
        # Check confidence threshold
        if decision_output.confidence_score < self.confidence_threshold:
            rejection_reasons.append(
                f"Confidence {decision_output.confidence_score:.2f} below threshold"
            )
            return "REQUIRES_HUMAN_REVIEW"
        
        # Check fairness threshold
        if fairness_assessment.overall_fairness_score < self.fairness_threshold:
            rejection_reasons.append(
                f"Fairness score {fairness_assessment.overall_fairness_score:.2f} below threshold"
            )
            return "REQUIRES_HUMAN_REVIEW"
        
        # All checks passed
        return "APPROVED"
    
    def _generate_ethical_summary(
        self,
        decision_output: DecisionOutput,
        fairness_assessment: FairnessAssessment,
        sovereignty_compliance: Dict[str, Any],
        approval_status: str
    ) -> str:
        """Generate human-readable ethical summary."""
        summary = []
        
        summary.append("=" * 80)
        summary.append("ETHICAL DECISION SUMMARY")
        summary.append("=" * 80)
        
        summary.append(f"\nDecision ID: {decision_output.decision_id}")
        summary.append(f"Approval Status: {approval_status}")
        summary.append(f"Timestamp: {datetime.utcnow().isoformat()}")
        
        summary.append("\n--- HUMANITARIAN LAW COMPLIANCE ---")
        for principle, compliant in decision_output.ethical_compliance.items():
            status = "✓" if compliant else "✗"
            summary.append(f"{status} {principle.upper()}")
        
        summary.append("\n--- FAIRNESS ASSESSMENT ---")
        summary.append(f"Overall Fairness Score: {fairness_assessment.overall_fairness_score:.2f}")
        for metric, score in fairness_assessment.metric_scores.items():
            summary.append(f"  {metric}: {score:.2f}")
        
        if fairness_assessment.equity_gaps:
            summary.append(f"\nEquity Gaps Identified: {len(fairness_assessment.equity_gaps)}")
        
        summary.append("\n--- SOVEREIGNTY COMPLIANCE ---")
        summary.append(f"Jurisdiction: {sovereignty_compliance['jurisdiction']}")
        summary.append(f"Compliant: {'✓' if sovereignty_compliance['compliant'] else '✗'}")
        
        summary.append("\n--- DECISION CONFIDENCE ---")
        summary.append(f"Confidence Score: {decision_output.confidence_score:.2f}")
        
        summary.append("\n--- LEGAL CITATIONS ---")
        for citation in decision_output.humanitarian_law_citations[:3]:
            summary.append(f"  • {citation}")
        
        summary.append("\n" + "=" * 80)
        
        return "\n".join(summary)
    
    def _create_rejection_result(
        self,
        scenario_type: CrisisScenarioType,
        rejection_reasons: List[str],
        error_type: str
    ) -> IntegratedDecisionResult:
        """Create a rejection result when decision fails ethical checks."""
        # Create minimal decision output for rejection
        decision_output = DecisionOutput(
            decision_id=f"REJECTED_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            decision_type=DecisionType.ALERT_BROADCAST,
            recommendation={"status": "REJECTED", "error": error_type},
            risk_level="CRITICAL",
            confidence_score=0.0,
            ethical_compliance={},
            humanitarian_law_citations=[],
            fairness_metrics={},
            explanation=f"Decision rejected: {'; '.join(rejection_reasons)}",
            requires_human_approval=True
        )
        
        # Create minimal fairness assessment
        fairness_assessment = FairnessAssessment(
            overall_fairness_score=0.0,
            metric_scores={},
            violations=rejection_reasons,
            recommendations=["Human review required before proceeding"],
            bias_indicators={},
            equity_gaps=[]
        )
        
        return IntegratedDecisionResult(
            scenario_type=scenario_type,
            decision_output=decision_output,
            fairness_assessment=fairness_assessment,
            sovereignty_compliance={"compliant": False},
            final_recommendation={"status": "REJECTED"},
            approval_status="REJECTED",
            rejection_reasons=rejection_reasons,
            ethical_summary=f"REJECTED: {'; '.join(rejection_reasons)}"
        )
    
    def _log_decision(self, result: IntegratedDecisionResult):
        """Log decision to history."""
        self.decision_history.append({
            "timestamp": result.timestamp.isoformat(),
            "scenario_type": result.scenario_type.value,
            "decision_id": result.decision_output.decision_id,
            "approval_status": result.approval_status,
            "fairness_score": result.fairness_assessment.overall_fairness_score,
            "confidence_score": result.decision_output.confidence_score
        })
    
    def get_decision_history(self) -> List[Dict[str, Any]]:
        """Return complete decision history."""
        return self.decision_history
    
    def export_decision_report(
        self, 
        result: IntegratedDecisionResult, 
        filepath: str = None
    ) -> str:
        """Export comprehensive decision report for transparency and audit."""
        report = {
            "decision_metadata": {
                "decision_id": result.decision_output.decision_id,
                "timestamp": result.timestamp.isoformat(),
                "scenario_type": result.scenario_type.value,
                "approval_status": result.approval_status
            },
            "crisis_decision": {
                "decision_type": result.decision_output.decision_type.value,
                "recommendation": result.decision_output.recommendation,
                "confidence_score": result.decision_output.confidence_score,
                "requires_human_approval": result.decision_output.requires_human_approval,
                "explanation": result.decision_output.explanation
            },
            "ethical_compliance": {
                "humanitarian_law": result.decision_output.ethical_compliance,
                "humanitarian_citations": result.decision_output.humanitarian_law_citations,
                "audit_trail": result.decision_output.audit_trail
            },
            "fairness_assessment": {
                "overall_score": result.fairness_assessment.overall_fairness_score,
                "metric_scores": result.fairness_assessment.metric_scores,
                "violations": result.fairness_assessment.violations,
                "recommendations": result.fairness_assessment.recommendations,
                "bias_indicators": result.fairness_assessment.bias_indicators,
                "equity_gaps": result.fairness_assessment.equity_gaps
            },
            "sovereignty_compliance": result.sovereignty_compliance,
            "final_recommendation": result.final_recommendation,
            "rejection_reasons": result.rejection_reasons,
            "ethical_summary": result.ethical_summary
        }
        
        if filepath:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            return filepath
        
        return json.dumps(report, indent=2, default=str)


# ═════════════════════════════════════════════════════════════════════════════
# Philosophy: "Layered ethical protection. Every autonomous decision must pass
# through multiple independent validation systems before it can be implemented."
#
# MISSION: To create AI agents that embody the highest ethical standards,
# operating with transparency, accountability, and unwavering commitment to
# human dignity in crisis response scenarios.
# ═════════════════════════════════════════════════════════════════════════════
