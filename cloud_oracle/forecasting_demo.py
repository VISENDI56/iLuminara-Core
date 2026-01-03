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
Multi-scale Outbreak Forecasting Demo
═════════════════════════════════════════════════════════════════════════════

Demonstrates the complete outbreak forecasting pipeline:
1. Load historical data to BigQuery
2. Stream real-time surveillance data
3. Generate multi-scale forecasts with Vertex AI
4. Visualize predictions across spatial hierarchy

This demo showcases iLuminara's predictive capabilities for early outbreak
detection and resource allocation.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any

# Add cloud_oracle to path
sys.path.insert(0, os.path.dirname(__file__))

from cloud_oracle.bigquery_integration import (
    BigQueryIntegration,
    load_simulated_data_to_bigquery
)
from cloud_oracle.vertex_ai_forecasting import (
    VertexAIForecasting,
    create_spatial_hierarchy_example
)
from cloud_oracle.dataflow_pipeline import (
    DataflowPipeline,
    create_pubsub_topics
)


def demo_bigquery_integration(project_id: str, credentials_path: str = None):
    """
    Demonstrate BigQuery integration for historical and streaming data.
    
    Args:
        project_id: GCP project ID
        credentials_path: Path to service account JSON
    """
    print("=" * 80)
    print("DEMO: BigQuery Integration")
    print("=" * 80)
    
    # Initialize BigQuery integration
    print("\n1️⃣  Initializing BigQuery Integration...")
    bq = BigQueryIntegration(
        project_id=project_id,
        dataset_id="outbreak_surveillance",
        credentials_path=credentials_path
    )
    
    # Initialize schema
    print("\n2️⃣  Creating BigQuery schema...")
    schema_info = bq.get_schema()
    print(f"   Schema fields: {len(schema_info)}")
    
    # Note: Actual table creation requires credentials
    print("\n   ⚠️  Note: Table creation requires valid GCP credentials")
    print("   To create table, set GCP_PROJECT_ID and run with credentials")
    
    # Demo: Batch load simulation data
    print("\n3️⃣  Demo batch load from simulated_outbreak.json...")
    simulation_file = os.path.join(
        os.path.dirname(__file__), 
        'simulated_outbreak.json'
    )
    
    if os.path.exists(simulation_file):
        with open(simulation_file, 'r') as f:
            data = json.load(f)
        
        events = data.get('events', [])
        print(f"   Found {len(events)} events to load")
        print(f"   Duration: {data['simulation_metadata']['duration_hours']} hours")
        print(f"   Location: {data['simulation_metadata']['location']}")
    else:
        print(f"   ⚠️  File not found: {simulation_file}")
        print("   Run: python edge_node/frenasa_engine/simulate_outbreak.py")
    
    # Demo: Time-series query
    print("\n4️⃣  Demo time-series query structure...")
    start_time = (datetime.utcnow() - timedelta(days=7)).isoformat()
    end_time = datetime.utcnow().isoformat()
    
    print(f"   Query window: {start_time} to {end_time}")
    print("   Aggregation: 1-hour windows")
    print("   Output: event_count, avg_z_score, confirmed_cases")
    
    # Demo: Spatial hierarchy query
    print("\n5️⃣  Demo spatial hierarchy query structure...")
    print("   Query: Aggregate by H3 hexagon")
    print("   Output: total_events, avg_z_score, critical_alerts")
    
    print("\n✅ BigQuery integration demo complete")


