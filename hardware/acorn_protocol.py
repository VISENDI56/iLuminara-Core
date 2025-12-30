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
Acorn Protocol (IP-03): Somatic Security
═════════════════════════════════════════════════════════════════════════════

Philosophy: "Your body is the key."

The Acorn Protocol uses biometric and behavioral signals as a cryptographic
authentication factor, preventing "Panic Access" during crisis scenarios.

Traditional authentication (passwords, tokens) can be compromised under duress.
Acorn Protocol adds a somatic layer that detects:
1. Posture (slouched vs. upright)
2. Location (GPS + venue context)
3. Stillness (micro-movements, tremor detection)

During high-stress scenarios (e.g., disease outbreak, conflict zone), operators
may be coerced or operating under extreme duress. Acorn Protocol can detect
anomalous somatic signatures and:
- Require additional verification steps
- Limit access to sensitive operations
- Alert security monitoring systems
- Create audit trail of duress indicators

Technical Implementation:
- Integrates with device sensors (accelerometer, gyroscope, GPS)
- Establishes baseline somatic profile for each operator
- Calculates deviation score in real-time
- Triggers adaptive authentication based on somatic anomalies
"""

from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import math


class PostureState(Enum):
    """Operator posture classification."""
    UPRIGHT = "UPRIGHT"  # Normal seated/standing
    SLOUCHED = "SLOUCHED"  # Fatigue or stress
    PRONE = "PRONE"  # Lying down (unusual for work)
    UNKNOWN = "UNKNOWN"


class StillnessLevel(Enum):
    """Operator movement classification."""
    STILL = "STILL"  # Minimal movement
    NORMAL = "NORMAL"  # Typical work movements
    RESTLESS = "RESTLESS"  # Fidgeting, anxiety
    TREMOR = "TREMOR"  # Significant tremor detected


class DuressLevel(Enum):
    """Duress assessment based on somatic signals."""
    NORMAL = "NORMAL"  # No indicators of duress
    ELEVATED = "ELEVATED"  # Minor deviations from baseline
    SUSPECTED = "SUSPECTED"  # Multiple anomaly indicators
    CONFIRMED = "CONFIRMED"  # High confidence duress detection


@dataclass
class SomaticSignature:
    """Snapshot of operator biometric/behavioral state."""
    timestamp: datetime
    
    # Posture metrics (from accelerometer/gyroscope)
    tilt_x: float = 0.0  # Degrees from vertical, X-axis
    tilt_y: float = 0.0  # Degrees from vertical, Y-axis
    posture_state: PostureState = PostureState.UNKNOWN
    
    # Location metrics (from GPS)
    latitude: float = 0.0
    longitude: float = 0.0
    location_confidence: float = 0.0  # 0.0 - 1.0
    venue_context: str = "UNKNOWN"  # e.g., "OFFICE", "FIELD", "HOME"
    
    # Stillness metrics (from accelerometer)
    movement_magnitude: float = 0.0  # m/s² RMS
    stillness_level: StillnessLevel = StillnessLevel.NORMAL
    
    # Composite score
    anomaly_score: float = 0.0  # 0.0 = normal, 1.0 = high anomaly
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "tilt_x": self.tilt_x,
            "tilt_y": self.tilt_y,
            "posture_state": self.posture_state.value,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_confidence": self.location_confidence,
            "venue_context": self.venue_context,
            "movement_magnitude": self.movement_magnitude,
            "stillness_level": self.stillness_level.value,
            "anomaly_score": self.anomaly_score,
        }


@dataclass
class AuthenticationDecision:
    """Acorn Protocol authentication result."""
    timestamp: datetime
    operator_id: str
    authenticated: bool
    duress_level: DuressLevel
    somatic_anomaly_score: float
    required_additional_verification: bool
    reasoning: str
    access_restrictions: list
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "operator_id": self.operator_id,
            "authenticated": self.authenticated,
            "duress_level": self.duress_level.value,
            "somatic_anomaly_score": self.somatic_anomaly_score,
            "required_additional_verification": self.required_additional_verification,
            "reasoning": self.reasoning,
            "access_restrictions": self.access_restrictions,
        }


class AcornProtocol:
    """
    Somatic security layer using Posture + Location + Stillness as authentication.
    
    Prevents "Panic Access" by detecting duress through biometric anomalies.
    
    Usage:
        acorn = AcornProtocol(operator_id="OPERATOR_001")
        
        # Establish baseline somatic profile
        acorn.establish_baseline(
            posture_samples=[...],
            location_samples=[...],
            movement_samples=[...]
        )
        
        # During authentication: capture somatic signature
        signature = acorn.capture_somatic_signature(
            tilt_x=5.2,
            tilt_y=-3.1,
            latitude=1.2921,
            longitude=36.8219,
            movement_magnitude=0.12
        )
        
        # Authenticate with somatic layer
        decision = acorn.authenticate(signature)
        
        if decision.duress_level in [DuressLevel.SUSPECTED, DuressLevel.CONFIRMED]:
            # Trigger security protocols
            alert_security_team(decision)
    """
    
    def __init__(self, operator_id: str):
        """
        Initialize Acorn Protocol for an operator.
        
        Args:
            operator_id: Unique identifier for the operator
        """
        self.operator_id = operator_id
        self.baseline_profile: Optional[Dict[str, Any]] = None
        self.signature_history: list = []
        self.authentication_log: list = []
        
    def establish_baseline(
        self,
        posture_samples: list,
        location_samples: list,
        movement_samples: list
    ):
        """
        Establish baseline somatic profile for the operator.
        
        This should be done during normal, non-stressed work conditions.
        Typically requires 5-10 days of data collection.
        
        Args:
            posture_samples: List of (tilt_x, tilt_y) tuples
            location_samples: List of (lat, lon, venue) tuples
            movement_samples: List of movement_magnitude values
        """
        # Calculate posture baseline
        avg_tilt_x = sum(p[0] for p in posture_samples) / len(posture_samples)
        avg_tilt_y = sum(p[1] for p in posture_samples) / len(posture_samples)
        
        # Calculate location baseline (primary work location)
        primary_location = self._calculate_centroid(location_samples)
        
        # Calculate movement baseline
        avg_movement = sum(movement_samples) / len(movement_samples)
        
        self.baseline_profile = {
            "established_at": datetime.utcnow().isoformat(),
            "posture": {
                "avg_tilt_x": avg_tilt_x,
                "avg_tilt_y": avg_tilt_y,
                "std_tilt_x": self._calculate_std([p[0] for p in posture_samples]),
                "std_tilt_y": self._calculate_std([p[1] for p in posture_samples]),
            },
            "location": {
                "primary_latitude": primary_location[0],
                "primary_longitude": primary_location[1],
                "radius_meters": 500.0,  # Typical work area radius
            },
            "movement": {
                "avg_magnitude": avg_movement,
                "std_magnitude": self._calculate_std(movement_samples),
            },
        }
    
    def capture_somatic_signature(
        self,
        tilt_x: float,
        tilt_y: float,
        latitude: float,
        longitude: float,
        movement_magnitude: float,
        venue_context: str = "UNKNOWN"
    ) -> SomaticSignature:
        """
        Capture current somatic signature from device sensors.
        
        Args:
            tilt_x: Device tilt in degrees (X-axis)
            tilt_y: Device tilt in degrees (Y-axis)
            latitude: GPS latitude
            longitude: GPS longitude
            movement_magnitude: Accelerometer RMS (m/s²)
            venue_context: Venue classification
            
        Returns:
            SomaticSignature: Current biometric/behavioral snapshot
        """
        # Classify posture
        posture_state = self._classify_posture(tilt_x, tilt_y)
        
        # Classify stillness
        stillness_level = self._classify_stillness(movement_magnitude)
        
        # Calculate anomaly score
        anomaly_score = self._calculate_anomaly_score(
            tilt_x, tilt_y, latitude, longitude, movement_magnitude
        )
        
        signature = SomaticSignature(
            timestamp=datetime.utcnow(),
            tilt_x=tilt_x,
            tilt_y=tilt_y,
            posture_state=posture_state,
            latitude=latitude,
            longitude=longitude,
            location_confidence=0.8,  # Would come from GPS sensor
            venue_context=venue_context,
            movement_magnitude=movement_magnitude,
            stillness_level=stillness_level,
            anomaly_score=anomaly_score,
        )
        
        self.signature_history.append(signature)
        
        # Prune old signatures (keep last 100)
        if len(self.signature_history) > 100:
            self.signature_history = self.signature_history[-100:]
        
        return signature
    
    def authenticate(
        self,
        signature: SomaticSignature,
        traditional_auth_passed: bool = True
    ) -> AuthenticationDecision:
        """
        Authenticate operator with somatic security layer.
        
        Args:
            signature: Current somatic signature
            traditional_auth_passed: Whether password/token auth succeeded
            
        Returns:
            AuthenticationDecision: Authentication result with duress assessment
        """
        if not self.baseline_profile:
            # No baseline - cannot assess duress, allow with warning
            decision = AuthenticationDecision(
                timestamp=datetime.utcnow(),
                operator_id=self.operator_id,
                authenticated=traditional_auth_passed,
                duress_level=DuressLevel.NORMAL,
                somatic_anomaly_score=0.0,
                required_additional_verification=False,
                reasoning="No baseline profile established; somatic assessment skipped",
                access_restrictions=[],
            )
            
            self.authentication_log.append(decision)
            return decision
        
        # Assess duress level
        duress_level = self._assess_duress(signature)
        
        # Determine authentication decision
        authenticated = traditional_auth_passed
        required_additional_verification = False
        access_restrictions = []
        
        if duress_level == DuressLevel.SUSPECTED:
            required_additional_verification = True
            access_restrictions = ["SENSITIVE_DATA_OPERATIONS", "BULK_EXPORTS"]
            reasoning = (
                f"Somatic anomaly detected (score: {signature.anomaly_score:.2f}). "
                "Additional verification required for sensitive operations."
            )
        
        elif duress_level == DuressLevel.CONFIRMED:
            access_restrictions = [
                "SENSITIVE_DATA_OPERATIONS",
                "BULK_EXPORTS",
                "ADMINISTRATIVE_FUNCTIONS",
                "EXTERNAL_COMMUNICATIONS",
            ]
            reasoning = (
                f"High somatic anomaly detected (score: {signature.anomaly_score:.2f}). "
                "Possible duress situation. Access restricted to read-only operations."
            )
        
        else:
            reasoning = "Normal somatic profile; no duress indicators detected"
        
        decision = AuthenticationDecision(
            timestamp=datetime.utcnow(),
            operator_id=self.operator_id,
            authenticated=authenticated,
            duress_level=duress_level,
            somatic_anomaly_score=signature.anomaly_score,
            required_additional_verification=required_additional_verification,
            reasoning=reasoning,
            access_restrictions=access_restrictions,
        )
        
        self.authentication_log.append(decision)
        
        return decision
    
    def _classify_posture(self, tilt_x: float, tilt_y: float) -> PostureState:
        """Classify posture from device tilt."""
        total_tilt = math.sqrt(tilt_x**2 + tilt_y**2)
        
        if total_tilt < 15.0:
            return PostureState.UPRIGHT
        elif total_tilt < 45.0:
            return PostureState.SLOUCHED
        else:
            return PostureState.PRONE
    
    def _classify_stillness(self, movement_magnitude: float) -> StillnessLevel:
        """Classify movement from accelerometer."""
        if movement_magnitude < 0.05:
            return StillnessLevel.STILL
        elif movement_magnitude < 0.2:
            return StillnessLevel.NORMAL
        elif movement_magnitude < 0.5:
            return StillnessLevel.RESTLESS
        else:
            return StillnessLevel.TREMOR
    
    def _calculate_anomaly_score(
        self,
        tilt_x: float,
        tilt_y: float,
        latitude: float,
        longitude: float,
        movement_magnitude: float
    ) -> float:
        """
        Calculate composite anomaly score from somatic signals.
        
        Returns score in range [0.0, 1.0]
        """
        if not self.baseline_profile:
            return 0.0
        
        # Posture deviation
        baseline_posture = self.baseline_profile["posture"]
        posture_deviation = (
            abs(tilt_x - baseline_posture["avg_tilt_x"]) / (baseline_posture["std_tilt_x"] + 1e-6) +
            abs(tilt_y - baseline_posture["avg_tilt_y"]) / (baseline_posture["std_tilt_y"] + 1e-6)
        ) / 2.0
        posture_anomaly = min(1.0, posture_deviation / 3.0)  # Normalize to [0, 1]
        
        # Location deviation
        baseline_location = self.baseline_profile["location"]
        distance_meters = self._haversine_distance(
            latitude, longitude,
            baseline_location["primary_latitude"],
            baseline_location["primary_longitude"]
        )
        location_anomaly = min(1.0, distance_meters / 5000.0)  # Anomalous if >5km
        
        # Movement deviation
        baseline_movement = self.baseline_profile["movement"]
        movement_deviation = abs(
            movement_magnitude - baseline_movement["avg_magnitude"]
        ) / (baseline_movement["std_magnitude"] + 1e-6)
        movement_anomaly = min(1.0, movement_deviation / 3.0)
        
        # Weighted composite
        weights = {
            "posture": 0.3,
            "location": 0.4,  # Location is strongest signal
            "movement": 0.3,
        }
        
        composite_score = (
            posture_anomaly * weights["posture"] +
            location_anomaly * weights["location"] +
            movement_anomaly * weights["movement"]
        )
        
        return composite_score
    
    def _assess_duress(self, signature: SomaticSignature) -> DuressLevel:
        """Assess duress level from somatic signature."""
        score = signature.anomaly_score
        
        if score < 0.3:
            return DuressLevel.NORMAL
        elif score < 0.6:
            return DuressLevel.ELEVATED
        elif score < 0.8:
            return DuressLevel.SUSPECTED
        else:
            return DuressLevel.CONFIRMED
    
    def _calculate_centroid(self, locations: list) -> Tuple[float, float]:
        """Calculate geographic centroid of location samples."""
        avg_lat = sum(loc[0] for loc in locations) / len(locations)
        avg_lon = sum(loc[1] for loc in locations) / len(locations)
        return (avg_lat, avg_lon)
    
    def _calculate_std(self, values: list) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    def _haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula.
        
        Returns distance in meters.
        """
        R = 6371000  # Earth radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = (
            math.sin(delta_phi / 2) ** 2 +
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def get_authentication_audit_trail(self) -> list:
        """Retrieve complete authentication audit trail."""
        return [decision.to_dict() for decision in self.authentication_log]
    
    def get_baseline_profile(self) -> Optional[Dict[str, Any]]:
        """Get current baseline somatic profile."""
        return self.baseline_profile


# ═════════════════════════════════════════════════════════════════════════════
# IP-03: Acorn Protocol
# 
# "Your body is the key."
# 
# Core Innovation:
# - Somatic authentication (Posture + Location + Stillness)
# - Duress detection during authentication
# - Prevents "Panic Access" under coercion
# - Adaptive access restrictions based on biometric anomalies
# ═════════════════════════════════════════════════════════════════════════════
