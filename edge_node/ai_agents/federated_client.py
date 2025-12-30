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
Federated Learning Client
═════════════════════════════════════════════════════════════════════════════

Privacy-preserving federated learning implementation for distributed model
training without sharing raw data.

Philosophy: "Learn together. Share nothing but wisdom."
"""

from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import json
import hashlib
import numpy as np
from .base_agent import AgentCapability
from .offline_agent import OfflineAgent


class DifferentialPrivacy:
    """
    Differential privacy mechanisms for protecting individual data points.
    
    Implements noise injection to ensure privacy guarantees while maintaining
    model utility.
    """
    
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        """
        Initialize differential privacy mechanism.
        
        Args:
            epsilon: Privacy budget (lower = more privacy)
            delta: Privacy relaxation parameter
        """
        self.epsilon = epsilon
        self.delta = delta
    
    def add_noise(
        self,
        data: List[float],
        sensitivity: float = 1.0,
    ) -> List[float]:
        """
        Add Laplacian noise for differential privacy.
        
        Args:
            data: Original data
            sensitivity: Sensitivity of the query
            
        Returns:
            Noised data
        """
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale, len(data))
        return (np.array(data) + noise).tolist()
    
    def clip_gradients(
        self,
        gradients: List[float],
        max_norm: float = 1.0,
    ) -> List[float]:
        """
        Clip gradients to bound sensitivity.
        
        Args:
            gradients: Original gradients
            max_norm: Maximum L2 norm
            
        Returns:
            Clipped gradients
        """
        grad_array = np.array(gradients)
        norm = np.linalg.norm(grad_array)
        
        if norm > max_norm:
            grad_array = grad_array * (max_norm / norm)
        
        return grad_array.tolist()


class SecureAggregation:
    """
    Secure aggregation protocol for combining model updates without
    revealing individual contributions.
    """
    
    def __init__(self):
        """Initialize secure aggregation."""
        self.contributions: List[Dict[str, Any]] = []
    
    def add_contribution(
        self,
        agent_id: str,
        model_update: Dict[str, Any],
        weight: float = 1.0,
    ):
        """
        Add a model update contribution.
        
        Args:
            agent_id: Contributor agent ID
            model_update: Model update (e.g., gradients, parameters)
            weight: Contribution weight (e.g., based on data size)
        """
        contribution = {
            "agent_id": agent_id,
            "model_update": model_update,
            "weight": weight,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.contributions.append(contribution)
    
    def aggregate(self) -> Dict[str, Any]:
        """
        Aggregate contributions using weighted averaging.
        
        Returns:
            Aggregated model update
        """
        if not self.contributions:
            return {}
        
        # Simple weighted averaging
        # In production: Use secure multi-party computation
        
        total_weight = sum(c["weight"] for c in self.contributions)
        
        aggregated = {
            "aggregation_method": "weighted_average",
            "num_contributors": len(self.contributions),
            "total_weight": total_weight,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Simulate parameter aggregation
        # In production: Aggregate actual model parameters
        aggregated["parameters"] = {
            "simulated": "aggregated_parameters",
            "contributors": [c["agent_id"] for c in self.contributions],
        }
        
        return aggregated
    
    def clear(self):
        """Clear contributions."""
        self.contributions = []


class FederatedLearningClient(OfflineAgent):
    """
    Federated learning client for privacy-preserving distributed training.
    
    Features:
    - Privacy-preserving model updates
    - Differential privacy guarantees
    - Secure aggregation protocol
    - Local model training
    - Gradient/parameter sharing without raw data
    
    Usage:
        client = FederatedLearningClient(
            name="FL Client - Hospital A",
            epsilon=1.0,  # Privacy budget
        )
        
        # Train locally
        client.train_local_model(training_data)
        
        # Share model update (not raw data)
        update = client.get_model_update()
        
        # Receive aggregated model
        client.apply_global_model(aggregated_model)
    """
    
    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        capabilities: Optional[List[AgentCapability]] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        epsilon: float = 1.0,
        delta: float = 1e-5,
        gradient_clip_norm: float = 1.0,
    ):
        """
        Initialize federated learning client.
        
        Args:
            name: Client name
            version: Client version
            capabilities: Additional capabilities
            description: Client description
            tags: Categorization tags
            epsilon: Differential privacy epsilon
            delta: Differential privacy delta
            gradient_clip_norm: Gradient clipping norm
        """
        # Add federated learning capabilities
        fl_capabilities = [
            AgentCapability.FEDERATED_LEARNING,
            AgentCapability.PRIVACY_PRESERVING,
            AgentCapability.MODEL_UPDATE,
        ]
        
        all_capabilities = list(set(fl_capabilities + (capabilities or [])))
        
        super().__init__(
            name=name,
            version=version,
            capabilities=all_capabilities,
            description=description,
            tags=tags,
        )
        
        self.privacy = DifferentialPrivacy(epsilon=epsilon, delta=delta)
        self.aggregator = SecureAggregation()
        self.gradient_clip_norm = gradient_clip_norm
        
        self.local_model: Optional[Dict[str, Any]] = None
        self.training_rounds = 0
        self.training_history: List[Dict[str, Any]] = []
    
    def train_local_model(
        self,
        training_data: List[Dict[str, Any]],
        epochs: int = 1,
    ) -> Dict[str, Any]:
        """
        Train model locally on private data.
        
        Args:
            training_data: Local training data (never leaves device)
            epochs: Number of training epochs
            
        Returns:
            Training metrics
        """
        self._log(f"Training local model with {len(training_data)} samples for {epochs} epochs")
        
        # Simulate local training
        # In production: Actual model training on local data
        
        training_result = {
            "training_round": self.training_rounds,
            "samples": len(training_data),
            "epochs": epochs,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "loss": 0.25,  # Simulated
                "accuracy": 0.92,  # Simulated
            },
        }
        
        self.training_rounds += 1
        self.training_history.append(training_result)
        
        # Update local model
        self.local_model = {
            "version": self.training_rounds,
            "parameters": f"model_params_v{self.training_rounds}",
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        self.save_local_state("local_model", self.local_model)
        
        return training_result
    
    def get_model_update(
        self,
        apply_privacy: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate privacy-preserving model update for aggregation.
        
        Raw data never leaves the device. Only model updates are shared.
        
        Args:
            apply_privacy: Whether to apply differential privacy
            
        Returns:
            Model update (gradients/parameters with privacy guarantees)
        """
        if not self.local_model:
            raise ValueError("No local model available. Train first.")
        
        # Simulate gradient computation
        # In production: Compute actual gradients
        gradients = [0.1, -0.05, 0.3, -0.15, 0.2]  # Simulated
        
        # Apply privacy mechanisms
        if apply_privacy:
            # Clip gradients to bound sensitivity
            gradients = self.privacy.clip_gradients(
                gradients,
                max_norm=self.gradient_clip_norm
            )
            
            # Add differential privacy noise
            gradients = self.privacy.add_noise(
                gradients,
                sensitivity=self.gradient_clip_norm
            )
        
        model_update = {
            "agent_id": self.metadata.agent_id,
            "round": self.training_rounds,
            "update_type": "gradients",
            "gradients": gradients,
            "privacy_applied": apply_privacy,
            "privacy_params": {
                "epsilon": self.privacy.epsilon,
                "delta": self.privacy.delta,
                "clip_norm": self.gradient_clip_norm,
            } if apply_privacy else None,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Queue for sync to aggregation server
        self.sync_queue.add_sync(
            "model_update",
            model_update,
            priority=10  # High priority
        )
        
        self._log(f"Generated privacy-preserving model update (round {self.training_rounds})")
        
        return model_update
    
    def apply_global_model(
        self,
        global_model: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Apply aggregated global model from federated server.
        
        Args:
            global_model: Aggregated model from server
            
        Returns:
            Application result
        """
        self._log(f"Applying global model update")
        
        # Update local model with global parameters
        self.local_model = {
            "version": self.training_rounds,
            "global_round": global_model.get("round", "unknown"),
            "parameters": global_model.get("parameters", {}),
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        self.save_local_state("local_model", self.local_model)
        
        return {
            "status": "applied",
            "global_round": global_model.get("round"),
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def validate_model(
        self,
        validation_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Validate current model on local validation set.
        
        Args:
            validation_data: Validation data (stays local)
            
        Returns:
            Validation metrics
        """
        if not self.local_model:
            raise ValueError("No model to validate")
        
        # Simulate validation
        # In production: Actual model evaluation
        
        validation_result = {
            "samples": len(validation_data),
            "metrics": {
                "accuracy": 0.89,  # Simulated
                "precision": 0.91,  # Simulated
                "recall": 0.87,  # Simulated
                "f1_score": 0.89,  # Simulated
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        self._log(f"Validation completed: {validation_result['metrics']}")
        
        return validation_result
    
    def get_training_stats(self) -> Dict[str, Any]:
        """
        Get training statistics.
        
        Returns:
            Training statistics
        """
        return {
            "total_rounds": self.training_rounds,
            "training_history": self.training_history,
            "current_model_version": self.local_model.get("version") if self.local_model else None,
            "privacy_params": {
                "epsilon": self.privacy.epsilon,
                "delta": self.privacy.delta,
            },
        }
    
    def compute_privacy_spent(self) -> Dict[str, Any]:
        """
        Compute privacy budget spent across training rounds.
        
        Uses composition theorems for differential privacy.
        
        Returns:
            Privacy accounting information
        """
        # Simple composition: epsilon adds up across rounds
        # In production: Use advanced composition (e.g., Rényi DP)
        
        total_epsilon = self.privacy.epsilon * self.training_rounds
        
        return {
            "per_round_epsilon": self.privacy.epsilon,
            "total_rounds": self.training_rounds,
            "total_epsilon_spent": total_epsilon,
            "delta": self.privacy.delta,
            "privacy_budget_exhausted": total_epsilon >= 10.0,  # Example threshold
        }


# ═════════════════════════════════════════════════════════════════════════════
# Philosophy: "Learn together. Share nothing but wisdom."
# 
# Federated Learning ensures:
# - Data sovereignty: Raw data never leaves the edge
# - Privacy guarantees: Differential privacy protects individuals
# - Collaborative learning: Models improve through secure aggregation
# ═════════════════════════════════════════════════════════════════════════════
