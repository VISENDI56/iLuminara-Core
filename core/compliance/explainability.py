"""
Right-to-explanation artifact generator
"""
from typing import Dict, Any


def generate_explanation(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "decision_id": record["decision_id"],
        "summary": "This decision was generated under sovereign governance constraints.",
        "inputs_used": list(record["inputs"].keys()),
        "constraints_applied": list(record["constraints_applied"].keys()),
        "policies_referenced": record["policy_references"],
        "human_override": record["human_override"],
    }
