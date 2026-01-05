"""
Full State Migration Engine - Supports Multiple Versions
Auto-upgrade with preservation and validation
"""

import json
import logging
from datetime import datetime, timezone
from .schema import DEFAULT_STATE, STATE_SCHEMA_VERSION, validate_state

logger = logging.getLogger("StateMigration")

def migrate_legacy_to_2026_01(old_state: dict) -> dict:
    """Migration from pre-2026 to current"""
    logger.info("Applying legacy migration")
    new_state = DEFAULT_STATE.copy()
    # Preserve non-invariant data
    for key, value in old_state.items():
        if key not in INVARIANT_KEYS:
            new_state[key] = value
    new_state["schema_version"] = STATE_SCHEMA_VERSION
    return new_state

def load_and_migrate(file_path: str = "state.json") -> dict:
    """Complete load, migrate, validate, save cycle"""
    try:
        with open(file_path, "r") as f:
            state = json.load(f)
        logger.info("State loaded successfully")
    except FileNotFoundError:
        logger.warning("No state file - initializing fresh sovereign state")
        state = DEFAULT_STATE.copy()
    except json.JSONDecodeError as e:
        logger.error(f"Corrupt state file: {e} - resetting to defaults")
        state = DEFAULT_STATE.copy()

    # Migration chain
    current_version = state.get("schema_version")
    if current_version != STATE_SCHEMA_VERSION:
        if current_version is None:
            state = migrate_legacy_to_2026_01(state)
        # Add future migrations here
        logger.info(f"Migrated from {current_version or 'legacy'} to {STATE_SCHEMA_VERSION}")

    state["last_updated"] = datetime.now(timezone.utc).isoformat()

    if not validate_state(state):
        logger.critical("Validation failed post-migration - forcing defaults")
        state = DEFAULT_STATE.copy()

    save_state(state, file_path)
    return state

def save_state(state: dict, file_path: str = "state.json"):
    try:
        with open(file_path, "w") as f:
            json.dump(state, f, indent=2)
        logger.info("State persisted")
    except Exception as e:
        logger.critical(f"State save failed: {e}")
        raise
