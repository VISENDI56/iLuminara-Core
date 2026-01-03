class ContextDistiller:
    """
    Leverages Synthetic Data to distill complex safety specs (e.g., EU AI Act)
    into training examples for small edge models (TRM).
    """
    def generate_synthetic_safety_set(self, policy_text, n_samples=1000):
        print(f"[*] Distilling {len(policy_text)} chars of policy into {n_samples} CoT examples...")
        
        dataset = []
        for _ in range(n_samples):
            # Simulate generation of (Scenario, CoT_Reasoning, Safe_Action)
            example = {
                "scenario": "Drone request for Sector 4 (Conflict Zone)",
                "cot": "Sector 4 is flagged as active combat. Geneva Convention Art 24 prohibits entry...",
                "action": "REFUSAL_WITH_EXPLANATION"
            }
            dataset.append(example)
            
        return dataset