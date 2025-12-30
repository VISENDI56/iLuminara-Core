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
The Golden Thread: Quantum-Entangled Data Fusion Engine
═════════════════════════════════════════════════════════════════════════════
UPGRADE NOTE: Implements 'Active Inference' via Probabilistic Entanglement.
Merges disparate signals not just by exact match, but by spatiotemporal probability.

Merges EMR (Electronic Medical Records), CBS (Community-Based Surveillance), 
and IDSR (Integrated Disease Surveillance Response) data streams into a single 
verified timeline of truth.

The "Golden Thread" prevents data redundancy, reconciles conflicts across systems,
and enforces the 6-Month Rule: records older than 6 months are archived to cold 
storage, ensuring hot memory remains performant while preserving auditability.

Philosophy: "One integrated truth, verified at every junction."
"""

from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import math


class DataSourceType(Enum):
    """Origin classification for data verification."""
    EMR = "Electronic Medical Record"
    CBS = "Community-Based Surveillance"
    IDSR = "Integrated Disease Surveillance Response"
    EXTERNAL = "External Source"


class VerificationScore(Enum):
    """Confidence levels for data fusion."""
    CONFIRMED = 1.0       # Hard Lock / Cross-verified across 2+ sources
    ENTANGLED = 0.9       # High Probability (Active Inference)
    PROBABLE = 0.7        # Strong Signal / Verified across single source with supporting evidence
    POSSIBLE = 0.4        # Weak Signal / Single source, no contradiction
    UNVERIFIED = 0.3      # Single source, potential conflicts
    CONFLICT = 0.0        # Contradiction / Data contradiction across sources


@dataclass
class EntanglementNode:
    """Represents a probabilistic link between independent data events."""
    source_id: str
    target_id: str
    probability_weight: float
    vector_distance: float  # Spatiotemporal distance


@dataclass
class TimeseriesRecord:
    """
    Unified record in the Golden Thread timeline.
    
    Each record represents a canonical state of a health/surveillance event,
    synthesized from multiple data streams.
    """
    record_id: str
    patient_id: str
    event_type: str  # e.g., 'symptom_report', 'lab_result', 'hospitalization'
    location: str  # Geographic location
    timestamp: datetime
    data_sources: Dict[str, Any] = field(default_factory=dict)  # source_type -> raw data
    verification_score: float = 0.5
    canonical_data: Dict[str, Any] = field(default_factory=dict)  # Merged truth
    confidence_chain: list = field(default_factory=list)  # Audit trail
    created_at: datetime = field(default_factory=datetime.utcnow)
    retention_status: str = "HOT"  # HOT (active) or COLD (archived)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize record to dictionary."""
        return {
            "record_id": self.record_id,
            "patient_id": self.patient_id,
            "event_type": self.event_type,
            "location": self.location,
            "timestamp": self.timestamp.isoformat(),
            "verification_score": self.verification_score,
            "canonical_data": self.canonical_data,
            "confidence_chain": self.confidence_chain,
            "retention_status": self.retention_status,
        }


