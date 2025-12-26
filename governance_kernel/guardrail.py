import requests
import json

class OpaGuardrail:
    def __init__(self, opa_url="http://localhost:8181/v1/data/iluminara/allow"):
        self.opa_url = opa_url

    def check(self, region, data_type):
        payload = {"input": {"region": region, "data_type": data_type}}
        resp = requests.post(self.opa_url, data=json.dumps(payload))
        if resp.ok:
            return resp.json().get("result", False)
        return False

# Usage:
# guardrail = OpaGuardrail()
# allowed = guardrail.check("EU", "phi")
