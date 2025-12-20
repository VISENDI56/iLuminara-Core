"""
Governance Kernel: Ethical and Legal Compliance Engine
═══════════════════════════════════════════════════════

The constitutional guardian of iLuminara-Core, ensuring all actions comply with:
- 14 global legal frameworks (GDPR, HIPAA, KDPA, etc.)
- International humanitarian law (Geneva Conventions)
- WHO outbreak response guidelines (IHR 2005)
"""

from .vector_ledger import (
    SovereignGuardrail,
    SovereigntyViolationError,
    JurisdictionFramework,
    ComplianceAction
)

from .ethical_engine import (
    EthicalEngine,
    HumanitarianViolationError,
    ActionContext
)

__all__ = [
    # Sovereignty and compliance
    'SovereignGuardrail',
    'SovereigntyViolationError',
    'JurisdictionFramework',
    'ComplianceAction',
    # Humanitarian and ethical
    'EthicalEngine',
    'HumanitarianViolationError',
    'ActionContext',
]
