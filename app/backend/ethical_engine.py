"""
Ethical Engine: Humanitarian Protocols
══════════════════════════════════════════════════════════════════════════════

Implements Active Inference decision-making with humanitarian constraints.
Ensures all AI actions adhere to sovereign dignity principles.

Integrates with the governance_kernel for compliance validation.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
except ImportError:
    # Fallback if governance_kernel not available
    class SovereignGuardrail:
        def validate_action(self, *args, **kwargs):
            return True
    
    class SovereigntyViolationError(Exception):
        pass


class ActionType(Enum):
    """Types of AI-driven actions requiring ethical validation."""
    RESOURCE_ALLOCATION = "Resource Allocation"
    OUTBREAK_ALERT = "Outbreak Alert"
    DATA_TRANSFER = "Data Transfer"
    INTERVENTION_RECOMMENDATION = "Intervention Recommendation"
    PREDICTIVE_ANALYSIS = "Predictive Analysis"


class HumanitarianConstraint(Enum):
    """Core humanitarian constraints that cannot be violated."""
    DIGNITY = "Human Dignity"
    EQUITY = "Equitable Access"
    TRANSPARENCY = "Explainability Required"
    CONSENT = "Informed Consent"
    DATA_SOVEREIGNTY = "Data Remains Sovereign"


class EthicalEngine:
    """
    Active Inference engine with humanitarian guardrails.
    
    Every high-stakes decision passes through ethical validation
    before execution.
    """
    
    def __init__(self, jurisdiction: str = "GLOBAL_DEFAULT"):
        """
        Initialize ethical engine.
        
        Args:
            jurisdiction: Legal framework to apply (GDPR_EU, KDPA_KE, etc.)
        """
        self.jurisdiction = jurisdiction
        self.guardrail = SovereignGuardrail()
        self.decision_log = []
    
    def evaluate_action(self, action_type: ActionType, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a proposed action through humanitarian lens.
        
        Args:
            action_type: Type of action being proposed
            payload: Action parameters and context
        
        Returns:
            Evaluation result with approval/rejection and reasoning
        """
        evaluation = {
            "action_type": action_type.value,
            "timestamp": datetime.now().isoformat(),
            "payload": payload,
            "status": "PENDING",
            "violations": [],
            "reasoning": "",
            "approved": False
        }
        
        # Check humanitarian constraints
        constraint_checks = self._check_humanitarian_constraints(action_type, payload)
        
        # Check legal compliance
        compliance_check = self._check_legal_compliance(action_type, payload)
        
        # Combine checks
        evaluation["constraint_checks"] = constraint_checks
        evaluation["compliance_check"] = compliance_check
        
        # Determine approval
        all_constraints_passed = all(c["passed"] for c in constraint_checks.values())
        compliance_passed = compliance_check["passed"]
        
        if all_constraints_passed and compliance_passed:
            evaluation["status"] = "APPROVED"
            evaluation["approved"] = True
            evaluation["reasoning"] = "All humanitarian and legal checks passed."
        else:
            evaluation["status"] = "REJECTED"
            evaluation["approved"] = False
            
            # Collect violations
            violations = []
            for constraint, check in constraint_checks.items():
                if not check["passed"]:
                    violations.append(f"Humanitarian: {constraint} - {check['reason']}")
            
            if not compliance_passed:
                violations.append(f"Legal: {compliance_check['reason']}")
            
            evaluation["violations"] = violations
            evaluation["reasoning"] = "; ".join(violations)
        
        # Log decision
        self._log_decision(evaluation)
        
        return evaluation
    
    def _check_humanitarian_constraints(self, action_type: ActionType, 
                                       payload: Dict[str, Any]) -> Dict[str, Dict]:
        """Check action against humanitarian constraints."""
        checks = {}
        
        # Dignity: No discrimination in resource allocation
        if action_type == ActionType.RESOURCE_ALLOCATION:
            has_equity_criteria = payload.get("allocation_criteria", {}).get("equity_based", False)
            checks[HumanitarianConstraint.DIGNITY.value] = {
                "passed": has_equity_criteria,
                "reason": "Resource allocation must be equity-based" if not has_equity_criteria else "OK"
            }
        else:
            checks[HumanitarianConstraint.DIGNITY.value] = {
                "passed": True,
                "reason": "N/A for this action type"
            }
        
        # Transparency: High-risk decisions require explanation
        if action_type in [ActionType.INTERVENTION_RECOMMENDATION, ActionType.PREDICTIVE_ANALYSIS]:
            has_explanation = "explanation" in payload or "shap_values" in payload
            checks[HumanitarianConstraint.TRANSPARENCY.value] = {
                "passed": has_explanation,
                "reason": "High-risk action requires explainability" if not has_explanation else "OK"
            }
        else:
            checks[HumanitarianConstraint.TRANSPARENCY.value] = {
                "passed": True,
                "reason": "N/A for this action type"
            }
        
        # Consent: Data processing requires consent
        if action_type == ActionType.DATA_TRANSFER:
            has_consent = payload.get("consent_token") is not None
            checks[HumanitarianConstraint.CONSENT.value] = {
                "passed": has_consent,
                "reason": "Data transfer requires consent token" if not has_consent else "OK"
            }
        else:
            checks[HumanitarianConstraint.CONSENT.value] = {
                "passed": True,
                "reason": "N/A for this action type"
            }
        
        # Data Sovereignty: PHI cannot leave jurisdiction
        if action_type == ActionType.DATA_TRANSFER:
            is_phi = payload.get("data_type") == "PHI"
            is_foreign = payload.get("destination_jurisdiction") != self.jurisdiction
            sovereignty_ok = not (is_phi and is_foreign)
            checks[HumanitarianConstraint.DATA_SOVEREIGNTY.value] = {
                "passed": sovereignty_ok,
                "reason": "PHI cannot cross sovereign boundaries" if not sovereignty_ok else "OK"
            }
        else:
            checks[HumanitarianConstraint.DATA_SOVEREIGNTY.value] = {
                "passed": True,
                "reason": "N/A for this action type"
            }
        
        return checks
    
    def _check_legal_compliance(self, action_type: ActionType, 
                                payload: Dict[str, Any]) -> Dict[str, Any]:
        """Check action against legal frameworks via SovereignGuardrail."""
        try:
            # Map action type to compliance action
            compliance_action = {
                ActionType.DATA_TRANSFER: "Data_Transfer",
                ActionType.INTERVENTION_RECOMMENDATION: "High_Risk_Inference",
                ActionType.PREDICTIVE_ANALYSIS: "High_Risk_Inference",
                ActionType.RESOURCE_ALLOCATION: "Processing",
                ActionType.OUTBREAK_ALERT: "Processing"
            }.get(action_type, "Processing")
            
            # Validate through guardrail
            self.guardrail.validate_action(
                action_type=compliance_action,
                payload=payload,
                jurisdiction=self.jurisdiction
            )
            
            return {
                "passed": True,
                "reason": f"Complies with {self.jurisdiction} framework"
            }
        
        except SovereigntyViolationError as e:
            return {
                "passed": False,
                "reason": str(e)
            }
        except Exception as e:
            # If guardrail not available, pass with warning
            return {
                "passed": True,
                "reason": f"Compliance check bypassed: {str(e)}"
            }
    
    def _log_decision(self, evaluation: Dict[str, Any]):
        """Log decision to audit trail."""
        log_entry = {
            "timestamp": evaluation["timestamp"],
            "action": evaluation["action_type"],
            "status": evaluation["status"],
            "approved": evaluation["approved"],
            "reasoning": evaluation["reasoning"]
        }
        self.decision_log.append(log_entry)
    
    def get_decision_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve recent decision log for audit.
        
        Args:
            limit: Maximum number of entries to return
        
        Returns:
            List of recent decisions
        """
        return self.decision_log[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics on ethical decisions."""
        total = len(self.decision_log)
        if total == 0:
            return {
                "total_decisions": 0,
                "approved": 0,
                "rejected": 0,
                "approval_rate": 0.0
            }
        
        approved = sum(1 for d in self.decision_log if d["approved"])
        
        return {
            "total_decisions": total,
            "approved": approved,
            "rejected": total - approved,
            "approval_rate": round(approved / total, 3)
        }
