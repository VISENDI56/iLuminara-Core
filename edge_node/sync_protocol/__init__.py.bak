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
Edge Node Sync Protocol Module
═══════════════════════════════════════════════════════════════════════════

Provides data synchronization and fusion capabilities for edge deployments.

Components:
- GoldenThread: Data fusion engine merging EMR, CBS, and IDSR streams
- SovereignSync: 80% offline capability with cloud-first fallback
"""

from .golden_thread import GoldenThread, TimeseriesRecord, DataSourceType, VerificationScore
from .sovereign_sync import SovereignSync, CloudUnavailableError

__all__ = [
    'GoldenThread',
    'TimeseriesRecord',
    'DataSourceType',
    'VerificationScore',
    'SovereignSync',
    'CloudUnavailableError',
]
