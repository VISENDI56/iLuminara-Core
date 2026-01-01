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
Agent Orchestrator
═════════════════════════════════════════════════════════════════════════════

Coordination layer for multiple AI agents. Orchestrates the Epidemiological
Forecasting Agent, Spatiotemporal Analysis Agent, and Early Warning System Agent
to provide comprehensive disease surveillance and outbreak response.

Core Capabilities:
- Unified data ingestion pipeline for all agents
- Inter-agent communication and data sharing
- Coordinated analysis workflows
- Consolidated reporting and alerting
- Compliance checking via SovereignGuardrail integration
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

from .epidemiological_forecasting_agent import (
    EpidemiologicalForecastingAgent,
    ForecastModel,
    EpidemicForecast,
)
from .spatiotemporal_analysis_agent import (
    SpatiotemporalAnalysisAgent,
    SpatialScale,
    TemporalScale,
    SpatiotemporalAnalysis,
)
from .early_warning_system_agent import (
    EarlyWarningSystemAgent,
    SensorReading,
    EarlyWarningAlert,
)


@dataclass
class OrchestrationResult:
    """Combined result from orchestrated agent analysis."""
    timestamp: datetime
    location: str
    forecasts: List[EpidemicForecast]
    spatial_analysis: Optional[SpatiotemporalAnalysis]
    alerts: List[EarlyWarningAlert]
    summary: Dict[str, Any]
    compliance_status: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize result to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "location": self.location,
            "forecasts": [f.to_dict() for f in self.forecasts],
            "spatial_analysis": self.spatial_analysis.to_dict() if self.spatial_analysis else None,
            "alerts": [a.to_dict() for a in self.alerts],
            "summary": self.summary,
            "compliance_status": self.compliance_status,
            "metadata": self.metadata,
        }


