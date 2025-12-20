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
# Cloud Oracle: Multi-scale Outbreak Forecasting

> **Predictive Analytics for Global Health Surveillance**

The Cloud Oracle module integrates iLuminara with Google Cloud Platform services to enable multi-scale outbreak forecasting, real-time data fusion, and predictive modeling across spatial hierarchies.

---

## 🎯 Overview

The Cloud Oracle provides three integrated capabilities:

1. **BigQuery Integration**: Historical outbreak data storage + real-time streaming
2. **Vertex AI Time Series**: Predictive modeling across spatial hierarchies  
3. **Dataflow Pipeline**: Real-time data fusion (community + environmental + clinical)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                         │
│  CBS Surveillance │ EMR Clinical │ Environmental Monitoring     │
│       (Pub/Sub)   │   (Pub/Sub)  │        (Pub/Sub)            │
└───────────────┬─────────────┬──────────────┬───────────────────┘
                │             │              │
                ▼             ▼              ▼
┌───────────────────────────────────────────────────────────────┐
│              DATAFLOW REAL-TIME FUSION                        │
│  • 5-minute windowing                                         │
│  • Cross-source validation                                    │
│  • Environmental risk integration                             │
│  • Alert generation                                           │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│                    BIGQUERY STORAGE                           │
│  • Time-partitioned tables                                    │
│  • H3 spatial clustering                                      │
│  • 730-day retention                                          │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│            VERTEX AI TIME-SERIES FORECASTING                  │
│  • Multi-scale predictions                                    │
│  • Community → District → Region → National                   │
│  • 72-hour forecast horizon                                   │
│  • 95% confidence intervals                                   │
└───────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Configuration

Set environment variables:

```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

Or configure in `config.py`:

```python
from cloud_oracle.config import get_config, validate_config

config = get_config()
if validate_config():
    print("✅ Configuration valid")
```

### 2. BigQuery Integration

Load historical outbreak data:

```python
from cloud_oracle.bigquery_integration import BigQueryIntegration

bq = BigQueryIntegration(
    project_id="my-project",
    dataset_id="outbreak_surveillance"
)

# Initialize schema
bq.initialize_schema()

# Batch load historical data
bq.batch_load_events(events)

# Stream real-time event
bq.stream_event({
    "event_id": "EVENT_001",
    "timestamp": "2025-12-19T10:00:00Z",
    "location": "Dadaab",
    "source": "CBS",
    "symptom_vector": {"fever": 0.8, "cough": 0.6}
})
```

### 3. Vertex AI Forecasting

Generate multi-scale forecasts:

```python
from cloud_oracle.vertex_ai_forecasting import (
    VertexAIForecasting,
    create_spatial_hierarchy_example
)

forecaster = VertexAIForecasting(
    project_id="my-project",
    location="us-central1"
)

# Create spatial hierarchy
hierarchy = create_spatial_hierarchy_example()

# Generate multi-scale forecast
forecast = forecaster.multi_scale_forecast(
    time_series_data=data_by_level,
    spatial_hierarchy=hierarchy,
    forecast_horizon=72
)
```

### 4. Dataflow Pipeline

Deploy real-time data fusion:

```python
from cloud_oracle.dataflow_pipeline import DataflowPipeline

pipeline = DataflowPipeline(
    project_id="my-project",
    region="us-central1"
)

