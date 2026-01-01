from pydantic import BaseModel
from typing import List
from core.config.corporate_identity import visendi_identity

class AIAgentIdentity(BaseModel):
    agent_id: str
    role: str  # e.g., 'Financial_Auditor', 'HR_Forecaster'
    jurisdiction: str  # USA or KENYA
    auth_token: str  # Microsoft Entra ID integration

class DigitalLaborRegistry:
    """
    Manages AI Agent identities as 'Digital Labor' per IBM standards.
    Ensures agents operate under the correct legal entity.
    """
    def __init__(self):
        self.agents = []

    def register_agent(self, agent_id, role, region):
        entity = visendi_identity.usa_entity if region == "USA" else visendi_identity.kenya_entity
        new_agent = AIAgentIdentity(
            agent_id=agent_id,
            role=role,
            jurisdiction=region,
            auth_token=f"ENTRA_{agent_id}_{entity.registration_number}"
        )
        self.agents.append(new_agent)
        return new_agent

registry = DigitalLaborRegistry()
registry.register_agent("AG-FIN-01", "Fraud_Detector", "USA")
registry.register_agent("AG-PROC-01", "Supplier_Investigator", "KENYA")