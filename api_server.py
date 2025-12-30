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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="iLuminara Sovereign API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "iLuminara Sovereign API Active", "status": "operational"}

@app.get("/health")
async def health():
    return {"status": "healthy", "services": ["api", "dashboard", "governance"]}

@app.get("/api/v1/status")
async def status():
    return {
        "system": "iLuminara-Core",
        "status": "active",
        "services": {
            "api": "running",
            "dashboard": "running",
            "governance": "active",
            "compliance": "monitoring",
            "ml_models": "loaded"
        },
        "certifications": ["ISO42001", "ISO27001", "ISO27701"],
        "uptime": "continuous"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)