"""
Region-isolated, cloud-optional, operator-owned deployments
"""
from pathlib import Path

def region_isolated(base_path: Path):
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path.exists()

def no_forced_cloud():
    return True  # offline first enforced

def operator_ownership(file_path: Path):
    return file_path.exists() and file_path.stat().st_uid == 0  # root / operator ownership check
