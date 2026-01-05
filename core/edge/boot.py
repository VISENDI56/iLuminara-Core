"""
Edge-only boot path with no cloud dependency
"""
from core.state.sovereign_bus import bus
from core.edge.runtime import system_health


def boot_edge():
    health = system_health()

    bus.set("hardware_health", health)
    bus.set("status", "ACTIVE" if health["cpu_percent"] < 95 else "DEGRADED")

    return health
