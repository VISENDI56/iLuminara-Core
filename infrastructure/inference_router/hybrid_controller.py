from governance_kernel.omni_law_interceptor import OmniLawMatrix

class HybridInferenceRouter:
    """
    Intelligent Router.
    Decides whether to process on 'IGX Orin' (Local) or 'Nebius' (Cloud).
    """
    def __init__(self):
        self.law = OmniLawMatrix()
        self.nebius_url = "https://api.studio.nebius.ai/v1/chat/completions"

    def route_query(self, query_context, thermal_load_percent):
        # 1. Check Sovereignty/Privacy Laws
        compliance = self.law.intercept_call("cloud_offload", query_context)

        # 2. Decision Logic
        if thermal_load_percent > 90 and compliance == "COMPLIANT":
            return self._offload_to_nebius(query_context)
        else:
            return "ROUTE_LOCAL_IGX"

    def _offload_to_nebius(self, context):
        print("   [Router] Local Edge Saturated (>90%). Offloading to Nebius (EU Region)...")
        # Actual API call would happen here using OpenAI-compatible SDK
        return "CLOUD_RESPONSE_RECEIVED"