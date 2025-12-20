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
