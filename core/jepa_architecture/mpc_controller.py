import numpy as np
import torch
from core.reasoning.tiny_recursive import TinyRecursiveModel

class EnergyBasedMPC:
    """
    Upgraded MPC Controller using TRM for fast latent simulation.
    """
    def __init__(self):
        # Replaces heavy World Model with Tiny Recursive Model (7M params)
        self.trm_planner = TinyRecursiveModel(recursion_depth=16)
        
    def plan_trajectory(self, current_state_vector):
        """
        Uses Recursive Reasoning to simulate outcomes.
        """
        # Convert state to tensor
        x = torch.tensor(current_state_vector).float().unsqueeze(0)
        y_prev = torch.zeros_like(x)
        
        # "Think" for 16 recursive steps to find optimal path
        action_pred, latent_thought = self.trm_planner(x, y_prev)
        
        # Evaluate Energy (Risk)
        risk = torch.sigmoid(action_pred).item()
        
        if risk > 0.8:
            return "TRIGGER_RL_ADAPTATION"
            
        return "OPTIMAL_TRM_ACTION"