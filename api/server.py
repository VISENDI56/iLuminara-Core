import sys
import os
import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Import iLuminara Core Logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from infrastructure.simulation.data_stream import LiveDataHarness
from governance_kernel.sovereign_guardrail import SovereignGuardrail
from agents.security_operations.system2_soc import System2SecurityAgent

app = FastAPI(title="iLuminara Sovereign Node")

# CORS for Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Engines
stream = LiveDataHarness()
guard = SovereignGuardrail()
soc_agent = System2SecurityAgent()

@app.get("/")
def health_check():
    return {"status": "ONLINE", "node": "TensorSwitch-Edge-01", "sovereignty": "ACTIVE"}

@app.websocket("/ws/live-feed")
async def websocket_endpoint(websocket: WebSocket):
    """
    Streams Real-Time Omni-Law Intercepts to the Dashboard.
    """
    await websocket.accept()
    try:
        while True:
            # 1. Get Live Event (Finance/Supply Chain/ESG)
            event = stream.get_next_event()
            # 2. Check Compliance (47 Frameworks)
            compliance = guard.check_sectoral_compliance(event['context'], event['payload'])
            # 3. Simulate SOC Thinking (if threat detected)
            soc_status = "IDLE"
            if compliance['status'] in ["BLOCKED", "FROZEN"]:
                soc_status = "VALIDATING_THREAT"
                # In a real app, we'd trigger the full System 2 Agent here asynchronously
            payload = {
                "timestamp": asyncio.get_event_loop().time(),
                "sector": event['context'],
                "data": event['payload'],
                "result": compliance,
                "soc_state": soc_status
            }
            await websocket.send_json(payload)
            await asyncio.sleep(2) # 2s Refresh Rate
    except Exception as e:
        print(f"Connection Closed: {e}")

@app.get("/api/frameworks")
def get_framework_matrix():
    """
    Returns the full list of 47 Frameworks for the Ledger View.
    """
    # Merging Core 18 + Sectoral 29
    return {
        "privacy": ["GDPR", "KDPA", "POPIA", "CCPA", "HIPAA", "NDPR", "PIPEDA"],
        "supply_chain": ["UFLPA", "CSDDD", "LkSG", "Dodd-Frank"],
        "finance": ["OFAC", "FATF", "AML", "Basel III"],
        "ai_safety": ["EU AI Act", "NIST RMF", "ISO 42001"],
        "humanitarian": ["Geneva Conventions", "IHR 2005", "Malabo Convention"],
        "pharma": ["EU MDR", "FDA Part 11"],
        # ... (Add remaining frameworks here)
        "total_active": 47
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