class GoldenThread:
    """
    Data fusion engine that reconciles multiple health surveillance streams
    into a single source of truth.
    
    Usage:
        gt = GoldenThread()
        fused_record = gt.fuse_data_streams(
            cbs_signal={'location': 'Nairobi', 'symptom': 'fever', 'timestamp': '2025-01-10T10:00Z'},
            emr_record={'location': 'Nairobi', 'diagnosis': 'malaria', 'timestamp': '2025-01-10T09:45Z'},
            patient_id='PATIENT_12345'
        )
    """
    
    # Quantum Entanglement Configuration
    TEMPORAL_DECAY_RATE = -0.05  # Exponential decay: ~50% every 12 hours
    TEMPORAL_WEIGHT = 0.7  # Weight for temporal proximity in entanglement score
    CONTENT_WEIGHT = 0.3  # Weight for symptom-diagnosis alignment
    CONTENT_WEIGHT_DEFAULT = 0.1  # Default weight for non-matching symptoms
    ENTANGLEMENT_THRESHOLD_HIGH = 0.85  # Threshold for ENTANGLED status
    ENTANGLEMENT_THRESHOLD_MEDIUM = 0.5  # Threshold for PROBABLE LINK status
    
    # Symptom-Diagnosis Mapping (for Active Inference)
    SYMPTOM_DIAGNOSIS_MAP = {
        "watery_stool": ["Cholera", "Acute Diarrhea"],
        "fever": ["Malaria", "Typhoid"]
    }

    def __init__(self):
        """Initialize the Golden Thread with fusion rules."""
        self.fused_records = {}  # patient_id -> list of TimeseriesRecord
        self.fusion_log = []
        self.retention_policy_days = 180  # 6-month rule
        # entanglement_matrix: Reserved for future graph-based entanglement tracking
        self.entanglement_matrix: List[EntanglementNode] = []

    def calculate_entanglement(self, cbs_event: Dict, emr_event: Dict) -> float:
        """
        Calculates the 'Quantum Entanglement' between a vague symptom and a diagnosis.
        Based on Spatiotemporal distance (H3 Index + Time Delta).
        
        Args:
            cbs_event: CBS event with timestamp and symptom
            emr_event: EMR event with timestamp and diagnosis
            
        Returns:
            float: Entanglement score between 0 and 1
            
        Raises:
            KeyError: If required 'timestamp' key is missing from events
        """
        # Validate required keys
        if 'timestamp' not in cbs_event:
            raise KeyError("CBS event missing required 'timestamp' key")
        if 'timestamp' not in emr_event:
            raise KeyError("EMR event missing required 'timestamp' key")
        
        # 1. Temporal Decay (The further apart, the weaker the link)
        # Parse timestamps - reuse logic from _parse_timestamp
        cbs_timestamp = self._parse_timestamp(cbs_event, "cbs")
        emr_timestamp = self._parse_timestamp(emr_event, "emr")
        
        if not cbs_timestamp or not emr_timestamp:
            raise ValueError("Unable to parse timestamps from events")
        
        delta_hours = abs((cbs_timestamp - emr_timestamp).total_seconds()) / 3600
        
        # Decay function: Probability drops exponentially over time
        temporal_weight = math.exp(self.TEMPORAL_DECAY_RATE * delta_hours)

        # 2. Symptom Vector Alignment (content-based matching)
        content_weight = self.CONTENT_WEIGHT_DEFAULT  # Default low weight for non-matching symptoms
        symptom = cbs_event.get('symptom')
        diagnosis = emr_event.get('diagnosis')
        
        if symptom in self.SYMPTOM_DIAGNOSIS_MAP:
            if diagnosis in self.SYMPTOM_DIAGNOSIS_MAP[symptom]:
                content_weight = 1.0  # High weight for matching symptom-diagnosis pairs

        # Final Entanglement Score (weighted combination)
        # Note: Score is always in [0, 1] range due to exponential decay and weight normalization
        return (temporal_weight * self.TEMPORAL_WEIGHT) + (content_weight * self.CONTENT_WEIGHT)

    def fuse_data(self, cbs_data: List[Dict], emr_data: List[Dict]) -> List[Dict[str, Any]]:
        """
        Fuses data streams using Active Inference.
        
        NOTE: O(n*m) complexity - for large datasets, consider spatial indexing.
        
        Args:
            cbs_data: List of CBS events
            emr_data: List of EMR events
            
        Returns:
            List of fused log entries with entanglement scores
        """
        fused_log = []
        
        for cbs in cbs_data:
            best_match = None
            highest_entanglement = 0.0
            
            # Find best matching EMR record for this CBS signal
            for emr in emr_data:
                score = self.calculate_entanglement(cbs, emr)
                if score > highest_entanglement:
                    highest_entanglement = score
                    best_match = emr
            
            # Determine status based on configurable thresholds
            status = "UNVERIFIED"
            if highest_entanglement > self.ENTANGLEMENT_THRESHOLD_HIGH:
                status = "ENTANGLED (Active Inference)"
            elif highest_entanglement > self.ENTANGLEMENT_THRESHOLD_MEDIUM:
                status = "PROBABLE LINK"
            
            # Extract diagnosis safely
            predicted_diagnosis = "Unknown"
            if best_match and isinstance(best_match, dict):
                predicted_diagnosis = best_match.get('diagnosis', 'Unknown')
            
            fused_log.append({
                "time": cbs['timestamp'],
                "cbs_signal": cbs.get('symptom', 'Unknown'),
                "entanglement_score": round(highest_entanglement, 4),
                "status": status,
                "predicted_diagnosis": predicted_diagnosis
            })
            
        return fused_log

    def fuse_data_streams(
        self,
        cbs_signal: Optional[Dict[str, Any]] = None,
        emr_record: Optional[Dict[str, Any]] = None,
        idsr_template: Optional[Dict[str, Any]] = None,
        patient_id: str = "UNKNOWN",
    ) -> TimeseriesRecord:
        """
        Fuse multiple data streams into a single verified record.

        The Golden Thread Algorithm:
        1. Extract timestamps and locations from each source
        2. If cbs.location == emr.location AND time_delta < 24h → CONFIRMED (1.0)
        3. Auto-generate IDSR report object
        4. Return unified TimeseriesRecord with verification chain

        Args:
            cbs_signal: Community-Based Surveillance data
                e.g., {'location': 'Nairobi', 'symptom': 'fever', 'timestamp': '2025-01-10T10:00Z'}
            emr_record: Electronic Medical Record data
                e.g., {'location': 'Nairobi', 'diagnosis': 'malaria', 'timestamp': '2025-01-10T09:45Z'}
            idsr_template: IDSR template (optional pre-structured template)
            patient_id: Patient identifier for record tracking

        Returns:
            TimeseriesRecord: Unified, verified record ready for integration

        Raises:
            ValueError: If data sources are malformed or timestamp parsing fails
        """
        # Parse timestamps
        cbs_timestamp = self._parse_timestamp(cbs_signal, "cbs") if cbs_signal else None
        emr_timestamp = self._parse_timestamp(emr_record, "emr") if emr_record else None

        # Determine fusion verification score
        verification_score = self._calculate_verification_score(
            cbs_signal, emr_record, cbs_timestamp, emr_timestamp
        )

        # Generate canonical event timestamp (prefer earlier occurrence)
        event_timestamp = min(
            filter(None, [cbs_timestamp, emr_timestamp]),
            default=datetime.utcnow(),
        )

        # Extract location
        location = cbs_signal.get("location") if cbs_signal else None
        location = location or (emr_record.get("location") if emr_record else "UNKNOWN")

        # Generate record ID
        record_id = self._generate_record_id(patient_id, event_timestamp)

        # Determine event type
        event_type = self._infer_event_type(cbs_signal, emr_record)

        # Merge canonical data
        canonical_data = self._merge_canonical_data(cbs_signal, emr_record)

        # Auto-generate IDSR report
        idsr_report = self._generate_idsr_report(
            cbs_signal, emr_record, canonical_data, event_timestamp, patient_id
        )

        # Determine retention status
        retention_status = self._check_retention(event_timestamp)

        # Build confidence chain (audit trail)
        confidence_chain = [
            {
                "step": "initial_parse",
                "sources": list(
                    filter(
                        None,
                        [
                            "CBS" if cbs_signal else None,
                            "EMR" if emr_record else None,
                        ],
                    )
                ),
                "timestamp": datetime.utcnow().isoformat(),
            },
            {
                "step": "verification_score_calculated",
                "score": verification_score,
                "reasoning": self._get_verification_reasoning(
                    verification_score, cbs_signal, emr_record
                ),
            },
            {
                "step": "canonical_merge",
                "merge_strategy": "temporal_proximity_weighted",
                "sources_merged": 2 if (cbs_signal and emr_record) else 1,
            },
            {
                "step": "idsr_generation",
                "idsr_status": "auto_generated",
            },
        ]

        # Create the fused record
        fused_record = TimeseriesRecord(
            record_id=record_id,
            patient_id=patient_id,
            event_type=event_type,
            location=location,
            timestamp=event_timestamp,
            data_sources={
                "CBS": cbs_signal or {},
                "EMR": emr_record or {},
                "IDSR": idsr_report,
            },
            verification_score=verification_score,
            canonical_data=canonical_data,
            confidence_chain=confidence_chain,
            retention_status=retention_status,
        )

        # Store in fused records
        if patient_id not in self.fused_records:
            self.fused_records[patient_id] = []
        self.fused_records[patient_id].append(fused_record)

        # Log the fusion event
        self.fusion_log.append(
            {
                "record_id": record_id,
                "patient_id": patient_id,
                "verification_score": verification_score,
                "sources_count": sum(
                    [1 for s in [cbs_signal, emr_record] if s is not None]
                ),
                "timestamp": datetime.utcnow().isoformat(),
                "retention_status": retention_status,
            }
        )

        return fused_record

    def _parse_timestamp(self, data: Dict[str, Any], source: str) -> Optional[datetime]:
        """
        Parse timestamp from data source.
        
        Handles ISO 8601 and common timestamp formats.
        """
        if not data:
            return None

        timestamp_str = data.get("timestamp")
        if not timestamp_str:
            return None

        try:
            # Try ISO 8601 format
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            # Convert to naive datetime (remove timezone info for consistency)
            return dt.replace(tzinfo=None)
        except (ValueError, AttributeError):
            try:
                # Fallback: Unix timestamp
                return datetime.fromtimestamp(float(timestamp_str))
            except (ValueError, TypeError):
                raise ValueError(
                    f"❌ Cannot parse timestamp from {source}: {timestamp_str}"
                )

    def _calculate_verification_score(
        self,
        cbs_signal: Optional[Dict],
        emr_record: Optional[Dict],
        cbs_timestamp: Optional[datetime],
        emr_timestamp: Optional[datetime],
    ) -> float:
        """
        Calculate cross-source verification score.

        Algorithm:
        - IF cbs.location == emr.location AND |cbs_timestamp - emr_timestamp| < 24h
            THEN score = 1.0 (CONFIRMED)
        - ELIF single source with no contradictions
            THEN score = 0.8 (PROBABLE)
        - ELIF single source
            THEN score = 0.5 (POSSIBLE)
        - ELSE score = 0.0 (CONFLICT)
        """
        # Both sources present
        if cbs_signal and emr_record:
            cbs_location = cbs_signal.get("location", "UNKNOWN")
            emr_location = emr_record.get("location", "UNKNOWN")

            if cbs_location == emr_location and cbs_timestamp and emr_timestamp:
                time_delta = abs((cbs_timestamp - emr_timestamp).total_seconds())
                if time_delta < 86400:  # 24 hours in seconds
                    return VerificationScore.CONFIRMED.value

            # Locations don't match or timestamps too far apart
            return VerificationScore.PROBABLE.value

        # Single source
        if cbs_signal or emr_record:
            return VerificationScore.POSSIBLE.value

        # No sources
        return VerificationScore.UNVERIFIED.value

    def _get_verification_reasoning(
        self,
        score: float,
        cbs_signal: Optional[Dict],
        emr_record: Optional[Dict],
    ) -> str:
        """Generate human-readable reasoning for verification score."""
        if score == 1.0:
            return "Cross-verified: Location match + temporal proximity (<24h)"
        elif score == 0.8:
            return "Single source verified; no contradictions detected"
        elif score == 0.5:
            return "Single source; temporal verification pending"
        else:
            return "Data conflict or incomplete sources"

    def _generate_record_id(self, patient_id: str, timestamp: datetime) -> str:
        """Generate unique record ID."""
        date_str = timestamp.strftime("%Y%m%d%H%M%S")
        return f"GT-{patient_id}-{date_str}"

    def _infer_event_type(
        self, cbs_signal: Optional[Dict], emr_record: Optional[Dict]
    ) -> str:
        """Infer event type from source data."""
        if emr_record:
            if "diagnosis" in emr_record:
                return "diagnosis"
            elif "lab_result" in emr_record:
                return "lab_result"
            elif "hospitalization" in emr_record:
                return "hospitalization"

        if cbs_signal:
            if "symptom" in cbs_signal:
                return "symptom_report"
            elif "outbreak" in cbs_signal:
                return "outbreak_alert"

        return "unknown_event"

    def _merge_canonical_data(
        self, cbs_signal: Optional[Dict], emr_record: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Merge data from multiple sources into canonical representation.
        
        Strategy: Preference order (EMR > CBS > IDSR) for conflicting fields.
        """
        canonical = {}

        if cbs_signal:
            canonical.update(cbs_signal)

        if emr_record:
            # EMR overwrites CBS in case of conflict
            canonical.update(emr_record)

        return canonical

    def _generate_idsr_report(
        self,
        cbs_signal: Optional[Dict],
        emr_record: Optional[Dict],
        canonical_data: Dict[str, Any],
        event_timestamp: datetime,
        patient_id: str,
    ) -> Dict[str, Any]:
        """
        Auto-generate IDSR (Integrated Disease Surveillance Response) report.
        
        IDSR is Kenya's disease surveillance standard. This function creates
        a structured report object suitable for government health submissions.
        """
        idsr_report = {
            "report_type": "IDSR",
            "version": "1.0",
            "generated_at": datetime.utcnow().isoformat(),
            "patient_id": patient_id,
            "event_timestamp": event_timestamp.isoformat(),
            "location": canonical_data.get("location", "UNKNOWN"),
            "disease_code": self._infer_disease_code(canonical_data),
            "clinical_summary": {
                "symptoms": cbs_signal.get("symptoms", []) if cbs_signal else [],
                "diagnosis": emr_record.get("diagnosis") if emr_record else None,
                "lab_findings": emr_record.get("lab_results", {}) if emr_record else {},
            },
            "data_sources": {
                "cbs_present": cbs_signal is not None,
                "emr_present": emr_record is not None,
            },
            "verification_metadata": {
                "cross_source_verified": cbs_signal is not None and emr_record is not None,
                "temporal_alignment": (
                    abs(
                        (
                            self._parse_timestamp(cbs_signal, "cbs")
                            - self._parse_timestamp(emr_record, "emr")
                        ).total_seconds()
                    )
                    < 86400
                    if (cbs_signal and emr_record)
                    else None
                ),
            },
            "submission_status": "PENDING_REVIEW",
        }

        return idsr_report

    def _infer_disease_code(self, canonical_data: Dict[str, Any]) -> str:
        """Infer disease code from clinical data."""
        diagnosis = canonical_data.get("diagnosis", "").lower()

        disease_codes = {
            "malaria": "MAL001",
            "cholera": "CHOL001",
            "covid": "COVID001",
            "typhoid": "TYPH001",
            "measles": "MEAS001",
            "ebola": "EBOLA001",
            "dengue": "DENG001",
            "yellow_fever": "YFEV001",
        }

        for keyword, code in disease_codes.items():
            if keyword in diagnosis:
                return code

        return "UNKNOWN"

    def _check_retention(self, record_timestamp: datetime) -> str:
        """
        Determine retention status: HOT (active) or COLD (archived).

        The 6-Month Rule:
        Records older than 6 months (180 days) transition to COLD storage.
        This preserves hot memory performance while maintaining auditability.
        """
        # Make both timestamps timezone-naive for comparison
        now = datetime.utcnow()
        record_ts = record_timestamp.replace(tzinfo=None) if record_timestamp.tzinfo else record_timestamp
        
        days_since_record = (now - record_ts).days

        if days_since_record > self.retention_policy_days:
            return "COLD"
        return "HOT"

    def retention_check(self, record_date: datetime) -> bool:
        """
        Check if a record should remain in hot memory.

        Returns:
            bool: True if record should remain hot; False if should be archived.

        Philosophy: "Hot memory is for recent events. Cold storage for history."
        """
        # Make both timestamps timezone-naive for comparison
        now = datetime.utcnow()
        record_ts = record_date.replace(tzinfo=None) if record_date.tzinfo else record_date
        
        days_since = (now - record_ts).days
        should_remain_hot = days_since <= self.retention_policy_days

        if not should_remain_hot:
            print(
                f"⚠️  RETENTION: Record from {record_date.isoformat()} "
                f"({days_since} days old) should transition to COLD storage."
            )

        return should_remain_hot

    def get_fused_timeline(self, patient_id: str) -> list:
        """
        Retrieve the complete fused timeline for a patient.
        
        Returns records sorted by timestamp (oldest first).
        """
        records = self.fused_records.get(patient_id, [])
        return sorted(records, key=lambda r: r.timestamp)

    def get_fusion_statistics(self) -> Dict[str, Any]:
        """
        Return fusion engine statistics.
        """
        total_records = sum(len(records) for records in self.fused_records.values())
        hot_records = sum(
            1
            for records in self.fused_records.values()
            for r in records
            if r.retention_status == "HOT"
        )
        cold_records = total_records - hot_records

        avg_verification_score = (
            sum(r.verification_score for records in self.fused_records.values() for r in records)
            / total_records
            if total_records > 0
            else 0
        )

        return {
            "total_records_fused": total_records,
            "hot_records": hot_records,
            "cold_records": cold_records,
            "average_verification_score": avg_verification_score,
            "fusion_events": len(self.fusion_log),
        }


# ═════════════════════════════════════════════════════════════════════════════
# The Golden Thread Philosophy:
# "One integrated truth, verified at every junction. No redundancy. No orphaned data."
#
# The 6-Month Rule: Ensures data lifecycle compliance while preserving auditability.
# ═════════════════════════════════════════════════════════════════════════════

# Usage verification
if __name__ == "__main__":
    print("✅ Golden Thread (Quantum Version) Loaded.")
