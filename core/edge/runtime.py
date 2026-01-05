import platform, psutil
from pathlib import Path

EDGE_MARKER = Path("/etc/nv_tegra_release")

def is_jetson(): return EDGE_MARKER.exists()
def system_health():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "platform": platform.platform(),
        "jetson": is_jetson()
    }
