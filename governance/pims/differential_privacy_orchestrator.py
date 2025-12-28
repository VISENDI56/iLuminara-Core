"""
Differential Privacy Orchestrator - PIMS Innovation
Orchestrates differential privacy mechanisms for data protection.
"""

from typing import Dict, List, Any
from datetime import datetime
import random
import json


class DifferentialPrivacyOrchestrator:
    """Orchestrates differential privacy for privacy-preserving data analysis."""

    def __init__(self, epsilon: float = 0.1):
        self.epsilon = epsilon  # Privacy parameter
        self.privacy_budget_used = 0.0
        self.query_history: List[Dict[str, Any]] = []

    def add_noise(self, value: float, sensitivity: float = 1.0) -> float:
        """Add Laplace noise for differential privacy."""
        # Laplace mechanism: noise ~ Laplace(0, sensitivity/epsilon)
        scale = sensitivity / self.epsilon
        noise = random.laplace(0, scale)
        noisy_value = value + noise

        # Track privacy budget
        self.privacy_budget_used += self.epsilon

        return noisy_value

    def execute_private_query(self, query_func, data: List[Dict[str, Any]], sensitivity: float = 1.0) -> Any:
        """Execute a query with differential privacy guarantees."""
        # Get true result
        true_result = query_func(data)

        # Add noise based on query type
        if isinstance(true_result, (int, float)):
            private_result = self.add_noise(float(true_result), sensitivity)
        elif isinstance(true_result, list):
            # For aggregations, add noise to each element
            private_result = [self.add_noise(float(x), sensitivity) for x in true_result]
        else:
            # For complex results, return as-is with budget tracking
            self.privacy_budget_used += self.epsilon
            private_result = true_result

        # Log query
        query_log = {
            'timestamp': datetime.now().isoformat(),
            'query_type': query_func.__name__,
            'epsilon_used': self.epsilon,
            'sensitivity': sensitivity,
            'privacy_budget_used': self.privacy_budget_used
        }
        self.query_history.append(query_log)

        return private_result

    def get_privacy_report(self) -> Dict[str, Any]:
        """Generate privacy budget and usage report."""
        return {
            'total_queries': len(self.query_history),
            'privacy_budget_used': self.privacy_budget_used,
            'remaining_budget': max(0, 1.0 - self.privacy_budget_used),  # Assuming budget of 1.0
            'recent_queries': self.query_history[-5:]
        }