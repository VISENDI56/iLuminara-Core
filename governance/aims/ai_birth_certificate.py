# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

"""
AI Birth Certificate - AIMS Innovation
Provides provenance and birth certificates for AI systems.
"""

from typing import Dict, List, Any
from datetime import datetime
import uuid
import json


class AIBirthCertificate:
    """Digital birth certificate for AI systems."""

    def __init__(self, ai_name: str, creator: str, purpose: str, training_data: Dict[str, Any]):
        self.certificate_id = str(uuid.uuid4())
        self.ai_name = ai_name
        self.creator = creator
        self.purpose = purpose
        self.training_data = training_data
        self.birth_timestamp = datetime.now()
        self.certification_status = "issued"

    def to_dict(self) -> Dict[str, Any]:
        """Convert certificate to dictionary."""
        return {
            'certificate_id': self.certificate_id,
            'ai_name': self.ai_name,
            'creator': self.creator,
            'purpose': self.purpose,
            'training_data_summary': self.training_data,
            'birth_timestamp': self.birth_timestamp.isoformat(),
            'certification_status': self.certification_status
        }

    def validate_integrity(self) -> bool:
        """Validate certificate integrity."""
        # Placeholder validation
        return self.certification_status == "issued"


class AIProvenanceRegistry:
    """Registry for tracking AI provenance and lineage."""

    def __init__(self):
        self.certificates: Dict[str, AIBirthCertificate] = {}
        self.lineage_graph: Dict[str, List[str]] = {}

    def register_ai(self, certificate: AIBirthCertificate) -> str:
        """Register a new AI birth certificate."""
        self.certificates[certificate.certificate_id] = certificate
        self.lineage_graph[certificate.certificate_id] = []
        return certificate.certificate_id

    def establish_lineage(self, parent_id: str, child_id: str):
        """Establish lineage relationship between AI systems."""
        if parent_id in self.lineage_graph:
            self.lineage_graph[parent_id].append(child_id)

    def get_provenance_chain(self, ai_id: str) -> List[Dict[str, Any]]:
        """Get the full provenance chain for an AI."""
        chain = []
        current = ai_id
        while current in self.certificates:
            chain.append(self.certificates[current].to_dict())
            # For simplicity, assume single parent
            parents = [k for k, v in self.lineage_graph.items() if ai_id in v]
            current = parents[0] if parents else None
        return chain

    def audit_provenance(self) -> Dict[str, Any]:
        """Audit all registered AI provenance."""
        return {
            'total_registered': len(self.certificates),
            'lineage_connections': sum(len(v) for v in self.lineage_graph.values()),
            'certificates': [cert.to_dict() for cert in self.certificates.values()]
        }