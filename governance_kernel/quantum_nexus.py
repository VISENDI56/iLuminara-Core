"""
Quantum Nexus - Multi-Law Harmonization Engine
═════════════════════════════════════════════════════════════════════════════

Resolves conflicts between overlapping regulations using quantum-inspired
conflict resolution and retroactive alignment capabilities.

This module implements:
- harmonize_risk_vectors: Resolves conflicts between laws (e.g., GDPR vs. HIPAA)
- retroactive_alignment_engine: Scans historical data for compliance gaps via IP-09

Philosophy: "When laws collide, harmony emerges from the highest standard."
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class ConflictResolutionStrategy(Enum):
    """Strategies for resolving regulatory conflicts."""
    STRICTEST_REQUIREMENTS = "apply_strictest_requirements"
    TERRITORIAL_PRIORITY = "territorial_priority"
    PUBLIC_HEALTH_OVERRIDE = "public_health_emergency_override"
    TEMPORAL_PRECEDENCE = "temporal_precedence"
    SECTORAL_SPECIALIZATION = "sectoral_specialization"


@dataclass
class LawConflict:
    """Represents a conflict between two or more laws."""
    conflict_id: str
    laws_involved: List[str]
    conflict_type: str
    description: str
    severity: float  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class HarmonizationResult:
    """Result of harmonizing conflicting laws."""
    conflict: LawConflict
    resolution_strategy: ConflictResolutionStrategy
    resolved_requirements: List[str]
    priority_order: List[str]
    justification: str
    confidence: float


@dataclass
class RetroactiveAuditResult:
    """Result of retroactive compliance audit."""
    audit_id: str
    time_range: Tuple[datetime, datetime]
    records_scanned: int
    violations_found: int
    violations_by_law: Dict[str, int]
    remediation_required: List[Dict[str, Any]]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class QuantumNexus:
    """
    Main quantum nexus class for multi-law harmonization and
    retroactive compliance alignment.
    """
    
    def __init__(self, sectoral_laws_path: Optional[str] = None):
        """
        Initialize the Quantum Nexus.
        
        Args:
            sectoral_laws_path: Path to sectoral_laws.json file
        """
        if sectoral_laws_path is None:
            import os
            sectoral_laws_path = os.path.join(
                os.path.dirname(__file__), "sectoral_laws.json"
            )
        
        self.sectoral_laws_path = sectoral_laws_path
        self.laws_registry = self._load_laws_registry()
        self.conflict_matrix = self._load_conflict_matrix()
        self.harmonization_history: List[HarmonizationResult] = []
        self.audit_history: List[RetroactiveAuditResult] = []
        logger.info("QuantumNexus initialized")
    
    def _load_laws_registry(self) -> Dict[str, Any]:
        """Load the sectoral laws registry."""
        try:
            with open(self.sectoral_laws_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Sectoral laws file not found: {self.sectoral_laws_path}")
            return {"45_law_quantum_nexus": {"laws": {}, "conflict_resolution_matrix": {}}}
    
    def _load_conflict_matrix(self) -> Dict[str, Any]:
        """Load the conflict resolution matrix."""
        nexus = self.laws_registry.get("45_law_quantum_nexus", {})
        return nexus.get("conflict_resolution_matrix", {})
    
    def harmonize_risk_vectors(
        self, 
        applicable_laws: List[str],
        operation_context: Dict[str, Any]
    ) -> HarmonizationResult:
        """
        Harmonize conflicting requirements from multiple applicable laws.
        
        Args:
            applicable_laws: List of law IDs that apply to the operation
            operation_context: Context of the operation including location, sector, etc.
            
        Returns:
            HarmonizationResult with resolved requirements and priority order
        """
        logger.info(f"Harmonizing {len(applicable_laws)} applicable laws")
        
        # Detect conflicts
        conflict = self._detect_conflicts(applicable_laws, operation_context)
        
        if not conflict:
            # No conflicts, combine all requirements
            return self._combine_non_conflicting_laws(applicable_laws, operation_context)
        
        # Resolve conflicts using appropriate strategy
        resolution_strategy = self._determine_resolution_strategy(conflict, operation_context)
        
        result = self._apply_resolution_strategy(
            conflict, 
            resolution_strategy, 
            applicable_laws,
            operation_context
        )
        
        self.harmonization_history.append(result)
        
        logger.info(
            f"Harmonization complete: {len(result.resolved_requirements)} "
            f"requirements, strategy: {resolution_strategy.value}"
        )
        
        return result
    
    def _detect_conflicts(
        self, 
        applicable_laws: List[str],
        operation_context: Dict[str, Any]
    ) -> Optional[LawConflict]:
        """
        Detect conflicts between applicable laws.
        
        Args:
            applicable_laws: List of law IDs
            operation_context: Operation context
            
        Returns:
            LawConflict if conflicts exist, None otherwise
        """
        # Check predefined conflict matrix
        for conflict_key, conflict_data in self.conflict_matrix.items():
            laws_in_conflict = conflict_key.split("_vs_")
            
            # Map conflict key names to law IDs
            # E.g., "GDPR" in key maps to "LAW-006", "HIPAA" to "LAW-007"
            law_name_to_id = {
                "GDPR": "LAW-006",
                "HIPAA": "LAW-007",
                "MALABO": "LAW-003",
                "IHR": "LAW-002"
            }
            
            conflict_law_ids = []
            for law_name in laws_in_conflict:
                for key, law_id in law_name_to_id.items():
                    if key in law_name:
                        conflict_law_ids.append(law_id)
                        break
            
            # Check if the laws from conflict matrix are in applicable laws
            if len(conflict_law_ids) >= 2 and all(law_id in applicable_laws for law_id in conflict_law_ids):
                conflict_id = f"CONFLICT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
                
                return LawConflict(
                    conflict_id=conflict_id,
                    laws_involved=laws_in_conflict,
                    conflict_type=conflict_data.get("harmonization_strategy", "unknown"),
                    description=conflict_data.get("resolution", "Conflict detected"),
                    severity=0.7  # Default severity
                )
        
        # Check for requirement overlaps that may conflict
        requirements_by_law = {}
        laws = self.laws_registry.get("45_law_quantum_nexus", {}).get("laws", {})
        
        for law_id in applicable_laws:
            for law_key, law_data in laws.items():
                if law_data.get("id") == law_id:
                    enforcement = law_data.get("enforcement_action", {})
                    requirements_by_law[law_id] = set(enforcement.get("requirements", []))
        
        # Simple heuristic: if requirements sets are very different, potential conflict
        if len(requirements_by_law) >= 2:
            all_requirements = [reqs for reqs in requirements_by_law.values()]
            if all_requirements:
                # Check for conflicting requirements (e.g., consent vs. no consent)
                # This is a simplified check
                pass
        
        return None  # No conflicts detected
    
    def _determine_resolution_strategy(
        self, 
        conflict: LawConflict,
        operation_context: Dict[str, Any]
    ) -> ConflictResolutionStrategy:
        """
        Determine the appropriate conflict resolution strategy.
        
        Args:
            conflict: Detected conflict
            operation_context: Operation context
            
        Returns:
            ConflictResolutionStrategy to use
        """
        # Check if it's a public health emergency
        if operation_context.get("emergency_type") == "pandemic":
            return ConflictResolutionStrategy.PUBLIC_HEALTH_OVERRIDE
        
        # Check if it's a territorial conflict
        if "territorial" in conflict.conflict_type.lower():
            return ConflictResolutionStrategy.TERRITORIAL_PRIORITY
        
        # Check predefined strategy from conflict matrix
        for conflict_key, conflict_data in self.conflict_matrix.items():
            if all(law in conflict_key for law in conflict.laws_involved):
                strategy_str = conflict_data.get("harmonization_strategy", "")
                if strategy_str == "apply_strictest_requirements":
                    return ConflictResolutionStrategy.STRICTEST_REQUIREMENTS
                elif strategy_str == "territorial_priority":
                    return ConflictResolutionStrategy.TERRITORIAL_PRIORITY
                elif strategy_str == "public_health_emergency_override":
                    return ConflictResolutionStrategy.PUBLIC_HEALTH_OVERRIDE
        
        # Default to strictest requirements
        return ConflictResolutionStrategy.STRICTEST_REQUIREMENTS
    
    def _apply_resolution_strategy(
        self,
        conflict: LawConflict,
        strategy: ConflictResolutionStrategy,
        applicable_laws: List[str],
        operation_context: Dict[str, Any]
    ) -> HarmonizationResult:
        """
        Apply the resolution strategy to resolve the conflict.
        
        Args:
            conflict: The conflict to resolve
            strategy: Resolution strategy to apply
            applicable_laws: List of applicable law IDs
            operation_context: Operation context
            
        Returns:
            HarmonizationResult with resolved requirements
        """
        laws = self.laws_registry.get("45_law_quantum_nexus", {}).get("laws", {})
        
        # Collect requirements from all applicable laws
        all_requirements = {}
        for law_id in applicable_laws:
            for law_key, law_data in laws.items():
                if law_data.get("id") == law_id:
                    enforcement = law_data.get("enforcement_action", {})
                    all_requirements[law_id] = enforcement.get("requirements", [])
        
        resolved_requirements = []
        priority_order = []
        justification = ""
        
        if strategy == ConflictResolutionStrategy.STRICTEST_REQUIREMENTS:
            # Combine all requirements (union)
            resolved_requirements = list(set(
                req for reqs in all_requirements.values() for req in reqs
            ))
            priority_order = applicable_laws
            justification = (
                "Applied strictest requirements strategy: all requirements from "
                "all applicable laws must be satisfied"
            )
        
        elif strategy == ConflictResolutionStrategy.TERRITORIAL_PRIORITY:
            # Prioritize based on location
            location = operation_context.get("location", "")
            
            # Simple priority: local jurisdiction first
            priority_order = self._sort_by_territorial_priority(
                applicable_laws, location, laws
            )
            
            # Use requirements from highest priority law, add non-conflicting from others
            if priority_order:
                resolved_requirements = list(all_requirements.get(priority_order[0], []))
            
            justification = (
                f"Applied territorial priority strategy: {priority_order[0]} "
                "takes precedence based on operation location"
            )
        
        elif strategy == ConflictResolutionStrategy.PUBLIC_HEALTH_OVERRIDE:
            # Public health laws take precedence
            public_health_laws = ["LAW-002"]  # IHR 2005
            
            priority_order = [
                law for law in applicable_laws if law in public_health_laws
            ] + [
                law for law in applicable_laws if law not in public_health_laws
            ]
            
            # IHR requirements override privacy requirements in emergency
            resolved_requirements = []
            for law_id in priority_order:
                if law_id in all_requirements:
                    resolved_requirements.extend(all_requirements[law_id])
            
            resolved_requirements = list(set(resolved_requirements))
            
            justification = (
                "Applied public health emergency override: IHR 2005 data sharing "
                "requirements override privacy requirements under PHEIC declaration"
            )
        
        else:
            # Fallback to strictest requirements
            resolved_requirements = list(set(
                req for reqs in all_requirements.values() for req in reqs
            ))
            priority_order = applicable_laws
            justification = "Applied default strictest requirements strategy"
        
        return HarmonizationResult(
            conflict=conflict,
            resolution_strategy=strategy,
            resolved_requirements=resolved_requirements,
            priority_order=priority_order,
            justification=justification,
            confidence=0.85  # Base confidence
        )
    
    def _combine_non_conflicting_laws(
        self,
        applicable_laws: List[str],
        operation_context: Dict[str, Any]
    ) -> HarmonizationResult:
        """
        Combine requirements from non-conflicting laws.
        
        Args:
            applicable_laws: List of law IDs
            operation_context: Operation context
            
        Returns:
            HarmonizationResult with combined requirements
        """
        laws = self.laws_registry.get("45_law_quantum_nexus", {}).get("laws", {})
        
        all_requirements = set()
        for law_id in applicable_laws:
            for law_key, law_data in laws.items():
                if law_data.get("id") == law_id:
                    enforcement = law_data.get("enforcement_action", {})
                    all_requirements.update(enforcement.get("requirements", []))
        
        # Create a dummy conflict for non-conflicting case
        conflict = LawConflict(
            conflict_id="NO_CONFLICT",
            laws_involved=applicable_laws,
            conflict_type="none",
            description="No conflicts detected",
            severity=0.0
        )
        
        return HarmonizationResult(
            conflict=conflict,
            resolution_strategy=ConflictResolutionStrategy.STRICTEST_REQUIREMENTS,
            resolved_requirements=list(all_requirements),
            priority_order=applicable_laws,
            justification="No conflicts detected; combined all requirements",
            confidence=1.0
        )
    
    def _sort_by_territorial_priority(
        self,
        applicable_laws: List[str],
        location: str,
        laws: Dict[str, Any]
    ) -> List[str]:
        """
        Sort laws by territorial priority based on location.
        
        Args:
            applicable_laws: List of law IDs
            location: Operation location
            laws: Laws registry
            
        Returns:
            Sorted list of law IDs
        """
        priority_scores = {}
        
        for law_id in applicable_laws:
            for law_key, law_data in laws.items():
                if law_data.get("id") == law_id:
                    jurisdiction = law_data.get("jurisdiction", "").lower()
                    
                    # Score based on jurisdiction match
                    if location.lower() in jurisdiction:
                        priority_scores[law_id] = 3  # Exact match
                    elif "global" in jurisdiction:
                        priority_scores[law_id] = 1  # Global laws have lower priority
                    else:
                        priority_scores[law_id] = 2  # Regional laws
        
        # Sort by priority score (descending)
        return sorted(applicable_laws, key=lambda x: priority_scores.get(x, 0), reverse=True)
    
    def retroactive_alignment_engine(
        self,
        historical_data: List[Dict[str, Any]],
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> RetroactiveAuditResult:
        """
        Scan historical data for compliance gaps and generate remediation plan.
        
        This is the IP-09 integration that analyzes past operations for regulatory violations.
        
        Args:
            historical_data: List of historical operations to audit
            time_range: Optional time range to limit audit (start, end)
            
        Returns:
            RetroactiveAuditResult with violations found and remediation plan
        """
        logger.info(f"Starting retroactive compliance audit on {len(historical_data)} records")
        
        audit_id = f"AUDIT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        
        if time_range is None:
            # Default to last 90 days
            from datetime import timedelta
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=90)
            time_range = (start_time, end_time)
        
        violations_found = 0
        violations_by_law = {}
        remediation_required = []
        
        # Filter data by time range
        filtered_data = [
            record for record in historical_data
            if self._is_in_time_range(record, time_range)
        ]
        
        records_scanned = len(filtered_data)
        
        # Audit each record
        laws = self.laws_registry.get("45_law_quantum_nexus", {}).get("laws", {})
        
        for record in filtered_data:
            record_violations = self._audit_record(record, laws)
            
            if record_violations:
                violations_found += len(record_violations)
                
                for violation in record_violations:
                    law_id = violation["law_id"]
                    violations_by_law[law_id] = violations_by_law.get(law_id, 0) + 1
                    
                    # Add to remediation plan
                    remediation_required.append({
                        "record_id": record.get("id", "unknown"),
                        "timestamp": record.get("timestamp", "unknown"),
                        "violation": violation,
                        "remediation_actions": self._generate_remediation_actions(violation)
                    })
        
        result = RetroactiveAuditResult(
            audit_id=audit_id,
            time_range=time_range,
            records_scanned=records_scanned,
            violations_found=violations_found,
            violations_by_law=violations_by_law,
            remediation_required=remediation_required
        )
        
        self.audit_history.append(result)
        
        logger.info(
            f"Retroactive audit complete: {violations_found} violations found "
            f"in {records_scanned} records"
        )
        
        return result
    
    def _is_in_time_range(
        self,
        record: Dict[str, Any],
        time_range: Tuple[datetime, datetime]
    ) -> bool:
        """Check if record is within time range."""
        record_time_str = record.get("timestamp")
        if not record_time_str:
            return True  # Include records without timestamp
        
        try:
            if isinstance(record_time_str, datetime):
                record_time = record_time_str
            else:
                record_time = datetime.fromisoformat(record_time_str.replace('Z', '+00:00'))
            
            return time_range[0] <= record_time <= time_range[1]
        except (ValueError, AttributeError):
            return True  # Include if can't parse
    
    def _audit_record(
        self,
        record: Dict[str, Any],
        laws: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Audit a single record for compliance violations.
        
        Args:
            record: Historical record to audit
            laws: Laws registry
            
        Returns:
            List of violations found
        """
        violations = []
        
        # Check each law
        for law_key, law_data in laws.items():
            law_id = law_data.get("id")
            enforcement = law_data.get("enforcement_action", {})
            requirements = enforcement.get("requirements", [])
            
            # Check if record has evidence of meeting requirements
            compliance_evidence = record.get("compliance_evidence", {})
            
            missing_requirements = [
                req for req in requirements
                if req.lower().replace(" ", "_").replace("-", "_") not in compliance_evidence
            ]
            
            if missing_requirements and self._was_law_applicable(record, law_data):
                violations.append({
                    "law_id": law_id,
                    "law_name": law_data.get("name", "Unknown"),
                    "missing_requirements": missing_requirements,
                    "severity": "high" if len(missing_requirements) > 3 else "medium"
                })
        
        return violations
    
    def _was_law_applicable(
        self,
        record: Dict[str, Any],
        law_data: Dict[str, Any]
    ) -> bool:
        """
        Determine if a law was applicable to a historical record.
        
        Args:
            record: Historical record
            law_data: Law details
            
        Returns:
            True if law was applicable
        """
        # Simple heuristic based on sector and location
        trigger = law_data.get("trigger_condition", {})
        params = trigger.get("parameters", {})
        
        if "sector" in params:
            record_sector = record.get("sector", "")
            if record_sector:
                sectors = params["sector"]
                if isinstance(sectors, list):
                    if record_sector not in sectors:
                        return False
                elif record_sector != sectors:
                    return False
        
        return True
    
    def _generate_remediation_actions(
        self,
        violation: Dict[str, Any]
    ) -> List[str]:
        """
        Generate remediation actions for a violation.
        
        Args:
            violation: Violation details
            
        Returns:
            List of remediation actions
        """
        actions = [
            "Review historical record for compliance gaps",
            "Collect missing compliance evidence",
            "Update record with required documentation"
        ]
        
        if violation.get("severity") == "high":
            actions.extend([
                "Notify compliance officer",
                "Conduct impact assessment",
                "Implement corrective measures"
            ])
        
        return actions
    
    def get_harmonization_stats(self) -> Dict[str, Any]:
        """
        Get statistics on harmonization operations.
        
        Returns:
            Dictionary with harmonization statistics
        """
        if not self.harmonization_history:
            return {
                "total_harmonizations": 0,
                "conflicts_resolved": 0,
                "average_confidence": 0.0
            }
        
        conflicts_resolved = sum(
            1 for h in self.harmonization_history
            if h.conflict.conflict_id != "NO_CONFLICT"
        )
        
        avg_confidence = sum(h.confidence for h in self.harmonization_history) / len(self.harmonization_history)
        
        return {
            "total_harmonizations": len(self.harmonization_history),
            "conflicts_resolved": conflicts_resolved,
            "average_confidence": avg_confidence,
            "strategies_used": self._count_strategies_used()
        }
    
    def _count_strategies_used(self) -> Dict[str, int]:
        """Count usage of each resolution strategy."""
        strategy_counts = {}
        
        for h in self.harmonization_history:
            strategy = h.resolution_strategy.value
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return strategy_counts
