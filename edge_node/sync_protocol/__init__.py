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
