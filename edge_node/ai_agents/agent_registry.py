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
Agent Registry & Discovery Service
═════════════════════════════════════════════════════════════════════════════

Registry for discovering and matching AI agents based on capabilities,
tags, and requirements.

Philosophy: "Find the right agent for the right task, anywhere, anytime."
"""

from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from .base_agent import BaseAgent, AgentCapability, AgentStatus


class AgentRegistry:
    """
    Registry for AI agent discovery and search.
    
    Features:
    - Agent registration and discovery
    - Capability-based search
    - Tag-based filtering
    - Status monitoring
    - Multi-criteria matching
    
    Usage:
        registry = AgentRegistry()
        
        # Register agents
        registry.register(agent1)
        registry.register(agent2)
        
        # Search by capabilities
        offline_agents = registry.search_by_capabilities([
            AgentCapability.OFFLINE_OPERATION,
            AgentCapability.FEDERATED_LEARNING
        ])
        
        # Search by tags
        health_agents = registry.search_by_tags(["health", "surveillance"])
    """
    
    def __init__(self):
        """Initialize agent registry."""
        self.agents: Dict[str, BaseAgent] = {}
        self.registration_log: List[Dict[str, Any]] = []
    
    def register(self, agent: BaseAgent) -> bool:
        """
        Register an agent in the registry.
        
        Args:
            agent: Agent to register
            
        Returns:
            True if registered successfully
        """
        agent_id = agent.metadata.agent_id
        
        if agent_id in self.agents:
            print(f"⚠️  Agent already registered: {agent.metadata.name} ({agent_id})")
            return False
        
        self.agents[agent_id] = agent
        
        self.registration_log.append({
            "agent_id": agent_id,
            "name": agent.metadata.name,
            "timestamp": datetime.utcnow().isoformat(),
            "action": "registered",
        })
        
        print(f"✅ Registered agent: {agent.metadata.name} ({agent_id})")
        return True
    
    def unregister(self, agent_id: str) -> bool:
        """
        Unregister an agent from the registry.
        
        Args:
            agent_id: ID of agent to unregister
            
        Returns:
            True if unregistered successfully
        """
        if agent_id not in self.agents:
            print(f"⚠️  Agent not found: {agent_id}")
            return False
        
        agent = self.agents[agent_id]
        del self.agents[agent_id]
        
        self.registration_log.append({
            "agent_id": agent_id,
            "name": agent.metadata.name,
            "timestamp": datetime.utcnow().isoformat(),
            "action": "unregistered",
        })
        
        print(f"✅ Unregistered agent: {agent.metadata.name} ({agent_id})")
        return True
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get agent by ID.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent instance or None
        """
        return self.agents.get(agent_id)
    
    def search_by_capabilities(
        self,
        required_capabilities: List[AgentCapability],
        match_all: bool = True,
    ) -> List[BaseAgent]:
        """
        Search agents by capabilities.
        
        Args:
            required_capabilities: List of required capabilities
            match_all: If True, agent must have ALL capabilities.
                      If False, agent must have ANY capability.
            
        Returns:
            List of matching agents
        """
        matching_agents = []
        
        for agent in self.agents.values():
            agent_capabilities = set(agent.get_capabilities())
            required_set = set(required_capabilities)
            
            if match_all:
                # Agent must have all required capabilities
                if required_set.issubset(agent_capabilities):
                    matching_agents.append(agent)
            else:
                # Agent must have at least one required capability
                if required_set.intersection(agent_capabilities):
                    matching_agents.append(agent)
        
        return matching_agents
    
    def search_by_tags(
        self,
        tags: List[str],
        match_all: bool = False,
    ) -> List[BaseAgent]:
        """
        Search agents by tags.
        
        Args:
            tags: List of tags to search for
            match_all: If True, agent must have ALL tags.
                      If False, agent must have ANY tag.
            
        Returns:
            List of matching agents
        """
        matching_agents = []
        
        for agent in self.agents.values():
            agent_tags = set(agent.metadata.tags)
            search_tags = set(tags)
            
            if match_all:
                if search_tags.issubset(agent_tags):
                    matching_agents.append(agent)
            else:
                if search_tags.intersection(agent_tags):
                    matching_agents.append(agent)
        
        return matching_agents
    
    def search_by_status(
        self,
        status: AgentStatus,
    ) -> List[BaseAgent]:
        """
        Search agents by status.
        
        Args:
            status: Agent status to filter by
            
        Returns:
            List of agents with matching status
        """
        return [
            agent for agent in self.agents.values()
            if agent.status == status
        ]
    
    def search_by_name(
        self,
        name_pattern: str,
        case_sensitive: bool = False,
    ) -> List[BaseAgent]:
        """
        Search agents by name pattern.
        
        Args:
            name_pattern: Pattern to match in agent name
            case_sensitive: Whether search is case-sensitive
            
        Returns:
            List of matching agents
        """
        matching_agents = []
        
        for agent in self.agents.values():
            agent_name = agent.metadata.name
            pattern = name_pattern
            
            if not case_sensitive:
                agent_name = agent_name.lower()
                pattern = pattern.lower()
            
            if pattern in agent_name:
                matching_agents.append(agent)
        
        return matching_agents
    
    def advanced_search(
        self,
        capabilities: Optional[List[AgentCapability]] = None,
        tags: Optional[List[str]] = None,
        status: Optional[AgentStatus] = None,
        name_pattern: Optional[str] = None,
        custom_filter: Optional[Callable[[BaseAgent], bool]] = None,
    ) -> List[BaseAgent]:
        """
        Advanced multi-criteria agent search.
        
        Args:
            capabilities: Required capabilities
            tags: Required tags
            status: Required status
            name_pattern: Name pattern to match
            custom_filter: Custom filter function
            
        Returns:
            List of matching agents
        """
        results = list(self.agents.values())
        
        # Filter by capabilities
        if capabilities:
            results = [
                agent for agent in results
                if set(capabilities).issubset(set(agent.get_capabilities()))
            ]
        
        # Filter by tags
        if tags:
            results = [
                agent for agent in results
                if set(tags).intersection(set(agent.metadata.tags))
            ]
        
        # Filter by status
        if status:
            results = [
                agent for agent in results
                if agent.status == status
            ]
        
        # Filter by name pattern
        if name_pattern:
            pattern = name_pattern.lower()
            results = [
                agent for agent in results
                if pattern in agent.metadata.name.lower()
            ]
        
        # Apply custom filter
        if custom_filter:
            results = [
                agent for agent in results
                if custom_filter(agent)
            ]
        
        return results
    
    def get_all_agents(self) -> List[BaseAgent]:
        """Get all registered agents."""
        return list(self.agents.values())
    
    def get_agent_count(self) -> int:
        """Get total number of registered agents."""
        return len(self.agents)
    
    def get_capability_distribution(self) -> Dict[str, int]:
        """
        Get distribution of capabilities across all agents.
        
        Returns:
            Dict mapping capability to count of agents with that capability
        """
        distribution = {}
        
        for agent in self.agents.values():
            for capability in agent.get_capabilities():
                cap_name = capability.value
                distribution[cap_name] = distribution.get(cap_name, 0) + 1
        
        return distribution
    
    def get_status_distribution(self) -> Dict[str, int]:
        """
        Get distribution of agent statuses.
        
        Returns:
            Dict mapping status to count
        """
        distribution = {}
        
        for agent in self.agents.values():
            status_name = agent.status.value
            distribution[status_name] = distribution.get(status_name, 0) + 1
        
        return distribution
    
    def get_registry_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive registry summary.
        
        Returns:
            Registry summary information
        """
        return {
            "total_agents": self.get_agent_count(),
            "capability_distribution": self.get_capability_distribution(),
            "status_distribution": self.get_status_distribution(),
            "agents": [
                {
                    "id": agent.metadata.agent_id,
                    "name": agent.metadata.name,
                    "status": agent.status.value,
                    "capabilities": [c.value for c in agent.get_capabilities()],
                    "tags": agent.metadata.tags,
                }
                for agent in self.agents.values()
            ],
        }
    
    def export_registry(self) -> Dict[str, Any]:
        """
        Export registry for persistence or sharing.
        
        Returns:
            Serializable registry data
        """
        return {
            "export_timestamp": datetime.utcnow().isoformat(),
            "agent_count": self.get_agent_count(),
            "agents": [
                agent.get_status() for agent in self.agents.values()
            ],
            "registration_log": self.registration_log,
        }


# ═════════════════════════════════════════════════════════════════════════════
# Philosophy: "Find the right agent for the right task, anywhere, anytime."
# 
# The Agent Registry enables:
# - Dynamic agent discovery
# - Capability-based matching
# - Flexible search criteria
# - Distributed agent coordination
# ═════════════════════════════════════════════════════════════════════════════
