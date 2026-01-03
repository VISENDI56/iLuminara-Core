class SafetyRewardModel:
    """
    RL Reward Model.
    Provides positive rewards for:
    - Policy Adherence
    - Explicit CoT Clarity
    - Sovereign Decision Making (Local > Cloud)
    """
    def calculate_reward(self, action, cot_trace, feedback):
        reward = 0.0
        
        # 1. Policy Adherence Reward
        if action['is_compliant']: reward += 1.0
        
        # 2. CoT Clarity Reward (Penalty for opacity)
        if len(cot_trace) < 50: reward -= 0.5
        
        # 3. Sovereignty Reward (Agency)
        if action['source'] == 'LOCAL_EDGE': reward += 0.5
        
        return reward