# Cloud Oracle: Spatiotemporal Forecasting

The Cloud Oracle module provides hierarchical spatiotemporal modeling capabilities for epidemic prediction, leveraging Google Cloud BigQuery and Vertex AI.

## Overview

The `spatiotemporal_model` module enables multi-scale epidemic forecasting by fusing:
- **Community-based surveillance (CBS)** - Population-level symptom reports
- **Electronic medical records (EMR)** - Clinical diagnosis and patient data
- **Environmental sensors (IoT)** - Water quality, temperature, and other environmental factors

## Key Features

- **Multi-scale data fusion** - Spatial joins (ST_DWithin) combine data sources within configurable geographic radius
- **Hierarchical forecasting** - Predictions across geographic hierarchies (e.g., district → region → country)
- **Time series modeling** - Vertex AI integration for advanced temporal pattern recognition
- **Deployment ready** - One-command deployment to prediction endpoints

## Quick Start

### 1. Basic Usage

```python
from cloud_oracle.spatiotemporal_model import (
    HierarchicalSpatiotemporalModel,
    MultiScaleDataset,
    ForecastConfig
)

# Configure data sources
config = MultiScaleDataset(
    community_symptoms_table="project.dataset.community_symptoms",
    emr_data_table="project.dataset.emr_data",
    iot_sensors_table="project.dataset.iot_sensors",
    project_id="your-project-id"
)

# Initialize model
model = HierarchicalSpatiotemporalModel(config)

# Create dataset, train, and deploy
dataset = model.create_multiscale_dataset()
forecaster = model.train_forecaster(dataset)
endpoint = model.deploy_forecaster(forecaster, "hstpu-forecaster")
```

### 2. Using the Convenience Function

```python
from cloud_oracle.spatiotemporal_model import create_spatiotemporal_pipeline

model = create_spatiotemporal_pipeline(
    community_table="project.dataset.community_symptoms",
    emr_table="project.dataset.emr_data",
    iot_table="project.dataset.iot_sensors"
)
```

## Configuration

### MultiScaleDataset

Defines the data sources for multi-scale fusion:

```python
config = MultiScaleDataset(
    community_symptoms_table="project.dataset.community_symptoms",  # Required
    emr_data_table="project.dataset.emr_data",                      # Required
    iot_sensors_table="project.dataset.iot_sensors",                # Required
    project_id="your-project-id",                                    # Optional
    dataset_id="your-dataset-id"                                     # Optional
)
```

### ForecastConfig

Customizes forecasting parameters:

```python
config = ForecastConfig(
    target_column="case_count",              # Variable to forecast
    time_column="timestamp",                 # Temporal index
    hierarchical_columns=["location"],       # Geographic hierarchy
    spatial_radius_meters=800.0,             # Spatial join radius
    forecast_horizon=14                      # Days to forecast ahead
)
```

## SQL Query Structure

The model automatically generates a BigQuery query that:

1. **Spatial Joins**: Uses `ST_DWithin(geography1, geography2, radius)` to correlate environmental sensors with community reports
2. **Temporal Alignment**: Joins clinical records on matching dates
3. **Aggregation**: Counts distinct patient cases by location and time

Example generated query:

```sql
WITH community AS (SELECT * FROM `community_symptoms`),
     clinical AS (SELECT * FROM `emr_data`),
     environmental AS (SELECT * FROM `iot_sensors`)
SELECT 
  c.timestamp,
  c.location,
  c.symptoms,
  e.water_quality,
  e.temperature,
  COUNT(DISTINCT p.patient_id) as case_count
FROM community c
LEFT JOIN environmental e ON ST_DWithin(c.geography, e.geography, 800)
LEFT JOIN clinical p ON DATE(p.onset_time) = DATE(c.timestamp)
GROUP BY 1,2,3,4,5
```

## Data Schema Requirements

### community_symptoms table
- `timestamp` (TIMESTAMP) - When symptom was reported
- `location` (STRING) - Geographic location identifier
- `geography` (GEOGRAPHY) - Geospatial point for spatial joins
- `symptoms` (STRING) - Reported symptoms

### emr_data table
- `patient_id` (STRING) - Unique patient identifier
- `onset_time` (TIMESTAMP) - When symptoms began
- Additional clinical fields as needed

### iot_sensors table
- `geography` (GEOGRAPHY) - Sensor location
- `water_quality` (FLOAT) - Water quality measurements
- `temperature` (FLOAT) - Temperature readings
- Additional environmental fields as needed

## Prerequisites

### Google Cloud Setup

1. **Enable APIs**:
   ```bash
   gcloud services enable bigquery.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   ```

2. **Authentication**:
   ```bash
   gcloud auth application-default login
   ```

3. **Install Dependencies**:
   ```bash
   pip install google-cloud-bigquery
   pip install google-cloud-aiplatform
   ```

### IAM Permissions

Required roles:
- `roles/bigquery.dataViewer` - Read BigQuery tables
- `roles/bigquery.jobUser` - Execute queries
- `roles/aiplatform.user` - Train and deploy models

## API Reference

### HierarchicalSpatiotemporalModel

Main class for spatiotemporal forecasting.

#### Methods

- **`create_multiscale_dataset() -> DataFrame`**
  - Executes BigQuery fusion query
  - Returns pandas DataFrame with combined data

- **`train_forecaster(dataset) -> Forecaster`**
  - Trains hierarchical time series model
  - Returns trained Vertex AI forecaster

- **`deploy_forecaster(forecaster, endpoint_name) -> Endpoint`**
  - Deploys model to prediction endpoint
  - Returns deployment endpoint

- **`predict(input_data, endpoint_name=None) -> Dict`**
  - Generates predictions from deployed model
  - Returns predictions with metadata

- **`get_model_info() -> Dict`**
  - Returns model configuration and status

### Exceptions

- **`SpatiotemporalModelError`**
  - Raised for model operation failures
  - Includes detailed error messages

## Examples

See `cloud_oracle/example_spatiotemporal_usage.py` for a complete working example.

## Compliance & Data Sovereignty

The Cloud Oracle respects data sovereignty constraints:

- Uses cloud services only when explicitly configured
- Falls back gracefully when GCP libraries unavailable
- Supports local/edge deployment through governance kernel integration
- All predictions auditable through iLuminara-Core's governance layer

## Integration with iLuminara-Core

The spatiotemporal model integrates with:

- **Governance Kernel** - Respects data sovereignty rules
- **Golden Thread** - Can consume fused EMR/CBS/IDSR data
- **Edge Nodes** - Provides predictions for local decision-making

## Troubleshooting

### "google-cloud-bigquery not available"
Install with: `pip install google-cloud-bigquery`

### "vertexai not available"
Install with: `pip install google-cloud-aiplatform`

### Authentication errors
Run: `gcloud auth application-default login`

### Table not found
Verify table paths use format: `project.dataset.table`

## License

Part of iLuminara-Core. VISENDI56 © 2025. All rights reserved.
