"""
Canonical Sovereign State Schema - Versioned, Invariant-Protected
Version: 2026.01
"""

from datetime import datetime, timezone
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StateSchema")

STATE_SCHEMA_VERSION = "2026.01"

DEFAULT_STATE = {
    "schema_version": STATE_SCHEMA_VERSION,
    "system_status": "INITIALIZING",
    "mode": "SOVEREIGN",
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "trust_index": 0.0,
    "ethical_drift": 0.0,
    "battery_level": 0,
    "offline_mode": True,
    "pilot_active": False,
    "compliance_score": 0.0,
    "active_frameworks": 0
}

INVARIANT_KEYS = ["schema_version", "system_status", "mode", "last_updated"]

def validate_state(state: dict) -> bool:
    """Comprehensive validation with detailed logging"""
    try:
        if state.get("schema_version") != STATE_SCHEMA_VERSION:
            logger.warning(f"Schema version mismatch: {state.get('schema_version')}")
            return False
        for key in INVARIANT_KEYS:
            if key not in state:
                logger.error(f"Missing invariant: {key}")
                return False
        logger.info("State validation passed")
        return True
    except Exception as e:
        logger.error(f"Validation exception: {e}")
        return False

def get_readonly_snapshot(state: dict) -> dict:
    """Immutable snapshot for external use"""
    return json.loads(json.dumps(state))
