#!/usr/bin/env python3
"""
Problem Statement Implementation
═════════════════════════════════════════════════════════════════════════════

This script demonstrates the EXACT implementation pattern from the problem
statement, showing how the hierarchical spatiotemporal model is used.

This matches the code structure from the issue requirements.
"""

# Building hierarchical spatiotemporal model
from google.cloud import bigquery
from vertexai import time_series

# 1. Create multi-scale dataset
client = bigquery.Client()
query = """
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
"""

# 2. Train time series model
dataset = client.query(query).to_dataframe()
model = time_series.TimeSeriesDataset(dataset)
forecaster = model.train(
    target_column="case_count",
    time_column="timestamp",
    hierarchical_columns=["location"]
)

# 3. Deploy predictive endpoint
forecaster.deploy(endpoint_name="hstpu-forecaster")
