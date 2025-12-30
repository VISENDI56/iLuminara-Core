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

#!/usr/bin/env python3
"""
iLuminara Cloud Run Startup Script
Provides a simple health check endpoint for the deployment
"""

from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="iLuminara Core", version="1.0.0")

@app.get("/")
async def root():
    """Root endpoint - service information"""
    return {
        "service": "iluminara-core",
        "version": "1.0.0",
        "status": "running",
        "description": "Global Sovereign Health Architecture"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {
        "status": "healthy",
        "service": "iluminara-core"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
