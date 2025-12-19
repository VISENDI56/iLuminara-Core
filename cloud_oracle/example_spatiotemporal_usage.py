#!/usr/bin/env python3
"""
Example: Hierarchical Spatiotemporal Model Usage
═════════════════════════════════════════════════════════════════════════════

Demonstrates how to build a multi-scale epidemic forecasting model using
community surveillance, clinical records, and environmental sensor data.

This example shows the exact usage pattern from the problem statement.
"""

from cloud_oracle.spatiotemporal_model import (
    HierarchicalSpatiotemporalModel,
    MultiScaleDataset,
    ForecastConfig,
    SpatiotemporalModelError
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Build and deploy hierarchical spatiotemporal model.
    
    Follows the pattern from the problem statement:
    1. Create multi-scale dataset from BigQuery
    2. Train time series model with Vertex AI
    3. Deploy predictive endpoint
    """
    
    logger.info("=" * 80)
    logger.info("Building Hierarchical Spatiotemporal Model")
    logger.info("=" * 80)
    
    try:
        # 1. Configure multi-scale data sources
        dataset_config = MultiScaleDataset(
            community_symptoms_table="your-project.your-dataset.community_symptoms",
            emr_data_table="your-project.your-dataset.emr_data",
            iot_sensors_table="your-project.your-dataset.iot_sensors",
            project_id="your-project-id"  # Optional, uses default project if None
        )
        
        # Optional: Configure forecast parameters
        forecast_config = ForecastConfig(
            target_column="case_count",
            time_column="timestamp",
            hierarchical_columns=["location"],
            spatial_radius_meters=800.0,  # ST_DWithin radius for spatial joins
            forecast_horizon=14  # Days to forecast ahead
        )
        
        # Initialize model
        logger.info("Initializing spatiotemporal model...")
        model = HierarchicalSpatiotemporalModel(
            dataset_config=dataset_config,
            forecast_config=forecast_config
        )
        
        # 2. Create multi-scale dataset
        logger.info("Creating multi-scale dataset from BigQuery...")
        dataset = model.create_multiscale_dataset()
        logger.info(f"Dataset created with {len(dataset)} records")
        
        # 3. Train time series model
        logger.info("Training hierarchical time series forecaster...")
        forecaster = model.train_forecaster(dataset)
        logger.info("Training completed successfully")
        
        # 4. Deploy predictive endpoint
        logger.info("Deploying forecaster to endpoint...")
        endpoint = model.deploy_forecaster(forecaster, endpoint_name="hstpu-forecaster")
        logger.info(f"Forecaster deployed to endpoint: {endpoint}")
        
        # Display model information
        logger.info("\n" + "=" * 80)
        logger.info("Model Information:")
        logger.info("=" * 80)
        info = model.get_model_info()
        for key, value in info.items():
            logger.info(f"{key}: {value}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ Hierarchical spatiotemporal model built successfully!")
        logger.info("=" * 80)
        
        return model
        
    except SpatiotemporalModelError as e:
        logger.error(f"❌ Spatiotemporal model error: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    # Note: This example requires:
    # 1. Google Cloud project with BigQuery enabled
    # 2. Vertex AI API enabled
    # 3. Appropriate IAM permissions
    # 4. Authentication configured (gcloud auth application-default login)
    # 5. Tables created in BigQuery with appropriate schema
    
    logger.info("Example: Hierarchical Spatiotemporal Model")
    logger.info("This example demonstrates the usage pattern from the problem statement.")
    logger.info("\nPrerequisites:")
    logger.info("  - Google Cloud project configured")
    logger.info("  - BigQuery tables with community_symptoms, emr_data, iot_sensors")
    logger.info("  - Vertex AI API enabled")
    logger.info("  - Authenticated with appropriate permissions")
    logger.info("\nTo run this example, update the table names and project ID above.\n")
    
    # Uncomment to run (requires GCP setup):
    # model = main()
