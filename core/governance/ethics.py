"""
Deterministic ethical conflict resolution
"""
from typing import Dict, Any


PRIORITY_ORDER = [
    "human_safety",
    "legal_compliance",
    "data_minimization",
    "operational_efficiency",
]


def resolve(constraints: Dict[str, Any]) -> Dict[str, Any]:
    resolved = {}
    for key in PRIORITY_ORDER:
        if key in constraints:
            resolved[key] = constraints[key]
    return resolved
