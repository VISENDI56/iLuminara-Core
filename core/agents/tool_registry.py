class AgentToolRegistry:
    """
    Ensures agents have direct access to business-value tools.
    """
    def __init__(self):
        self.tools = {
            "bionemo_design": "ml_health.bionemo_genomics.evo2_engine",
            "logistics_route": "infrastructure.logistics.cuopt_agent",
            "legal_compliance": "governance_kernel.omni_law_interceptor",
            "spatial_query": "geospatial_esri.native_geoghost"
        }

    def get_tool(self, tool_name, agent_clearance_level):
        if tool_name in self.tools:
            print(f"   [Registry] Granting {tool_name} access to Agent (Level {agent_clearance_level})")
            return self.tools[tool_name]
        raise PermissionError("Tool not found or unauthorized.")