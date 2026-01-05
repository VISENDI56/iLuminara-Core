"""
Decision provenance model
Every inference is traceable, explainable, and auditable
"""
from datetime import datetime
from typing import Dict, Any
import uuid


def new_provenance(
    inputs: Dict[str, Any],
    constraints: Dict[str, Any],
    outcome: Dict[str, Any],
    policy_refs: Dict[str, str],
    overridden: bool = False,
    override_actor: str | None = None,
):
    return {
        "decision_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "inputs": inputs,
        "constraints_applied": constraints,
        "outcome": outcome,
        "policy_references": policy_refs,
        "human_override": {
            "applied": overridden,
            "actor": override_actor,
        },
    }
