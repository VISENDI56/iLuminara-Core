def load_state():
    """Mock shared memory state loader."""
    return {
        "system_status": "active",
        "jurisdiction": "GLOBAL_DEFAULT",
        "compliance_mode": "STRICT"
    }