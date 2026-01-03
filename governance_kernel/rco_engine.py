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
Regenerative Compliance Oracle (RCO) Engine
═════════════════════════════════════════════════════════════════════════════

The self-updating regulatory intelligence system that detects legal drift,
auto-generates compliance patches, and predicts future regulatory amendments.

This module implements:
- RegulatoryEntropySensor: Measures drift from baseline compliance using KL Divergence
- AutoPatchGenerator: Generates hotfixes when regulations change
- Predictive Amendment Engine: Forecasts regulatory changes from external signals

Philosophy: "The law is not static. Neither should compliance be."
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from scipy.stats import entropy

logger = logging.getLogger(__name__)


class RegulatoryDriftError(Exception):
    """Raised when regulatory drift exceeds acceptable thresholds."""
    pass


@dataclass
class RegulatorySignal:
    """External signal indicating potential regulatory change."""
    source: str
    signal_type: str  # "legislative", "judicial", "regulatory", "emergency"
    jurisdiction: str
    content: str
    confidence_score: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class CompliancePatch:
    """Auto-generated compliance hotfix."""
    patch_id: str
    law_id: str
    drift_score: float
    patch_type: str  # "rule_update", "threshold_adjustment", "new_requirement"
    changes: Dict[str, Any]
    validation_status: str = "pending"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class RegulatoryEntropySensor:
    """
    Measures regulatory drift using KL Divergence to detect when
    operational patterns deviate from compliance baselines.
    """
    
    def __init__(self, baseline_distributions: Optional[Dict[str, np.ndarray]] = None):
        """
        Initialize the entropy sensor.
        
        Args:
            baseline_distributions: Dictionary mapping law IDs to baseline probability distributions
        """
        self.baseline_distributions = baseline_distributions or {}
        self.drift_history: List[Dict[str, Any]] = []
        logger.info("RegulatoryEntropySensor initialized")
    
    def measure_drift(self, data_stream: Dict[str, Any]) -> Dict[str, float]:
        """
        Measure regulatory drift using KL Divergence.
        
        Args:
            data_stream: Current operational data with observed frequencies
            
        Returns:
            Dictionary mapping law IDs to drift scores (KL divergence values)
        """
        drift_scores = {}
        
        for law_id, observed_dist in data_stream.get("distributions", {}).items():
            if law_id not in self.baseline_distributions:
                logger.warning(f"No baseline distribution for {law_id}, creating from observed")
                self.baseline_distributions[law_id] = observed_dist
                drift_scores[law_id] = 0.0
                continue
            
            baseline = self.baseline_distributions[law_id]
            observed = np.array(observed_dist)
            
            # Ensure distributions are normalized
            baseline_norm = baseline / np.sum(baseline)
            observed_norm = observed / np.sum(observed)
            
            # Add small epsilon to avoid log(0)
            epsilon = 1e-10
            baseline_norm = baseline_norm + epsilon
            observed_norm = observed_norm + epsilon
            
            # Calculate KL Divergence: D_KL(P || Q) = sum(P * log(P/Q))
            kl_divergence = entropy(observed_norm, baseline_norm)
            
            drift_scores[law_id] = float(kl_divergence)
            
            logger.info(f"Drift measured for {law_id}: {kl_divergence:.4f}")
        
        # Record drift measurement
        self.drift_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "drift_scores": drift_scores
        })
        
        return drift_scores
    
    def is_drift_critical(self, drift_score: float, threshold: float = 0.5) -> bool:
        """
        Determine if drift score exceeds critical threshold.
        
        Args:
            drift_score: KL divergence value
            threshold: Critical threshold (default 0.5)
            
        Returns:
            True if drift is critical
        """
        return drift_score > threshold
    
    def get_drift_trend(self, law_id: str, window: int = 10) -> Optional[str]:
        """
        Analyze trend of drift over recent measurements.
        
        Args:
            law_id: Law identifier
            window: Number of recent measurements to analyze
            
        Returns:
            "increasing", "decreasing", "stable", or None
        """
        if len(self.drift_history) < 2:
            return None
        
        recent_scores = [
            entry["drift_scores"].get(law_id, 0.0)
            for entry in self.drift_history[-window:]
            if law_id in entry["drift_scores"]
        ]
        
        if len(recent_scores) < 2:
            return None
        
        # Simple linear trend
        trend_slope = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
        
        if trend_slope > 0.5:
            return "increasing"
        elif trend_slope < -0.5:
            return "decreasing"
        else:
            return "stable"


