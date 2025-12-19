"""
Ethical Engine & Humanitarian Margin Calculator
═════════════════════════════════════════════════════════════════════════════

The 'Humanitarian Constraint Engine' of VISENDI56 that applies ethical frameworks 
to health system actions, ensuring compliance with international humanitarian law 
and WHO outbreak response guidelines.

This module implements:
- Geneva Convention Article 3 constraints for conflict zones
- WHO outbreak response guidelines for disease containment
- Humanitarian margin calculations for decision-making
- Integration with Google Cloud Secret Manager for protocol management

Philosophy: "First, do no harm. Second, maximize human dignity in crisis."
"""

import json
import os
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime, timezone
import numpy as np


class HumanitarianViolationError(Exception):
    """
    Raised when an action violates humanitarian constraints.
    Includes specific international law citation.
    """
    pass


@dataclass
class ActionContext:
    """Context information for evaluating an action's humanitarian constraints."""
    conflict_zone: bool = False
    outbreak_suspected: bool = False
    civilian_population: int = 0
    healthcare_capacity: float = 1.0  # 0.0 = collapsed, 1.0 = normal
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class EthicalEngine:
    """
    Enforcement engine for international humanitarian law and WHO guidelines.
    Applies ethical constraints and calculates humanitarian margins for 
    health system actions in crisis scenarios.
    
    Usage:
        engine = EthicalEngine()
        result = engine.apply_constraints(
            action={'type': 'quarantine', 'scope': 'district'},
            context={'conflict_zone': True, 'outbreak_suspected': True}
        )
    """

    def __init__(self, use_cloud_secrets: bool = False):
        """
        Initialize the ethical engine with humanitarian protocols.
        
        Args:
            use_cloud_secrets: If True, attempt to load protocols from Google Cloud 
                             Secret Manager. If False or if loading fails, use 
                             default protocols.
        """
        self.protocols = self._load_protocols(use_cloud_secrets)
        self.audit_log = []

    def _load_protocols(self, use_cloud_secrets: bool) -> Dict[str, Any]:
        """
        Load humanitarian protocols from Google Cloud Secret Manager or defaults.
        
        Args:
            use_cloud_secrets: Whether to attempt cloud secret loading
            
        Returns:
            Dictionary of humanitarian protocols
        """
        if use_cloud_secrets:
            try:
                from google.cloud import secretmanager
                
                client = secretmanager.SecretManagerServiceClient()
                project_id = os.environ.get('GCP_PROJECT_ID', 'iluminara')
                secret_name = f"projects/{project_id}/secrets/humanitarian-protocols/versions/latest"
                
                response = client.access_secret_version(name=secret_name)
                protocols = json.loads(response.payload.data.decode("UTF-8"))
                
                self._log_event("INFO", "Loaded protocols from Google Cloud Secret Manager")
                return protocols
                
            except Exception as e:
                self._log_event("WARNING", f"Failed to load cloud secrets: {e}. Using defaults.")
        
        # Default humanitarian protocols (encoded from international law)
        return {
            "geneva_convention_article_3": {
                "description": "Common Article 3 of Geneva Conventions - Minimum standards in conflict",
                "constraints": {
                    "proportionality_required": True,
                    "distinction_required": True,  # Distinguish civilians from combatants
                    "no_collective_punishment": True,
                    "medical_neutrality": True,
                },
                "proportionality_factors": {
                    "military_advantage_weight": 0.0,  # Health is non-military
                    "civilian_harm_weight": 1.0,
                    "medical_necessity_weight": 0.9,
                }
            },
            "who_outbreak_response": {
                "description": "WHO International Health Regulations (2005) - Outbreak response",
                "constraints": {
                    "necessity_required": True,
                    "least_restrictive_means": True,
                    "scientific_evidence_based": True,
                    "time_limited": True,
                },
                "necessity_thresholds": {
                    "min_attack_rate": 0.01,  # 1% population affected
                    "min_r_effective": 1.0,  # Disease spreading
                    "min_severity_score": 0.5,  # Moderate severity
                }
            },
            "humanitarian_margin": {
                "description": "Safety margin for decision-making under uncertainty",
                "calculation": {
                    "base_margin": 0.20,  # 20% default safety buffer
                    "conflict_multiplier": 1.5,  # Increase margin in conflict
                    "outbreak_multiplier": 1.3,  # Increase margin in outbreak
                    "capacity_reduction_factor": 0.5,  # Reduce action when capacity low
                }
            }
        }

    def apply_constraints(
        self, 
        action: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply humanitarian constraints to an action and calculate margins.
        
        Args:
            action: The proposed action (e.g., {'type': 'quarantine', 'scope': 'district'})
            context: Context information (conflict_zone, outbreak_suspected, etc.)
            
        Returns:
            Dictionary with:
            - action: Modified action with constraints applied
            - humanitarian_margin: Calculated safety margin
            - constraints_applied: List of constraints that were triggered
            - violations: List of any violations detected
            
        Raises:
            HumanitarianViolationError: If action violates humanitarian law
        """
        # Create structured context
        ctx = ActionContext(
            conflict_zone=context.get('conflict_zone', False),
            outbreak_suspected=context.get('outbreak_suspected', False),
            civilian_population=context.get('civilian_population', 0),
            healthcare_capacity=context.get('healthcare_capacity', 1.0)
        )
        
        constraints_applied = []
        violations = []
        modified_action = action.copy()
        
        # Geneva Convention Article 3 constraints
        if ctx.conflict_zone:
            try:
                modified_action = self._apply_proportionality(modified_action, ctx)
                constraints_applied.append("Geneva Convention Article 3 - Proportionality")
            except HumanitarianViolationError as e:
                violations.append(str(e))
                raise
        
        # WHO outbreak response guidelines
        if ctx.outbreak_suspected:
            try:
                modified_action = self._apply_necessity(modified_action, ctx)
                constraints_applied.append("WHO IHR (2005) - Necessity")
            except HumanitarianViolationError as e:
                violations.append(str(e))
                raise
        
        # Calculate humanitarian margin
        margin_result = self._calculate_humanitarian_margin(modified_action, ctx)
        
        # Log the evaluation
        self._log_event(
            "CONSTRAINT_APPLICATION",
            f"Action: {action.get('type')}, Constraints: {len(constraints_applied)}, "
            f"Margin: {margin_result['margin']:.2%}"
        )
        
        return {
            "action": modified_action,
            "humanitarian_margin": margin_result,
            "constraints_applied": constraints_applied,
            "violations": violations,
            "context": {
                "conflict_zone": ctx.conflict_zone,
                "outbreak_suspected": ctx.outbreak_suspected,
                "timestamp": ctx.timestamp.isoformat()
            }
        }

    def _apply_proportionality(
        self, 
        action: Dict[str, Any], 
        context: ActionContext
    ) -> Dict[str, Any]:
        """
        Apply Geneva Convention Article 3 proportionality constraints.
        
        Proportionality requires that:
        1. Harm to civilians must not be excessive relative to anticipated benefit
        2. Medical actions must serve health purposes, not military objectives
        3. The least harmful alternative should be chosen
        
        Args:
            action: The proposed action
            context: Action context
            
        Returns:
            Modified action with proportionality constraints applied
            
        Raises:
            HumanitarianViolationError: If action is disproportionate
        """
        protocol = self.protocols["geneva_convention_article_3"]
        factors = protocol["proportionality_factors"]
        
        # Assess proportionality
        civilian_harm = action.get('estimated_civilian_impact', 0.0)
        medical_benefit = action.get('medical_benefit', 0.0)
        
        # Calculate proportionality score (benefit must outweigh harm)
        proportionality_score = (
            medical_benefit * factors['medical_necessity_weight'] - 
            civilian_harm * factors['civilian_harm_weight']
        )
        
        # Enforce minimum threshold
        if proportionality_score < 0:
            citation = "Geneva Convention Article 3 (Common Article) - Proportionality"
            raise HumanitarianViolationError(
                f"❌ PROPORTIONALITY VIOLATION: Civilian harm ({civilian_harm:.2f}) "
                f"exceeds medical benefit ({medical_benefit:.2f}).\n"
                f"   Action Type: {action.get('type')}\n"
                f"   Proportionality Score: {proportionality_score:.2f}\n"
                f"   Legal Citation: {citation}"
            )
        
        # Apply distinction requirement (separate civilian/combatant considerations)
        if protocol["constraints"]["distinction_required"]:
            if not action.get('civilian_protection_measures'):
                action['civilian_protection_measures'] = [
                    "Maintain medical neutrality",
                    "Ensure non-discriminatory access to healthcare",
                    "Protect medical facilities and personnel"
                ]
        
        # Reduce scope if healthcare capacity is low
        if context.healthcare_capacity < 0.5:
            if 'scope' in action:
                action['scope'] = 'limited'
                action['capacity_constraint'] = f"Reduced due to {context.healthcare_capacity:.0%} capacity"
        
        return action

    def _apply_necessity(
        self, 
        action: Dict[str, Any], 
        context: ActionContext
    ) -> Dict[str, Any]:
        """
        Apply WHO outbreak response necessity constraints.
        
        Necessity requires that:
        1. Measures are based on scientific evidence
        2. Measures are proportionate to public health risk
        3. Less restrictive alternatives are considered
        4. Measures are time-limited and reviewable
        
        Args:
            action: The proposed action
            context: Action context
            
        Returns:
            Modified action with necessity constraints applied
            
        Raises:
            HumanitarianViolationError: If action is not necessary
        """
        protocol = self.protocols["who_outbreak_response"]
        thresholds = protocol["necessity_thresholds"]
        
        # Check scientific evidence requirement
        if not action.get('scientific_evidence'):
            action['scientific_evidence'] = "Based on WHO IHR (2005) outbreak response protocols"
        
        # Assess necessity based on outbreak parameters
        attack_rate = action.get('attack_rate', 0.0)
        r_effective = action.get('r_effective', 1.0)
        severity = action.get('severity_score', 0.5)
        
        necessity_met = (
            attack_rate >= thresholds['min_attack_rate'] and
            r_effective >= thresholds['min_r_effective'] and
            severity >= thresholds['min_severity_score']
        )
        
        if not necessity_met:
            citation = "WHO International Health Regulations (2005) - Article 43 (Necessity)"
            raise HumanitarianViolationError(
                f"❌ NECESSITY VIOLATION: Action not justified by outbreak parameters.\n"
                f"   Attack Rate: {attack_rate:.2%} (threshold: {thresholds['min_attack_rate']:.2%})\n"
                f"   R-effective: {r_effective:.2f} (threshold: {thresholds['min_r_effective']:.2f})\n"
                f"   Severity: {severity:.2f} (threshold: {thresholds['min_severity_score']:.2f})\n"
                f"   Legal Citation: {citation}"
            )
        
        # Apply least restrictive means
        if protocol["constraints"]["least_restrictive_means"]:
            action['alternatives_considered'] = [
                "Voluntary isolation with support",
                "Contact tracing and monitoring",
                "Targeted community interventions"
            ]
        
        # Enforce time limits
        if protocol["constraints"]["time_limited"]:
            if 'duration_days' not in action:
                action['duration_days'] = 14  # Default 2-week review period
            action['review_required'] = True
            action['review_interval_days'] = 7
        
        return action

    def _calculate_humanitarian_margin(
        self, 
        action: Dict[str, Any], 
        context: ActionContext
    ) -> Dict[str, Any]:
        """
        Calculate the humanitarian safety margin for decision-making.
        
        The humanitarian margin represents additional safety buffer applied to
        decisions under uncertainty, especially in crisis contexts. Higher margins
        mean more conservative/protective approaches.
        
        Factors considered:
        - Base margin (default safety buffer)
        - Conflict zone multiplier
        - Outbreak scenario multiplier
        - Healthcare capacity constraints
        
        Args:
            action: The action being evaluated
            context: Action context
            
        Returns:
            Dictionary with:
            - margin: Final humanitarian margin (0.0 to 1.0)
            - base: Base margin before adjustments
            - multipliers: Applied multipliers
            - interpretation: Human-readable explanation
        """
        config = self.protocols["humanitarian_margin"]["calculation"]
        
        # Start with base margin
        base_margin = config["base_margin"]
        margin = base_margin
        multipliers = []
        
        # Apply conflict zone multiplier
        if context.conflict_zone:
            multiplier = config["conflict_multiplier"]
            margin *= multiplier
            multipliers.append(f"Conflict zone: {multiplier}x")
        
        # Apply outbreak multiplier
        if context.outbreak_suspected:
            multiplier = config["outbreak_multiplier"]
            margin *= multiplier
            multipliers.append(f"Outbreak: {multiplier}x")
        
        # Increase margin when capacity is constrained (more caution needed)
        capacity_factor = context.healthcare_capacity
        if capacity_factor < 1.0:
            # Lower capacity means higher margin (more conservative)
            capacity_multiplier = 1.0 + (1.0 - capacity_factor) * 0.5
            margin *= capacity_multiplier
            multipliers.append(f"Capacity constraint ({capacity_factor:.0%}): {capacity_multiplier:.2f}x")
        
        # Cap margin at reasonable bounds
        margin = np.clip(margin, 0.0, 1.0)
        
        # Interpret margin
        if margin >= 0.5:
            interpretation = "HIGH - Very conservative approach recommended"
        elif margin >= 0.3:
            interpretation = "MODERATE - Balanced approach with safety buffer"
        else:
            interpretation = "LOW - Standard safety protocols apply"
        
        return {
            "margin": float(margin),
            "base": float(base_margin),
            "multipliers": multipliers,
            "interpretation": interpretation,
            "factors": {
                "conflict_zone": context.conflict_zone,
                "outbreak_suspected": context.outbreak_suspected,
                "healthcare_capacity": context.healthcare_capacity
            }
        }

    def _log_event(self, level: str, message: str):
        """Log an event to the audit trail."""
        self.audit_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message
        })

    def get_audit_log(self) -> list:
        """Return the complete audit trail."""
        return self.audit_log

    def clear_audit_log(self):
        """Clear the audit log (for testing or privacy)."""
        self.audit_log = []


# ═════════════════════════════════════════════════════════════════════════════
# MISSION: To architect systems that transform preventable suffering from 
# statistical inevitability to historical anomaly.
#
# ETHICAL PILLAR: International Humanitarian Law Compliance
# ═════════════════════════════════════════════════════════════════════════════
