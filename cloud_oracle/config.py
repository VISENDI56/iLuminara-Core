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
Configuration for Multi-scale Outbreak Forecasting
═════════════════════════════════════════════════════════════════════════════

GCP service configuration for BigQuery, Vertex AI, and Dataflow integration.
"""

import os
from typing import Dict, Any

# ═════════════════════════════════════════════════════════════════════════════
# GCP Project Configuration
# ═════════════════════════════════════════════════════════════════════════════

# GCP Project ID (override via environment variable)
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'iluminara-outbreak-forecasting')

# GCP Region for services
GCP_REGION = os.getenv('GCP_REGION', 'us-central1')

# Service Account Credentials Path
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


# ═════════════════════════════════════════════════════════════════════════════
# BigQuery Configuration
# ═════════════════════════════════════════════════════════════════════════════

BIGQUERY_CONFIG = {
    'project_id': GCP_PROJECT_ID,
    'dataset_id': 'outbreak_surveillance',
    'table_id': 'surveillance_events',
    'location': 'US',
    'credentials_path': GOOGLE_APPLICATION_CREDENTIALS,
    
    # Time partitioning
    'partition_field': 'timestamp',
    'partition_type': 'DAY',
    
    # Clustering for query optimization
    'clustering_fields': ['location', 'h3_index', 'source'],
    
    # Data retention (days)
    'retention_days': 730,  # 2 years
}


# ═════════════════════════════════════════════════════════════════════════════
# Vertex AI Configuration
# ═════════════════════════════════════════════════════════════════════════════

VERTEX_AI_CONFIG = {
    'project_id': GCP_PROJECT_ID,
    'location': GCP_REGION,
    'credentials_path': GOOGLE_APPLICATION_CREDENTIALS,
    
    # Training configuration
    'training_budget_hours': 3,
    'optimization_objective': 'minimize-rmse',
    
    # Forecasting parameters
    'forecast_horizon': 72,  # hours
    'context_window': 168,  # 7 days
    'confidence_level': 0.95,
    
    # Model configuration
    'model_display_name_prefix': 'outbreak_forecast',
    'dataset_display_name_prefix': 'outbreak_timeseries',
    
    # Target column
    'target_column': 'event_count',
    'time_column': 'timestamp',
    'time_series_identifier_column': 'location',
}


# ═════════════════════════════════════════════════════════════════════════════
# Dataflow Configuration
# ═════════════════════════════════════════════════════════════════════════════

DATAFLOW_CONFIG = {
    'project_id': GCP_PROJECT_ID,
    'region': GCP_REGION,
    
    # GCS paths
    'temp_location': f'gs://{GCP_PROJECT_ID}-dataflow/temp',
    'staging_location': f'gs://{GCP_PROJECT_ID}-dataflow/staging',
    
    # Pub/Sub topics
    'cbs_topic': f'projects/{GCP_PROJECT_ID}/topics/cbs-surveillance',
    'emr_topic': f'projects/{GCP_PROJECT_ID}/topics/emr-clinical',
    'environmental_topic': f'projects/{GCP_PROJECT_ID}/topics/environmental-monitoring',
    'alerts_topic': f'projects/{GCP_PROJECT_ID}/topics/outbreak-alerts',
    
    # Windowing configuration
    'window_size_seconds': 300,  # 5 minutes
    'allowed_lateness_seconds': 60,  # 1 minute
    
    # Output configuration
    'output_table': f'{GCP_PROJECT_ID}:outbreak_surveillance.fused_events',
    
    # Worker configuration
    'max_num_workers': 10,
    'machine_type': 'n1-standard-2',
    'disk_size_gb': 50,
}


# ═════════════════════════════════════════════════════════════════════════════
# Spatial Hierarchy Configuration
# ═════════════════════════════════════════════════════════════════════════════

SPATIAL_HIERARCHY_CONFIG = {
    # H3 resolution levels for different scales
    'community_resolution': 9,  # ~0.1 km²
    'district_resolution': 7,   # ~5 km²
    'region_resolution': 5,     # ~250 km²
    'national_resolution': 3,   # ~12,000 km²
    
    # Hierarchy levels
    'hierarchy_levels': [
        'community',
        'district',
        'region',
        'national'
    ],
    
    # Location metadata
    'locations': {
        'dadaab': {
            'zones': [
                'Ifo Camp',
                'Hagadera Camp',
                'Dagahaley Camp',
                'Kambios'
            ],
            'district': 'Dadaab District',
            'region': 'Garissa Region',
            'country': 'Kenya'
        }
    }
}


# ═════════════════════════════════════════════════════════════════════════════
# Alert Configuration
# ═════════════════════════════════════════════════════════════════════════════

ALERT_CONFIG = {
    # Z-score thresholds for alert levels
    'thresholds': {
        'GREEN': 0.0,
        'YELLOW': 1.0,
        'ORANGE': 2.576,  # 99% confidence
        'RED': 4.2,       # Parametric bond trigger
        'CRITICAL': 5.0
    },
    
    # Fusion score thresholds
    'fusion_score_minimum': 0.7,  # Minimum score for high confidence
    
    # Alert notification targets
    'notification_endpoints': {
        'email': os.getenv('ALERT_EMAIL'),
        'sms': os.getenv('ALERT_SMS'),
        'webhook': os.getenv('ALERT_WEBHOOK')
    }
}


# ═════════════════════════════════════════════════════════════════════════════
# Feature Engineering Configuration
# ═════════════════════════════════════════════════════════════════════════════

FEATURE_CONFIG = {
    # Time-based features
    'temporal_features': [
        'hour_of_day',
        'day_of_week',
        'week_of_year',
        'is_weekend',
        'is_holiday'
    ],
    
    # Spatial features
    'spatial_features': [
        'h3_index',
        'population_density',
        'distance_to_water_source',
        'elevation'
    ],
    
    # Surveillance features
    'surveillance_features': [
        'event_count',
        'avg_z_score',
        'confirmed_cases',
        'cbs_signals',
        'emr_records',
        'lab_confirmed_ratio'
    ],
    
    # Environmental features
    'environmental_features': [
        'water_quality_index',
        'temperature_celsius',
        'rainfall_mm',
        'humidity_percent',
        'air_quality_index'
    ],
    
    # Lag features (historical context)
    'lag_periods': [1, 6, 12, 24, 48, 72, 168],  # hours
}


# ═════════════════════════════════════════════════════════════════════════════
# Export Configuration
# ═════════════════════════════════════════════════════════════════════════════

def get_config() -> Dict[str, Any]:
    """
    Get complete configuration dictionary.
    
    Returns:
        Dictionary containing all configuration sections
    """
    return {
        'gcp_project_id': GCP_PROJECT_ID,
        'gcp_region': GCP_REGION,
        'bigquery': BIGQUERY_CONFIG,
        'vertex_ai': VERTEX_AI_CONFIG,
        'dataflow': DATAFLOW_CONFIG,
        'spatial_hierarchy': SPATIAL_HIERARCHY_CONFIG,
        'alerts': ALERT_CONFIG,
        'features': FEATURE_CONFIG
    }


def validate_config() -> bool:
    """
    Validate configuration settings.
    
    Returns:
        True if configuration is valid
    """
    required_settings = [
        ('GCP_PROJECT_ID', GCP_PROJECT_ID),
        ('GCP_REGION', GCP_REGION),
    ]
    
    missing = []
    for name, value in required_settings:
        if not value or value.startswith('iluminara-'):
            missing.append(name)
    
    if missing:
        print(f"⚠️  Configuration incomplete: {', '.join(missing)}")
        print("   Set environment variables or update config.py")
        return False
    
    return True


# ═════════════════════════════════════════════════════════════════════════════
# Configuration Notes:
#
# Environment Variables:
#   GCP_PROJECT_ID              - GCP project identifier
#   GCP_REGION                  - GCP region (e.g., us-central1)
#   GOOGLE_APPLICATION_CREDENTIALS - Path to service account JSON
#   ALERT_EMAIL                 - Email for alert notifications
#   ALERT_SMS                   - Phone number for SMS alerts
#   ALERT_WEBHOOK               - Webhook URL for alert integration
#
# To use:
#   from cloud_oracle.config import get_config, validate_config
#   config = get_config()
#   if validate_config():
#       # proceed with GCP services
# ═════════════════════════════════════════════════════════════════════════════
