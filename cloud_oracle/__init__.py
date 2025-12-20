"""
Cloud Oracle: Multi-scale Outbreak Forecasting System
═════════════════════════════════════════════════════════════════════════════

Integration with Google Cloud Platform for predictive outbreak analytics:
- BigQuery: Historical data storage and real-time streaming
- Vertex AI: Time-series forecasting across spatial hierarchies
- Dataflow: Real-time data fusion (CBS + EMR + Environmental)

This module enables iLuminara to forecast outbreak dynamics across scales,
from community-level early warning to national-level strategic planning.
"""

__all__ = [
    'BigQueryIntegration',
    'VertexAIForecasting',
    'DataflowPipeline',
    'get_config',
]
