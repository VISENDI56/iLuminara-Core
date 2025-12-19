"""
Hierarchical Spatiotemporal Model
═════════════════════════════════════════════════════════════════════════════

Multi-scale epidemic forecasting engine that fuses community surveillance,
clinical records, and environmental sensors into hierarchical time series
predictions. Leverages Google Cloud BigQuery and Vertex AI for cloud-based
inference while respecting data sovereignty constraints.

Philosophy: "Predict outbreaks across space and time with hierarchical precision."
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Google Cloud imports (with fallback for environments without GCP)
try:
    from google.cloud import bigquery
    from google.cloud.exceptions import GoogleCloudError
    HAS_BIGQUERY = True
except ImportError:
    HAS_BIGQUERY = False
    logging.warning("google-cloud-bigquery not available. BigQuery features disabled.")

try:
    from vertexai import time_series
    HAS_VERTEX_AI = True
except ImportError:
    HAS_VERTEX_AI = False
    logging.warning("vertexai not available. Vertex AI time series features disabled.")


logger = logging.getLogger(__name__)


class SpatiotemporalModelError(Exception):
    """Raised when spatiotemporal model operations fail."""
    pass


@dataclass
class MultiScaleDataset:
    """
    Configuration for multi-scale epidemic data sources.
    
    Combines community surveillance (CBS), clinical records (EMR),
    and environmental monitoring (IoT sensors) for comprehensive
    outbreak prediction.
    """
    community_symptoms_table: str
    emr_data_table: str
    iot_sensors_table: str
    project_id: Optional[str] = None
    dataset_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate table references."""
        if not self.community_symptoms_table:
            raise ValueError("community_symptoms_table is required")
        if not self.emr_data_table:
            raise ValueError("emr_data_table is required")
        if not self.iot_sensors_table:
            raise ValueError("iot_sensors_table is required")


@dataclass
class ForecastConfig:
    """
    Configuration for time series forecasting.
    
    Defines target variable, temporal granularity, and hierarchical
    structure for spatiotemporal predictions.
    """
    target_column: str = "case_count"
    time_column: str = "timestamp"
    hierarchical_columns: List[str] = field(default_factory=lambda: ["location"])
    spatial_radius_meters: float = 800.0  # ST_DWithin radius for spatial joins
    forecast_horizon: int = 14  # Days to forecast ahead
    
    def __post_init__(self):
        """Validate configuration."""
        if self.spatial_radius_meters <= 0:
            raise ValueError("spatial_radius_meters must be positive")
        if self.forecast_horizon <= 0:
            raise ValueError("forecast_horizon must be positive")


