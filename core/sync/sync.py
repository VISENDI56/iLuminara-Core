"""
Conflict-free state synchronization
Last-write-wins with event replay
"""
from core.state.sovereign_bus import bus
from core.sync.event_log import append_event


def record_state_change(key, value):
    append_event("STATE_CHANGE", {"key": key, "value": value})
    bus.set(key, value)


def replay_events(events):
    for event in sorted(events, key=lambda e: e["timestamp"]):
        payload = event["payload"]
        bus.set(payload["key"], payload["value"])
