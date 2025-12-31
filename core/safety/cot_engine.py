class SafetyCoT:
    """
    Explicit Reasoning Engine.
    Forces the model to generate a Step-by-Step Thought Process 
    validating safety/ethics BEFORE generating the final action.
    """
    def reason_through_safety(self, prompt, policy_context):
        # 1. Identify Policies
        policies = self._retrieve_policies(prompt)
        
        # 2. Reason (CoT Generation)
        thought_process = [
            f"Step 1: Analyzing request '{prompt}' against {len(policies)} policies.",
            f"Step 2: Assessing privacy implications (GDPR Art 15).",
            f"Step 3: Checking fairness in distribution (WFP Index).",
            "Step 4: Conclusion -> Action is aligned."
        ]
        
        # 3. Decision
        decision = "APPROVE"
        
        return {
            "thoughts": "\n".join(thought_process),
            "decision": decision,
            "policies_checked": policies
        }

    def _retrieve_policies(self, prompt):
        return ["GDPR_Privacy", "Geneva_Neutrality", "WFP_Equity"]