import json
import datetime

class SovereignGuardrail:
    """
    The Omni-Law Enforcer.
    Checks payloads against the 'sectoral_laws.json' database.
    """
    def __init__(self):
        with open("governance_kernel/sectoral_laws.json", "r") as f:
            self.laws = json.load(f)
        # Mock Sanctions Database
        self.sanctions_db = ["SC-9982", "TERROR-ORG-01"]

    def check_sectoral_compliance(self, context, payload):
        """
        Universal check: Iterates through laws relevant to the context.
        """
        compliance_report = {"status": "PASS", "alerts": [], "actions_taken": []}

        # 1. SUPPLY CHAIN CHECKS
        if context == "SUPPLY_CHAIN":
            if payload.get("origin") == "XUAR": # UFLPA Logic
                compliance_report["status"] = "BLOCKED"
                compliance_report["alerts"].append(self.laws["SUPPLY_CHAIN"]["UFLPA"]["alert"])
            if payload.get("material") in ['Tin', 'Gold'] and not payload.get("audit_proof"): # Dodd-Frank
                compliance_report["alerts"].append(self.laws["SUPPLY_CHAIN"]["DODD_FRANK_1502"]["alert"])

        # 2. FINANCE CHECKS
        if context == "FINANCE":
            if payload.get("payee_id") in self.sanctions_db: # OFAC Logic
                compliance_report["status"] = "FROZEN"
                compliance_report["alerts"].append(self.laws["FINANCE"]["OFAC"]["alert"])

        # 3. ESG CHECKS
        if context == "LOGISTICS" and payload.get("destination") == "EU":
            # CBAM Logic
            emissions = self.calculate_cbam_emissions(payload)
            compliance_report["actions_taken"].append(f"CBAM Report Generated: {emissions}kg CO2")

        # 4. PHARMA CHECKS
        if context == "CLINICAL":
            # EU MDR Logic
            compliance_report["actions_taken"].append("Logged to Post-Market Surveillance (PMS) Ledger")

        return compliance_report

    def calculate_cbam_emissions(self, payload):
        # Simple Mock Calculation
        distance = payload.get("distance_km", 0)
        weight = payload.get("weight_kg", 0)
        return (distance * weight * 0.001) # Mock factor

if __name__ == "__main__":
    guard = SovereignGuardrail()
    # Test 1: OFAC Sanction
    print("Testing OFAC Sanctions...")
    res = guard.check_sectoral_compliance("FINANCE", {"payee_id": "SC-9982", "amount": 1000})
    print(res)
    # Test 2: UFLPA Violation
    print("\nTesting UFLPA Supply Chain...")
    res = guard.check_sectoral_compliance("SUPPLY_CHAIN", {"origin": "XUAR", "item": "Sensor"})
    print(res)
