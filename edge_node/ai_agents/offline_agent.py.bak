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
Offline Agent Implementation
═════════════════════════════════════════════════════════════════════════════

AI agent specialized for offline operation with intermittent connectivity
handling and edge-to-cloud synchronization.

Philosophy: "Operations continue even when clouds vanish."
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import time
import json
from .base_agent import (
    BaseAgent,
    AgentCapability,
    AgentStatus,
    OperationRecord,
)


class ConnectivityManager:
    """
    Manages network connectivity detection and retry logic.
    
    Features:
    - Connection monitoring
    - Exponential backoff for retries
    - Network availability detection
    """
    
    def __init__(
        self,
        check_interval: int = 60,
        max_backoff: int = 3600,
    ):
        """
        Initialize connectivity manager.
        
        Args:
            check_interval: Seconds between connectivity checks
            max_backoff: Maximum backoff time in seconds
        """
        self.check_interval = check_interval
        self.max_backoff = max_backoff
        self.last_check: Optional[datetime] = None
        self.is_connected = False
        self.backoff_seconds = 1
        self.connection_history: List[Dict[str, Any]] = []
    
    def check_connectivity(self) -> bool:
        """
        Check network connectivity.
        
        In production, this would ping a reliable endpoint.
        For edge deployment, checks local gateway availability.
        
        Returns:
            True if connected, False otherwise
        """
        # Simulate connectivity check
        # In production: ping gateway, check DNS, etc.
        self.last_check = datetime.utcnow()
        
        # Record connection event
        self.connection_history.append({
            "timestamp": self.last_check.isoformat(),
            "connected": self.is_connected,
        })
        
        return self.is_connected
    
    def set_connectivity(self, connected: bool):
        """
        Manually set connectivity status.
        
        Args:
            connected: Network connectivity status
        """
        old_status = self.is_connected
        self.is_connected = connected
        
        if connected and not old_status:
            # Reset backoff on successful reconnection
            self.backoff_seconds = 1
        
        self.connection_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "connected": connected,
            "event": "status_change",
        })
    
    def get_backoff_time(self) -> int:
        """
        Get current backoff time using exponential backoff strategy.
        
        Returns:
            Backoff time in seconds
        """
        backoff = min(self.backoff_seconds, self.max_backoff)
        self.backoff_seconds = min(self.backoff_seconds * 2, self.max_backoff)
        return backoff
    
    def reset_backoff(self):
        """Reset backoff counter."""
        self.backoff_seconds = 1
    
    def should_check_connection(self) -> bool:
        """
        Determine if it's time to check connection again.
        
        Returns:
            True if should check, False otherwise
        """
        if not self.last_check:
            return True
        
        elapsed = (datetime.utcnow() - self.last_check).total_seconds()
        return elapsed >= self.check_interval
    
    def get_connection_history(self) -> List[Dict[str, Any]]:
        """Get connection history."""
        return self.connection_history