class HierarchicalSpatiotemporalModel:
    """
    Multi-scale epidemic forecasting model.
    
    Integrates community surveillance, clinical records, and environmental
    data to predict disease outbreaks across geographic hierarchies.
    
    Example:
        >>> config = MultiScaleDataset(
        ...     community_symptoms_table="project.dataset.community_symptoms",
        ...     emr_data_table="project.dataset.emr_data",
        ...     iot_sensors_table="project.dataset.iot_sensors"
        ... )
        >>> model = HierarchicalSpatiotemporalModel(config)
        >>> dataset = model.create_multiscale_dataset()
        >>> forecaster = model.train_forecaster(dataset)
        >>> endpoint = model.deploy_forecaster(forecaster, "hstpu-forecaster")
    """
    
    def __init__(
        self,
        dataset_config: MultiScaleDataset,
        forecast_config: Optional[ForecastConfig] = None,
        bigquery_client: Optional[Any] = None
    ):
        """
        Initialize hierarchical spatiotemporal model.
        
        Args:
            dataset_config: Multi-scale data source configuration
            forecast_config: Forecasting parameters (uses defaults if None)
            bigquery_client: Pre-configured BigQuery client (creates new if None)
        
        Raises:
            SpatiotemporalModelError: If required dependencies unavailable
        """
        if not HAS_BIGQUERY:
            raise SpatiotemporalModelError(
                "google-cloud-bigquery is required for spatiotemporal modeling. "
                "Install with: pip install google-cloud-bigquery"
            )
        
        self.dataset_config = dataset_config
        self.forecast_config = forecast_config or ForecastConfig()
        
        # Initialize BigQuery client
        if bigquery_client is not None:
            self.client = bigquery_client
        else:
            try:
                self.client = bigquery.Client(project=dataset_config.project_id)
            except Exception as e:
                raise SpatiotemporalModelError(
                    f"Failed to initialize BigQuery client: {e}"
                )
        
        self.trained_model = None
        self.deployed_endpoint = None
        
        logger.info("HierarchicalSpatiotemporalModel initialized")
    
    def _build_multiscale_query(self) -> str:
        """
        Construct SQL query for multi-scale data fusion.
        
        Combines community surveillance, clinical records, and environmental
        sensors using spatial joins (ST_DWithin) and temporal alignment.
        
        Returns:
            SQL query string for BigQuery execution
        """
        radius = self.forecast_config.spatial_radius_meters
        
        query = f"""
        WITH community AS (
            SELECT * FROM `{self.dataset_config.community_symptoms_table}`
        ),
        clinical AS (
            SELECT * FROM `{self.dataset_config.emr_data_table}`
        ),
        environmental AS (
            SELECT * FROM `{self.dataset_config.iot_sensors_table}`
        )
        SELECT 
            c.timestamp,
            c.location,
            c.symptoms,
            e.water_quality,
            e.temperature,
            COUNT(DISTINCT p.patient_id) as case_count
        FROM community c
        LEFT JOIN environmental e 
            ON ST_DWithin(c.geography, e.geography, {radius})
        LEFT JOIN clinical p 
            ON DATE(p.onset_time) = DATE(c.timestamp)
        GROUP BY 1, 2, 3, 4, 5
        ORDER BY c.timestamp DESC
        """
        
        return query
    
    def create_multiscale_dataset(self) -> Any:
        """
        Execute multi-scale data fusion query.
        
        Retrieves and combines community, clinical, and environmental data
        into a unified pandas DataFrame for time series modeling.
        
        Returns:
            pandas.DataFrame with fused multi-scale observations
        
        Raises:
            SpatiotemporalModelError: If query execution fails
        """
        query = self._build_multiscale_query()
        
        logger.info("Executing multi-scale data fusion query...")
        logger.debug(f"Query: {query}")
        
        try:
            query_job = self.client.query(query)
            dataset = query_job.to_dataframe()
            
            logger.info(f"Retrieved {len(dataset)} records from multi-scale dataset")
            return dataset
            
        except GoogleCloudError as e:
            raise SpatiotemporalModelError(
                f"BigQuery query failed: {e}"
            )
        except Exception as e:
            raise SpatiotemporalModelError(
                f"Failed to create multi-scale dataset: {e}"
            )
    
    def train_forecaster(self, dataset: Any) -> Any:
        """
        Train hierarchical time series forecaster.
        
        Uses Vertex AI time series models to learn spatiotemporal patterns
        with hierarchical structure by location.
        
        Args:
            dataset: pandas.DataFrame with multi-scale observations
        
        Returns:
            Trained forecaster model (Vertex AI TimeSeriesDataset)
        
        Raises:
            SpatiotemporalModelError: If training fails
        """
        if not HAS_VERTEX_AI:
            raise SpatiotemporalModelError(
                "vertexai is required for model training. "
                "Install with: pip install google-cloud-aiplatform"
            )
        
        logger.info("Training hierarchical time series forecaster...")
        
        try:
            # Create time series dataset
            ts_dataset = time_series.TimeSeriesDataset(dataset)
            
            # Train with hierarchical structure
            forecaster = ts_dataset.train(
                target_column=self.forecast_config.target_column,
                time_column=self.forecast_config.time_column,
                hierarchical_columns=self.forecast_config.hierarchical_columns
            )
            
            self.trained_model = forecaster
            logger.info("Forecaster training completed successfully")
            
            return forecaster
            
        except Exception as e:
            raise SpatiotemporalModelError(
                f"Failed to train forecaster: {e}"
            )
    
    def deploy_forecaster(
        self,
        forecaster: Any,
        endpoint_name: str = "hstpu-forecaster"
    ) -> Any:
        """
        Deploy trained forecaster to prediction endpoint.
        
        Creates a Vertex AI endpoint for real-time spatiotemporal predictions.
        
        Args:
            forecaster: Trained time series model
            endpoint_name: Name for deployment endpoint
        
        Returns:
            Deployed endpoint object
        
        Raises:
            SpatiotemporalModelError: If deployment fails
        """
        if not forecaster:
            raise SpatiotemporalModelError(
                "Cannot deploy: no trained forecaster provided"
            )
        
        logger.info(f"Deploying forecaster to endpoint: {endpoint_name}")
        
        try:
            endpoint = forecaster.deploy(endpoint_name=endpoint_name)
            
            self.deployed_endpoint = endpoint
            logger.info(f"Forecaster deployed successfully to {endpoint_name}")
            
            return endpoint
            
        except Exception as e:
            raise SpatiotemporalModelError(
                f"Failed to deploy forecaster: {e}"
            )
    
    def predict(
        self,
        input_data: Dict[str, Any],
        endpoint_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate spatiotemporal predictions.
        
        Args:
            input_data: Input features for prediction
            endpoint_name: Optional endpoint to use (uses deployed if None)
        
        Returns:
            Dictionary with predictions and metadata
        
        Raises:
            SpatiotemporalModelError: If prediction fails
        """
        if not self.deployed_endpoint:
            raise SpatiotemporalModelError(
                "No deployed endpoint available. Call deploy_forecaster() first."
            )
        
        logger.info("Generating spatiotemporal predictions...")
        
        try:
            predictions = self.deployed_endpoint.predict(input_data)
            
            return {
                "predictions": predictions,
                "timestamp": datetime.utcnow().isoformat(),
                "endpoint": endpoint_name or "default"
            }
            
        except Exception as e:
            raise SpatiotemporalModelError(
                f"Prediction failed: {e}"
            )
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retrieve model configuration and status.
        
        Returns:
            Dictionary with model metadata
        """
        return {
            "dataset_config": {
                "community_symptoms": self.dataset_config.community_symptoms_table,
                "emr_data": self.dataset_config.emr_data_table,
                "iot_sensors": self.dataset_config.iot_sensors_table
            },
            "forecast_config": {
                "target_column": self.forecast_config.target_column,
                "time_column": self.forecast_config.time_column,
                "hierarchical_columns": self.forecast_config.hierarchical_columns,
                "spatial_radius_meters": self.forecast_config.spatial_radius_meters,
                "forecast_horizon_days": self.forecast_config.forecast_horizon
            },
            "status": {
                "trained": self.trained_model is not None,
                "deployed": self.deployed_endpoint is not None
            }
        }


def create_spatiotemporal_pipeline(
    community_table: str,
    emr_table: str,
    iot_table: str,
    project_id: Optional[str] = None
) -> HierarchicalSpatiotemporalModel:
    """
    Convenience function to create a spatiotemporal modeling pipeline.
    
    Args:
        community_table: BigQuery table for community symptoms
        emr_table: BigQuery table for EMR/clinical data
        iot_table: BigQuery table for IoT sensor data
        project_id: GCP project ID (uses default if None)
    
    Returns:
        Configured HierarchicalSpatiotemporalModel instance
    
    Example:
        >>> model = create_spatiotemporal_pipeline(
        ...     community_table="project.dataset.community_symptoms",
        ...     emr_table="project.dataset.emr_data",
        ...     iot_table="project.dataset.iot_sensors"
        ... )
        >>> dataset = model.create_multiscale_dataset()
    """
    config = MultiScaleDataset(
        community_symptoms_table=community_table,
        emr_data_table=emr_table,
        iot_sensors_table=iot_table,
        project_id=project_id
    )
    
    return HierarchicalSpatiotemporalModel(config)
