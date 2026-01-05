import uuid, json
from datetime import datetime
from pathlib import Path

GOV_LOG = Path("core/governance/logs")
GOV_LOG.mkdir(exist_ok=True)

def govern(inputs, constraints, outcome, policy_refs):
    decision = {
        "decision_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "inputs": inputs,
        "constraints_applied": constraints,
        "outcome": outcome,
        "policy_refs": policy_refs
    }
    path = GOV_LOG / f"{decision['decision_id']}.json"
    with open(path, "w") as f:
        json.dump(decision, f, indent=2)
    return decision
