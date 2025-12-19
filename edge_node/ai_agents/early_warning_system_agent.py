"""
Early Warning System Agent
═════════════════════════════════════════════════════════════════════════════

Specialized AI agent for early outbreak detection and warning generation.
Integrates IoT sensor data (environmental, biosensors) with community-based
surveillance (CBS) and electronic medical records (EMR) to provide real-time
outbreak alerts with minimal latency.

Core Capabilities:
- Multi-source data fusion (IoT sensors + CBS + EMR)
- Real-time anomaly detection and outbreak scoring
- Automated alert generation with severity classification
- Integration with LoRa mesh networks for low-latency edge communication
- Threshold-based and ML-based early warning triggers
- Alert prioritization and stakeholder notification routing
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# Environmental risk thresholds
# Heavy rainfall increases cholera transmission risk through water contamination
HEAVY_RAINFALL_THRESHOLD_MM = 100
# Optimal temperature range for mosquito breeding (malaria vectors)
VECTOR_OPTIMAL_TEMP_MIN_C = 25
VECTOR_OPTIMAL_TEMP_MAX_C = 30
# High humidity threshold for mosquito activity
HIGH_HUMIDITY_THRESHOLD_PCT = 60
# Cold weather threshold for respiratory disease transmission
COLD_WEATHER_THRESHOLD_C = 15


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "Info"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class DataSourceType(Enum):
    """Data source types for early warning system."""
    IOT_ENVIRONMENTAL = "IoT Environmental Sensor"  # Temperature, humidity, rainfall
    IOT_BIOSENSOR = "IoT Biosensor"  # Pathogen detection, air quality
    CBS_REPORT = "Community-Based Surveillance"  # CHV reports, symptom surveys
    EMR_RECORD = "Electronic Medical Record"  # Hospital/clinic confirmations
    EXTERNAL_ALERT = "External Alert"  # WHO, CDC, or regional health alerts


@dataclass
class SensorReading:
    """IoT sensor reading."""
    sensor_id: str
    sensor_type: str
    location: Tuple[float, float]  # (lat, lon)
    timestamp: datetime
    readings: Dict[str, float]  # sensor-specific readings
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EarlyWarningAlert:
    """Generated early warning alert."""
    alert_id: str
    severity: str
    alert_type: str  # "Outbreak", "Anomaly", "Environmental Risk"
    disease: Optional[str]
    location: Tuple[float, float]
    affected_radius_km: float
    timestamp: datetime
    confidence: float  # 0.0 to 1.0
    data_sources: List[str]  # Source types that triggered alert
    evidence: Dict[str, Any]  # Supporting evidence
    recommendations: List[str]
    stakeholders: List[str]  # Who should be notified
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize alert to dictionary."""
        return {
            "alert_id": self.alert_id,
            "severity": self.severity,
            "alert_type": self.alert_type,
            "disease": self.disease,
            "location": self.location,
            "affected_radius_km": self.affected_radius_km,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "data_sources": self.data_sources,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "stakeholders": self.stakeholders,
            "metadata": self.metadata,
        }


@dataclass
class MultiSourceSignal:
    """Fused signal from multiple data sources."""
    signal_id: str
    location: Tuple[float, float]
    timestamp: datetime
    iot_signals: List[SensorReading]
    cbs_reports: List[Dict[str, Any]]
    emr_records: List[Dict[str, Any]]
    composite_score: float  # Combined risk score
    verification_status: str  # "Unverified", "Partial", "Confirmed"
    metadata: Dict[str, Any] = field(default_factory=dict)