class SyncQueue:
    """
    Manages edge-to-cloud synchronization queue.
    
    Handles data and model updates that need to be synced when
    connectivity is available.
    """
    
    def __init__(self):
        """Initialize sync queue."""
        self.pending_syncs: List[Dict[str, Any]] = []
        self.completed_syncs: List[Dict[str, Any]] = []
        self.failed_syncs: List[Dict[str, Any]] = []
    
    def add_sync(
        self,
        sync_type: str,
        data: Dict[str, Any],
        priority: int = 0,
    ) -> str:
        """
        Add item to sync queue.
        
        Args:
            sync_type: Type of sync ("model_update", "data_sync", "telemetry")
            data: Data to synchronize
            priority: Sync priority (higher = more urgent)
            
        Returns:
            Sync ID
        """
        sync_id = f"sync_{len(self.pending_syncs)}_{int(time.time())}"
        sync_item = {
            "sync_id": sync_id,
            "sync_type": sync_type,
            "data": data,
            "priority": priority,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
        }
        self.pending_syncs.append(sync_item)
        
        # Sort by priority (highest first)
        self.pending_syncs.sort(key=lambda x: x["priority"], reverse=True)
        
        return sync_id
    
    def get_next_sync(self) -> Optional[Dict[str, Any]]:
        """Get next item from sync queue."""
        if self.pending_syncs:
            return self.pending_syncs[0]
        return None
    
    def mark_completed(self, sync_id: str):
        """Mark sync as completed."""
        for i, sync_item in enumerate(self.pending_syncs):
            if sync_item["sync_id"] == sync_id:
                sync_item["status"] = "completed"
                sync_item["completed_at"] = datetime.utcnow().isoformat()
                self.completed_syncs.append(sync_item)
                self.pending_syncs.pop(i)
                break
    
    def mark_failed(self, sync_id: str, error: str):
        """Mark sync as failed."""
        for i, sync_item in enumerate(self.pending_syncs):
            if sync_item["sync_id"] == sync_id:
                sync_item["status"] = "failed"
                sync_item["error"] = error
                sync_item["failed_at"] = datetime.utcnow().isoformat()
                self.failed_syncs.append(sync_item)
                self.pending_syncs.pop(i)
                break
    
    def get_stats(self) -> Dict[str, int]:
        """Get sync queue statistics."""
        return {
            "pending": len(self.pending_syncs),
            "completed": len(self.completed_syncs),
            "failed": len(self.failed_syncs),
        }


