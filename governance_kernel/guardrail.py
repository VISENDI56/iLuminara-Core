import requests
import json

class OpaGuardrail:
    def __init__(self, opa_url="http://localhost:8181/v1/data/iluminara/allow"):
        self.opa_url = opa_url
        # Guiding Principles from Global Strategy on Digital Health
        self.guiding_principles = ["institutionalize", "integrate", "appropriate_use", "address_impediments"]
        self.maturity_levels = ["people_centred", "integrated", "equitable"]

    def check(self, region, data_type):
        payload = {"input": {"region": region, "data_type": data_type}}
        resp = requests.post(self.opa_url, data=json.dumps(payload))
        if resp.ok:
            return resp.json().get("result", False)
        return False

    def enforce_principles(self, action):
        # Strategic Objectives Hub: Global collaboration, national strategy, multi-level governance
        return all(principle in action for principle in self.guiding_principles)

# Usage:
# guardrail = OpaGuardrail()
# allowed = guardrail.check("EU", "phi")
