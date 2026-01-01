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
Mock GCP Services
══════════════════════════════════════════════════════════════════════════════

Simulates Google Cloud Platform services (BigQuery, Vertex AI, Speech-to-Text)
for local development without requiring active GCP credentials.

This allows the iLuminara prototype to run immediately in Codespaces.
"""

from typing import Dict, List, Any
import random
import json
from datetime import datetime


class MockBigQuery:
    """Simulates BigQuery analytics for health outbreak data."""
    
    def query(self, query: str) -> Dict[str, Any]:
        """
        Mock BigQuery query execution.
        Returns synthetic outbreak statistics.
        """
        # Generate realistic outbreak metrics
        return {
            "rows": [
                {
                    "region": "Dadaab",
                    "outbreak_probability": round(random.uniform(0.2, 0.95), 3),
                    "population_at_risk": random.randint(5000, 50000),
                    "cases_confirmed": random.randint(10, 500),
                    "cases_suspected": random.randint(50, 1000),
                    "z_score": round(random.uniform(1.5, 4.2), 2)
                },
                {
                    "region": "Nairobi",
                    "outbreak_probability": round(random.uniform(0.1, 0.6), 3),
                    "population_at_risk": random.randint(10000, 100000),
                    "cases_confirmed": random.randint(5, 200),
                    "cases_suspected": random.randint(20, 500),
                    "z_score": round(random.uniform(0.8, 2.5), 2)
                },
                {
                    "region": "Mombasa",
                    "outbreak_probability": round(random.uniform(0.05, 0.4), 3),
                    "population_at_risk": random.randint(8000, 80000),
                    "cases_confirmed": random.randint(2, 100),
                    "cases_suspected": random.randint(10, 300),
                    "z_score": round(random.uniform(0.5, 1.8), 2)
                }
            ],
            "total_rows": 3,
            "query_id": f"mock_query_{datetime.now().timestamp()}"
        }


class MockVertexAI:
    """Simulates Vertex AI machine learning predictions."""
    
    def predict(self, instances: List[Dict]) -> Dict[str, Any]:
        """
        Mock ML prediction for outbreak forecasting.
        Returns synthetic HSTPU (Hierarchical Spatiotemporal) forecasts.
        """
        predictions = []
        for instance in instances:
            predictions.append({
                "outbreak_risk_score": round(random.uniform(0.1, 0.9), 3),
                "peak_time_estimate": f"{random.randint(7, 30)} days",
                "confidence": round(random.uniform(0.7, 0.95), 3),
                "recommended_action": random.choice([
                    "Monitor closely",
                    "Deploy intervention team",
                    "Activate emergency protocols",
                    "Maintain surveillance"
                ])
            })
        
        return {
            "predictions": predictions,
            "model_id": "hstpu_forecast_v2",
            "timestamp": datetime.now().isoformat()
        }


class MockSpeechToText:
    """Simulates Google Cloud Speech-to-Text API."""
    
    def transcribe(self, audio_content: bytes) -> Dict[str, Any]:
        """
        Mock audio transcription.
        Returns synthetic health report transcription.
        """
        # Simulate realistic health worker voice report
        mock_transcriptions = [
            "Patient reporting fever and headache for three days. No travel history. Community cluster suspected.",
            "Five new cases in the eastern district. All showing similar symptoms. Request immediate supplies.",
            "Outbreak containment measures in effect. Twenty cases confirmed. Field team deployed.",
            "Water source contamination suspected. Multiple cases of gastroenteritis reported.",
            "Respiratory illness cluster identified. Contact tracing initiated. Fifteen individuals quarantined."
        ]
        
        transcription = random.choice(mock_transcriptions)
        
        return {
            "transcript": transcription,
            "confidence": round(random.uniform(0.85, 0.98), 3),
            "language_code": "en-US",
            "words": [
                {
                    "word": word,
                    "start_time": f"{i * 0.5}s",
                    "end_time": f"{(i + 1) * 0.5}s"
                }
                for i, word in enumerate(transcription.split()[:10])  # First 10 words
            ]
        }
    
    def process_audio_file(self, file_path: str) -> Dict[str, Any]:
        """Process an uploaded audio file."""
        # For demo, we don't actually process the file
        return self.transcribe(b"mock_audio_content")


class MockGCP:
    """
    Unified mock GCP service interface.
    Provides all necessary GCP services for local development.
    """
    
    def __init__(self):
        self.bigquery = MockBigQuery()
        self.vertex_ai = MockVertexAI()
        self.speech = MockSpeechToText()
    
    def get_bigquery_client(self):
        """Returns mock BigQuery client."""
        return self.bigquery
    
    def get_vertex_ai_client(self):
        """Returns mock Vertex AI client."""
        return self.vertex_ai
    
    def get_speech_client(self):
        """Returns mock Speech-to-Text client."""
        return self.speech
