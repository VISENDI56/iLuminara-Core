"""
Append-only event log for offline safety
"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

EVENT_DIR = Path("core/sync/events")
EVENT_DIR.mkdir(exist_ok=True)


def append_event(event_type: str, payload: Dict[str, Any]):
    event = {
        "event_id": str(uuid.uuid4()),
        "type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload,
    }

    path = EVENT_DIR / f"{event['event_id']}.json"
    with open(path, "w") as f:
        json.dump(event, f, indent=2)

    return event
