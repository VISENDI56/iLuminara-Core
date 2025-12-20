"""
iLuminara AI Agents: Swahili Medical Intelligence
═════════════════════════════════════════════════════════════════════════════

Google Cloud AI integration for Swahili medical tasks with sovereignty-first
architecture. All modules enforce data sovereignty through the governance kernel.

Modules:
    - swahili_translator: GDPR-compliant Swahili-English medical translation
    - swahili_entity_extractor: Medical entity extraction from Swahili text
    - swahili_triage_agent: Dialogflow CX conversational symptom triage
    - swahili_medical_qa: Gemini Pro medical question answering
    - hybrid_sync_manager: Edge-cloud synchronization with de-identification

Philosophy: "Intelligence without sovereignty is surveillance."
"""

from .swahili_translator import SwahiliMedicalTranslator
from .swahili_entity_extractor import SwahiliMedicalEntityExtractor
from .swahili_triage_agent import SwahiliTriageAgent
from .swahili_medical_qa import SwahiliMedicalQA
from .hybrid_sync_manager import HybridSyncManager

__all__ = [
    'SwahiliMedicalTranslator',
    'SwahiliMedicalEntityExtractor',
    'SwahiliTriageAgent',
    'SwahiliMedicalQA',
    'HybridSyncManager',
]

__version__ = "1.0.0"
AI Agents Module
═════════════════════════════════════════════════════════════════════════════

Autonomous AI agents designed for offline operation, intermittent connectivity,
and edge-to-cloud synchronization with privacy-preserving federated learning.
"""

from .base_agent import BaseAgent, AgentCapability, AgentStatus
from .offline_agent import OfflineAgent
from .federated_client import FederatedLearningClient
from .agent_registry import AgentRegistry

__all__ = [
    "BaseAgent",
    "AgentCapability",
    "AgentStatus",
    "OfflineAgent",
    "FederatedLearningClient",
    "AgentRegistry",
]
