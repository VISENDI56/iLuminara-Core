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
5DM Distribution Gateway Module
═════════════════════════════════════════════════════════════════════════════

Exports the Distribution Bridge API for integrating iLuminara health signals
into 5DM Africa's existing content distribution networks.

Usage:
    from edge_node.distribution_gateway import DistributionBridge, ChannelStats, get_live_network_stats
    
    bridge = DistributionBridge()
    result = bridge.inject_signal({"alert": "CHOLERA_SPIKE_ZONE_4"})
"""

from .gateway_bridge import DistributionBridge, ChannelStats, get_live_network_stats

__all__ = ["DistributionBridge", "ChannelStats", "get_live_network_stats"]
