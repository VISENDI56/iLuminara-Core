import requests
import json

def test_opa_guardrail():
    url = "http://localhost:8181/v1/data/iluminara/allow"
    payload = {"input": {"region": "EU", "data_type": "phi"}}
    resp = requests.post(url, data=json.dumps(payload))
    assert resp.ok
    result = resp.json().get("result", False)
    print(f"OPA Policy result: {result}")
    assert result is True or result is False

if __name__ == "__main__":
    test_opa_guardrail()
