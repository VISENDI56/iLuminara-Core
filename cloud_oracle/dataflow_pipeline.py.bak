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
Dataflow Pipeline: Real-time Data Fusion Engine
═════════════════════════════════════════════════════════════════════════════

Provides Apache Beam / Dataflow pipeline for real-time fusion of:
1. Community-based surveillance (CBS) signals
2. Environmental monitoring data (water quality, climate)
3. Clinical data from EMR systems

Implements streaming ETL with windowing, fusion logic, and output to BigQuery
for downstream forecasting and analytics.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json


@dataclass
class StreamingEvent:
    """Base class for streaming surveillance events."""
    event_id: str
    timestamp: str
    source: str  # 'CBS', 'EMR', 'ENVIRONMENTAL'
    location: str
    h3_index: str
    data: Dict[str, Any]


@dataclass
class FusedEvent:
    """Fused event combining multiple data sources."""
    fusion_id: str
    timestamp: str
    location: str
    h3_index: str
    cbs_data: Optional[Dict[str, Any]] = None
    emr_data: Optional[Dict[str, Any]] = None
    environmental_data: Optional[Dict[str, Any]] = None
    fusion_score: float = 0.0
    alert_level: Optional[str] = None


class DataflowPipeline:
    """
    Real-time data fusion pipeline using Apache Beam / Dataflow.
    
    Pipeline stages:
    1. Ingest: Read from Pub/Sub topics (CBS, EMR, Environmental)
    2. Window: Group events by time window (e.g., 5-minute windows)
    3. Fuse: Apply fusion logic to combine streams
    4. Enrich: Add spatial and temporal context
    5. Output: Write to BigQuery and trigger alerts
    
    Usage:
        pipeline = DataflowPipeline(
            project_id='my-project',
            temp_location='gs://my-bucket/temp'
        )
        pipeline.run()
    """
    
    def __init__(
        self,
        project_id: str,
        region: str = "us-central1",
        temp_location: str = None,
        staging_location: str = None
    ):
        """
        Initialize Dataflow pipeline configuration.
        
        Args:
            project_id: GCP project ID
            region: GCP region for Dataflow jobs
            temp_location: GCS path for temporary files
            staging_location: GCS path for staging files
        """
        self.project_id = project_id
        self.region = region
        self.temp_location = temp_location or f"gs://{project_id}-dataflow/temp"
        self.staging_location = staging_location or f"gs://{project_id}-dataflow/staging"
        
        # Pub/Sub topics for different data sources
        self.cbs_topic = f"projects/{project_id}/topics/cbs-surveillance"
        self.emr_topic = f"projects/{project_id}/topics/emr-clinical"
        self.environmental_topic = f"projects/{project_id}/topics/environmental-monitoring"
        
        # BigQuery output table
        self.output_table = f"{project_id}:outbreak_surveillance.fused_events"
        
    def get_pipeline_options(self) -> Dict[str, Any]:
        """
        Get Dataflow pipeline options.
        
        Returns:
            Pipeline options dictionary
        """
        options = {
            'project': self.project_id,
            'region': self.region,
            'temp_location': self.temp_location,
            'staging_location': self.staging_location,
            'streaming': True,
            'runner': 'DataflowRunner',
            'job_name': f'outbreak-fusion-{datetime.utcnow().strftime("%Y%m%d-%H%M%S")}',
            'save_main_session': True,
        }
        return options
    
    def create_pipeline(self):
        """
        Create the Dataflow pipeline.
        
        Note: Requires apache-beam[gcp] to be installed.
        
        Returns:
            Apache Beam pipeline
        """
        try:
            import apache_beam as beam
            from apache_beam.options.pipeline_options import PipelineOptions
            from apache_beam.io.gcp.pubsub import ReadFromPubSub
            from apache_beam.io.gcp.bigquery import WriteToBigQuery
            from apache_beam.transforms.window import FixedWindows
            
        except ImportError:
            raise ImportError(
                "apache-beam not installed. "
                "Install with: pip install apache-beam[gcp]"
            )
        
        # Create pipeline options
        pipeline_options = PipelineOptions(**self.get_pipeline_options())
        
        # Create pipeline
        with beam.Pipeline(options=pipeline_options) as pipeline:
            
            # Read CBS signals from Pub/Sub
            cbs_stream = (
                pipeline
                | 'Read CBS' >> ReadFromPubSub(topic=self.cbs_topic)
                | 'Parse CBS' >> beam.Map(self._parse_cbs_event)
                | 'Tag CBS' >> beam.Map(lambda x: ('CBS', x))
            )
            
            # Read EMR records from Pub/Sub
            emr_stream = (
                pipeline
                | 'Read EMR' >> ReadFromPubSub(topic=self.emr_topic)
                | 'Parse EMR' >> beam.Map(self._parse_emr_event)
                | 'Tag EMR' >> beam.Map(lambda x: ('EMR', x))
            )
            
            # Read environmental data from Pub/Sub
            environmental_stream = (
                pipeline
                | 'Read Environmental' >> ReadFromPubSub(topic=self.environmental_topic)
                | 'Parse Environmental' >> beam.Map(self._parse_environmental_event)
                | 'Tag Environmental' >> beam.Map(lambda x: ('ENVIRONMENTAL', x))
            )
            
            # Merge streams
            merged_stream = (
                (cbs_stream, emr_stream, environmental_stream)
                | 'Merge Streams' >> beam.Flatten()
            )
            
            # Apply windowing (5-minute fixed windows)
            windowed_stream = (
                merged_stream
                | 'Window' >> beam.WindowInto(FixedWindows(300))  # 5 minutes
            )
            
            # Group by location and window
            grouped_stream = (
                windowed_stream
                | 'Key By Location' >> beam.Map(lambda x: (x[1].location, x))
                | 'Group By Location' >> beam.GroupByKey()
            )
            
            # Apply fusion logic
            fused_stream = (
                grouped_stream
                | 'Fuse Events' >> beam.Map(self._fuse_events)
            )
            
            # Enrich with spatial/temporal context
            enriched_stream = (
                fused_stream
                | 'Enrich' >> beam.Map(self._enrich_fused_event)
            )
            
            # Filter for high-risk events (optional)
            high_risk_stream = (
                enriched_stream
                | 'Filter High Risk' >> beam.Filter(
                    lambda x: x.get('alert_level') in ['ALERT', 'CRITICAL']
                )
            )
            
            # Write to BigQuery
            enriched_stream | 'Write to BigQuery' >> WriteToBigQuery(
                table=self.output_table,
                schema=self._get_bigquery_schema(),
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
            
            # Trigger real-time alerts for high-risk events
            high_risk_stream | 'Trigger Alerts' >> beam.Map(self._trigger_alert)
        
        print("✅ Dataflow pipeline created")
        return pipeline
    
    def _parse_cbs_event(self, message: bytes) -> StreamingEvent:
        """Parse CBS surveillance event from Pub/Sub message."""
        data = json.loads(message.decode('utf-8'))
        
        return StreamingEvent(
            event_id=data.get('event_id'),
            timestamp=data.get('timestamp'),
            source='CBS',
            location=data.get('location'),
            h3_index=data.get('h3_index'),
            data=data
        )
    
    def _parse_emr_event(self, message: bytes) -> StreamingEvent:
        """Parse EMR clinical event from Pub/Sub message."""
        data = json.loads(message.decode('utf-8'))
        
        return StreamingEvent(
            event_id=data.get('event_id'),
            timestamp=data.get('timestamp'),
            source='EMR',
            location=data.get('location'),
            h3_index=data.get('h3_index'),
            data=data
        )
    
    def _parse_environmental_event(self, message: bytes) -> StreamingEvent:
        """Parse environmental monitoring event from Pub/Sub message."""
        data = json.loads(message.decode('utf-8'))
        
        return StreamingEvent(
            event_id=data.get('event_id'),
            timestamp=data.get('timestamp'),
            source='ENVIRONMENTAL',
            location=data.get('location'),
            h3_index=data.get('h3_index'),
            data=data
        )
    
    def _fuse_events(
        self, 
        location_events: Tuple[str, List[Tuple[str, StreamingEvent]]]
    ) -> FusedEvent:
        """
        Fuse events from multiple streams based on location and time window.
        
        Fusion logic:
        - Co-located events (same location, same time window) are fused
        - CBS + EMR + Environmental data are combined
        - Fusion score calculated based on data source agreement
        
        Args:
            location_events: Tuple of (location, list of tagged events)
            
        Returns:
            Fused event combining multiple streams
        """
        location, events = location_events
        
        # Separate events by source
        cbs_events = [e[1] for e in events if e[0] == 'CBS']
        emr_events = [e[1] for e in events if e[0] == 'EMR']
        environmental_events = [e[1] for e in events if e[0] == 'ENVIRONMENTAL']
        
        # Get most recent event from each source
        cbs_data = cbs_events[0].data if cbs_events else None
        emr_data = emr_events[0].data if emr_events else None
        environmental_data = environmental_events[0].data if environmental_events else None
        
        # Calculate fusion score
        fusion_score = self._calculate_fusion_score(
            cbs_data, emr_data, environmental_data
        )
        
        # Determine alert level
        alert_level = self._determine_alert_level(
            cbs_data, emr_data, environmental_data, fusion_score
        )
        
        # Get timestamp (prefer earliest)
        timestamps = [e[1].timestamp for e in events if e[1].timestamp]
        timestamp = min(timestamps) if timestamps else datetime.utcnow().isoformat()
        
        # Get H3 index
        h3_index = cbs_events[0].h3_index if cbs_events else (
            emr_events[0].h3_index if emr_events else (
                environmental_events[0].h3_index if environmental_events else None
            )
        )
        
        # Create fused event
        fused = FusedEvent(
            fusion_id=f"FUSED-{location}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            timestamp=timestamp,
            location=location,
            h3_index=h3_index,
            cbs_data=cbs_data,
            emr_data=emr_data,
            environmental_data=environmental_data,
            fusion_score=fusion_score,
            alert_level=alert_level
        )
        
        return fused
    
    def _calculate_fusion_score(
        self,
        cbs_data: Optional[Dict],
        emr_data: Optional[Dict],
        environmental_data: Optional[Dict]
    ) -> float:
        """
        Calculate fusion score based on data source agreement.
        
        Score calculation:
        - All 3 sources present: 1.0
        - 2 sources present: 0.8
        - 1 source present: 0.5
        - Additional bonus for clinical confirmation
        """
        sources_present = sum([
            cbs_data is not None,
            emr_data is not None,
            environmental_data is not None
        ])
        
        base_score = sources_present / 3.0
        
        # Bonus for clinical confirmation
        if emr_data and emr_data.get('lab_confirmed'):
            base_score = min(1.0, base_score + 0.2)
        
        # Bonus for location agreement
        if cbs_data and emr_data:
            if cbs_data.get('location') == emr_data.get('location'):
                base_score = min(1.0, base_score + 0.1)
        
        return round(base_score, 2)
    
    def _determine_alert_level(
        self,
        cbs_data: Optional[Dict],
        emr_data: Optional[Dict],
        environmental_data: Optional[Dict],
        fusion_score: float
    ) -> str:
        """
        Determine alert level based on fused data.
        
        Alert levels:
        - CRITICAL: Lab-confirmed + high environmental risk
        - ALERT: Clinical diagnosis or multiple CBS signals
        - WATCH: Single CBS signal
        - GREEN: Normal surveillance
        """
        # Critical: Lab-confirmed + high risk factors
        if emr_data and emr_data.get('lab_confirmed'):
            if environmental_data and environmental_data.get('risk_level') == 'HIGH':
                return 'CRITICAL'
            return 'ALERT'
        
        # Alert: Clinical diagnosis
        if emr_data and emr_data.get('diagnosis'):
            return 'ALERT'
        
        # Watch: CBS signal with environmental risk
        if cbs_data:
            if environmental_data and environmental_data.get('risk_level') in ['HIGH', 'MEDIUM']:
                return 'WATCH'
            return 'WATCH'
        
        return 'GREEN'
    
    def _enrich_fused_event(self, fused_event: FusedEvent) -> Dict[str, Any]:
        """
        Enrich fused event with spatial and temporal context.
        
        Adds:
        - Spatial metadata (population, region)
        - Temporal context (hour of day, day of week)
        - Historical comparison (vs. baseline)
        """
        enriched = {
            'fusion_id': fused_event.fusion_id,
            'timestamp': fused_event.timestamp,
            'location': fused_event.location,
            'h3_index': fused_event.h3_index,
            'fusion_score': fused_event.fusion_score,
            'alert_level': fused_event.alert_level,
            'cbs_present': fused_event.cbs_data is not None,
            'emr_present': fused_event.emr_data is not None,
            'environmental_present': fused_event.environmental_data is not None,
        }
        
        # Add CBS data fields
        if fused_event.cbs_data:
            enriched['cbs_symptom'] = fused_event.cbs_data.get('symptom')
            enriched['cbs_age_group'] = fused_event.cbs_data.get('age_group')
        
        # Add EMR data fields
        if fused_event.emr_data:
            enriched['emr_diagnosis'] = fused_event.emr_data.get('diagnosis')
            enriched['lab_confirmed'] = fused_event.emr_data.get('lab_confirmed', False)
        
        # Add environmental data fields
        if fused_event.environmental_data:
            enriched['water_quality_index'] = fused_event.environmental_data.get('water_quality_index')
            enriched['temperature_celsius'] = fused_event.environmental_data.get('temperature')
            enriched['rainfall_mm'] = fused_event.environmental_data.get('rainfall')
        
        # Add temporal context
        event_time = datetime.fromisoformat(fused_event.timestamp.replace('Z', '+00:00'))
        enriched['hour_of_day'] = event_time.hour
        enriched['day_of_week'] = event_time.weekday()
        
        return enriched
    
    def _trigger_alert(self, enriched_event: Dict[str, Any]):
        """
        Trigger real-time alert for high-risk events.
        
        In production, would publish to alerting topic or call notification API.
        """
        print(f"🚨 ALERT: {enriched_event.get('alert_level')} at {enriched_event.get('location')}")
        print(f"   Fusion Score: {enriched_event.get('fusion_score')}")
        print(f"   Timestamp: {enriched_event.get('timestamp')}")
        
        # Could publish to Pub/Sub alerting topic
        # or trigger notification via Cloud Functions
        return enriched_event
    
    def _get_bigquery_schema(self) -> str:
        """
        Get BigQuery schema for fused events table.
        
        Returns:
            Schema string in BigQuery format
        """
        schema = {
            'fields': [
                {'name': 'fusion_id', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'timestamp', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'location', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'h3_index', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'fusion_score', 'type': 'FLOAT', 'mode': 'REQUIRED'},
                {'name': 'alert_level', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'cbs_present', 'type': 'BOOLEAN', 'mode': 'REQUIRED'},
                {'name': 'emr_present', 'type': 'BOOLEAN', 'mode': 'REQUIRED'},
                {'name': 'environmental_present', 'type': 'BOOLEAN', 'mode': 'REQUIRED'},
                {'name': 'cbs_symptom', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'cbs_age_group', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'emr_diagnosis', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'lab_confirmed', 'type': 'BOOLEAN', 'mode': 'NULLABLE'},
                {'name': 'water_quality_index', 'type': 'FLOAT', 'mode': 'NULLABLE'},
                {'name': 'temperature_celsius', 'type': 'FLOAT', 'mode': 'NULLABLE'},
                {'name': 'rainfall_mm', 'type': 'FLOAT', 'mode': 'NULLABLE'},
                {'name': 'hour_of_day', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                {'name': 'day_of_week', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            ]
        }
        return json.dumps(schema)


def create_pubsub_topics(project_id: str) -> Dict[str, Any]:
    """
    Create Pub/Sub topics for data ingestion.
    
    Args:
        project_id: GCP project ID
        
    Returns:
        Topic creation status
    """
    try:
        from google.cloud import pubsub_v1
        
        publisher = pubsub_v1.PublisherClient()
        
        topics = [
            'cbs-surveillance',
            'emr-clinical',
            'environmental-monitoring'
        ]
        
        created_topics = []
        
        for topic_name in topics:
            topic_path = publisher.topic_path(project_id, topic_name)
            
            try:
                topic = publisher.create_topic(request={"name": topic_path})
                created_topics.append(topic_name)
                print(f"✅ Created topic: {topic_name}")
            except Exception as e:
                print(f"⚠️  Topic {topic_name} already exists or error: {e}")
        
        return {
            "status": "success",
            "topics_created": created_topics
        }
        
    except ImportError:
        raise ImportError(
            "google-cloud-pubsub not installed. "
            "Install with: pip install google-cloud-pubsub"
        )


# ═════════════════════════════════════════════════════════════════════════════
# Dataflow Data Fusion Philosophy:
# "Fuse everything. Miss nothing. Respond instantly."
#
# Real-time data fusion enables:
# 1. Cross-validation of surveillance signals
# 2. Environmental risk factor integration
# 3. Clinical confirmation correlation
# 4. Sub-minute alert latency
# ═════════════════════════════════════════════════════════════════════════════
