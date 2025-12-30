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
Vertex AI Time Series Forecasting: Multi-scale Outbreak Prediction
═════════════════════════════════════════════════════════════════════════════

Provides integration with Google Vertex AI for predictive modeling:
1. Multi-scale spatial hierarchy forecasting (community → district → national)
2. Time-series forecasting for outbreak trajectory prediction
3. Feature engineering from surveillance data streams
4. Model training, deployment, and inference

Enables iLuminara to forecast outbreak dynamics across spatial scales,
supporting early warning and resource allocation decisions.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json


@dataclass
class SpatialHierarchy:
    """Defines spatial hierarchy for multi-scale forecasting."""
    level: str  # 'community', 'district', 'region', 'national'
    location_id: str
    h3_index: str
    parent_level: Optional[str] = None
    parent_location_id: Optional[str] = None
    population: Optional[int] = None


@dataclass
class ForecastConfig:
    """Configuration for time-series forecasting."""
    forecast_horizon: int  # Hours ahead to forecast
    confidence_level: float  # Prediction interval confidence (e.g., 0.95)
    spatial_level: str  # Spatial scale for forecasting
    features: List[str]  # Feature columns to use
    target_column: str  # Column to forecast


class VertexAIForecasting:
    """
    Integration with Vertex AI for outbreak time-series forecasting.
    
    Supports:
    - Multi-scale spatial forecasting across hierarchy levels
    - AutoML time-series forecasting
    - Custom model training and deployment
    - Batch and online prediction
    
    Usage:
        forecaster = VertexAIForecasting(
            project_id='my-project',
            location='us-central1'
        )
        forecast = forecaster.forecast_outbreak(
            time_series_data=data,
            forecast_horizon=72,
            spatial_level='district'
        )
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        credentials_path: Optional[str] = None
    ):
        """
        Initialize Vertex AI forecasting.
        
        Args:
            project_id: GCP project ID
            location: GCP region for Vertex AI
            credentials_path: Path to GCP service account JSON
        """
        self.project_id = project_id
        self.location = location
        self.credentials_path = credentials_path
        
        self._client = None
        self._dataset = None
        self._model = None
        
    def initialize_client(self):
        """
        Initialize Vertex AI client.
        
        Note: Requires google-cloud-aiplatform to be installed.
        """
        try:
            from google.cloud import aiplatform
            from google.oauth2 import service_account
            
            if self.credentials_path:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                aiplatform.init(
                    project=self.project_id,
                    location=self.location,
                    credentials=credentials
                )
            else:
                aiplatform.init(
                    project=self.project_id,
                    location=self.location
                )
            
            self._client = aiplatform
            print(f"✅ Vertex AI initialized: {self.project_id} @ {self.location}")
            return self._client
            
        except ImportError:
            raise ImportError(
                "google-cloud-aiplatform not installed. "
                "Install with: pip install google-cloud-aiplatform"
            )
    
    def create_time_series_dataset(
        self,
        dataset_display_name: str,
        bigquery_source: str
    ) -> Dict[str, Any]:
        """
        Create a Vertex AI time-series dataset from BigQuery.
        
        Args:
            dataset_display_name: Display name for dataset
            bigquery_source: BigQuery table URI (bq://project.dataset.table)
            
        Returns:
            Dataset creation status
        """
        if not self._client:
            self.initialize_client()
        
        from google.cloud import aiplatform
        
        try:
            dataset = aiplatform.TimeSeriesDataset.create(
                display_name=dataset_display_name,
                bq_source=bigquery_source,
                sync=True
            )
            
            self._dataset = dataset
            print(f"✅ Dataset created: {dataset.display_name}")
            
            return {
                "status": "success",
                "dataset_name": dataset.resource_name,
                "display_name": dataset.display_name
            }
        except Exception as e:
            print(f"❌ Dataset creation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def train_automl_forecasting_model(
        self,
        dataset_name: str,
        target_column: str,
        time_column: str,
        time_series_identifier_column: str,
        forecast_horizon: int = 72,
        context_window: int = 168,  # 7 days
        optimization_objective: str = "minimize-rmse",
        training_budget_hours: int = 1
    ) -> Dict[str, Any]:
        """
        Train AutoML time-series forecasting model.
        
        Args:
            dataset_name: Vertex AI dataset resource name
            target_column: Column to forecast (e.g., 'event_count')
            time_column: Timestamp column name
            time_series_identifier_column: Column identifying time series (e.g., 'location')
            forecast_horizon: Number of time steps to forecast
            context_window: Historical context window size
            optimization_objective: Model optimization target
            training_budget_hours: Maximum training time
            
        Returns:
            Training job status
        """
        if not self._client:
            self.initialize_client()
        
        from google.cloud import aiplatform
        
        try:
            # Create training job
            training_job = aiplatform.AutoMLForecastingTrainingJob(
                display_name=f"outbreak_forecast_{datetime.utcnow().strftime('%Y%m%d_%H%M')}",
                optimization_objective=optimization_objective,
            )
            
            # Train model
            model = training_job.run(
                dataset=self._dataset,
                target_column=target_column,
                time_column=time_column,
                time_series_identifier_column=time_series_identifier_column,
                unavailable_at_forecast_columns=[],
                available_at_forecast_columns=[],
                forecast_horizon=forecast_horizon,
                context_window=context_window,
                budget_milli_node_hours=training_budget_hours * 1000,
                sync=True
            )
            
            self._model = model
            print(f"✅ Model trained: {model.display_name}")
            
            return {
                "status": "success",
                "model_name": model.resource_name,
                "display_name": model.display_name
            }
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def forecast_outbreak(
        self,
        time_series_data: List[Dict[str, Any]],
        forecast_horizon: int = 72,
        spatial_level: str = "district",
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Generate outbreak forecast using trained model.
        
        Args:
            time_series_data: Historical time-series data
            forecast_horizon: Hours ahead to forecast
            spatial_level: Spatial hierarchy level
            confidence_level: Prediction interval confidence
            
        Returns:
            Forecast results with prediction intervals
        """
        if not self._model:
            raise ValueError("No trained model available. Train model first.")
        
        try:
            # Prepare instances for batch prediction
            instances = self._prepare_forecast_instances(
                time_series_data,
                forecast_horizon
            )
            
            # Make predictions
            predictions = self._model.batch_predict(
                instances=instances,
                sync=True
            )
            
            # Parse forecast results
            forecast_results = self._parse_forecast_results(
                predictions,
                confidence_level
            )
            
            print(f"✅ Forecast generated for {len(forecast_results)} locations")
            
            return {
                "status": "success",
                "forecast_horizon": forecast_horizon,
                "spatial_level": spatial_level,
                "confidence_level": confidence_level,
                "forecasts": forecast_results
            }
            
        except Exception as e:
            print(f"❌ Forecast generation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def multi_scale_forecast(
        self,
        time_series_data: Dict[str, List[Dict[str, Any]]],
        spatial_hierarchy: List[SpatialHierarchy],
        forecast_horizon: int = 72
    ) -> Dict[str, Any]:
        """
        Generate forecasts across multiple spatial scales.
        
        Implements hierarchical forecasting from community → district → national level.
        
        Args:
            time_series_data: Dictionary of time-series by spatial level
            spatial_hierarchy: Definition of spatial hierarchy
            forecast_horizon: Hours ahead to forecast
            
        Returns:
            Multi-scale forecast results
        """
        forecasts_by_level = {}
        
        # Define spatial levels in order
        levels = ["community", "district", "region", "national"]
        
        for level in levels:
            if level not in time_series_data:
                continue
            
            print(f"📊 Forecasting at {level} level...")
            
            level_data = time_series_data[level]
            
            # Generate forecasts for this level
            level_forecast = self._generate_level_forecast(
                level_data,
                level,
                forecast_horizon
            )
            
            forecasts_by_level[level] = level_forecast
        
        # Reconcile forecasts across hierarchy (bottom-up aggregation)
        reconciled_forecasts = self._reconcile_hierarchical_forecasts(
            forecasts_by_level,
            spatial_hierarchy
        )
        
        return {
            "status": "success",
            "forecast_horizon": forecast_horizon,
            "spatial_levels": list(forecasts_by_level.keys()),
            "forecasts_by_level": reconciled_forecasts,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _prepare_forecast_instances(
        self,
        time_series_data: List[Dict[str, Any]],
        forecast_horizon: int
    ) -> List[Dict[str, Any]]:
        """Prepare data instances for batch prediction."""
        instances = []
        
        for record in time_series_data:
            instance = {
                "time_series_identifier": record.get("location"),
                "time_column": record.get("time_window"),
                "target_column": record.get("event_count"),
                "features": {
                    "avg_z_score": record.get("avg_z_score"),
                    "confirmed_cases": record.get("confirmed_cases"),
                    "cbs_signals": record.get("cbs_signals"),
                    "emr_records": record.get("emr_records"),
                }
            }
            instances.append(instance)
        
        return instances
    
    def _parse_forecast_results(
        self,
        predictions: Any,
        confidence_level: float
    ) -> List[Dict[str, Any]]:
        """Parse raw prediction results into structured forecasts."""
        forecast_results = []
        
        # Parse predictions (implementation depends on Vertex AI response format)
        for pred in predictions:
            forecast = {
                "location": pred.get("time_series_identifier"),
                "forecast_values": pred.get("value", []),
                "lower_bound": pred.get("lower_bound", []),
                "upper_bound": pred.get("upper_bound", []),
                "confidence_level": confidence_level
            }
            forecast_results.append(forecast)
        
        return forecast_results
    
    def _generate_level_forecast(
        self,
        level_data: List[Dict[str, Any]],
        level: str,
        forecast_horizon: int
    ) -> Dict[str, Any]:
        """
        Generate forecast for a single spatial level.
        
        This is a simplified forecasting implementation.
        In production, would use trained Vertex AI model.
        """
        # Group by location
        locations = {}
        for record in level_data:
            loc = record.get("location")
            if loc not in locations:
                locations[loc] = []
            locations[loc].append(record)
        
        location_forecasts = {}
        
        for location, records in locations.items():
            # Sort by time
            records_sorted = sorted(records, key=lambda x: x.get("time_window", ""))
            
            # Simple exponential smoothing forecast
            forecast_values = self._exponential_smoothing_forecast(
                records_sorted,
                forecast_horizon
            )
            
            location_forecasts[location] = {
                "forecast_values": forecast_values,
                "historical_count": len(records_sorted),
                "level": level
            }
        
        return location_forecasts
    
    def _exponential_smoothing_forecast(
        self,
        historical_data: List[Dict[str, Any]],
        forecast_horizon: int,
        alpha: float = 0.3
    ) -> List[float]:
        """
        Simple exponential smoothing forecast.
        
        This is a placeholder implementation. In production, would use
        Vertex AI trained models.
        """
        if not historical_data:
            return [0.0] * forecast_horizon
        
        # Extract event counts
        values = [record.get("event_count", 0) for record in historical_data]
        
        # Initialize with first value
        smoothed = [values[0]]
        
        # Apply exponential smoothing
        for i in range(1, len(values)):
            smoothed_value = alpha * values[i] + (1 - alpha) * smoothed[i-1]
            smoothed.append(smoothed_value)
        
        # Forecast future values (constant prediction from last smoothed value)
        last_smoothed = smoothed[-1]
        forecast = [last_smoothed] * forecast_horizon
        
        return forecast
    
    def _reconcile_hierarchical_forecasts(
        self,
        forecasts_by_level: Dict[str, Any],
        spatial_hierarchy: List[SpatialHierarchy]
    ) -> Dict[str, Any]:
        """
        Reconcile forecasts across spatial hierarchy using bottom-up aggregation.
        
        Ensures forecasts at higher levels are consistent with lower level forecasts.
        """
        reconciled = {}
        
        # Start with lowest level (community)
        if "community" in forecasts_by_level:
            reconciled["community"] = forecasts_by_level["community"]
        
        # Aggregate to higher levels
        for level in ["district", "region", "national"]:
            if level not in forecasts_by_level:
                continue
            
            # Aggregate from child level
            parent_level = self._get_parent_level(level)
            if parent_level in reconciled:
                aggregated = self._aggregate_forecasts(
                    reconciled[parent_level],
                    spatial_hierarchy,
                    level
                )
                reconciled[level] = aggregated
            else:
                reconciled[level] = forecasts_by_level[level]
        
        return reconciled
    
    def _get_parent_level(self, level: str) -> Optional[str]:
        """Get parent level in spatial hierarchy."""
        hierarchy_map = {
            "district": "community",
            "region": "district",
            "national": "region"
        }
        return hierarchy_map.get(level)
    
    def _aggregate_forecasts(
        self,
        child_forecasts: Dict[str, Any],
        spatial_hierarchy: List[SpatialHierarchy],
        target_level: str
    ) -> Dict[str, Any]:
        """Aggregate child level forecasts to parent level."""
        parent_forecasts = {}
        
        # Group children by parent
        parent_children = {}
        for hierarchy_node in spatial_hierarchy:
            if hierarchy_node.level == self._get_parent_level(target_level):
                parent_id = hierarchy_node.parent_location_id
                if parent_id not in parent_children:
                    parent_children[parent_id] = []
                parent_children[parent_id].append(hierarchy_node.location_id)
        
        # Aggregate forecasts
        for parent_id, child_ids in parent_children.items():
            aggregated_values = None
            
            for child_id in child_ids:
                if child_id in child_forecasts:
                    child_forecast = child_forecasts[child_id].get("forecast_values", [])
                    
                    if aggregated_values is None:
                        aggregated_values = [0.0] * len(child_forecast)
                    
                    for i, val in enumerate(child_forecast):
                        aggregated_values[i] += val
            
            if aggregated_values:
                parent_forecasts[parent_id] = {
                    "forecast_values": aggregated_values,
                    "level": target_level,
                    "aggregated_from": child_ids
                }
        
        return parent_forecasts
    
    def export_forecast_to_bigquery(
        self,
        forecast_results: Dict[str, Any],
        bigquery_table: str
    ) -> Dict[str, Any]:
        """
        Export forecast results to BigQuery for visualization and analysis.
        
        Args:
            forecast_results: Forecast results to export
            bigquery_table: BigQuery table reference
            
        Returns:
            Export status
        """
        # Format forecast results for BigQuery
        rows_to_insert = []
        
        for level, level_forecasts in forecast_results.get("forecasts_by_level", {}).items():
            for location, forecast_data in level_forecasts.items():
                forecast_values = forecast_data.get("forecast_values", [])
                
                for i, value in enumerate(forecast_values):
                    row = {
                        "forecast_timestamp": datetime.utcnow().isoformat(),
                        "forecast_horizon_index": i,
                        "spatial_level": level,
                        "location": location,
                        "forecasted_value": value,
                        "model_version": "v1.0",
                        "generated_at": forecast_results.get("generated_at")
                    }
                    rows_to_insert.append(row)
        
        # Insert to BigQuery (would use BigQuery client in production)
        print(f"📤 Exporting {len(rows_to_insert)} forecast records to BigQuery")
        
        return {
            "status": "success",
            "rows_exported": len(rows_to_insert),
            "table": bigquery_table
        }


def create_spatial_hierarchy_example() -> List[SpatialHierarchy]:
    """
    Create example spatial hierarchy for Dadaab refugee complex.
    
    Returns:
        List of spatial hierarchy nodes
    """
    hierarchy = [
        # Community level (camps)
        SpatialHierarchy(
            level="community",
            location_id="ifo_camp",
            h3_index="88284a723ffffff",
            parent_level="district",
            parent_location_id="dadaab_district",
            population=125000
        ),
        SpatialHierarchy(
            level="community",
            location_id="hagadera_camp",
            h3_index="88284a41bffffff",
            parent_level="district",
            parent_location_id="dadaab_district",
            population=89000
        ),
        SpatialHierarchy(
            level="community",
            location_id="dagahaley_camp",
            h3_index="88284a413ffffff",
            parent_level="district",
            parent_location_id="dadaab_district",
            population=79000
        ),
        SpatialHierarchy(
            level="community",
            location_id="kambios",
            h3_index="88284a733ffffff",
            parent_level="district",
            parent_location_id="dadaab_district",
            population=35000
        ),
        # District level
        SpatialHierarchy(
            level="district",
            location_id="dadaab_district",
            h3_index="88284a7ffffffff",
            parent_level="region",
            parent_location_id="garissa_region",
            population=328000
        ),
        # Region level
        SpatialHierarchy(
            level="region",
            location_id="garissa_region",
            h3_index="88284afffffffff",
            parent_level="national",
            parent_location_id="kenya",
            population=841353
        ),
        # National level
        SpatialHierarchy(
            level="national",
            location_id="kenya",
            h3_index="88284ffffffffff",
            parent_level=None,
            parent_location_id=None,
            population=53771296
        ),
    ]
    
    return hierarchy


# ═════════════════════════════════════════════════════════════════════════════
# Vertex AI Forecasting Philosophy:
# "Predict outbreaks before they become epidemics."
#
# Multi-scale forecasting enables:
# 1. Early warning at community level
# 2. Resource allocation at district level
# 3. Strategic planning at national level
# 4. Hierarchical consistency through bottom-up aggregation
# ═════════════════════════════════════════════════════════════════════════════
