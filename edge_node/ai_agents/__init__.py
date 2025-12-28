
"""
AI Agents Module
# ============================================================================
# Sovereign Section: Core AI Agent Orchestration
# Specialized AI agents for epidemiological forecasting, multi-scale spatiotemporal
# analysis, and early warning systems that integrate IoT sensor data with community
# health reports.
#
# This module provides autonomous agents that operate within the iLuminara-Core
# framework, respecting sovereignty constraints and compliance requirements.
# ============================================================================
"""

from .epidemiological_forecasting_agent import EpidemiologicalForecastingAgent
from .spatiotemporal_analysis_agent import SpatiotemporalAnalysisAgent
from .early_warning_system_agent import EarlyWarningSystemAgent
from .agent_orchestrator import AgentOrchestrator


__all__ = [
    'EpidemiologicalForecastingAgent',
    'SpatiotemporalAnalysisAgent',
    'EarlyWarningSystemAgent',
    'AgentOrchestrator',
]

# --- Section --- Swahili Medical Intelligence
# Google Cloud AI integration for Swahili medical tasks with sovereignty-first
# architecture. All modules enforce data sovereignty through the governance kernel.
#
# Modules:
#     - swahili_translator: GDPR-compliant Swahili-English medical translation
#     - swahili_entity_extractor: Medical entity extraction from Swahili text
#     - swahili_triage_agent: Dialogflow CX conversational symptom triage
#     - swahili_medical_qa: Gemini Pro medical question answering
#     - hybrid_sync_manager: Edge-cloud synchronization with de-identification
#
# Philosophy: "Intelligence without sovereignty is surveillance."
# ---

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

# --- Section --- Offline & Federated Agents
# Autonomous AI agents designed for offline operation, intermittent connectivity,
# and edge-to-cloud synchronization with privacy-preserving federated learning.
# ---

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
