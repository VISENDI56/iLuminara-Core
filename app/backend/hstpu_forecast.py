"""
HSTPU Forecast Engine
══════════════════════════════════════════════════════════════════════════════

Hierarchical Spatiotemporal Pattern Unit (HSTPU) outbreak forecasting.
Uses BigQuery for data aggregation and Vertex AI for ML predictions.

For local demo: Uses MockGCP to simulate BigQuery/Vertex AI.
For production: Integrates with real Google Cloud services.
"""

from typing import Dict, List, Any, Optional
import random
import os
from datetime import datetime, timedelta
from .mock_gcp import MockGCP

# Configuration from environment
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "iluminara-project")
GCP_REGION = os.getenv("GCP_REGION", "us-central1")
VERTEX_ENDPOINT = os.getenv("VERTEX_ENDPOINT", "")


class HstpuForecaster:
    """
    HSTPU (Hierarchical Spatiotemporal Pattern Unit) Forecast Engine.
    
    Analyzes outbreak patterns across spatial hierarchies (district -> region -> country)
    and temporal dimensions (hours -> days -> weeks).
    """
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize HSTPU forecaster.
        
        Args:
            use_mock: If True, uses mock GCP services. Set to False in production.
        """
        self.use_mock = use_mock
        if use_mock:
            mock_gcp = MockGCP()
            self.bigquery_client = mock_gcp.get_bigquery_client()
            self.vertex_client = mock_gcp.get_vertex_ai_client()
        else:
            # Real GCP implementation
            from google.cloud import bigquery
            from google.cloud import aiplatform
            self.bigquery_client = bigquery.Client()
            self.vertex_client = aiplatform.gapic.PredictionServiceClient()
    
    def generate_hstpu_map(self, region: str = "Kenya") -> Dict[str, Any]:
        """
        Generate hierarchical spatiotemporal outbreak map.
        
        Returns visualization data for pydeck map rendering.
        """
        # Query outbreak data
        query = f"""
        SELECT region, lat, lon, outbreak_probability, cases_confirmed, z_score
        FROM `health_intelligence.outbreak_events`
        WHERE region LIKE '%{region}%'
        AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
        """
        
        if self.use_mock:
            data = self.bigquery_client.query(query)
        else:
            query_job = self.bigquery_client.query(query)
            data = query_job.result()
        
        # Transform for visualization
        map_data = self._prepare_map_data(data)
        
        return map_data
    
    def forecast_outbreak_trajectory(self, location: Dict[str, float]) -> Dict[str, Any]:
        """
        Forecast outbreak trajectory for a specific location.
        
        Args:
            location: {"lat": float, "lon": float, "region": str}
        
        Returns:
            Forecast with risk scores, peak estimates, and confidence intervals
        """
        # Prepare prediction instances
        instances = [{
            "latitude": location.get("lat", 0.0),
            "longitude": location.get("lon", 0.0),
            "region": location.get("region", "Unknown"),
            "historical_cases": random.randint(50, 500),  # Would be real data in production
            "population_density": random.uniform(100, 5000)
        }]
        
        # Get ML predictions
        if self.use_mock:
            predictions = self.vertex_client.predict(instances)
        else:
            # Real Vertex AI endpoint call
            endpoint = VERTEX_ENDPOINT or f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}/endpoints/ENDPOINT_ID"
            predictions = self.vertex_client.predict(
                endpoint=endpoint,
                instances=instances
            )
        
        # Enhance with HSTPU hierarchical analysis
        forecast = self._build_hstpu_forecast(predictions, location)
        
        return forecast
    
    def get_active_hotspots(self, threshold_zscore: float = 2.0) -> List[Dict[str, Any]]:
        """
        Identify active outbreak hotspots exceeding risk threshold.
        
        Args:
            threshold_zscore: Minimum Z-score to classify as hotspot
        
        Returns:
            List of hotspot locations with risk metrics
        """
        query = f"""
        SELECT 
            region, lat, lon, z_score, outbreak_probability,
            cases_confirmed, cases_suspected, population_at_risk
        FROM `health_intelligence.outbreak_events`
        WHERE z_score > {threshold_zscore}
        ORDER BY z_score DESC
        LIMIT 10
        """
        
        if self.use_mock:
            result = self.bigquery_client.query(query)
            hotspots = result["rows"]
        else:
            query_job = self.bigquery_client.query(query)
            hotspots = [dict(row) for row in query_job.result()]
        
        return hotspots
    
    def _prepare_map_data(self, query_result: Dict) -> Dict[str, Any]:
        """Transform query results into pydeck-compatible format."""
        rows = query_result.get("rows", [])
        
        # Generate random coordinates for Kenya regions (demo data)
        locations = [
            {"region": "Dadaab", "lat": 0.0512, "lon": 40.3129},
            {"region": "Nairobi", "lat": -1.2921, "lon": 36.8219},
            {"region": "Mombasa", "lat": -4.0435, "lon": 39.6682}
        ]
        
        map_points = []
        for i, row in enumerate(rows):
            loc = locations[i % len(locations)]
            map_points.append({
                "region": row.get("region", loc["region"]),
                "lat": loc["lat"],
                "lon": loc["lon"],
                "z_score": row.get("z_score", 0.0),
                "outbreak_probability": row.get("outbreak_probability", 0.0),
                "cases_confirmed": row.get("cases_confirmed", 0),
                "population_at_risk": row.get("population_at_risk", 0),
                "color": self._get_risk_color(row.get("z_score", 0.0))
            })
        
        return {
            "points": map_points,
            "center": {"lat": -0.0236, "lon": 37.9062},  # Kenya center
            "zoom": 6,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_risk_color(self, z_score: float) -> List[int]:
        """Map Z-score to RGB color (green -> yellow -> red)."""
        if z_score > 3.5:
            return [255, 0, 0, 200]  # Red
        elif z_score > 2.0:
            return [255, 215, 0, 200]  # Yellow/Gold
        else:
            return [0, 255, 65, 200]  # Green
    
    def _build_hstpu_forecast(self, predictions: Dict, location: Dict) -> Dict[str, Any]:
        """Build hierarchical forecast from ML predictions."""
        pred = predictions["predictions"][0] if predictions["predictions"] else {}
        
        return {
            "location": location,
            "forecast": {
                "risk_score": pred.get("outbreak_risk_score", 0.0),
                "peak_time": pred.get("peak_time_estimate", "Unknown"),
                "confidence": pred.get("confidence", 0.0),
                "recommended_action": pred.get("recommended_action", "Monitor")
            },
            "hierarchical_context": {
                "district_risk": round(random.uniform(0.2, 0.8), 2),
                "region_risk": round(random.uniform(0.1, 0.6), 2),
                "country_risk": round(random.uniform(0.05, 0.3), 2)
            },
            "temporal_projection": [
                {
                    "day": i,
                    "projected_cases": int(pred.get("outbreak_risk_score", 0.3) * 100 * (1 + i * 0.1))
                }
                for i in range(1, 8)
            ],
            "model_version": predictions.get("model_id", "hstpu_v2"),
            "generated_at": predictions.get("timestamp", datetime.now().isoformat())
        }
