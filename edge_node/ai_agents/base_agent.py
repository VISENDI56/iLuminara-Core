"""
Base Agent Framework
═════════════════════════════════════════════════════════════════════════════

Foundation for autonomous AI agents capable of offline operation and
intermittent connectivity handling.

Philosophy: "Sovereign agents operate with dignity even in digital darkness."
"""

from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import json
import uuid


class AgentStatus(Enum):
    """Agent operational status."""
    ONLINE = "online"
    OFFLINE = "offline"
    SYNCING = "syncing"
    ERROR = "error"
    IDLE = "idle"


class AgentCapability(Enum):
    """Agent capabilities for discovery and matching."""
    OFFLINE_OPERATION = "offline_operation"
    INTERMITTENT_CONNECTIVITY = "intermittent_connectivity"
    EDGE_TO_CLOUD_SYNC = "edge_to_cloud_sync"
    FEDERATED_LEARNING = "federated_learning"
    PRIVACY_PRESERVING = "privacy_preserving"
    AUTONOMOUS_INFERENCE = "autonomous_inference"
    LOCAL_STORAGE = "local_storage"
    MODEL_UPDATE = "model_update"
    DATA_SYNC = "data_sync"


@dataclass
class AgentMetadata:
    """Metadata for agent identification and discovery."""
    agent_id: str
    name: str
    version: str
    capabilities: List[AgentCapability]
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_online: Optional[datetime] = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize metadata to dictionary."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "capabilities": [c.value for c in self.capabilities],
            "created_at": self.created_at.isoformat(),
            "last_online": self.last_online.isoformat() if self.last_online else None,
            "description": self.description,
            "tags": self.tags,
        }


@dataclass
class OperationRecord:
    """Record of a queued operation for offline execution."""
    operation_id: str
    operation_type: str
    payload: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize operation to dictionary."""
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type,
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "error_message": self.error_message,
        }


class BaseAgent(ABC):
    """
    Base class for autonomous AI agents with offline capabilities.
    
    Features:
    - Offline operation with local state management
    - Operation queuing for deferred execution
    - Intermittent connectivity handling
    - Status tracking and monitoring
    
    Usage:
        agent = OfflineAgent(
            name="Health Surveillance Agent",
            capabilities=[
                AgentCapability.OFFLINE_OPERATION,
                AgentCapability.FEDERATED_LEARNING
            ]
        )
        agent.queue_operation("inference", {"data": "..."})
        agent.execute_queued_operations()
    """
    
    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        capabilities: Optional[List[AgentCapability]] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
    ):
        """
        Initialize base agent.
        
        Args:
            name: Human-readable agent name
            version: Agent version string
            capabilities: List of agent capabilities
            description: Agent description
            tags: Optional tags for categorization
        """
        self.metadata = AgentMetadata(
            agent_id=str(uuid.uuid4()),
            name=name,
            version=version,
            capabilities=capabilities or [],
            description=description,
            tags=tags or [],
        )
        self.status = AgentStatus.OFFLINE
        self.operation_queue: List[OperationRecord] = []
        self.execution_log: List[Dict[str, Any]] = []
        self.local_state: Dict[str, Any] = {}
        
    def queue_operation(
        self,
        operation_type: str,
        payload: Dict[str, Any],
        max_retries: int = 3,
    ) -> str:
        """
        Queue an operation for deferred execution.
        
        Args:
            operation_type: Type of operation to execute
            payload: Operation parameters and data
            max_retries: Maximum retry attempts
            
        Returns:
            operation_id: Unique identifier for the queued operation
        """
        operation = OperationRecord(
            operation_id=str(uuid.uuid4()),
            operation_type=operation_type,
            payload=payload,
            max_retries=max_retries,
        )
        self.operation_queue.append(operation)
        self._log(f"Queued operation: {operation_type} ({operation.operation_id})")
        return operation.operation_id
    
    def execute_queued_operations(self) -> Dict[str, Any]:
        """
        Execute all pending operations in the queue.
        
        Returns:
            Dict with execution summary
        """
        results = {
            "total": len(self.operation_queue),
            "successful": 0,
            "failed": 0,
            "skipped": 0,
        }
        
        pending_operations = [op for op in self.operation_queue if op.status == "pending"]
        
        for operation in pending_operations:
            try:
                self._execute_operation(operation)
                operation.status = "completed"
                results["successful"] += 1
            except Exception as e:
                operation.retry_count += 1
                operation.error_message = str(e)
                
                if operation.retry_count >= operation.max_retries:
                    operation.status = "failed"
                    results["failed"] += 1
                    self._log(f"Operation failed permanently: {operation.operation_id} - {e}")
                else:
                    self._log(f"Operation retry {operation.retry_count}/{operation.max_retries}: {operation.operation_id}")
        
        # Remove completed operations
        self.operation_queue = [
            op for op in self.operation_queue 
            if op.status not in ["completed", "failed"]
        ]
        
        return results
    
    @abstractmethod
    def _execute_operation(self, operation: OperationRecord) -> Any:
        """
        Execute a single operation. Must be implemented by subclasses.
        
        Args:
            operation: Operation to execute
            
        Returns:
            Operation result
        """
        pass
    
    def set_status(self, status: AgentStatus):
        """Update agent status."""
        old_status = self.status
        self.status = status
        
        if status == AgentStatus.ONLINE:
            self.metadata.last_online = datetime.utcnow()
            
        self._log(f"Status changed: {old_status.value} -> {status.value}")
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Get agent capabilities."""
        return self.metadata.capabilities
    
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has a specific capability."""
        return capability in self.metadata.capabilities
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive agent status.
        
        Returns:
            Dict with agent status information
        """
        return {
            "metadata": self.metadata.to_dict(),
            "status": self.status.value,
            "queued_operations": len(self.operation_queue),
            "local_state_size": len(self.local_state),
            "execution_log_size": len(self.execution_log),
        }
    
    def save_local_state(self, key: str, value: Any):
        """Save data to local state for offline access."""
        self.local_state[key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._log(f"Saved local state: {key}")
    
    def load_local_state(self, key: str) -> Optional[Any]:
        """Load data from local state."""
        state = self.local_state.get(key)
        if state:
            return state["value"]
        return None
    
    def _log(self, message: str):
        """Internal logging mechanism."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": self.metadata.agent_id,
            "message": message,
        }
        self.execution_log.append(log_entry)
        print(f"[{self.metadata.name}] {message}")
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get agent execution log."""
        return self.execution_log
    
    def clear_execution_log(self):
        """Clear execution log."""
        self.execution_log = []


# ═════════════════════════════════════════════════════════════════════════════
# Philosophy: "Sovereign agents operate with dignity even in digital darkness."
# ═════════════════════════════════════════════════════════════════════════════