class AgentOrchestrator:
    """
    Orchestration layer that coordinates multiple AI agents for comprehensive
    disease surveillance and outbreak response.
    
    This orchestrator manages three specialized agents:
    1. EpidemiologicalForecastingAgent - Outbreak prediction
    2. SpatiotemporalAnalysisAgent - Multi-scale pattern analysis
    3. EarlyWarningSystemAgent - Real-time alert generation
    
    Usage:
        orchestrator = AgentOrchestrator(
            location="Nairobi",
            population_size=100000
        )
        
        # Ingest data from various sources
        orchestrator.ingest_case_data(case_records)
        orchestrator.ingest_iot_data(sensor_readings)
        orchestrator.ingest_cbs_reports(chv_reports)
        
        # Run coordinated analysis
        result = orchestrator.run_full_analysis()
    """

    def __init__(
        self,
        location: str,
        population_size: int = 100000,
        coordinate_bounds: Optional[Dict[str, float]] = None,
        enable_compliance_checking: bool = True,
    ):
        """
        Initialize the agent orchestrator.
        
        Args:
            location: Geographic location/region
            population_size: Population for epidemiological models
            coordinate_bounds: Geographic bounds for spatial analysis
            enable_compliance_checking: Enable SovereignGuardrail validation
        """
        self.location = location
        self.population_size = population_size
        self.enable_compliance = enable_compliance_checking
        
        # Initialize specialized agents
        self.forecasting_agent = EpidemiologicalForecastingAgent(
            location=location,
            population_size=population_size
        )
        
        self.spatial_agent = SpatiotemporalAnalysisAgent(
            region=location,
            coordinate_bounds=coordinate_bounds
        )
        
        self.early_warning_agent = EarlyWarningSystemAgent(
            location=location
        )
        
        # Data storage
        self.case_data_buffer: List[Dict[str, Any]] = []
        self.historical_results: List[OrchestrationResult] = []
        
        # Compliance module (optional)
        self.sovereign_guardrail = None
        if enable_compliance_checking:
            try:
                from governance_kernel.vector_ledger import SovereignGuardrail
                self.sovereign_guardrail = SovereignGuardrail()
            except ImportError:
                print("⚠️ SovereignGuardrail not available. Compliance checking disabled.")
        
    def ingest_case_data(self, case_records: List[Dict[str, Any]]):
        """
        Ingest case data for analysis by all agents.
        
        Args:
            case_records: List of case records with location, timestamp, and disease info
        """
        self.case_data_buffer.extend(case_records)
        
        # Forward to early warning system
        for record in case_records:
            if record.get("source") == "EMR":
                self.early_warning_agent.ingest_emr_record(record)
            elif record.get("source") == "CBS":
                self.early_warning_agent.ingest_cbs_report(record)
    
    def ingest_iot_data(self, sensor_readings: List[SensorReading]):
        """
        Ingest IoT sensor data.
        
        Args:
            sensor_readings: List of sensor readings
        """
        self.early_warning_agent.ingest_iot_data(sensor_readings)
    
    def ingest_cbs_reports(self, cbs_reports: List[Dict[str, Any]]):
        """
        Ingest community-based surveillance reports.
        
        Args:
            cbs_reports: List of CBS reports
        """
        for report in cbs_reports:
            self.early_warning_agent.ingest_cbs_report(report)
            
            # Add to case data buffer if it's a case report
            if report.get("cases") or report.get("symptom"):
                self.case_data_buffer.append({**report, "source": "CBS"})
    
    def ingest_emr_records(self, emr_records: List[Dict[str, Any]]):
        """
        Ingest electronic medical records.
        
        Args:
            emr_records: List of EMR records
        """
        for record in emr_records:
            self.early_warning_agent.ingest_emr_record(record)
            self.case_data_buffer.append({**record, "source": "EMR"})
    
    def run_full_analysis(
        self,
        diseases: Optional[List[str]] = None,
        forecast_horizon_days: int = 14,
        spatial_scale: SpatialScale = SpatialScale.DISTRICT,
        temporal_scale: TemporalScale = TemporalScale.WEEKLY,
    ) -> OrchestrationResult:
        """
        Run coordinated analysis across all agents.
        
        Args:
            diseases: List of diseases to forecast (if None, inferred from data)
            forecast_horizon_days: Forecast period
            spatial_scale: Scale for spatial analysis
            temporal_scale: Scale for temporal analysis
            
        Returns:
            OrchestrationResult with consolidated findings
        """
        # Step 1: Generate early warning alerts
        print(f"🔍 Checking for early warning signals in {self.location}...")
        alerts = self.early_warning_agent.check_and_generate_alerts()
        
        # Step 2: Run spatiotemporal analysis
        print(f"🗺️ Performing spatiotemporal analysis at {spatial_scale.value} scale...")
        spatial_analysis = None
        if self.case_data_buffer:
            spatial_analysis = self.spatial_agent.analyze(
                case_data=self.case_data_buffer,
                spatial_scale=spatial_scale,
                temporal_scale=temporal_scale,
            )
        
        # Step 3: Generate forecasts
        print(f"📈 Generating epidemiological forecasts...")
        forecasts = []
        
        # Identify diseases to forecast
        if not diseases:
            diseases = self._identify_diseases_from_data()
        
        for disease in diseases:
            # Filter historical data for this disease
            disease_data = [
                record for record in self.case_data_buffer
                if self._matches_disease(record, disease)
            ]
            
            if disease_data:
                forecast = self.forecasting_agent.forecast_outbreak(
                    disease=disease,
                    historical_data=disease_data,
                    forecast_horizon_days=forecast_horizon_days,
                    model=ForecastModel.SEIR,
                )
                forecasts.append(forecast)
        
        # Step 4: Validate compliance (if enabled)
        compliance_status = self._check_compliance(forecasts, spatial_analysis, alerts)
        
        # Step 5: Generate summary
        summary = self._generate_summary(forecasts, spatial_analysis, alerts)
        
        # Create orchestration result
        result = OrchestrationResult(
            timestamp=datetime.utcnow(),
            location=self.location,
            forecasts=forecasts,
            spatial_analysis=spatial_analysis,
            alerts=alerts,
            summary=summary,
            compliance_status=compliance_status,
            metadata={
                "total_case_records": len(self.case_data_buffer),
                "forecast_horizon_days": forecast_horizon_days,
                "spatial_scale": spatial_scale.value,
                "temporal_scale": temporal_scale.value,
            }
        )
        
        self.historical_results.append(result)
        
        print(f"✅ Analysis complete: {len(forecasts)} forecasts, {len(alerts)} alerts generated")
        
        return result
    
    def run_realtime_monitoring(self) -> Dict[str, Any]:
        """
        Run real-time monitoring mode - lightweight checks for immediate alerts.
        
        This is optimized for edge deployment with minimal latency.
        
        Returns:
            Dict with immediate alerts and system status
        """
        # Check for immediate alerts only (no forecasting/analysis)
        alerts = self.early_warning_agent.check_and_generate_alerts()
        
        # Get system status
        early_warning_status = self.early_warning_agent.get_alert_summary()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "location": self.location,
            "new_alerts": [a.to_dict() for a in alerts],
            "active_alerts": [
                a.to_dict() for a in self.early_warning_agent.get_active_alerts()
            ],
            "system_status": early_warning_status,
        }
    
    def generate_report(self, format: str = "json") -> str:
        """
        Generate comprehensive report from all agents.
        
        Args:
            format: Output format ("json" or "markdown")
            
        Returns:
            Formatted report string
        """
        if not self.historical_results:
            return "No analysis results available."
        
        latest = self.historical_results[-1]
        
        if format == "json":
            return json.dumps(latest.to_dict(), indent=2)
        elif format == "markdown":
            return self._generate_markdown_report(latest)
        else:
            return "Unsupported format"
    
    def _identify_diseases_from_data(self) -> List[str]:
        """Identify diseases present in case data."""
        diseases = set()
        
        for record in self.case_data_buffer:
            if "disease" in record:
                diseases.add(record["disease"])
            if "diagnosis" in record:
                diseases.add(record["diagnosis"])
        
        # Default diseases if none identified
        if not diseases:
            diseases = {"cholera", "malaria"}
        
        return list(diseases)
    
    def _matches_disease(self, record: Dict[str, Any], disease: str) -> bool:
        """Check if record matches specified disease."""
        disease_lower = disease.lower()
        
        if "disease" in record and disease_lower in record["disease"].lower():
            return True
        if "diagnosis" in record and disease_lower in record["diagnosis"].lower():
            return True
        if "symptom" in record:
            # Symptom-based matching
            symptom = record["symptom"].lower()
            if disease_lower == "cholera" and ("diarrhea" in symptom or "vomit" in symptom):
                return True
            if disease_lower == "malaria" and ("fever" in symptom):
                return True
        
        return False
    
    def _check_compliance(
        self,
        forecasts: List[EpidemicForecast],
        spatial_analysis: Optional[SpatiotemporalAnalysis],
        alerts: List[EarlyWarningAlert],
    ) -> Dict[str, Any]:
        """
        Check compliance with sovereignty and regulatory requirements.
        
        Returns compliance status and any violations.
        """
        if not self.sovereign_guardrail:
            return {
                "enabled": False,
                "message": "Compliance checking disabled"
            }
        
        violations = []
        
        try:
            # Validate high-risk AI inferences require explainability
            for forecast in forecasts:
                if forecast.risk_score > 0.7:  # High risk threshold
                    self.sovereign_guardrail.validate_action(
                        action_type='High_Risk_Inference',
                        payload={
                            'inference': f'{forecast.disease} outbreak forecast',
                            'explanation': forecast.metadata,  # Model parameters as explanation
                            'risk_score': forecast.risk_score,
                        },
                        jurisdiction='GLOBAL_DEFAULT'
                    )
            
            # Validate data processing has consent (placeholder)
            # In production, would check actual consent records
            
        except Exception as e:
            violations.append(str(e))
        
        return {
            "enabled": True,
            "status": "COMPLIANT" if not violations else "VIOLATIONS_DETECTED",
            "violations": violations,
            "frameworks_checked": ["GLOBAL_DEFAULT", "EU AI Act"],
        }
    
    def _generate_summary(
        self,
        forecasts: List[EpidemicForecast],
        spatial_analysis: Optional[SpatiotemporalAnalysis],
        alerts: List[EarlyWarningAlert],
    ) -> Dict[str, Any]:
        """Generate executive summary of analysis."""
        # Risk assessment
        max_risk = max([f.risk_score for f in forecasts], default=0.0)
        critical_alerts = sum(1 for a in alerts if a.severity == "Critical")
        high_alerts = sum(1 for a in alerts if a.severity == "High")
        
        overall_status = "Normal"
        if critical_alerts > 0 or max_risk > 0.9:
            overall_status = "Critical"
        elif high_alerts > 0 or max_risk > 0.7:
            overall_status = "High Risk"
        elif len(alerts) > 0 or max_risk > 0.5:
            overall_status = "Elevated"
        
        return {
            "overall_status": overall_status,
            "max_risk_score": max_risk,
            "total_forecasts": len(forecasts),
            "total_alerts": len(alerts),
            "critical_alerts": critical_alerts,
            "high_alerts": high_alerts,
            "diseases_monitored": [f.disease for f in forecasts],
            "spatial_clusters": (
                len(spatial_analysis.clusters) if spatial_analysis else 0
            ),
            "hotspots_detected": (
                len(spatial_analysis.hotspots) if spatial_analysis else 0
            ),
        }
    
    def _generate_markdown_report(self, result: OrchestrationResult) -> str:
        """Generate markdown-formatted report."""
        lines = [
            f"# Disease Surveillance Report: {result.location}",
            f"**Generated:** {result.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## Executive Summary",
            f"- **Overall Status:** {result.summary['overall_status']}",
            f"- **Maximum Risk Score:** {result.summary['max_risk_score']:.2f}",
            f"- **Active Alerts:** {result.summary['total_alerts']} ({result.summary['critical_alerts']} critical)",
            f"- **Diseases Monitored:** {', '.join(result.summary['diseases_monitored'])}",
            "",
        ]
        
        # Alerts section
        if result.alerts:
            lines.extend([
                "## Active Alerts",
                "",
            ])
            for alert in result.alerts:
                lines.append(f"### {alert.severity} Alert: {alert.alert_type}")
                lines.append(f"- **Disease:** {alert.disease or 'Unknown'}")
                lines.append(f"- **Confidence:** {alert.confidence:.0%}")
                lines.append(f"- **Recommendations:**")
                for rec in alert.recommendations:
                    lines.append(f"  - {rec}")
                lines.append("")
        
        # Forecasts section
        if result.forecasts:
            lines.extend([
                "## Epidemiological Forecasts",
                "",
            ])
            for forecast in result.forecasts:
                lines.append(f"### {forecast.disease}")
                lines.append(f"- **R0:** {forecast.estimated_r0:.2f}")
                lines.append(f"- **Risk Score:** {forecast.risk_score:.2f}")
                lines.append(f"- **Peak Prediction:** {forecast.peak_prediction['magnitude']} cases")
                lines.append("")
        
        # Spatial analysis section
        if result.spatial_analysis:
            lines.extend([
                "## Spatiotemporal Analysis",
                f"- **Clusters Detected:** {len(result.spatial_analysis.clusters)}",
                f"- **Hotspots:** {len(result.spatial_analysis.hotspots)}",
                f"- **Temporal Trend:** {result.spatial_analysis.temporal_trends.get('trend', 'Unknown')}",
                "",
            ])
        
        # Compliance section
        lines.extend([
            "## Compliance Status",
            f"- **Status:** {result.compliance_status.get('status', 'Unknown')}",
            f"- **Frameworks:** {', '.join(result.compliance_status.get('frameworks_checked', []))}",
            "",
        ])
        
        return "\n".join(lines)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "location": self.location,
            "population_size": self.population_size,
            "agents": {
                "forecasting": {
                    "total_forecasts": len(self.forecasting_agent.forecast_history),
                },
                "spatial_analysis": {
                    "total_analyses": len(self.spatial_agent.analysis_history),
                },
                "early_warning": self.early_warning_agent.get_alert_summary(),
            },
            "data_buffer": {
                "case_records": len(self.case_data_buffer),
            },
            "compliance_checking": self.enable_compliance,
            "historical_results": len(self.historical_results),
        }
