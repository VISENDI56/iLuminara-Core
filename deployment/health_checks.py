import os

def liveness_probe():
    return os.path.exists("/app/core/state/state.json")

def readiness_probe():
    return liveness_probe() and os.path.exists("/app/data")
