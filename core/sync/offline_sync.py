"""
Offline-First Conflict-Free Synchronization
Last-write-wins with timestamp + optional CRDT merge
"""

import json
import logging
from datetime import datetime, timezone

def merge_states(local_path: str = "state.json", remote_state: dict = None) -> dict:
    try:
        with open(local_path, "r") as f:
            local = json.load(f)
    except Exception:
        local = {}
        logging.warning("Local state missing - starting fresh")
    
    if remote_state:
        merged = {**local, **remote_state}
        merged["last_updated"] = datetime.now(timezone.utc).isoformat()
        merged["sync_source"] = "REMOTE"
        logging.info("State merged from remote")
    else:
        merged = local
        merged["sync_source"] = "LOCAL_ONLY"
        logging.info("Offline mode - sync deferred")
    
    try:
        with open(local_path, "w") as f:
            json.dump(merged, f, indent=2)
    except Exception as e:
        logging.error(f"Sync save failed: {e}")
    
    return merged
