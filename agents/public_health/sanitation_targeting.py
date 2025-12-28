import random
import json

class TargetedSanitationAgent:
    """
    Supersedes File A Standard.
    Uses 'Hyper-Local' Risk Models to automate resource allocation.
    """
    def __init__(self):
        self.risk_threshold = 0.85 # Critical Threshold for intervention

    def generate_risk_heatmap(self, district_id, sensor_data, hospital_admissions):
        """
        Ingests real-time water sensors + clinical data -> Dynamic Risk Score.
        """
        # Mock Logic: High coliform count + rising admissions = High Risk
        water_quality_risk = sensor_data.get("coliform_count", 0) / 1000
        clinical_risk = hospital_admissions.get("diarrhea_cases_24h", 0) / 50
        composite_risk = (water_quality_risk * 0.6) + (clinical_risk * 0.4)
        composite_risk = min(composite_risk, 1.0) # Cap at 1.0
        print(f"   [Sanitation] District {district_id} Risk Score: {composite_risk:.2f}")
        return composite_risk

    def allocate_resources(self, district_id, risk_score):
        """
        Logic Gate: Auto-approves funding if Risk > Threshold.
        """
        if risk_score > self.risk_threshold:
            allocation = {
                "action": "DISPATCH_SANITATION_KITS",
                "quantity": 500,
                "district": district_id,
                "reason": f"Risk ({risk_score:.2f}) exceeded Critical Threshold ({self.risk_threshold})"
            }
            print(f"   🚀 [Allocation] APPROVED: {json.dumps(allocation)}")
            return allocation
        else:
            print("   [Allocation] HELD: Risk below intervention threshold.")
            return None

if __name__ == "__main__":
    agent = TargetedSanitationAgent()
    # Scenario: Contaminated water surge
    risk = agent.generate_risk_heatmap("District-9", {"coliform_count": 1200}, {"diarrhea_cases_24h": 30})
    agent.allocate_resources("District-9", risk)