def demo_vertex_ai_forecasting(project_id: str, credentials_path: str = None):
    """
    Demonstrate Vertex AI time-series forecasting.
    
    Args:
        project_id: GCP project ID
        credentials_path: Path to service account JSON
    """
    print("\n" + "=" * 80)
    print("DEMO: Vertex AI Multi-scale Forecasting")
    print("=" * 80)
    
    # Initialize Vertex AI forecasting
    print("\n1️⃣  Initializing Vertex AI Forecasting...")
    forecaster = VertexAIForecasting(
        project_id=project_id,
        location="us-central1",
        credentials_path=credentials_path
    )
    
    print("   ⚠️  Note: Model training requires valid GCP credentials")
    
    # Demo: Spatial hierarchy
    print("\n2️⃣  Creating spatial hierarchy for Dadaab...")
    hierarchy = create_spatial_hierarchy_example()
    
    print(f"   Levels: {set(h.level for h in hierarchy)}")
    print(f"   Total locations: {len(hierarchy)}")
    
    for level in ["community", "district", "region", "national"]:
        level_nodes = [h for h in hierarchy if h.level == level]
        if level_nodes:
            total_pop = sum(h.population for h in level_nodes if h.population)
            print(f"   {level.capitalize()}: {len(level_nodes)} locations, pop={total_pop:,}")
    
    # Demo: Forecast configuration
    print("\n3️⃣  Forecast configuration...")
    forecast_config = {
        "forecast_horizon": 72,  # 72 hours (3 days)
        "confidence_level": 0.95,
        "spatial_level": "district",
        "features": [
            "event_count",
            "avg_z_score",
            "confirmed_cases",
            "cbs_signals",
            "emr_records"
        ],
        "target_column": "event_count"
    }
    
    print(f"   Forecast horizon: {forecast_config['forecast_horizon']} hours")
    print(f"   Confidence level: {forecast_config['confidence_level']}")
    print(f"   Spatial level: {forecast_config['spatial_level']}")
    print(f"   Features: {', '.join(forecast_config['features'])}")
    
    # Demo: Multi-scale forecasting structure
    print("\n4️⃣  Multi-scale forecasting structure...")
    print("   Community level → District level → Region level → National level")
    print("   Bottom-up aggregation ensures hierarchical consistency")
    
    # Demo: Sample forecast output
    print("\n5️⃣  Sample forecast output structure...")
    sample_forecast = {
        "status": "success",
        "forecast_horizon": 72,
        "spatial_levels": ["community", "district", "region"],
        "forecasts_by_level": {
            "community": {
                "ifo_camp": {
                    "forecast_values": [12, 15, 18, 22],  # Simulated
                    "lower_bound": [10, 12, 14, 17],
                    "upper_bound": [14, 18, 22, 27]
                }
            },
            "district": {
                "dadaab_district": {
                    "forecast_values": [45, 55, 68, 82],
                    "aggregated_from": ["ifo_camp", "hagadera_camp", "dagahaley_camp", "kambios"]
                }
            }
        }
    }
    
    print(f"   Sample community forecast: {sample_forecast['forecasts_by_level']['community']['ifo_camp']['forecast_values']}")
    print(f"   Sample district forecast: {sample_forecast['forecasts_by_level']['district']['dadaab_district']['forecast_values']}")
    
    print("\n✅ Vertex AI forecasting demo complete")


def demo_dataflow_pipeline(project_id: str):
    """
    Demonstrate Dataflow real-time data fusion pipeline.
    
    Args:
        project_id: GCP project ID
    """
    print("\n" + "=" * 80)
    print("DEMO: Dataflow Real-time Data Fusion")
    print("=" * 80)
    
    # Initialize Dataflow pipeline
    print("\n1️⃣  Initializing Dataflow Pipeline...")
    pipeline = DataflowPipeline(
        project_id=project_id,
        region="us-central1"
    )
    
    print(f"   Project: {pipeline.project_id}")
    print(f"   Region: {pipeline.region}")
    
    # Demo: Pub/Sub topics
    print("\n2️⃣  Pub/Sub topics for data ingestion...")
    print(f"   CBS Surveillance: {pipeline.cbs_topic}")
    print(f"   EMR Clinical: {pipeline.emr_topic}")
    print(f"   Environmental: {pipeline.environmental_topic}")
    
    # Demo: Pipeline stages
    print("\n3️⃣  Pipeline stages...")
    stages = [
        "1. Ingest: Read from Pub/Sub topics",
        "2. Window: Group events by 5-minute windows",
        "3. Fuse: Combine CBS + EMR + Environmental data",
        "4. Enrich: Add spatial/temporal context",
        "5. Output: Write to BigQuery & trigger alerts"
    ]
    
    for stage in stages:
        print(f"   {stage}")
    
    # Demo: Fusion logic
    print("\n4️⃣  Fusion logic example...")
    print("   Input: CBS signal (watery stool) + EMR record (cholera diagnosis)")
    print("   Fusion score calculation:")
    print("   - All 3 sources present: 1.0")
    print("   - 2 sources present: 0.8")
    print("   - 1 source present: 0.5")
    print("   - Bonus for lab confirmation: +0.2")
    print("   - Bonus for location agreement: +0.1")
    
    # Demo: Alert levels
    print("\n5️⃣  Alert level determination...")
    alert_logic = {
        "CRITICAL": "Lab-confirmed + high environmental risk",
        "ALERT": "Clinical diagnosis or multiple CBS signals",
        "WATCH": "Single CBS signal",
        "GREEN": "Normal surveillance"
    }
    
    for level, condition in alert_logic.items():
        print(f"   {level}: {condition}")
    
    # Demo: Output schema
    print("\n6️⃣  BigQuery output schema...")
    output_fields = [
        "fusion_id", "timestamp", "location", "h3_index",
        "fusion_score", "alert_level",
        "cbs_present", "emr_present", "environmental_present",
        "cbs_symptom", "emr_diagnosis", "lab_confirmed",
        "water_quality_index", "temperature_celsius", "rainfall_mm"
    ]
    
    print(f"   Output fields: {', '.join(output_fields)}")
    
    print("\n✅ Dataflow pipeline demo complete")


