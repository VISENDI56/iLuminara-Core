"""
Public Health Integration Module
================================

This module integrates global health strategies and interventions into iLuminara-Core,
focusing on sanitation, digital health, surveillance, governance, and generative AI.

Modules:
- sanitation: Targeted sanitation interventions for diarrhea prevention
- digital_strategy: WHO Global Strategy on Digital Health 2020-2025
- surveillance: AI-enhanced public health surveillance
- governance: African AI governance frameworks
- genai: Generative AI applications in public health
"""

from .sanitation.targeted_wash import SanitationInterventionEngine

__all__ = [
    'SanitationInterventionEngine'
]