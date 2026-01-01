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
Swahili AI Agents Configuration
═════════════════════════════════════════════════════════════════════════════

Configuration loader for Swahili AI agents with environment variable support.

Usage:
    from edge_node.ai_agents.config import SwahiliAIConfig
    
    config = SwahiliAIConfig()
    translator = SwahiliMedicalTranslator(
        project_id=config.google_cloud_project,
        location=config.google_cloud_region
    )
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class SwahiliAIConfig:
    """Configuration for Swahili AI agents."""
    
    # Google Cloud Configuration
    google_cloud_project: str = os.getenv('GOOGLE_CLOUD_PROJECT', 'iluminara-production')
    google_cloud_region: str = os.getenv('GOOGLE_CLOUD_REGION', 'europe-west4')
    google_application_credentials: str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    
    # Dialogflow CX
    dialogflow_agent_id: Optional[str] = os.getenv('DIALOGFLOW_AGENT_ID')
    dialogflow_location: str = os.getenv('DIALOGFLOW_LOCATION', 'europe-west4')
    
    # Vertex AI
    vertex_ai_endpoint: Optional[str] = os.getenv('VERTEX_AI_ENDPOINT')
    
    # Gemini Pro
    gemini_api_key: Optional[str] = os.getenv('GEMINI_API_KEY')
    
    # Data Sync
    gcs_sync_bucket: str = os.getenv('GCS_SYNC_BUCKET', 'iluminara-edge-sync-eu')
    sync_interval_seconds: int = int(os.getenv('SYNC_INTERVAL_SECONDS', '3600'))
    
    # Sovereignty Settings
    jurisdiction: str = os.getenv('JURISDICTION', 'GDPR_EU')
    allow_cloud_sync: bool = os.getenv('ALLOW_CLOUD_SYNC', 'true').lower() == 'true'
    
    # Feature Flags
    enable_translation: bool = os.getenv('ENABLE_TRANSLATION', 'true').lower() == 'true'
    enable_entity_extraction: bool = os.getenv('ENABLE_ENTITY_EXTRACTION', 'true').lower() == 'true'
    enable_triage_agent: bool = os.getenv('ENABLE_TRIAGE_AGENT', 'true').lower() == 'true'
    enable_medical_qa: bool = os.getenv('ENABLE_MEDICAL_QA', 'true').lower() == 'true'
    enable_cloud_sync: bool = os.getenv('ENABLE_CLOUD_SYNC', 'true').lower() == 'true'
    
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            True if configuration is valid
        """
        if not self.google_cloud_project:
            print("⚠️  GOOGLE_CLOUD_PROJECT not set")
            return False
        
        if self.enable_cloud_sync and not self.gcs_sync_bucket:
            print("⚠️  GCS_SYNC_BUCKET not set but cloud sync is enabled")
            return False
        
        return True
    
    def __str__(self) -> str:
        """Return configuration summary."""
        return f"""
Swahili AI Configuration:
  Project: {self.google_cloud_project}
  Region: {self.google_cloud_region}
  Jurisdiction: {self.jurisdiction}
  Cloud Sync: {'Enabled' if self.enable_cloud_sync else 'Disabled'}
  Features: Translation={self.enable_translation}, EntityExtraction={self.enable_entity_extraction}, Triage={self.enable_triage_agent}, QA={self.enable_medical_qa}
"""


# Global configuration instance
config = SwahiliAIConfig()