# Create pipeline (requires apache-beam[gcp])
pipeline.create_pipeline()
```

---

## 📊 Features

### BigQuery Integration

- **Time-partitioned tables** for efficient queries
- **H3 spatial clustering** for geographic queries
- **Streaming ingestion** with <1 second latency
- **SQL-based analytics** for time-series aggregation
- **Multi-scale queries** across spatial hierarchies

### Vertex AI Forecasting

- **AutoML time-series** for outbreak trajectory prediction
- **Multi-scale forecasting** across spatial hierarchies:
  - Community level (camps, villages)
  - District level (administrative units)
  - Region level (provinces, states)
  - National level (countries)
- **Hierarchical consistency** via bottom-up aggregation
- **72-hour forecast horizon** with confidence intervals
- **Feature engineering** from surveillance + environmental data

### Dataflow Pipeline

- **Real-time fusion** of CBS, EMR, Environmental streams
- **5-minute windowing** for near-real-time processing
- **Cross-source validation** with fusion scoring
- **Environmental risk integration** (water, climate)
- **Automated alert generation** for high-risk events
- **BigQuery output** for downstream analytics

---

## 🔧 Requirements

### Python Packages

```bash
pip install google-cloud-bigquery
pip install google-cloud-aiplatform
pip install apache-beam[gcp]
pip install google-cloud-pubsub
```

### GCP Services

- **BigQuery**: Data warehouse for surveillance data
- **Vertex AI**: AutoML forecasting models
- **Dataflow**: Real-time streaming ETL
- **Pub/Sub**: Message ingestion
- **Cloud Storage**: Dataflow staging

---

## 📖 Modules

### `bigquery_integration.py`

BigQuery integration for historical and streaming data.

**Key Classes:**
- `BigQueryIntegration`: Main integration class
- `OutbreakEvent`: Data structure for events

**Key Methods:**
- `initialize_schema()`: Create tables
- `batch_load_events()`: Load historical data
- `stream_event()`: Stream real-time event
- `query_time_series()`: Query aggregated data
- `query_spatial_hierarchy()`: Spatial queries

### `vertex_ai_forecasting.py`

Vertex AI time-series forecasting across spatial scales.

**Key Classes:**
- `VertexAIForecasting`: Forecasting engine
- `SpatialHierarchy`: Spatial hierarchy definition
- `ForecastConfig`: Forecast configuration

**Key Methods:**
- `train_automl_forecasting_model()`: Train model
- `forecast_outbreak()`: Generate forecasts
- `multi_scale_forecast()`: Multi-level predictions
- `export_forecast_to_bigquery()`: Export results

### `dataflow_pipeline.py`

Real-time data fusion with Apache Beam / Dataflow.

**Key Classes:**
- `DataflowPipeline`: Pipeline orchestration
- `StreamingEvent`: Input event structure
- `FusedEvent`: Fused output structure

**Key Methods:**
- `create_pipeline()`: Build Dataflow pipeline
- `_fuse_events()`: Fusion logic
- `_enrich_fused_event()`: Add context
- `_trigger_alert()`: Alert generation

### `config.py`

Configuration management for GCP services.

**Key Functions:**
- `get_config()`: Get complete configuration
- `validate_config()`: Validate settings

**Configuration Sections:**
- `BIGQUERY_CONFIG`: BigQuery settings
- `VERTEX_AI_CONFIG`: Vertex AI settings
- `DATAFLOW_CONFIG`: Dataflow settings
- `SPATIAL_HIERARCHY_CONFIG`: Hierarchy definition
- `ALERT_CONFIG`: Alert thresholds
- `FEATURE_CONFIG`: Feature engineering

---

## 🎬 Demo

Run the comprehensive demo:

```bash
python cloud_oracle/forecasting_demo.py
```

This demonstrates:
1. BigQuery integration for data storage
2. Vertex AI multi-scale forecasting
3. Dataflow real-time fusion pipeline
4. End-to-end workflow

---

## 🌍 Use Cases

### Early Warning System

Forecast outbreak trajectories 72 hours in advance at community level:

```python
forecast = forecaster.forecast_outbreak(
    time_series_data=community_data,
    forecast_horizon=72,
    spatial_level="community"
)

if forecast['forecasts'][0]['values'][-1] > threshold:
    trigger_early_warning_alert()
```

### Resource Allocation

Predict district-level case loads for resource planning:

```python
district_forecast = forecaster.multi_scale_forecast(
    time_series_data=data_by_level,
    spatial_hierarchy=hierarchy,
    forecast_horizon=72
)

district_cases = district_forecast['forecasts_by_level']['district']
allocate_resources_by_forecast(district_cases)
```

### Real-time Monitoring

Fuse CBS, EMR, and environmental data streams:

```python
pipeline = DataflowPipeline(project_id=project_id)
pipeline.create_pipeline()  # Runs continuously

# Fused events written to BigQuery
# High-risk events trigger alerts
```

---

## 🔐 Security & Compliance

- **Data sovereignty**: BigQuery data remains in specified region
- **IAM authentication**: Service account-based access
- **Audit logging**: All operations logged to Cloud Audit Logs
- **Encryption**: Data encrypted at rest and in transit
- **HIPAA compliance**: Available with GCP HIPAA BAA

---

## 📈 Performance

- **Ingestion latency**: <1 second (streaming)
- **Fusion latency**: <5 minutes (Dataflow window)
- **Forecast generation**: ~10 minutes (AutoML inference)
- **Query latency**: <2 seconds (BigQuery time-series)
- **Scalability**: Auto-scales with Dataflow workers

---

## 🤝 Integration

### With Existing iLuminara Components

```python
# Use with Golden Thread data fusion
from edge_node.sync_protocol.golden_thread import GoldenThread
from cloud_oracle.bigquery_integration import BigQueryIntegration

gt = GoldenThread()
bq = BigQueryIntegration(project_id="my-project")

# Fuse local data
fused = gt.fuse_data_streams(cbs_signal, emr_record)

# Stream to BigQuery
bq.stream_event(fused.to_dict())
```

### With External Systems

- **DHIS2**: Export forecasts for government dashboards
- **OpenMRS**: Stream EMR records to Pub/Sub
- **Weather APIs**: Ingest environmental data
- **SMS Gateways**: Trigger alerts via Cloud Functions

---

## 📚 References

- [BigQuery Time Series](https://cloud.google.com/bigquery/docs/timeseries)
- [Vertex AI Forecasting](https://cloud.google.com/vertex-ai/docs/forecasting)
- [Dataflow Streaming](https://cloud.google.com/dataflow/docs/concepts/streaming-pipelines)
- [H3 Spatial Indexing](https://h3geo.org/)

---

## 📄 License

Part of iLuminara-Core © 2025 VISENDI56. All rights reserved.

---

**The Cloud Oracle: "Predict outbreaks before they become epidemics."**