class EarlyWarningSystemAgent:
    """
    Autonomous AI agent for early outbreak detection and warning generation.
    
    This agent continuously monitors multiple data streams (IoT sensors, CBS, EMR)
    and generates timely alerts when outbreak patterns are detected. Designed for
    edge deployment with minimal latency (<5 seconds from signal to alert).
    
    Usage:
        agent = EarlyWarningSystemAgent(location="Dadaab")
        
        # Process IoT sensor data
        agent.ingest_iot_data(sensor_readings)
        
        # Process CBS reports
        agent.ingest_cbs_report(chv_report)
        
        # Check for alerts
        alerts = agent.check_and_generate_alerts()
    """

    def __init__(
        self,
        location: str,
        alert_thresholds: Optional[Dict[str, float]] = None,
        stakeholder_config: Optional[Dict[str, List[str]]] = None,
    ):
        """
        Initialize the early warning system agent.
        
        Args:
            location: Geographic location/region
            alert_thresholds: Custom thresholds for alert generation
            stakeholder_config: Mapping of alert types to stakeholder lists
        """
        self.location = location
        self.alert_thresholds = alert_thresholds or self._default_thresholds()
        self.stakeholder_config = stakeholder_config or self._default_stakeholders()
        
        # Data buffers (recent data for analysis)
        self.iot_buffer: List[SensorReading] = []
        self.cbs_buffer: List[Dict[str, Any]] = []
        self.emr_buffer: List[Dict[str, Any]] = []
        
        # Alert history
        self.active_alerts: List[EarlyWarningAlert] = []
        self.alert_history: List[EarlyWarningAlert] = []
        
        # Baseline statistics for anomaly detection
        self.baseline_stats = {}
        
    def ingest_iot_data(self, sensor_readings: List[SensorReading]):
        """
        Ingest IoT sensor data into the early warning system.
        
        Args:
            sensor_readings: List of sensor readings
        """
        self.iot_buffer.extend(sensor_readings)
        
        # Keep only recent data (last 24 hours)
        cutoff = datetime.utcnow() - timedelta(hours=24)
        self.iot_buffer = [
            r for r in self.iot_buffer
            if r.timestamp > cutoff
        ]
        
        # Update baseline statistics
        self._update_baseline_stats()
    
    def ingest_cbs_report(self, cbs_report: Dict[str, Any]):
        """
        Ingest community-based surveillance report.
        
        Args:
            cbs_report: CBS report from community health volunteer
        """
        self.cbs_buffer.append(cbs_report)
        
        # Keep only recent reports (last 7 days)
        cutoff = datetime.utcnow() - timedelta(days=7)
        self.cbs_buffer = [
            r for r in self.cbs_buffer
            if self._parse_timestamp(r.get("timestamp", datetime.utcnow())) > cutoff
        ]
    
    def ingest_emr_record(self, emr_record: Dict[str, Any]):
        """
        Ingest electronic medical record.
        
        Args:
            emr_record: EMR record from hospital/clinic
        """
        self.emr_buffer.append(emr_record)
        
        # Keep only recent records (last 14 days)
        cutoff = datetime.utcnow() - timedelta(days=14)
        self.emr_buffer = [
            r for r in self.emr_buffer
            if self._parse_timestamp(r.get("timestamp", datetime.utcnow())) > cutoff
        ]
    
    def check_and_generate_alerts(self) -> List[EarlyWarningAlert]:
        """
        Check all data sources and generate alerts if warranted.
        
        Returns:
            List of newly generated alerts
        """
        new_alerts = []
        
        # Fuse multi-source signals
        fused_signals = self._fuse_data_sources()
        
        # Check each fused signal for alert conditions
        for signal in fused_signals:
            alert = self._evaluate_signal_for_alert(signal)
            if alert:
                new_alerts.append(alert)
                self.active_alerts.append(alert)
                self.alert_history.append(alert)
        
        # Check IoT sensors for environmental risks
        env_alerts = self._check_environmental_risks()
        new_alerts.extend(env_alerts)
        
        # Check for anomalies
        anomaly_alerts = self._check_anomalies()
        new_alerts.extend(anomaly_alerts)
        
        return new_alerts
    
    def _fuse_data_sources(self) -> List[MultiSourceSignal]:
        """
        Fuse IoT, CBS, and EMR data sources into composite signals.
        
        Returns signals where multiple sources indicate potential outbreak.
        """
        fused_signals = []
        
        # Group data by spatial proximity and temporal window
        spatial_groups = self._group_by_location(
            iot_data=self.iot_buffer,
            cbs_data=self.cbs_buffer,
            emr_data=self.emr_buffer,
            radius_km=10.0,  # Group within 10km
        )
        
        for group_id, group_data in spatial_groups.items():
            # Calculate composite risk score
            composite_score = self._calculate_composite_score(group_data)
            
            # Determine verification status
            verification = self._determine_verification_status(group_data)
            
            if composite_score > 0.3:  # Minimum threshold for signal
                signal = MultiSourceSignal(
                    signal_id=f"SIGNAL_{len(fused_signals) + 1}",
                    location=group_data["center"],
                    timestamp=datetime.utcnow(),
                    iot_signals=group_data.get("iot", []),
                    cbs_reports=group_data.get("cbs", []),
                    emr_records=group_data.get("emr", []),
                    composite_score=composite_score,
                    verification_status=verification,
                )
                fused_signals.append(signal)
        
        return fused_signals
    
    def _evaluate_signal_for_alert(
        self,
        signal: MultiSourceSignal,
    ) -> Optional[EarlyWarningAlert]:
        """
        Evaluate a fused signal and generate alert if thresholds are met.
        
        Args:
            signal: Multi-source fused signal
            
        Returns:
            Alert if thresholds exceeded, None otherwise
        """
        # Determine alert severity based on composite score and verification
        severity = self._determine_severity(signal.composite_score, signal.verification_status)
        
        if severity == AlertSeverity.INFO:
            return None  # Below alert threshold
        
        # Identify likely disease from evidence
        disease = self._identify_disease(signal)
        
        # Gather supporting evidence
        evidence = {
            "composite_score": signal.composite_score,
            "verification_status": signal.verification_status,
            "iot_sensor_count": len(signal.iot_signals),
            "cbs_report_count": len(signal.cbs_reports),
            "emr_confirmation_count": len(signal.emr_records),
            "temporal_span_hours": self._calculate_temporal_span(signal),
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(severity, disease, signal)
        
        # Identify stakeholders to notify
        stakeholders = self._identify_stakeholders(severity, disease)
        
        # Calculate confidence
        confidence = self._calculate_alert_confidence(signal)
        
        alert = EarlyWarningAlert(
            alert_id=f"ALERT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            severity=severity.value,
            alert_type="Outbreak Detection",
            disease=disease,
            location=signal.location,
            affected_radius_km=10.0,  # Estimated from signal sources
            timestamp=datetime.utcnow(),
            confidence=confidence,
            data_sources=[
                ds.value for ds in [
                    DataSourceType.IOT_ENVIRONMENTAL if signal.iot_signals else None,
                    DataSourceType.CBS_REPORT if signal.cbs_reports else None,
                    DataSourceType.EMR_RECORD if signal.emr_records else None,
                ]
                if ds is not None
            ],
            evidence=evidence,
            recommendations=recommendations,
            stakeholders=stakeholders,
            metadata={
                "location_name": self.location,
                "signal_id": signal.signal_id,
            }
        )
        
        return alert
    
    def _check_environmental_risks(self) -> List[EarlyWarningAlert]:
        """
        Check IoT environmental sensors for risk conditions.
        
        Examples: Excessive rainfall (cholera risk), temperature spikes (vector-borne disease)
        """
        alerts = []
        
        # Analyze recent environmental readings
        recent_env_sensors = [
            s for s in self.iot_buffer
            if "environmental" in s.sensor_type.lower()
            and (datetime.utcnow() - s.timestamp).total_seconds() < 3600  # Last hour
        ]
        
        if not recent_env_sensors:
            return alerts
        
        # Check rainfall levels (cholera risk)
        rainfall_readings = [
            s.readings.get("rainfall_mm", 0)
            for s in recent_env_sensors
            if "rainfall_mm" in s.readings
        ]
        
        if rainfall_readings:
            avg_rainfall = sum(rainfall_readings) / len(rainfall_readings)
            if avg_rainfall > HEAVY_RAINFALL_THRESHOLD_MM:
                alert = EarlyWarningAlert(
                    alert_id=f"ENV_ALERT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    severity=AlertSeverity.MEDIUM.value,
                    alert_type="Environmental Risk",
                    disease="Cholera",
                    location=recent_env_sensors[0].location,
                    affected_radius_km=20.0,
                    timestamp=datetime.utcnow(),
                    confidence=0.7,
                    data_sources=[DataSourceType.IOT_ENVIRONMENTAL.value],
                    evidence={
                        "average_rainfall_mm": avg_rainfall,
                        "sensor_count": len(rainfall_readings),
                    },
                    recommendations=[
                        "Monitor water sources for contamination",
                        "Increase water treatment vigilance",
                        "Prepare rapid response for potential waterborne disease outbreak",
                    ],
                    stakeholders=["Environmental Health Officer", "Water Sanitation Manager"],
                )
                alerts.append(alert)
        
        # Check temperature patterns (vector-borne disease risk)
        temp_readings = [
            s.readings.get("temperature_c", 0)
            for s in recent_env_sensors
            if "temperature_c" in s.readings
        ]
        
        if temp_readings:
            avg_temp = sum(temp_readings) / len(temp_readings)
            if VECTOR_OPTIMAL_TEMP_MIN_C <= avg_temp <= VECTOR_OPTIMAL_TEMP_MAX_C:
                humidity_readings = [
                    s.readings.get("humidity_pct", 0)
                    for s in recent_env_sensors
                    if "humidity_pct" in s.readings
                ]
                
                if humidity_readings:
                    avg_humidity = sum(humidity_readings) / len(humidity_readings)
                    if avg_humidity > HIGH_HUMIDITY_THRESHOLD_PCT:
                        alert = EarlyWarningAlert(
                            alert_id=f"ENV_ALERT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_2",
                            severity=AlertSeverity.MEDIUM.value,
                            alert_type="Environmental Risk",
                            disease="Malaria",
                            location=recent_env_sensors[0].location,
                            affected_radius_km=15.0,
                            timestamp=datetime.utcnow(),
                            confidence=0.65,
                            data_sources=[DataSourceType.IOT_ENVIRONMENTAL.value],
                            evidence={
                                "average_temperature_c": avg_temp,
                                "average_humidity_pct": avg_humidity,
                            },
                            recommendations=[
                                "Increase vector control activities",
                                "Distribute mosquito nets in high-risk areas",
                                "Monitor for malaria case increases",
                            ],
                            stakeholders=["Vector Control Officer", "Malaria Program Manager"],
                        )
                        alerts.append(alert)
        
        return alerts
    
    def _check_anomalies(self) -> List[EarlyWarningAlert]:
        """
        Detect anomalous patterns in data streams using statistical methods.
        
        Returns alerts for significant deviations from baseline.
        """
        alerts = []
        
        # Check CBS report rate anomaly
        if len(self.cbs_buffer) > 0 and self.baseline_stats.get("cbs_daily_avg"):
            recent_24h = sum(
                1 for r in self.cbs_buffer
                if (datetime.utcnow() - self._parse_timestamp(r.get("timestamp"))).total_seconds() < 86400
            )
            
            baseline_avg = self.baseline_stats["cbs_daily_avg"]
            if recent_24h > baseline_avg * 3:  # 3x baseline
                alert = EarlyWarningAlert(
                    alert_id=f"ANOMALY_ALERT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    severity=AlertSeverity.HIGH.value,
                    alert_type="Anomaly Detection",
                    disease=None,
                    location=(0.0, 0.0),  # Would use actual location from reports
                    affected_radius_km=25.0,
                    timestamp=datetime.utcnow(),
                    confidence=0.8,
                    data_sources=[DataSourceType.CBS_REPORT.value],
                    evidence={
                        "recent_24h_reports": recent_24h,
                        "baseline_daily_avg": baseline_avg,
                        "multiplier": recent_24h / baseline_avg if baseline_avg > 0 else 0,
                    },
                    recommendations=[
                        "Investigate spike in community health reports",
                        "Conduct rapid syndromic surveillance",
                        "Verify with healthcare facilities",
                    ],
                    stakeholders=["Epidemiologist", "District Health Officer"],
                )
                alerts.append(alert)
        
        return alerts
    
    def get_active_alerts(self) -> List[EarlyWarningAlert]:
        """Get currently active alerts."""
        # Filter out alerts older than 48 hours
        cutoff = datetime.utcnow() - timedelta(hours=48)
        self.active_alerts = [
            a for a in self.active_alerts
            if a.timestamp > cutoff
        ]
        return self.active_alerts
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of alert system status."""
        return {
            "location": self.location,
            "active_alerts": len(self.get_active_alerts()),
            "total_alerts_generated": len(self.alert_history),
            "data_buffer_status": {
                "iot_readings": len(self.iot_buffer),
                "cbs_reports": len(self.cbs_buffer),
                "emr_records": len(self.emr_buffer),
            },
            "alert_breakdown": {
                severity: sum(1 for a in self.alert_history if a.severity == severity)
                for severity in ["Info", "Low", "Medium", "High", "Critical"]
            },
        }
    
    # Helper methods
    
    def _default_thresholds(self) -> Dict[str, float]:
        """Default alert thresholds."""
        return {
            "composite_score_low": 0.4,
            "composite_score_medium": 0.6,
            "composite_score_high": 0.8,
            "composite_score_critical": 0.9,
        }
    
    def _default_stakeholders(self) -> Dict[str, List[str]]:
        """Default stakeholder notification configuration."""
        return {
            "Critical": ["Ministry of Health", "WHO", "District Health Officer", "Epidemiologist"],
            "High": ["District Health Officer", "Epidemiologist", "Hospital Director"],
            "Medium": ["District Health Officer", "Environmental Health Officer"],
            "Low": ["Community Health Coordinator"],
        }
    
    def _update_baseline_stats(self):
        """Update baseline statistics for anomaly detection."""
        # Calculate average daily CBS reports
        if self.cbs_buffer:
            days_of_data = max(
                1,
                (
                    self._parse_timestamp(self.cbs_buffer[-1].get("timestamp")) -
                    self._parse_timestamp(self.cbs_buffer[0].get("timestamp"))
                ).days
            )
            self.baseline_stats["cbs_daily_avg"] = len(self.cbs_buffer) / days_of_data
        
        # Calculate average IoT readings
        if self.iot_buffer:
            self.baseline_stats["iot_sensor_count"] = len(self.iot_buffer)
    
    def _group_by_location(
        self,
        iot_data: List[SensorReading],
        cbs_data: List[Dict[str, Any]],
        emr_data: List[Dict[str, Any]],
        radius_km: float,
    ) -> Dict[str, Dict[str, Any]]:
        """Group data sources by spatial proximity."""
        groups = {}
        
        # Simple spatial grouping (would use more sophisticated algorithm in production)
        all_locations = []
        
        # Collect all locations
        for sensor in iot_data:
            all_locations.append(("iot", sensor, sensor.location))
        
        for cbs in cbs_data:
            lat = cbs.get("lat", cbs.get("latitude", 0.0))
            lon = cbs.get("lon", cbs.get("longitude", 0.0))
            all_locations.append(("cbs", cbs, (lat, lon)))
        
        for emr in emr_data:
            lat = emr.get("lat", emr.get("latitude", 0.0))
            lon = emr.get("lon", emr.get("longitude", 0.0))
            all_locations.append(("emr", emr, (lat, lon)))
        
        # Group locations within radius
        group_id = 0
        visited = set()
        
        for i, (source_type, data, loc) in enumerate(all_locations):
            if i in visited:
                continue
            
            group_key = f"GROUP_{group_id}"
            groups[group_key] = {
                "center": loc,
                "iot": [],
                "cbs": [],
                "emr": [],
            }
            
            visited.add(i)
            groups[group_key][source_type].append(data)
            
            # Find nearby locations
            for j, (other_type, other_data, other_loc) in enumerate(all_locations):
                if j != i and j not in visited:
                    dist = self._haversine_distance(loc[0], loc[1], other_loc[0], other_loc[1])
                    if dist <= radius_km:
                        groups[group_key][other_type].append(other_data)
                        visited.add(j)
            
            group_id += 1
        
        return groups
    
    def _calculate_composite_score(self, group_data: Dict[str, Any]) -> float:
        """Calculate composite risk score from grouped data sources."""
        iot_score = min(1.0, len(group_data.get("iot", [])) * 0.2)
        cbs_score = min(1.0, len(group_data.get("cbs", [])) * 0.3)
        emr_score = min(1.0, len(group_data.get("emr", [])) * 0.5)
        
        # Weighted combination with cross-verification bonus
        base_score = 0.3 * iot_score + 0.3 * cbs_score + 0.4 * emr_score
        
        # Bonus for multi-source verification
        source_count = sum([
            1 if group_data.get("iot") else 0,
            1 if group_data.get("cbs") else 0,
            1 if group_data.get("emr") else 0,
        ])
        verification_bonus = 0.2 if source_count >= 2 else 0
        
        return min(1.0, base_score + verification_bonus)
    
    def _determine_verification_status(self, group_data: Dict[str, Any]) -> str:
        """Determine verification status from multiple sources."""
        has_emr = len(group_data.get("emr", [])) > 0
        has_cbs = len(group_data.get("cbs", [])) > 0
        has_iot = len(group_data.get("iot", [])) > 0
        
        if has_emr and (has_cbs or has_iot):
            return "Confirmed"
        elif has_cbs and has_iot:
            return "Partial"
        else:
            return "Unverified"
    
    def _determine_severity(self, composite_score: float, verification_status: str) -> AlertSeverity:
        """Determine alert severity based on score and verification."""
        # Adjust score based on verification
        if verification_status == "Confirmed":
            adjusted_score = composite_score * 1.2
        elif verification_status == "Partial":
            adjusted_score = composite_score * 1.0
        else:
            adjusted_score = composite_score * 0.8
        
        if adjusted_score >= self.alert_thresholds["composite_score_critical"]:
            return AlertSeverity.CRITICAL
        elif adjusted_score >= self.alert_thresholds["composite_score_high"]:
            return AlertSeverity.HIGH
        elif adjusted_score >= self.alert_thresholds["composite_score_medium"]:
            return AlertSeverity.MEDIUM
        elif adjusted_score >= self.alert_thresholds["composite_score_low"]:
            return AlertSeverity.LOW
        else:
            return AlertSeverity.INFO
    
    def _identify_disease(self, signal: MultiSourceSignal) -> Optional[str]:
        """Identify likely disease from signal evidence."""
        # Extract disease mentions from CBS reports
        diseases = []
        for cbs in signal.cbs_reports:
            if "disease" in cbs:
                diseases.append(cbs["disease"])
            if "symptom" in cbs:
                # Map symptoms to likely diseases
                symptom = cbs["symptom"].lower()
                if "diarrhea" in symptom or "vomit" in symptom:
                    diseases.append("Cholera")
                elif "fever" in symptom and "joint pain" in symptom:
                    diseases.append("Malaria")
                elif "cough" in symptom or "respiratory" in symptom:
                    diseases.append("Respiratory Infection")
        
        # Extract from EMR records
        for emr in signal.emr_records:
            if "diagnosis" in emr:
                diseases.append(emr["diagnosis"])
        
        # Return most common disease
        if diseases:
            from collections import Counter
            return Counter(diseases).most_common(1)[0][0]
        
        return None
    
    def _generate_recommendations(
        self,
        severity: AlertSeverity,
        disease: Optional[str],
        signal: MultiSourceSignal,
    ) -> List[str]:
        """Generate action recommendations based on alert."""
        recommendations = []
        
        if severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH]:
            recommendations.append("Activate emergency response protocol")
            recommendations.append("Deploy rapid response team to affected area")
            recommendations.append("Notify WHO and regional health authorities")
        
        if disease:
            disease_lower = disease.lower()
            if "cholera" in disease_lower:
                recommendations.extend([
                    "Distribute oral rehydration solution (ORS)",
                    "Test water sources for contamination",
                    "Establish treatment centers",
                ])
            elif "malaria" in disease_lower:
                recommendations.extend([
                    "Distribute antimalarial medications",
                    "Intensify vector control (IRS, LLINs)",
                    "Conduct case investigation",
                ])
        
        if signal.verification_status == "Unverified":
            recommendations.append("Conduct field verification with healthcare facilities")
        
        return recommendations
    
    def _identify_stakeholders(self, severity: AlertSeverity, disease: Optional[str]) -> List[str]:
        """Identify stakeholders to notify."""
        stakeholders = self.stakeholder_config.get(severity.value, [])
        
        # Add disease-specific stakeholders
        if disease:
            disease_lower = disease.lower()
            if "malaria" in disease_lower:
                stakeholders.append("Malaria Program Manager")
            elif "cholera" in disease_lower:
                stakeholders.append("Water Sanitation Manager")
        
        return list(set(stakeholders))  # Remove duplicates
    
    def _calculate_alert_confidence(self, signal: MultiSourceSignal) -> float:
        """Calculate confidence level for alert."""
        # Base confidence from composite score
        base_confidence = signal.composite_score
        
        # Adjust for verification
        if signal.verification_status == "Confirmed":
            base_confidence *= 1.2
        elif signal.verification_status == "Unverified":
            base_confidence *= 0.8
        
        # Adjust for number of data points
        data_point_count = (
            len(signal.iot_signals) +
            len(signal.cbs_reports) +
            len(signal.emr_records)
        )
        data_bonus = min(0.2, data_point_count * 0.05)
        
        return min(1.0, base_confidence + data_bonus)
    
    def _calculate_temporal_span(self, signal: MultiSourceSignal) -> float:
        """Calculate temporal span of signal in hours."""
        all_timestamps = []
        
        for sensor in signal.iot_signals:
            all_timestamps.append(sensor.timestamp)
        
        for cbs in signal.cbs_reports:
            all_timestamps.append(self._parse_timestamp(cbs.get("timestamp")))
        
        for emr in signal.emr_records:
            all_timestamps.append(self._parse_timestamp(emr.get("timestamp")))
        
        if len(all_timestamps) < 2:
            return 0.0
        
        span = (max(all_timestamps) - min(all_timestamps)).total_seconds() / 3600
        return span
    
    def _parse_timestamp(self, timestamp: Any) -> datetime:
        """Parse timestamp from various formats."""
        if isinstance(timestamp, datetime):
            return timestamp
        elif isinstance(timestamp, str):
            try:
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return datetime.utcnow()
        else:
            return datetime.utcnow()
    
    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """Calculate distance between two points in kilometers."""
        import math
        R = 6371  # Earth radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
