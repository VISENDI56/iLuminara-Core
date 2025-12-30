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
BigQuery Integration: Historical Outbreak Data Storage & Real-time Streaming
═════════════════════════════════════════════════════════════════════════════

Provides integration with Google BigQuery for:
1. Historical outbreak data storage and querying
2. Real-time streaming ingestion of surveillance data
3. Time-series aggregation for predictive modeling

This module enables iLuminara to leverage BigQuery for large-scale
health surveillance data analytics and forecasting.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import json


@dataclass
class OutbreakEvent:
    """Structured outbreak event for BigQuery ingestion."""
    event_id: str
    timestamp: str
    location: str
    h3_index: str
    source: str  # EMR, CBS, IDSR
    age_group: str
    symptom_vector: Dict[str, float]
    z_score_component: float
    diagnosis: Optional[str] = None
    lab_confirmed: Optional[bool] = None
    alert_level: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None


class BigQueryIntegration:
    """
    Integration layer for Google BigQuery.
    
    Provides methods for:
    - Schema definition for outbreak surveillance data
    - Batch loading historical data
    - Streaming real-time surveillance signals
    - Querying aggregated time-series data
    
    Usage:
        bq = BigQueryIntegration(project_id='my-project', dataset_id='outbreak_surveillance')
        bq.initialize_schema()
        bq.stream_event(event_data)
    """
    
    def __init__(
        self, 
        project_id: str,
        dataset_id: str = "outbreak_surveillance",
        table_id: str = "surveillance_events",
        credentials_path: Optional[str] = None
    ):
        """
        Initialize BigQuery integration.
        
        Args:
            project_id: GCP project ID
            dataset_id: BigQuery dataset name
            table_id: BigQuery table name for surveillance events
            credentials_path: Path to GCP service account JSON (optional)
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.credentials_path = credentials_path
        
        # Full table reference
        self.table_ref = f"{project_id}.{dataset_id}.{table_id}"
        
        # Connection placeholder (will be initialized when client is available)
        self._client = None
        
    def get_schema(self) -> List[Dict[str, Any]]:
        """
        Define BigQuery schema for outbreak surveillance data.
        
        Returns:
            Schema definition compatible with BigQuery SchemaField format
        """
        schema = [
            {"name": "event_id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
            {"name": "location", "type": "STRING", "mode": "REQUIRED"},
            {"name": "h3_index", "type": "STRING", "mode": "REQUIRED"},
            {"name": "source", "type": "STRING", "mode": "REQUIRED"},
            {"name": "age_group", "type": "STRING", "mode": "NULLABLE"},
            {"name": "symptom_vector", "type": "JSON", "mode": "NULLABLE"},
            {"name": "z_score_component", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "diagnosis", "type": "STRING", "mode": "NULLABLE"},
            {"name": "lab_confirmed", "type": "BOOLEAN", "mode": "NULLABLE"},
            {"name": "alert_level", "type": "STRING", "mode": "NULLABLE"},
            {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "population", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "ingestion_time", "type": "TIMESTAMP", "mode": "REQUIRED"},
        ]
        return schema
    
    def initialize_client(self):
        """
        Initialize BigQuery client.
        
        Note: This requires google-cloud-bigquery to be installed.
        Wraps import to allow module to be imported without the dependency.
        """
        try:
            from google.cloud import bigquery
            from google.oauth2 import service_account
            
            if self.credentials_path:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self._client = bigquery.Client(
                    project=self.project_id,
                    credentials=credentials
                )
            else:
                # Use default credentials (Application Default Credentials)
                self._client = bigquery.Client(project=self.project_id)
                
            return self._client
        except ImportError:
            raise ImportError(
                "google-cloud-bigquery not installed. "
                "Install with: pip install google-cloud-bigquery"
            )
    
    def initialize_schema(self):
        """
        Create BigQuery dataset and table if they don't exist.
        
        Returns:
            Dict with creation status
        """
        if not self._client:
            self.initialize_client()
        
        # Import within method to avoid dependency issues
        from google.cloud import bigquery
        
        # Create dataset if doesn't exist
        dataset = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
        dataset.location = "US"
        
        try:
            dataset = self._client.create_dataset(dataset, exists_ok=True)
            print(f"✅ Dataset {self.dataset_id} ready")
        except Exception as e:
            print(f"⚠️  Dataset creation: {e}")
        
        # Create table with schema
        schema_fields = [
            bigquery.SchemaField(
                field["name"], 
                field["type"], 
                mode=field["mode"]
            )
            for field in self.get_schema()
        ]
        
        table = bigquery.Table(self.table_ref, schema=schema_fields)
        
        # Enable time-based partitioning on timestamp
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="timestamp"
        )
        
        try:
            table = self._client.create_table(table, exists_ok=True)
            print(f"✅ Table {self.table_id} ready")
            return {"status": "success", "table": self.table_ref}
        except Exception as e:
            print(f"❌ Table creation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def batch_load_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Batch load historical outbreak events to BigQuery.
        
        Args:
            events: List of outbreak event dictionaries
            
        Returns:
            Load job status
        """
        if not self._client:
            self.initialize_client()
        
        # Add ingestion timestamp to each event
        for event in events:
            event["ingestion_time"] = datetime.utcnow().isoformat()
        
        # Import within method
        from google.cloud import bigquery
        
        job_config = bigquery.LoadJobConfig(
            schema=None,  # Auto-detect from data
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        
        try:
            job = self._client.load_table_from_json(
                events, 
                self.table_ref, 
                job_config=job_config
            )
            job.result()  # Wait for completion
            
            print(f"✅ Loaded {len(events)} events to BigQuery")
            return {
                "status": "success",
                "events_loaded": len(events),
                "table": self.table_ref
            }
        except Exception as e:
            print(f"❌ Batch load failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def stream_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stream a single real-time surveillance event to BigQuery.
        
        Args:
            event: Outbreak event data
            
        Returns:
            Streaming insert status
        """
        if not self._client:
            self.initialize_client()
        
        # Add ingestion timestamp
        event["ingestion_time"] = datetime.utcnow().isoformat()
        
        try:
            errors = self._client.insert_rows_json(
                self.table_ref, 
                [event]
            )
            
            if errors:
                print(f"❌ Streaming insert errors: {errors}")
                return {"status": "error", "errors": errors}
            else:
                return {
                    "status": "success",
                    "event_id": event.get("event_id"),
                    "table": self.table_ref
                }
        except Exception as e:
            print(f"❌ Stream event failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def stream_events_batch(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Stream multiple real-time events in a batch for efficiency.
        
        Args:
            events: List of outbreak event data
            
        Returns:
            Batch streaming insert status
        """
        if not self._client:
            self.initialize_client()
        
        # Add ingestion timestamps
        for event in events:
            event["ingestion_time"] = datetime.utcnow().isoformat()
        
        try:
            errors = self._client.insert_rows_json(
                self.table_ref, 
                events
            )
            
            if errors:
                print(f"⚠️  Some streaming inserts failed: {errors}")
                return {
                    "status": "partial_success",
                    "errors": errors,
                    "events_attempted": len(events)
                }
            else:
                return {
                    "status": "success",
                    "events_streamed": len(events),
                    "table": self.table_ref
                }
        except Exception as e:
            print(f"❌ Batch stream failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def query_time_series(
        self, 
        start_time: str,
        end_time: str,
        location: Optional[str] = None,
        aggregation_window: str = "1 HOUR"
    ) -> List[Dict[str, Any]]:
        """
        Query aggregated time-series data for forecasting.
        
        Args:
            start_time: Start timestamp (ISO format)
            end_time: End timestamp (ISO format)
            location: Optional location filter
            aggregation_window: Time window for aggregation (e.g., "1 HOUR", "1 DAY")
            
        Returns:
            List of aggregated time-series records
        """
        if not self._client:
            self.initialize_client()
        
        location_filter = f"AND location = '{location}'" if location else ""
        
        query = f"""
        SELECT
            TIMESTAMP_TRUNC(timestamp, HOUR) AS time_window,
            location,
            h3_index,
            COUNT(*) AS event_count,
            AVG(z_score_component) AS avg_z_score,
            COUNTIF(lab_confirmed = TRUE) AS confirmed_cases,
            COUNTIF(source = 'CBS') AS cbs_signals,
            COUNTIF(source = 'EMR') AS emr_records,
            ARRAY_AGG(DISTINCT age_group IGNORE NULLS) AS age_groups_affected
        FROM `{self.table_ref}`
        WHERE timestamp BETWEEN TIMESTAMP('{start_time}') AND TIMESTAMP('{end_time}')
        {location_filter}
        GROUP BY time_window, location, h3_index
        ORDER BY time_window ASC
        """
        
        try:
            query_job = self._client.query(query)
            results = query_job.result()
            
            # Convert to list of dictionaries
            time_series_data = []
            for row in results:
                time_series_data.append({
                    "time_window": row.time_window.isoformat(),
                    "location": row.location,
                    "h3_index": row.h3_index,
                    "event_count": row.event_count,
                    "avg_z_score": float(row.avg_z_score) if row.avg_z_score else 0.0,
                    "confirmed_cases": row.confirmed_cases,
                    "cbs_signals": row.cbs_signals,
                    "emr_records": row.emr_records,
                    "age_groups_affected": row.age_groups_affected,
                })
            
            print(f"✅ Retrieved {len(time_series_data)} time-series records")
            return time_series_data
            
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return []
    
    def query_spatial_hierarchy(
        self,
        timestamp: str,
        h3_resolution: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query data aggregated by spatial hierarchy (H3 hexagon grid).
        
        Enables multi-scale forecasting across spatial scales.
        
        Args:
            timestamp: Timestamp for spatial snapshot
            h3_resolution: H3 resolution level (0-15, lower = larger hexagons)
            
        Returns:
            List of spatial aggregates by H3 cell
        """
        if not self._client:
            self.initialize_client()
        
        query = f"""
        SELECT
            h3_index,
            location,
            COUNT(*) AS total_events,
            AVG(z_score_component) AS avg_z_score,
            MAX(z_score_component) AS max_z_score,
            COUNTIF(lab_confirmed = TRUE) AS confirmed_cases,
            COUNTIF(alert_level = 'CRITICAL') AS critical_alerts,
            AVG(latitude) AS centroid_lat,
            AVG(longitude) AS centroid_lon
        FROM `{self.table_ref}`
        WHERE DATE(timestamp) = DATE('{timestamp}')
        GROUP BY h3_index, location
        ORDER BY total_events DESC
        """
        
        try:
            query_job = self._client.query(query)
            results = query_job.result()
            
            spatial_data = []
            for row in results:
                spatial_data.append({
                    "h3_index": row.h3_index,
                    "location": row.location,
                    "total_events": row.total_events,
                    "avg_z_score": float(row.avg_z_score) if row.avg_z_score else 0.0,
                    "max_z_score": float(row.max_z_score) if row.max_z_score else 0.0,
                    "confirmed_cases": row.confirmed_cases,
                    "critical_alerts": row.critical_alerts,
                    "centroid_lat": float(row.centroid_lat) if row.centroid_lat else None,
                    "centroid_lon": float(row.centroid_lon) if row.centroid_lon else None,
                })
            
            print(f"✅ Retrieved {len(spatial_data)} spatial aggregates")
            return spatial_data
            
        except Exception as e:
            print(f"❌ Spatial query failed: {e}")
            return []


def load_simulated_data_to_bigquery(
    project_id: str,
    simulation_file: str = "simulated_outbreak.json",
    dataset_id: str = "outbreak_surveillance",
    credentials_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Helper function to load simulated outbreak data to BigQuery.
    
    Args:
        project_id: GCP project ID
        simulation_file: Path to simulated outbreak JSON file
        dataset_id: BigQuery dataset name
        credentials_path: Path to GCP service account JSON
        
    Returns:
        Load status dictionary
    """
    # Initialize BigQuery integration
    bq = BigQueryIntegration(
        project_id=project_id,
        dataset_id=dataset_id,
        credentials_path=credentials_path
    )
    
    # Initialize schema
    bq.initialize_schema()
    
    # Load simulation data
    with open(simulation_file, 'r') as f:
        simulation_data = json.load(f)
    
    events = simulation_data.get("events", [])
    
    # Batch load to BigQuery
    result = bq.batch_load_events(events)
    
    return result


# ═════════════════════════════════════════════════════════════════════════════
# BigQuery Integration Philosophy:
# "Store everything. Query anything. Predict the future."
#
# BigQuery enables iLuminara to:
# 1. Store unlimited historical surveillance data
# 2. Stream real-time events with millisecond latency
# 3. Query multi-scale spatial-temporal patterns
# 4. Feed Vertex AI for predictive forecasting
# ═════════════════════════════════════════════════════════════════════════════
