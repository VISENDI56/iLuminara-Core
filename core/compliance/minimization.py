"""
Data minimization enforcement
"""
from typing import Dict, Any, Iterable


def minimize(inputs: Dict[str, Any], allowed_keys: Iterable[str]) -> Dict[str, Any]:
    return {k: v for k, v in inputs.items() if k in allowed_keys}
