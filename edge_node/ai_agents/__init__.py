"""
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
