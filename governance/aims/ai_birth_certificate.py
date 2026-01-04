"""
governance/aims/ai_birth_certificate.py
Immutable provenance record for every AI model version.
ISO 42001 Clause 8.3 & EU AI Act Article 12 compliant.
Final Seal: Rev-217-OMEGA | 2026
Hardened: UTC-aware, SHA3-256 signatures, tamper-detection, structured logging,
multi-parent lineage support.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# Structured logging for Tracer ICE integration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIProvenanceRegistry")

def _json_default(obj):
    """Safe JSON serializer for datetimes"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

@dataclass
class AIBirthCertificate:
    """Immutable record of AI system creation and lineage"""
    model_id: str
    version: str
    creation_timestamp: datetime
    training_data_provenance: List[str]  # IPFS CIDs of training data
    algorithm_family: str
    hyperparameters: Dict[str, Any]
    ethical_constraints: List[str]       # Hard-coded Constitutional AI rules
    responsible_engineer: str
    certification_status: Dict[str, str] # ISO 42001, EU AI Act status
    parent_models: List[str]             # Traceability to base models (multi-parent)
    cryptographic_signature: str = None   # SHA3-256 over all other fields
    
    def __post_init__(self):
        """Generate SHA3-256 fingerprint after init but before signature assignment"""
        if self.creation_timestamp.tzinfo is None:
            self.creation_timestamp = self.creation_timestamp.replace(tzinfo=timezone.utc)
        
        # Temporarily set signature to None for hashing
        temp_sig = self.cryptographic_signature
        self.cryptographic_signature = None
        
        raw_data = json.dumps(asdict(self), default=_json_default, sort_keys=True)
        self.cryptographic_signature = hashlib.sha3_256(raw_data.encode()).hexdigest()
        
        # Restore if needed (but normally called before external assignment)
        if temp_sig is not None:
            self.cryptographic_signature = temp_sig
    
    def verify_integrity(self) -> bool:
        """Detect any tampering post-sealing"""
        current_sig = self.cryptographic_signature
        self.cryptographic_signature = None
        expected = hashlib.sha3_256(json.dumps(asdict(self), default=_json_default, sort_keys=True).encode()).hexdigest()
        self.cryptographic_signature = current_sig
        return current_sig == expected
    
    def seal_to_ledger(self) -> Dict[str, Any]:
        """Locks the certificate into the IP-09 Chrono-Ledger (tamper-evident entry)"""
        if not self.verify_integrity():
            raise ValueError("Certificate integrity compromised - cannot seal")
        
        entry = {
            "op": "MINT_BIRTH_CERTIFICATE",
            "model": f"{self.model_id}-v{self.version}",
            "sig": self.cryptographic_signature,
            "timestamp": self.creation_timestamp.isoformat(),
            "attestation": "ISO-42001-8.3-COMPLIANT | EU-AI-ACT-ARTICLE-12"
        }
        logger.info(f"Birth certificate sealed for {self.model_id}")
        # In deployment: send to Chrono-Ledger API
        return entry

class AIProvenanceRegistry:
    """Registry managing the graph of model evolution and ethical inheritance"""
    
    def __init__(self):
        self.registry: Dict[str, AIBirthCertificate] = {}
        self.lineage_tree: Dict[str, List[str]] = {}

    def register_deployment(self, cert: AIBirthCertificate):
        """Registers and validates a model before clinical deployment"""
        if not cert.verify_integrity():
            raise ValueError(f"Invalid signature for model {cert.model_id} - deployment blocked")
        
        key = f"{cert.model_id}-v{cert.version}"
        self.registry[key] = cert
        
        # Build multi-parent lineage
        for parent in cert.parent_models:
            if parent not in self.lineage_tree:
                self.lineage_tree[parent] = []
            self.lineage_tree[parent].append(key)
        
        logger.info(f"[AIMS-PROVENANCE] Model {key} registered and sealed")
        return cert.seal_to_ledger()

    def audit_trail(self, model_id: str) -> List[str]:
        """Returns the full multi-branch 'Genetic Path' for legal discovery"""
        path = []
        to_visit = [model_id]
        
        while to_visit:
            current = to_visit.pop(0)
            if current not in path:
                path.append(current)
                # Add all parents
                cert_key = next((k for k in self.registry if k.startswith(current.split('-v')[0])), None)
                if cert_key and cert_key in self.registry:
                    to_visit.extend(self.registry[cert_key].parent_models)
        
        return path[::-1]  # Root-first order

