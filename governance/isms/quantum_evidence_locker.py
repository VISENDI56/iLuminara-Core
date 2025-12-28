"""
Quantum Evidence Locker - ISMS Innovation
Provides quantum-resistant secure storage for audit evidence.
"""

from typing import Dict, List, Any
from datetime import datetime
import hashlib
import json


class QuantumResistantEvidenceLocker:
    """Secure evidence storage with quantum resistance."""

    def __init__(self):
        self.evidence_store: Dict[str, Dict[str, Any]] = {}
        self.integrity_hashes: Dict[str, str] = {}

    def store_evidence(self, evidence_id: str, evidence_data: Dict[str, Any]) -> str:
        """Store evidence with quantum-resistant integrity."""
        # Create integrity hash
        data_str = json.dumps(evidence_data, sort_keys=True)
        integrity_hash = hashlib.sha256(data_str.encode()).hexdigest()

        evidence_entry = {
            'evidence_id': evidence_id,
            'data': evidence_data,
            'timestamp': datetime.now().isoformat(),
            'integrity_hash': integrity_hash
        }

        self.evidence_store[evidence_id] = evidence_entry
        self.integrity_hashes[evidence_id] = integrity_hash

        return evidence_id

    def retrieve_evidence(self, evidence_id: str) -> Dict[str, Any]:
        """Retrieve evidence and verify integrity."""
        if evidence_id not in self.evidence_store:
            raise ValueError(f"Evidence {evidence_id} not found")

        evidence = self.evidence_store[evidence_id]
        # Verify integrity
        data_str = json.dumps(evidence['data'], sort_keys=True)
        current_hash = hashlib.sha256(data_str.encode()).hexdigest()

        if current_hash != evidence['integrity_hash']:
            raise ValueError(f"Evidence integrity compromised for {evidence_id}")

        return evidence

    def audit_evidence_chain(self) -> Dict[str, Any]:
        """Audit the entire evidence chain."""
        compromised = []
        valid = []

        for evidence_id in self.evidence_store:
            try:
                self.retrieve_evidence(evidence_id)
                valid.append(evidence_id)
            except ValueError:
                compromised.append(evidence_id)

        return {
            'total_evidence': len(self.evidence_store),
            'valid_evidence': len(valid),
            'compromised_evidence': len(compromised),
            'integrity_status': 'secure' if not compromised else 'compromised'
        }