class OfflineAgent(BaseAgent):
    """
    AI agent optimized for offline operation and intermittent connectivity.
    
    Features:
    - Autonomous operation without network connectivity
    - Intelligent sync queue management
    - Exponential backoff for retry logic
    - Local inference and data storage
    - Edge-to-cloud synchronization
    
    Usage:
        agent = OfflineAgent(
            name="Health Monitor Agent",
            capabilities=[
                AgentCapability.OFFLINE_OPERATION,
                AgentCapability.INTERMITTENT_CONNECTIVITY,
                AgentCapability.EDGE_TO_CLOUD_SYNC
            ]
        )
        
        # Operate offline
        agent.queue_operation("inference", {"patient_id": "123", "symptoms": [...]})
        agent.execute_queued_operations()
        
        # Sync when connectivity available
        agent.connectivity.set_connectivity(True)
        agent.sync_to_cloud()
    """
    
    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        capabilities: Optional[List[AgentCapability]] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        check_interval: int = 60,
    ):
        """
        Initialize offline agent.
        
        Args:
            name: Agent name
            version: Agent version
            capabilities: Agent capabilities
            description: Agent description
            tags: Categorization tags
            check_interval: Connectivity check interval in seconds
        """
        # Add default capabilities for offline agents
        default_capabilities = [
            AgentCapability.OFFLINE_OPERATION,
            AgentCapability.INTERMITTENT_CONNECTIVITY,
            AgentCapability.EDGE_TO_CLOUD_SYNC,
            AgentCapability.LOCAL_STORAGE,
        ]
        
        all_capabilities = list(set(default_capabilities + (capabilities or [])))
        
        super().__init__(
            name=name,
            version=version,
            capabilities=all_capabilities,
            description=description,
            tags=tags,
        )
        
        self.connectivity = ConnectivityManager(check_interval=check_interval)
        self.sync_queue = SyncQueue()
        self.last_sync: Optional[datetime] = None
        
        # Start in offline mode
        self.set_status(AgentStatus.OFFLINE)
    
    def _execute_operation(self, operation: OperationRecord) -> Any:
        """
        Execute a queued operation.
        
        Args:
            operation: Operation to execute
            
        Returns:
            Operation result
        """
        operation_type = operation.operation_type
        payload = operation.payload
        
        self._log(f"Executing operation: {operation_type} ({operation.operation_id})")
        
        # Route to appropriate handler
        if operation_type == "inference":
            return self._handle_inference(payload)
        elif operation_type == "data_collection":
            return self._handle_data_collection(payload)
        elif operation_type == "model_update":
            return self._handle_model_update(payload)
        else:
            raise ValueError(f"Unknown operation type: {operation_type}")
    
    def _handle_inference(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle inference operation locally.
        
        Args:
            payload: Inference parameters
            
        Returns:
            Inference results
        """
        # Simulate local inference
        result = {
            "inference_id": f"inf_{int(time.time())}",
            "input": payload,
            "result": "simulated_inference_result",
            "confidence": 0.85,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Save to local state
        self.save_local_state(result["inference_id"], result)
        
        # Queue for sync when online
        self.sync_queue.add_sync("telemetry", result, priority=1)
        
        return result
    
    def _handle_data_collection(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle data collection and local storage.
        
        Args:
            payload: Data collection parameters
            
        Returns:
            Collection result
        """
        collection_id = f"data_{int(time.time())}"
        
        # Store locally
        self.save_local_state(collection_id, payload)
        
        # Queue for sync
        self.sync_queue.add_sync("data_sync", {
            "collection_id": collection_id,
            "data": payload,
        }, priority=2)
        
        return {"collection_id": collection_id, "status": "stored_locally"}
    
    def _handle_model_update(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle model update operation.
        
        Args:
            payload: Model update parameters
            
        Returns:
            Update result
        """
        model_version = payload.get("version", "unknown")
        
        # Save model to local state
        self.save_local_state("current_model", payload)
        
        self._log(f"Model updated to version: {model_version}")
        
        return {"status": "model_updated", "version": model_version}
    
    def sync_to_cloud(self) -> Dict[str, Any]:
        """
        Synchronize pending operations to cloud when connectivity is available.
        
        Returns:
            Sync statistics
        """
        if not self.connectivity.is_connected:
            self._log("Cannot sync: No connectivity")
            return {
                "status": "failed",
                "reason": "no_connectivity",
                "stats": self.sync_queue.get_stats(),
            }
        
        self.set_status(AgentStatus.SYNCING)
        
        synced = 0
        failed = 0
        
        while True:
            sync_item = self.sync_queue.get_next_sync()
            if not sync_item:
                break
            
            try:
                # Simulate cloud sync
                # In production: HTTP POST to cloud endpoint
                self._log(f"Syncing: {sync_item['sync_type']} ({sync_item['sync_id']})")
                
                # Simulate network delay
                time.sleep(0.1)
                
                self.sync_queue.mark_completed(sync_item["sync_id"])
                synced += 1
                
            except Exception as e:
                self._log(f"Sync failed: {sync_item['sync_id']} - {e}")
                self.sync_queue.mark_failed(sync_item["sync_id"], str(e))
                failed += 1
        
        self.last_sync = datetime.utcnow()
        self.set_status(AgentStatus.ONLINE)
        
        return {
            "status": "completed",
            "synced": synced,
            "failed": failed,
            "timestamp": self.last_sync.isoformat(),
            "stats": self.sync_queue.get_stats(),
        }
    
    def check_and_sync(self) -> Optional[Dict[str, Any]]:
        """
        Check connectivity and sync if available.
        
        Returns:
            Sync result if sync was performed, None otherwise
        """
        if self.connectivity.should_check_connection():
            self.connectivity.check_connectivity()
        
        if self.connectivity.is_connected:
            return self.sync_to_cloud()
        
        return None
    
    def get_sync_status(self) -> Dict[str, Any]:
        """
        Get comprehensive sync status.
        
        Returns:
            Sync status information
        """
        return {
            "connectivity": {
                "connected": self.connectivity.is_connected,
                "last_check": self.connectivity.last_check.isoformat() if self.connectivity.last_check else None,
            },
            "sync_queue": self.sync_queue.get_stats(),
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
        }


# ═════════════════════════════════════════════════════════════════════════════
# Philosophy: "Operations continue even when clouds vanish."
# ═════════════════════════════════════════════════════════════════════════════
