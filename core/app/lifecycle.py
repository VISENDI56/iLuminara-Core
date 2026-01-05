"""
Application lifecycle controller
BOOT → READY → ACTIVE → DEGRADED
"""

LIFECYCLE_STATES = (
    "BOOT",
    "READY",
    "ACTIVE",
    "DEGRADED",
)

DEFAULT_STATE = "BOOT"


def is_valid(state: str) -> bool:
    return state in LIFECYCLE_STATES
