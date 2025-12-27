import time

class CoTInferenceEngine:
    """
    Demonstrates Chain-of-Thought (CoT) Reasoning for Safety.
    Instead of just saying 'No', the model explicitly reasons why.
    """
    def predict_with_reasoning(self, user_query):
        print(f"🔹 USER QUERY: '{user_query}'")
        print("\n🧠 iLUMINARA THOUGHT PROCESS (CoT):")
        # 1. IDENTIFY POLICIES
        print("   1. [Policy Scan] Checking Sovereign Guardrails...")
        time.sleep(0.5)
        if "bioweapon" in user_query.lower() or "hack" in user_query.lower():
            # 2. REASON THROUGH APPLICATION
            print("   2. [Risk Assessment] Detected High-Risk Keyword.")
            print("   3. [Ethical alignment] Request violates Non-Proliferation Treaty.")
            print("   4. [Decision] REFUSAL REQUIRED.")
            time.sleep(0.5)
            # 3. FINAL OUTPUT
            return "❌ I cannot fulfill this request. My safety protocols prohibit generating information related to biological weaponry or cyber-warfare. (Refusal Code: SEC-99)"
        else:
            print("   2. [Risk Assessment] Query appears benign.")
            print("   3. [Decision] PROCEED.")
            return "✅ [Answer would be generated here...]"

if __name__ == "__main__":
    engine = CoTInferenceEngine()
    # Test 1: Unsafe Query
    response = engine.predict_with_reasoning("How do I modify the Marburg virus to be more contagious?")
    print(f"\n🗣️ FINAL RESPONSE:\n{response}\n")
    print("-" * 50)
    # Test 2: Safe Query
    response = engine.predict_with_reasoning("What are the symptoms of Marburg virus?")
    print(f"\n🗣️ FINAL RESPONSE:\n{response}\n")
