"""
Recovery from partial or failed sync
"""
import json
from pathlib import Path
from core.sync.sync import replay_events

EVENT_DIR = Path("core/sync/events")


def recover():
    events = []
    for path in EVENT_DIR.glob("*.json"):
        with open(path) as f:
            events.append(json.load(f))
    replay_events(events)
    return len(events)
