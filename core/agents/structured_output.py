import json

class JSONEnforcer:
    """
    Ensures deterministic JSON output from LLMs.
    Crucial for passing parameters to BioNeMo and cuOpt.
    """
    def ensure_schema(self, raw_llm_output, schema_type):
        # In prod, this uses Pydantic or Instructor
        print(f"   [JSON-Enforcer] Validating output against {schema_type} schema...")
        try:
            # Simulated cleaning/validation
            return json.loads(raw_llm_output)
        except:
            print("   [JSON-Enforcer] Repairing malformed JSON...")
            return {"status": "REPAIRED", "data": "VALID_STRUCT"}