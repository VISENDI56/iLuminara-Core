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
FastAPI Backend Service
══════════════════════════════════════════════════════════════════════════════

Main API service for iLuminara GCP prototype.
Exposes endpoints for voice processing, HSTPU forecasting, and ethical validation.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import json

from .voice_processor import VoiceProcessor
from .hstpu_forecast import HstpuForecaster
from .ethical_engine import EthicalEngine, ActionType

# Initialize FastAPI app
app = FastAPI(
    title="iLuminara Core API",
    description="Sovereign Health Intelligence Platform",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (with mock mode enabled for local demo)
voice_processor = VoiceProcessor(use_mock=True)
hstpu_forecaster = HstpuForecaster(use_mock=True)
ethical_engine = EthicalEngine(jurisdiction="GLOBAL_DEFAULT")


# Pydantic models for request/response
class VoiceMetadata(BaseModel):
    worker_id: Optional[str] = None
    location: Optional[str] = None
    timestamp: Optional[str] = None


class ForecastRequest(BaseModel):
    lat: float
    lon: float
    region: str


class EthicalActionRequest(BaseModel):
    action_type: str
    payload: Dict[str, Any]


# API Routes

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "iLuminara Core API",
        "status": "operational",
        "mode": "local_demo",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "services": {
            "voice_processor": "ready",
            "hstpu_forecaster": "ready",
            "ethical_engine": "ready"
        },
        "mock_mode": True
    }


@app.post("/voice/process")
async def process_voice(
    audio_file: UploadFile = File(...),
    metadata: Optional[str] = None
):
    """
    Process uploaded voice report.
    
    Converts audio to structured JSON with entity extraction.
    """
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        # Parse metadata if provided
        meta = None
        if metadata:
            meta = json.loads(metadata)
        
        # Process audio
        result = voice_processor.process_audio(audio_data, meta)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice/simulate")
async def simulate_voice_report(metadata: Optional[VoiceMetadata] = None):
    """
    Simulate a voice report (for demo without audio file).
    
    Generates synthetic voice report data.
    """
    try:
        # Process mock audio
        meta_dict = metadata.dict() if metadata else None
        result = voice_processor.process_audio(b"mock_audio", meta_dict)
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hstpu/map")
async def get_hstpu_map(region: str = "Kenya"):
    """
    Get HSTPU outbreak map data.
    
    Returns hierarchical spatiotemporal visualization data.
    """
    try:
        map_data = hstpu_forecaster.generate_hstpu_map(region)
        
        return {
            "success": True,
            "data": map_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hstpu/forecast")
async def forecast_outbreak(request: ForecastRequest):
    """
    Generate outbreak forecast for specific location.
    """
    try:
        location = {
            "lat": request.lat,
            "lon": request.lon,
            "region": request.region
        }
        
        forecast = hstpu_forecaster.forecast_outbreak_trajectory(location)
        
        return {
            "success": True,
            "data": forecast
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hstpu/hotspots")
async def get_hotspots(threshold: float = 2.0):
    """
    Get active outbreak hotspots.
    
    Args:
        threshold: Minimum Z-score threshold (default: 2.0)
    """
    try:
        hotspots = hstpu_forecaster.get_active_hotspots(threshold)
        
        return {
            "success": True,
            "data": {
                "hotspots": hotspots,
                "threshold": threshold,
                "count": len(hotspots)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ethics/evaluate")
async def evaluate_action(request: EthicalActionRequest):
    """
    Evaluate proposed action through ethical engine.
    
    Applies humanitarian constraints and legal compliance checks.
    """
    try:
        # Map string to ActionType enum
        action_type_map = {
            "resource_allocation": ActionType.RESOURCE_ALLOCATION,
            "outbreak_alert": ActionType.OUTBREAK_ALERT,
            "data_transfer": ActionType.DATA_TRANSFER,
            "intervention": ActionType.INTERVENTION_RECOMMENDATION,
            "prediction": ActionType.PREDICTIVE_ANALYSIS
        }
        
        action_type = action_type_map.get(
            request.action_type.lower().replace(" ", "_"),
            ActionType.PREDICTIVE_ANALYSIS
        )
        
        evaluation = ethical_engine.evaluate_action(action_type, request.payload)
        
        return {
            "success": True,
            "data": evaluation
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ethics/log")
async def get_decision_log(limit: int = 50):
    """
    Get recent ethical decision log.
    
    Args:
        limit: Maximum number of entries (default: 50)
    """
    try:
        log = ethical_engine.get_decision_log(limit)
        stats = ethical_engine.get_statistics()
        
        return {
            "success": True,
            "data": {
                "log": log,
                "statistics": stats
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ethics/stats")
async def get_ethics_statistics():
    """Get ethical engine statistics."""
    try:
        stats = ethical_engine.get_statistics()
        
        return {
            "success": True,
            "data": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