def demo_end_to_end_workflow(project_id: str, credentials_path: str = None):
    """
    Demonstrate complete end-to-end forecasting workflow.
    
    Args:
        project_id: GCP project ID
        credentials_path: Path to service account JSON
    """
    print("\n" + "=" * 80)
    print("DEMO: End-to-End Outbreak Forecasting Workflow")
    print("=" * 80)
    
    print("\n📊 WORKFLOW STAGES:")
    
    stages = [
        {
            "number": "1️⃣",
            "stage": "Data Ingestion",
            "description": "Stream CBS, EMR, Environmental data via Pub/Sub",
            "output": "Real-time events in Pub/Sub topics"
        },
        {
            "number": "2️⃣",
            "stage": "Data Fusion",
            "description": "Dataflow pipeline fuses multi-source data",
            "output": "Fused events with fusion scores"
        },
        {
            "number": "3️⃣",
            "stage": "Historical Storage",
            "description": "BigQuery stores fused events with time partitioning",
            "output": "Queryable time-series database"
        },
        {
            "number": "4️⃣",
            "stage": "Feature Engineering",
            "description": "Extract time-series features by spatial hierarchy",
            "output": "Training dataset for forecasting"
        },
        {
            "number": "5️⃣",
            "stage": "Model Training",
            "description": "Vertex AI AutoML trains forecasting models",
            "output": "Deployed forecasting endpoint"
        },
        {
            "number": "6️⃣",
            "stage": "Multi-scale Forecasting",
            "description": "Generate predictions across spatial hierarchy",
            "output": "Community → District → National forecasts"
        },
        {
            "number": "7️⃣",
            "stage": "Alert Generation",
            "description": "Trigger alerts for high-risk predictions",
            "output": "Real-time notifications to stakeholders"
        }
    ]
    
    for stage in stages:
        print(f"\n{stage['number']} {stage['stage']}")
        print(f"   Description: {stage['description']}")
        print(f"   Output: {stage['output']}")
    
    print("\n" + "=" * 80)
    print("🎯 KEY CAPABILITIES:")
    print("=" * 80)
    
    capabilities = [
        "✅ Real-time data fusion with <1 minute latency",
        "✅ Multi-scale forecasting (community → national)",
        "✅ Hierarchical consistency via bottom-up aggregation",
        "✅ 72-hour outbreak trajectory prediction",
        "✅ Automated alert generation for high-risk events",
        "✅ Environmental risk factor integration",
        "✅ Cross-validation across CBS, EMR, Environmental data"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print("\n✅ End-to-end workflow demo complete")


def main():
    """Run all demos."""
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 10 + "iLuminara Multi-scale Outbreak Forecasting Demo" + " " * 20 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Get configuration from environment
    project_id = os.getenv('GCP_PROJECT_ID', 'iluminara-demo')
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    print(f"\n📋 Configuration:")
    print(f"   GCP Project: {project_id}")
    print(f"   Credentials: {'Configured' if credentials_path else 'Using default ADC'}")
    
    print("\n⚠️  Note: This demo shows the structure and capabilities.")
    print("   To run with actual GCP services, set GCP_PROJECT_ID and credentials.")
    
    # Run demos
    try:
        demo_bigquery_integration(project_id, credentials_path)
        demo_vertex_ai_forecasting(project_id, credentials_path)
        demo_dataflow_pipeline(project_id)
        demo_end_to_end_workflow(project_id, credentials_path)
        
        print("\n" + "=" * 80)
        print("🎉 ALL DEMOS COMPLETE")
        print("=" * 80)
        
        print("\n📚 Next Steps:")
        print("   1. Set GCP_PROJECT_ID environment variable")
        print("   2. Set GOOGLE_APPLICATION_CREDENTIALS to service account JSON")
        print("   3. Run with actual GCP services for live deployment")
        print("   4. View forecasts in BigQuery or custom dashboard")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("   This is expected without valid GCP credentials")


if __name__ == "__main__":
    main()
