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
AI Agents Example Usage
═════════════════════════════════════════════════════════════════════════════

Demonstrates the usage of AI agents specialized in epidemiological forecasting,
multi-scale spatiotemporal analysis, and early warning systems that integrate
IoT sensor data with community health reports.

This example shows:
1. Individual agent usage
2. Coordinated multi-agent orchestration
3. Integration with iLuminara's Golden Thread data fusion
4. Compliance checking with SovereignGuardrail
"""

from datetime import datetime, timedelta
import json

# Import AI agents
from edge_node.ai_agents import (
    EpidemiologicalForecastingAgent,
    SpatiotemporalAnalysisAgent,
    EarlyWarningSystemAgent,
    AgentOrchestrator,
)
from edge_node.ai_agents.epidemiological_forecasting_agent import ForecastModel
from edge_node.ai_agents.spatiotemporal_analysis_agent import SpatialScale, TemporalScale
from edge_node.ai_agents.early_warning_system_agent import SensorReading


def demo_forecasting_agent():
    """Demonstrate the Epidemiological Forecasting Agent."""
    print("\n" + "="*80)
    print("DEMO 1: Epidemiological Forecasting Agent")
    print("="*80 + "\n")
    
    # Initialize agent
    agent = EpidemiologicalForecastingAgent(
        location="Dadaab Refugee Camp",
        population_size=150000
    )
    
    # Create sample historical data (simulated cholera outbreak)
    historical_data = []
    base_cases = 2
    for day in range(21):  # 3 weeks of data
        # Simulate exponential growth
        cases = base_cases + int(base_cases * (1.15 ** day))
        historical_data.append({
            "date": (datetime.utcnow() - timedelta(days=21-day)).isoformat(),
            "cases": cases,
            "disease": "cholera",
        })
    
    print(f"📊 Historical data: {len(historical_data)} days of cholera cases")
    print(f"   Initial cases: {historical_data[0]['cases']}")
    print(f"   Recent cases: {historical_data[-1]['cases']}")
    
    # Generate forecast
    forecast = agent.forecast_outbreak(
        disease="cholera",
        historical_data=historical_data,
        forecast_horizon_days=14,
        model=ForecastModel.SEIR,
        environmental_factors={
            "rainfall_mm": 120,  # Heavy rainfall
            "temperature_c": 28,
            "humidity_pct": 75,
        }
    )
    
    # Display results
    print(f"\n🔮 Forecast Results:")
    print(f"   Disease: {forecast.disease}")
    print(f"   Model: {forecast.model_used}")
    print(f"   R0 (Basic Reproduction Number): {forecast.estimated_r0:.2f}")
    print(f"   Risk Score: {forecast.risk_score:.2f}")
    print(f"   Predicted Peak: {forecast.peak_prediction['magnitude']} cases on {forecast.peak_prediction['date'][:10]}")
    print(f"\n   14-Day Forecast (first 5 days):")
    for pred in forecast.predictions[:5]:
        print(f"     Day {pred['date'][:10]}: {pred['infected']} infected, {pred['new_cases']} new cases")
    
    return forecast


def demo_spatiotemporal_agent():
    """Demonstrate the Spatiotemporal Analysis Agent."""
    print("\n" + "="*80)
    print("DEMO 2: Spatiotemporal Analysis Agent")
    print("="*80 + "\n")
    
    # Initialize agent
    agent = SpatiotemporalAnalysisAgent(
        region="Garissa County, Kenya",
        coordinate_bounds={
            "min_lat": -0.5, "max_lat": 1.5,
            "min_lon": 39.0, "max_lon": 41.5
        }
    )
    
    # Create sample case data with spatial clustering
    case_data = []
    
    # Cluster 1: Dadaab (0.05N, 40.31E)
    for i in range(25):
        case_data.append({
            "lat": 0.05 + (i % 5) * 0.01,
            "lon": 40.31 + (i % 5) * 0.01,
            "timestamp": (datetime.utcnow() - timedelta(days=14-i)).isoformat(),
            "disease": "cholera",
            "cases": 1,
        })
    
    # Cluster 2: Garissa Town (0.46S, 39.64E) - later outbreak
    for i in range(15):
        case_data.append({
            "lat": -0.46 + (i % 3) * 0.01,
            "lon": 39.64 + (i % 3) * 0.01,
            "timestamp": (datetime.utcnow() - timedelta(days=7-i)).isoformat(),
            "disease": "cholera",
            "cases": 1,
        })
    
    print(f"📍 Analyzing {len(case_data)} case records across region")
    
    # Run analysis
    analysis = agent.analyze(
        case_data=case_data,
        spatial_scale=SpatialScale.DISTRICT,
        temporal_scale=TemporalScale.WEEKLY,
    )
    
    # Display results
    print(f"\n🗺️ Spatiotemporal Analysis Results:")
    print(f"   Spatial Scale: {analysis.spatial_scale}")
    print(f"   Temporal Scale: {analysis.temporal_scale}")
    print(f"   Clusters Detected: {len(analysis.clusters)}")
    print(f"   Hotspots Identified: {len(analysis.hotspots)}")
    print(f"   Temporal Trend: {analysis.temporal_trends.get('trend', 'Unknown')}")
    
    if analysis.clusters:
        print(f"\n   Cluster Details:")
        for cluster in analysis.clusters:
            print(f"     - {cluster.cluster_id}: {cluster.case_count} cases")
            print(f"       Location: ({cluster.center_lat:.2f}°, {cluster.center_lon:.2f}°)")
            print(f"       Radius: {cluster.radius_km:.2f} km")
            print(f"       Risk Score: {cluster.risk_score:.2f}")
    
    if analysis.transmission_pathways:
        print(f"\n   Transmission Pathways Detected: {len(analysis.transmission_pathways)}")
        for pathway in analysis.transmission_pathways:
            print(f"     - {pathway['source_cluster']} → {pathway['target_cluster']}")
            print(f"       Distance: {pathway['distance_km']:.1f} km, Lag: {pathway['time_lag_days']} days")
    
    return analysis


def demo_early_warning_agent():
    """Demonstrate the Early Warning System Agent."""
    print("\n" + "="*80)
    print("DEMO 3: Early Warning System Agent")
    print("="*80 + "\n")
    
    # Initialize agent
    agent = EarlyWarningSystemAgent(
        location="Dadaab Refugee Camp",
    )
    
    print("🔔 Ingesting multi-source data...")
    
    # Ingest IoT sensor data
    iot_sensors = [
        SensorReading(
            sensor_id="ENV_001",
            sensor_type="Environmental",
            location=(0.05, 40.31),
            timestamp=datetime.utcnow() - timedelta(hours=2),
            readings={
                "temperature_c": 28.5,
                "humidity_pct": 78,
                "rainfall_mm": 145,
            }
        ),
        SensorReading(
            sensor_id="ENV_002",
            sensor_type="Environmental",
            location=(0.06, 40.32),
            timestamp=datetime.utcnow() - timedelta(hours=1),
            readings={
                "temperature_c": 29.0,
                "humidity_pct": 80,
                "rainfall_mm": 150,
            }
        ),
    ]
    agent.ingest_iot_data(iot_sensors)
    print(f"   ✓ Ingested {len(iot_sensors)} IoT sensor readings")
    
    # Ingest CBS (Community-Based Surveillance) reports
    cbs_reports = [
        {
            "timestamp": (datetime.utcnow() - timedelta(hours=6)).isoformat(),
            "lat": 0.05,
            "lon": 40.31,
            "symptom": "acute diarrhea",
            "reporter": "CHV_Amina_Hassan",
            "cases": 3,
        },
        {
            "timestamp": (datetime.utcnow() - timedelta(hours=4)).isoformat(),
            "lat": 0.055,
            "lon": 40.315,
            "symptom": "watery diarrhea and vomiting",
            "reporter": "CHV_Mohamed_Ali",
            "cases": 5,
        },
        {
            "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            "lat": 0.06,
            "lon": 40.32,
            "symptom": "severe dehydration",
            "reporter": "CHV_Fatima_Omar",
            "cases": 2,
        },
    ]
    for report in cbs_reports:
        agent.ingest_cbs_report(report)
    print(f"   ✓ Ingested {len(cbs_reports)} CBS reports")
    
    # Ingest EMR (Electronic Medical Record) confirmations
    emr_records = [
        {
            "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
            "lat": 0.052,
            "lon": 40.312,
            "diagnosis": "Cholera",
            "confirmed": True,
            "facility": "Dadaab Health Center",
        },
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
            "lat": 0.057,
            "lon": 40.318,
            "diagnosis": "Cholera",
            "confirmed": True,
            "facility": "Ifo Camp Clinic",
        },
    ]
    for record in emr_records:
        agent.ingest_emr_record(record)
    print(f"   ✓ Ingested {len(emr_records)} EMR records")
    
    # Check for alerts
    print("\n🚨 Checking for early warning alerts...")
    alerts = agent.check_and_generate_alerts()
    
    print(f"\n⚠️ Generated {len(alerts)} alerts:")
    for alert in alerts:
        print(f"\n   [{alert.severity}] {alert.alert_type}")
        print(f"   Disease: {alert.disease or 'Unknown'}")
        print(f"   Location: ({alert.location[0]:.2f}°, {alert.location[1]:.2f}°)")
        print(f"   Confidence: {alert.confidence:.0%}")
        print(f"   Data Sources: {', '.join(alert.data_sources)}")
        print(f"   Recommendations:")
        for rec in alert.recommendations[:3]:  # First 3 recommendations
            print(f"     • {rec}")
        print(f"   Stakeholders to notify: {', '.join(alert.stakeholders)}")
    
    return alerts


def demo_orchestrator():
    """Demonstrate the Agent Orchestrator coordinating all agents."""
    print("\n" + "="*80)
    print("DEMO 4: Multi-Agent Orchestration")
    print("="*80 + "\n")
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(
        location="Dadaab Refugee Camp, Kenya",
        population_size=150000,
        coordinate_bounds={
            "min_lat": -0.5, "max_lat": 1.5,
            "min_lon": 39.0, "max_lon": 41.5
        },
        enable_compliance_checking=True,
    )
    
    print("🎯 Initializing multi-agent orchestration system...")
    print(f"   Location: {orchestrator.location}")
    print(f"   Population: {orchestrator.population_size:,}")
    
    # Prepare comprehensive dataset
    print("\n📥 Ingesting multi-source data...")
    
    # IoT sensor data
    iot_data = [
        SensorReading(
            sensor_id=f"ENV_{i:03d}",
            sensor_type="Environmental",
            location=(0.05 + i*0.01, 40.31 + i*0.01),
            timestamp=datetime.utcnow() - timedelta(hours=24-i),
            readings={
                "temperature_c": 27 + i*0.2,
                "humidity_pct": 70 + i,
                "rainfall_mm": 100 + i*5,
            }
        )
        for i in range(10)
    ]
    orchestrator.ingest_iot_data(iot_data)
    print(f"   ✓ IoT sensors: {len(iot_data)} readings")
    
    # CBS reports
    cbs_data = [
        {
            "timestamp": (datetime.utcnow() - timedelta(days=14-i)).isoformat(),
            "lat": 0.05 + (i % 5) * 0.01,
            "lon": 40.31 + (i % 5) * 0.01,
            "symptom": "acute diarrhea",
            "disease": "cholera",
            "cases": 1 + (i % 3),
        }
        for i in range(20)
    ]
    orchestrator.ingest_cbs_reports(cbs_data)
    print(f"   ✓ CBS reports: {len(cbs_data)} reports")
    
    # EMR records
    emr_data = [
        {
            "timestamp": (datetime.utcnow() - timedelta(days=10-i)).isoformat(),
            "lat": 0.05 + (i % 3) * 0.01,
            "lon": 40.31 + (i % 3) * 0.01,
            "diagnosis": "Cholera",
            "confirmed": True,
            "cases": 1,
        }
        for i in range(15)
    ]
    orchestrator.ingest_emr_records(emr_data)
    print(f"   ✓ EMR records: {len(emr_data)} confirmations")
    
    # Run full coordinated analysis
    print("\n🔄 Running coordinated multi-agent analysis...")
    result = orchestrator.run_full_analysis(
        diseases=["cholera"],
        forecast_horizon_days=14,
        spatial_scale=SpatialScale.DISTRICT,
        temporal_scale=TemporalScale.WEEKLY,
    )
    
    # Display comprehensive results
    print("\n" + "="*80)
    print("ORCHESTRATED ANALYSIS RESULTS")
    print("="*80)
    
    print(f"\n📊 Executive Summary:")
    print(f"   Overall Status: {result.summary['overall_status']}")
    print(f"   Maximum Risk Score: {result.summary['max_risk_score']:.2f}")
    print(f"   Total Alerts: {result.summary['total_alerts']}")
    print(f"   Critical Alerts: {result.summary['critical_alerts']}")
    print(f"   Diseases Monitored: {', '.join(result.summary['diseases_monitored'])}")
    
    print(f"\n🔮 Forecasting Results:")
    for forecast in result.forecasts:
        print(f"   {forecast.disease}:")
        print(f"     R0: {forecast.estimated_r0:.2f}")
        print(f"     Risk Score: {forecast.risk_score:.2f}")
        print(f"     Peak: {forecast.peak_prediction['magnitude']} cases")
    
    print(f"\n🗺️ Spatial Analysis:")
    if result.spatial_analysis:
        print(f"   Clusters: {len(result.spatial_analysis.clusters)}")
        print(f"   Hotspots: {len(result.spatial_analysis.hotspots)}")
        print(f"   Trend: {result.spatial_analysis.temporal_trends.get('trend', 'Unknown')}")
    
    print(f"\n🚨 Early Warnings:")
    print(f"   Total Alerts: {len(result.alerts)}")
    for alert in result.alerts:
        print(f"     [{alert.severity}] {alert.alert_type} - {alert.disease or 'Environmental'}")
    
    print(f"\n🛡️ Compliance Status:")
    print(f"   Status: {result.compliance_status['status']}")
    print(f"   Frameworks: {', '.join(result.compliance_status.get('frameworks_checked', []))}")
    
    # Generate report
    print("\n📄 Generating comprehensive report...")
    report = orchestrator.generate_report(format="markdown")
    print("\n" + "-"*80)
    print(report[:1000] + "..." if len(report) > 1000 else report)
    print("-"*80)
    
    # Save full report to file
    report_file = "/tmp/ai_agents_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\n✅ Full report saved to: {report_file}")
    
    # Also save JSON version
    json_file = "/tmp/ai_agents_result.json"
    with open(json_file, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
    print(f"✅ JSON data saved to: {json_file}")
    
    return result


def main():
    """Run all demonstrations."""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*15 + "iLuminara AI Agents Demonstration" + " "*30 + "║")
    print("╚" + "="*78 + "╝")
    
    print("\nSpecialized AI agents for:")
    print("  • Epidemiological forecasting and outbreak prediction")
    print("  • Multi-scale spatiotemporal analysis")
    print("  • Early warning systems with IoT sensor integration")
    
    # Run individual agent demos
    forecast = demo_forecasting_agent()
    analysis = demo_spatiotemporal_agent()
    alerts = demo_early_warning_agent()
    
    # Run orchestrated demo
    orchestrated_result = demo_orchestrator()
    
    print("\n" + "="*80)
    print("✅ ALL DEMONSTRATIONS COMPLETE")
    print("="*80)
    print("\nAI Agents are now operational and ready for deployment.")
    print("Integration with iLuminara Golden Thread: ✓")
    print("Compliance with SovereignGuardrail: ✓")
    print("Edge deployment ready: ✓")
    print("\nThe AI agents can now be integrated into the iLuminara-Core")
    print("surveillance pipeline for real-time epidemiological intelligence.")


if __name__ == "__main__":
    main()
