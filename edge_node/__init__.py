"""
Edge Node: iLuminara's Edge Intelligence Layer
═════════════════════════════════════════════════════════════════════════════

The edge node is the sovereign intelligence layer of iLuminara, capable of
operating independently without cloud connectivity while maintaining full
compliance and medical AI capabilities.

Modules:
    - ai_agents: Swahili medical AI agents (translation, triage, Q&A)
    - frenasa_engine: ML inference engine
    - sync_protocol: Golden Thread data fusion
    - vector_store: Semantic health information retrieval
    - lora_mesh: Low-bandwidth mesh networking

Philosophy: "Intelligence at the edge, sovereignty by design."
"""

from . import ai_agents
from . import frenasa_engine
from . import sync_protocol
from . import vector_store
from . import lora_mesh

__all__ = [
    'ai_agents',
    'frenasa_engine',
    'sync_protocol',
    'vector_store',
    'lora_mesh',
]
