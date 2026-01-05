"""
Structured governance event logger
"""
import json
from pathlib import Path
from typing import Dict, Any

LOG_DIR = Path("governance_logs")
LOG_DIR.mkdir(exist_ok=True)

def log_decision(record: Dict[str, Any]):
    decision_id = record["decision_id"]
    path = LOG_DIR / f"{decision_id}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    return path