class AutoPatchGenerator:
    """
    Generates compliance hotfixes when regulatory drift is detected
    or when new regulations are enacted.
    """
    
    def __init__(self, sectoral_laws_path: Optional[str] = None):
        """
        Initialize the patch generator.
        
        Args:
            sectoral_laws_path: Path to sectoral_laws.json file
        """
        if sectoral_laws_path is None:
            sectoral_laws_path = os.path.join(
                os.path.dirname(__file__), "sectoral_laws.json"
            )
        
        self.sectoral_laws_path = sectoral_laws_path
        self.laws_registry = self._load_laws_registry()
        self.patch_history: List[CompliancePatch] = []
        logger.info("AutoPatchGenerator initialized")
    
    def _load_laws_registry(self) -> Dict[str, Any]:
        """Load the sectoral laws registry."""
        try:
            with open(self.sectoral_laws_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Sectoral laws file not found: {self.sectoral_laws_path}")
            return {"45_law_quantum_nexus": {"laws": {}}}
    
    def generate_hotfix(self, law_id: str, drift_score: float) -> CompliancePatch:
        """
        Generate a compliance hotfix for detected drift.
        
        Args:
            law_id: Identifier of the law experiencing drift
            drift_score: Measured KL divergence
            
        Returns:
            CompliancePatch object containing the hotfix
        """
        timestamp = datetime.now(timezone.utc)
        patch_id = f"PATCH-{law_id}-{timestamp.strftime('%Y%m%d%H%M%S')}"
        
        # Determine patch type based on drift severity
        if drift_score > 1.0:
            patch_type = "new_requirement"
        elif drift_score > 0.5:
            patch_type = "threshold_adjustment"
        else:
            patch_type = "rule_update"
        
        # Get law details
        law_details = self._get_law_details(law_id)
        
        # Generate appropriate changes
        changes = self._generate_changes(law_id, drift_score, patch_type, law_details)
        
        patch = CompliancePatch(
            patch_id=patch_id,
            law_id=law_id,
            drift_score=drift_score,
            patch_type=patch_type,
            changes=changes,
            validation_status="generated"
        )
        
        self.patch_history.append(patch)
        logger.info(f"Generated hotfix {patch_id} for {law_id} (drift: {drift_score:.4f})")
        
        return patch
    
    def _get_law_details(self, law_id: str) -> Dict[str, Any]:
        """Retrieve law details from registry."""
        laws = self.laws_registry.get("45_law_quantum_nexus", {}).get("laws", {})
        
        for law_key, law_data in laws.items():
            if law_data.get("id") == law_id:
                return law_data
        
        return {}
    
    def _generate_changes(
        self, 
        law_id: str, 
        drift_score: float, 
        patch_type: str,
        law_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate specific changes for the patch.
        
        Args:
            law_id: Law identifier
            drift_score: Drift score
            patch_type: Type of patch needed
            law_details: Details of the law from registry
            
        Returns:
            Dictionary of changes to apply
        """
        changes = {
            "law_id": law_id,
            "law_name": law_details.get("name", "Unknown"),
            "reason": f"Regulatory drift detected (score: {drift_score:.4f})",
            "recommended_actions": []
        }
        
        if patch_type == "new_requirement":
            changes["recommended_actions"].extend([
                "Review and update compliance procedures",
                "Conduct full audit of affected operations",
                "Update training materials",
                "Notify stakeholders of changes"
            ])
            changes["urgency"] = "high"
        elif patch_type == "threshold_adjustment":
            changes["recommended_actions"].extend([
                "Adjust monitoring thresholds",
                "Update validation rules",
                "Review recent operational data"
            ])
            changes["urgency"] = "medium"
        else:  # rule_update
            changes["recommended_actions"].extend([
                "Update rule parameters",
                "Test updated rules",
                "Document changes"
            ])
            changes["urgency"] = "low"
        
        # Add specific enforcement actions from law details
        enforcement = law_details.get("enforcement_action", {})
        if enforcement:
            changes["enforcement_requirements"] = enforcement.get("requirements", [])
            changes["validation_method"] = enforcement.get("validation", "")
        
        return changes
    
    def apply_patch(self, patch: CompliancePatch) -> bool:
        """
        Apply a generated patch to the system.
        
        Args:
            patch: CompliancePatch to apply
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Applying patch {patch.patch_id}")
            
            # In a real system, this would update configuration, rules, etc.
            # For now, we mark it as applied
            patch.validation_status = "applied"
            
            logger.info(f"Patch {patch.patch_id} applied successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to apply patch {patch.patch_id}: {e}")
            patch.validation_status = "failed"
            return False


class RegenerativeComplianceOracle:
    """
    Main RCO engine that orchestrates drift detection, patch generation,
    and predictive regulatory intelligence.
    """
    
    def __init__(self, sectoral_laws_path: Optional[str] = None):
        """
        Initialize the RCO engine.
        
        Args:
            sectoral_laws_path: Path to sectoral_laws.json file
        """
        self.entropy_sensor = RegulatoryEntropySensor()
        self.patch_generator = AutoPatchGenerator(sectoral_laws_path)
        self.predictive_signals: List[RegulatorySignal] = []
        logger.info("RegenerativeComplianceOracle initialized")
    
    def monitor_compliance(self, data_stream: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor compliance state and detect drift.
        
        Args:
            data_stream: Current operational data
            
        Returns:
            Dictionary containing drift analysis and generated patches
        """
        # Measure drift
        drift_scores = self.entropy_sensor.measure_drift(data_stream)
        
        # Generate patches for critical drift
        patches = []
        for law_id, score in drift_scores.items():
            if self.entropy_sensor.is_drift_critical(score):
                patch = self.patch_generator.generate_hotfix(law_id, score)
                patches.append(patch)
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "drift_scores": drift_scores,
            "critical_drifts": [
                law_id for law_id, score in drift_scores.items()
                if self.entropy_sensor.is_drift_critical(score)
            ],
            "patches_generated": len(patches),
            "patches": [
                {
                    "patch_id": p.patch_id,
                    "law_id": p.law_id,
                    "patch_type": p.patch_type,
                    "urgency": p.changes.get("urgency", "unknown")
                }
                for p in patches
            ]
        }
    
    def predict_amendment(self, external_signal: RegulatorySignal) -> Dict[str, Any]:
        """
        Predict potential regulatory amendments from external signals.
        
        Args:
            external_signal: Signal indicating potential regulatory change
            
        Returns:
            Dictionary containing prediction analysis
        """
        self.predictive_signals.append(external_signal)
        
        # Analyze signal
        prediction = {
            "signal_id": len(self.predictive_signals),
            "source": external_signal.source,
            "signal_type": external_signal.signal_type,
            "jurisdiction": external_signal.jurisdiction,
            "confidence": external_signal.confidence_score,
            "timestamp": external_signal.timestamp.isoformat(),
            "predicted_impact": self._assess_impact(external_signal),
            "recommended_preparation": self._generate_preparation_plan(external_signal)
        }
        
        logger.info(f"Amendment prediction generated for signal from {external_signal.source}")
        
        return prediction
    
    def _assess_impact(self, signal: RegulatorySignal) -> str:
        """Assess the potential impact of a regulatory signal."""
        if signal.confidence_score > 0.8:
            return "high"
        elif signal.confidence_score > 0.5:
            return "medium"
        else:
            return "low"
    
    def _generate_preparation_plan(self, signal: RegulatorySignal) -> List[str]:
        """Generate a preparation plan for predicted regulatory change."""
        plan = [
            "Monitor official sources for confirmation",
            "Review current compliance posture",
            "Identify affected systems and processes"
        ]
        
        if signal.signal_type == "emergency":
            plan.append("Prepare emergency response protocols")
        elif signal.signal_type == "legislative":
            plan.append("Engage with policy stakeholders")
        
        return plan
    
    def get_compliance_health_score(self) -> float:
        """
        Calculate overall compliance health score.
        
        Returns:
            Score from 0.0 (critical) to 1.0 (excellent)
        """
        if not self.entropy_sensor.drift_history:
            return 1.0
        
        # Get recent drift scores
        recent_drifts = self.entropy_sensor.drift_history[-10:]
        all_scores = []
        
        for entry in recent_drifts:
            all_scores.extend(entry["drift_scores"].values())
        
        if not all_scores:
            return 1.0
        
        # Calculate health score (inverse of average drift)
        avg_drift = np.mean(all_scores)
        health_score = max(0.0, 1.0 - (avg_drift / 2.0))  # Normalize
        
        return health_score
