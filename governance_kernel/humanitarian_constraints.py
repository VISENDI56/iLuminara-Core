"""
Humanitarian Constraint Encoding System
═════════════════════════════════════════════════════════════════════════════

Implements three critical components for humanitarian operations:
1. Vertex AI Explainable AI integration with SHAP analysis
2. Cloud Functions for real-time constraint checking
3. Secret Manager for secure storage of humanitarian protocols

Philosophy: "Every decision affecting human welfare must be transparent and auditable."
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import hashlib


class ConstraintSeverity(Enum):
    """Severity levels for humanitarian constraint violations."""
    CRITICAL = "CRITICAL"  # Immediate threat to life or dignity
    HIGH = "HIGH"  # Significant humanitarian concern
    MEDIUM = "MEDIUM"  # Moderate concern requiring monitoring
    LOW = "LOW"  # Minor procedural concern
    INFO = "INFO"  # Informational only


class ConstraintCategory(Enum):
    """Categories of humanitarian constraints."""
    MEDICAL_ETHICS = "Medical Ethics"
    RESOURCE_ALLOCATION = "Resource Allocation"
    DATA_SOVEREIGNTY = "Data Sovereignty"
    POPULATION_PROTECTION = "Population Protection"
    EMERGENCY_RESPONSE = "Emergency Response"
    CONSENT_DIGNITY = "Consent & Dignity"


@dataclass
class HumanitarianProtocol:
    """
    Represents a humanitarian protocol that must be followed.
    
    These protocols encode international humanitarian standards
    (WHO, ICRC, Sphere Standards, etc.) into executable constraints.
    """
    protocol_id: str
    name: str
    category: ConstraintCategory
    severity: ConstraintSeverity
    description: str
    constraint_function: str  # Name of the validation function
    parameters: Dict[str, Any] = field(default_factory=dict)
    legal_citations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"


@dataclass
class SHAPExplanation:
    """
    SHAP (SHapley Additive exPlanations) values for model explainability.
    
    Provides transparent insights into why a particular decision was made,
    fulfilling the "Right to Explanation" requirements.
    """
    decision_id: str
    model_prediction: Any
    base_value: float
    shap_values: Dict[str, float]  # feature_name -> SHAP value
    feature_values: Dict[str, Any]  # feature_name -> actual value
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def get_top_contributors(self, n: int = 5) -> List[Tuple[str, float]]:
        """Get top N features contributing to the decision."""
        sorted_features = sorted(
            self.shap_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        return sorted_features[:n]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize explanation to dictionary."""
        return {
            "decision_id": self.decision_id,
            "model_prediction": self.model_prediction,
            "base_value": self.base_value,
            "shap_values": self.shap_values,
            "feature_values": self.feature_values,
            "top_contributors": [
                {"feature": feat, "shap_value": val}
                for feat, val in self.get_top_contributors()
            ],
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ConstraintViolation:
    """Represents a detected violation of humanitarian constraints."""
    violation_id: str
    protocol_id: str
    severity: ConstraintSeverity
    category: ConstraintCategory
    description: str
    affected_entities: List[str]  # Patient IDs, location IDs, etc.
    remediation_steps: List[str]
    detected_at: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False
    shap_explanation: Optional[SHAPExplanation] = None


class VertexAIExplainableAI:
    """
    Integration with Google Cloud Vertex AI for explainable AI capabilities.
    
    Provides SHAP analysis for model predictions to ensure transparency
    in high-risk clinical decisions.
    
    Note: This is a framework implementation. In production, this would
    connect to actual Vertex AI services with proper authentication.
    """
    
    def __init__(self, project_id: str = "iluminara-core", region: str = "us-central1"):
        """Initialize Vertex AI client."""
        self.project_id = project_id
        self.region = region
        self.endpoint = f"https://{region}-aiplatform.googleapis.com"
        self.explanations_cache = {}
    
    def explain_prediction(
        self,
        model_id: str,
        input_data: Dict[str, Any],
        prediction: Any,
        feature_names: List[str],
    ) -> SHAPExplanation:
        """
        Generate SHAP explanation for a model prediction.
        
        In production, this would call Vertex AI Explainable AI API.
        For now, it generates a simulated SHAP analysis based on input features.
        
        Args:
            model_id: Identifier for the ML model
            input_data: Input features used for prediction
            prediction: The model's prediction
            feature_names: Names of input features
        
        Returns:
            SHAPExplanation with feature attributions
        """
        # Generate decision ID
        decision_id = self._generate_decision_id(model_id, input_data)
        
        # Simulate SHAP values (in production, this would call Vertex AI)
        shap_values = self._calculate_shap_values(input_data, feature_names)
        
        # Base value (average model output)
        base_value = self._get_base_value(model_id)
        
        explanation = SHAPExplanation(
            decision_id=decision_id,
            model_prediction=prediction,
            base_value=base_value,
            shap_values=shap_values,
            feature_values=input_data,
        )
        
        # Cache the explanation for audit trail
        self.explanations_cache[decision_id] = explanation
        
        return explanation
    
    def _generate_decision_id(self, model_id: str, input_data: Dict[str, Any]) -> str:
        """Generate unique decision ID."""
        data_str = json.dumps(input_data, sort_keys=True)
        hash_obj = hashlib.sha256(f"{model_id}:{data_str}".encode())
        return f"DECISION-{hash_obj.hexdigest()[:16]}"
    
    def _calculate_shap_values(
        self,
        input_data: Dict[str, Any],
        feature_names: List[str],
    ) -> Dict[str, float]:
        """
        Calculate SHAP values for features.
        
        In production, this would use Vertex AI's integrated SHAP support.
        This implementation provides a framework-level simulation.
        """
        shap_values = {}
        
        # Simulate SHAP values based on feature importance heuristics
        for feature in feature_names:
            if feature in input_data:
                value = input_data[feature]
                
                # High-risk features get higher attribution
                if any(keyword in feature.lower() for keyword in ["severity", "risk", "critical"]):
                    if isinstance(value, (int, float)):
                        shap_values[feature] = float(value) * 0.15
                    else:
                        shap_values[feature] = 0.2
                
                # Location features
                elif "location" in feature.lower():
                    shap_values[feature] = 0.1
                
                # Symptom/diagnosis features
                elif any(keyword in feature.lower() for keyword in ["symptom", "diagnosis"]):
                    shap_values[feature] = 0.12
                
                # Default attribution
                else:
                    if isinstance(value, (int, float)):
                        shap_values[feature] = float(value) * 0.05
                    else:
                        shap_values[feature] = 0.05
        
        return shap_values
    
    def _get_base_value(self, model_id: str) -> float:
        """Get base value (average prediction) for the model."""
        # In production, this would be retrieved from model metadata
        return 0.5
    
    def get_explanation(self, decision_id: str) -> Optional[SHAPExplanation]:
        """Retrieve cached explanation by decision ID."""
        return self.explanations_cache.get(decision_id)
    
    def validate_explainability(self, explanation: SHAPExplanation) -> bool:
        """
        Validate that an explanation meets transparency requirements.
        
        Enforces EU AI Act §6 and GDPR Art. 22 requirements for
        high-risk AI system explainability.
        """
        # Must have at least 3 contributing features
        if len(explanation.shap_values) < 3:
            return False
        
        # Top contributor must explain at least 10% of decision
        top_contributors = explanation.get_top_contributors(1)
        if not top_contributors or abs(top_contributors[0][1]) < 0.1:
            return False
        
        return True


class CloudFunctionConstraintChecker:
    """
    Real-time constraint checking system designed for deployment as
    Google Cloud Functions for serverless, scalable validation.
    
    Each constraint check can be deployed as an independent Cloud Function,
    enabling parallel validation and low-latency constraint enforcement.
    """
    
    def __init__(self):
        """Initialize constraint checker with humanitarian protocols."""
        self.protocols = self._load_humanitarian_protocols()
        self.violation_log = []
    
    def _load_humanitarian_protocols(self) -> Dict[str, HumanitarianProtocol]:
        """
        Load humanitarian protocols from secure storage.
        
        In production, this would load from Secret Manager.
        """
        protocols = {
            "MEDICAL_TRIAGE": HumanitarianProtocol(
                protocol_id="PROTO-001",
                name="Medical Triage Protocol",
                category=ConstraintCategory.MEDICAL_ETHICS,
                severity=ConstraintSeverity.CRITICAL,
                description="Ensures fair and ethical triage in resource-constrained settings",
                constraint_function="check_triage_fairness",
                legal_citations=["WHO Emergency Triage Guidelines", "ICRC Medical Ethics"],
            ),
            "RESOURCE_EQUITY": HumanitarianProtocol(
                protocol_id="PROTO-002",
                name="Resource Allocation Equity",
                category=ConstraintCategory.RESOURCE_ALLOCATION,
                severity=ConstraintSeverity.HIGH,
                description="Prevents discriminatory resource allocation",
                constraint_function="check_resource_equity",
                legal_citations=["Sphere Standards", "UN Humanitarian Principles"],
            ),
            "DATA_PROTECTION": HumanitarianProtocol(
                protocol_id="PROTO-003",
                name="Humanitarian Data Protection",
                category=ConstraintCategory.DATA_SOVEREIGNTY,
                severity=ConstraintSeverity.CRITICAL,
                description="Protects sensitive humanitarian data from misuse",
                constraint_function="check_data_protection",
                legal_citations=["ICRC Data Protection Policy", "GDPR Art. 9"],
            ),
            "VULNERABLE_POPULATIONS": HumanitarianProtocol(
                protocol_id="PROTO-004",
                name="Vulnerable Population Protection",
                category=ConstraintCategory.POPULATION_PROTECTION,
                severity=ConstraintSeverity.CRITICAL,
                description="Ensures special protections for vulnerable groups",
                constraint_function="check_vulnerable_protection",
                legal_citations=["UN Convention on Rights of the Child", "UNHCR Guidelines"],
            ),
            "EMERGENCY_ACCESS": HumanitarianProtocol(
                protocol_id="PROTO-005",
                name="Emergency Healthcare Access",
                category=ConstraintCategory.EMERGENCY_RESPONSE,
                severity=ConstraintSeverity.CRITICAL,
                description="Guarantees access to emergency healthcare regardless of circumstances",
                constraint_function="check_emergency_access",
                legal_citations=["WHO Constitution Art. 25", "Geneva Conventions"],
            ),
        }
        
        return protocols
    
    def check_constraint(
        self,
        protocol_id: str,
        action_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, Optional[ConstraintViolation]]:
        """
        Check if an action violates a humanitarian constraint.
        
        This method can be deployed as a Cloud Function for real-time validation.
        
        Args:
            protocol_id: ID of the protocol to check
            action_data: Data about the action being validated
            context: Additional context for validation
        
        Returns:
            Tuple of (is_valid, violation_if_any)
        """
        protocol = self.protocols.get(protocol_id)
        if not protocol:
            raise ValueError(f"Unknown protocol: {protocol_id}")
        
        # Route to appropriate constraint function
        constraint_function = getattr(self, protocol.constraint_function, None)
        if not constraint_function:
            raise ValueError(f"Constraint function not found: {protocol.constraint_function}")
        
        # Execute constraint check
        is_valid, violation_data = constraint_function(action_data, context or {})
        
        if not is_valid:
            violation = self._create_violation(protocol, violation_data)
            self.violation_log.append(violation)
            return False, violation
        
        return True, None
    
    def check_triage_fairness(
        self,
        action_data: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate medical triage decisions for fairness and ethics.
        
        Ensures triage is based solely on medical need, not on discriminatory factors.
        """
        # Extract triage decision parameters
        priority_level = action_data.get("priority_level")
        patient_demographics = action_data.get("patient_demographics", {})
        medical_severity = action_data.get("medical_severity")
        
        # Check for discriminatory factors
        protected_attributes = ["race", "ethnicity", "nationality", "religion", "gender"]
        if any(attr in action_data.get("decision_factors", []) for attr in protected_attributes):
            return False, {
                "reason": "Triage decision includes protected demographic attributes",
                "affected_entities": [action_data.get("patient_id", "UNKNOWN")],
                "remediation": [
                    "Remove demographic factors from triage algorithm",
                    "Base decision solely on medical severity and resource availability",
                    "Retrain model without protected attributes",
                ],
            }
        
        # Check for minimum medical justification
        if not medical_severity or medical_severity == "UNKNOWN":
            return False, {
                "reason": "Triage decision lacks medical severity justification",
                "affected_entities": [action_data.get("patient_id", "UNKNOWN")],
                "remediation": [
                    "Obtain medical severity assessment",
                    "Document clinical rationale for triage priority",
                ],
            }
        
        return True, None
    
    def check_resource_equity(
        self,
        action_data: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate resource allocation for equity and fairness.
        
        Prevents systematic bias in resource distribution.
        """
        resource_type = action_data.get("resource_type")
        allocation_method = action_data.get("allocation_method")
        beneficiaries = action_data.get("beneficiaries", [])
        
        # Check for minimum coverage
        if len(beneficiaries) == 0:
            return False, {
                "reason": "Resource allocation has no documented beneficiaries",
                "affected_entities": ["SYSTEM"],
                "remediation": [
                    "Document beneficiary list",
                    "Ensure transparent allocation criteria",
                ],
            }
        
        # Check for allocation method transparency
        if not allocation_method or allocation_method == "UNSPECIFIED":
            return False, {
                "reason": "Resource allocation method not specified",
                "affected_entities": beneficiaries,
                "remediation": [
                    "Specify allocation methodology",
                    "Document equity criteria",
                    "Ensure audit trail for all allocations",
                ],
            }
        
        return True, None
    
    def check_data_protection(
        self,
        action_data: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate data protection measures for humanitarian data.
        
        Humanitarian data requires extra protection due to vulnerability of subjects.
        """
        data_type = action_data.get("data_type")
        encryption_status = action_data.get("encryption_status")
        access_control = action_data.get("access_control")
        
        # Critical: Humanitarian PHI must be encrypted
        if data_type == "PHI" and encryption_status != "ENCRYPTED":
            return False, {
                "reason": "Humanitarian PHI not encrypted",
                "affected_entities": action_data.get("affected_patients", []),
                "remediation": [
                    "Enable encryption at rest and in transit",
                    "Use AES-256 or equivalent",
                    "Implement key rotation policy",
                ],
            }
        
        # Must have role-based access control
        if not access_control or access_control == "NONE":
            return False, {
                "reason": "No access control on humanitarian data",
                "affected_entities": action_data.get("affected_patients", []),
                "remediation": [
                    "Implement role-based access control (RBAC)",
                    "Define access policies for humanitarian workers",
                    "Enable audit logging for all access",
                ],
            }
        
        return True, None
    
    def check_vulnerable_protection(
        self,
        action_data: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate special protections for vulnerable populations.
        
        Includes children, refugees, displaced persons, elderly, disabled.
        """
        vulnerable_categories = action_data.get("vulnerable_categories", [])
        protection_measures = action_data.get("protection_measures", [])
        
        # If vulnerable populations identified, must have protection measures
        if vulnerable_categories and not protection_measures:
            return False, {
                "reason": "Vulnerable populations identified without protection measures",
                "affected_entities": action_data.get("affected_individuals", []),
                "remediation": [
                    "Implement enhanced consent procedures for vulnerable groups",
                    "Provide additional safeguards (e.g., guardian consent for minors)",
                    "Ensure culturally appropriate communication",
                    "Document special considerations in care plan",
                ],
            }
        
        return True, None
    
    def check_emergency_access(
        self,
        action_data: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate emergency healthcare access requirements.
        
        Emergency care must be provided regardless of ability to pay,
        documentation status, or other barriers.
        """
        emergency_severity = action_data.get("emergency_severity")
        access_barriers = action_data.get("access_barriers", [])
        
        # Critical emergencies cannot be blocked by administrative barriers
        if emergency_severity in ["CRITICAL", "LIFE_THREATENING"]:
            blocking_barriers = [
                b for b in access_barriers
                if b in ["PAYMENT_REQUIRED", "DOCUMENTATION_MISSING", "INSURANCE_VERIFICATION"]
            ]
            
            if blocking_barriers:
                return False, {
                    "reason": f"Life-threatening emergency blocked by: {', '.join(blocking_barriers)}",
                    "affected_entities": [action_data.get("patient_id", "UNKNOWN")],
                    "remediation": [
                        "Remove administrative barriers for emergency care",
                        "Provide immediate treatment per Geneva Conventions",
                        "Handle documentation/payment after stabilization",
                        "Escalate to humanitarian coordinator if needed",
                    ],
                }
        
        return True, None
    
    def _create_violation(
        self,
        protocol: HumanitarianProtocol,
        violation_data: Dict[str, Any],
    ) -> ConstraintViolation:
        """Create a ConstraintViolation object from violation data."""
        violation_id = self._generate_violation_id(protocol.protocol_id)
        
        return ConstraintViolation(
            violation_id=violation_id,
            protocol_id=protocol.protocol_id,
            severity=protocol.severity,
            category=protocol.category,
            description=violation_data.get("reason", "Constraint violation detected"),
            affected_entities=violation_data.get("affected_entities", []),
            remediation_steps=violation_data.get("remediation", []),
        )
    
    def _generate_violation_id(self, protocol_id: str) -> str:
        """Generate unique violation ID."""
        timestamp = datetime.utcnow().isoformat()
        hash_obj = hashlib.sha256(f"{protocol_id}:{timestamp}".encode())
        return f"VIOLATION-{hash_obj.hexdigest()[:16]}"
    
    def get_violations(
        self,
        severity: Optional[ConstraintSeverity] = None,
        unresolved_only: bool = True,
    ) -> List[ConstraintViolation]:
        """Retrieve logged violations with optional filtering."""
        violations = self.violation_log
        
        if unresolved_only:
            violations = [v for v in violations if not v.resolved]
        
        if severity:
            violations = [v for v in violations if v.severity == severity]
        
        return violations


class SecretManagerProtocolStore:
    """
    Integration with Google Cloud Secret Manager for secure storage
    of humanitarian protocols and sensitive configurations.
    
    Humanitarian protocols often contain sensitive information about
    operational procedures, contact information, and access credentials
    that must be protected while remaining accessible to authorized systems.
    """
    
    def __init__(self, project_id: str = "iluminara-core"):
        """Initialize Secret Manager client."""
        self.project_id = project_id
        self.secrets_cache = {}  # In-memory cache for accessed secrets
    
    def store_protocol(
        self,
        protocol: HumanitarianProtocol,
        secret_name: Optional[str] = None,
    ) -> str:
        """
        Store a humanitarian protocol in Secret Manager.
        
        Args:
            protocol: The protocol to store
            secret_name: Optional custom secret name (defaults to protocol_id)
        
        Returns:
            Secret name/path in Secret Manager
        """
        secret_name = secret_name or f"humanitarian-protocol-{protocol.protocol_id}"
        
        # Serialize protocol
        protocol_data = {
            "protocol_id": protocol.protocol_id,
            "name": protocol.name,
            "category": protocol.category.value,
            "severity": protocol.severity.value,
            "description": protocol.description,
            "constraint_function": protocol.constraint_function,
            "parameters": protocol.parameters,
            "legal_citations": protocol.legal_citations,
            "created_at": protocol.created_at.isoformat(),
            "version": protocol.version,
        }
        
        # In production, this would call Secret Manager API
        # For now, we store in local cache with encryption simulation
        encrypted_data = self._simulate_encryption(json.dumps(protocol_data))
        self.secrets_cache[secret_name] = encrypted_data
        
        return f"projects/{self.project_id}/secrets/{secret_name}"
    
    def retrieve_protocol(self, secret_name: str) -> Optional[HumanitarianProtocol]:
        """
        Retrieve a humanitarian protocol from Secret Manager.
        
        Args:
            secret_name: Name of the secret in Secret Manager
        
        Returns:
            HumanitarianProtocol object or None if not found
        """
        # In production, this would call Secret Manager API
        encrypted_data = self.secrets_cache.get(secret_name)
        if not encrypted_data:
            return None
        
        # Decrypt and deserialize
        decrypted_data = self._simulate_decryption(encrypted_data)
        protocol_dict = json.loads(decrypted_data)
        
        # Reconstruct protocol object
        protocol = HumanitarianProtocol(
            protocol_id=protocol_dict["protocol_id"],
            name=protocol_dict["name"],
            category=ConstraintCategory(protocol_dict["category"]),
            severity=ConstraintSeverity(protocol_dict["severity"]),
            description=protocol_dict["description"],
            constraint_function=protocol_dict["constraint_function"],
            parameters=protocol_dict.get("parameters", {}),
            legal_citations=protocol_dict.get("legal_citations", []),
            created_at=datetime.fromisoformat(protocol_dict["created_at"]),
            version=protocol_dict.get("version", "1.0"),
        )
        
        return protocol
    
    def list_protocols(self) -> List[str]:
        """List all stored protocol secret names."""
        return [name for name in self.secrets_cache.keys() if "humanitarian-protocol" in name]
    
    def delete_protocol(self, secret_name: str) -> bool:
        """
        Delete a protocol from Secret Manager.
        
        Args:
            secret_name: Name of the secret to delete
        
        Returns:
            True if deleted successfully
        """
        if secret_name in self.secrets_cache:
            del self.secrets_cache[secret_name]
            return True
        return False
    
    def _simulate_encryption(self, data: str) -> str:
        """
        Simulate encryption for Secret Manager storage.
        
        In production, Secret Manager handles encryption automatically
        using Google-managed or customer-managed keys (CMEK).
        """
        # Simple base64-like simulation (NOT SECURE - for framework only)
        import base64
        return base64.b64encode(data.encode()).decode()
    
    def _simulate_decryption(self, encrypted_data: str) -> str:
        """Simulate decryption for Secret Manager retrieval."""
        import base64
        return base64.b64decode(encrypted_data.encode()).decode()


# ═════════════════════════════════════════════════════════════════════════════
# Humanitarian Constraint Encoding System
# 
# Integrates three Google Cloud Platform services to ensure transparent,
# accountable, and secure humanitarian operations:
#
# 1. Vertex AI Explainable AI: SHAP analysis for decision transparency
# 2. Cloud Functions: Real-time constraint checking at scale
# 3. Secret Manager: Secure storage of humanitarian protocols
#
# Philosophy: "Every decision affecting human welfare must be transparent,
#             auditable, and aligned with humanitarian principles."
# ═════════════════════════════════════════════════════════════════════════════
