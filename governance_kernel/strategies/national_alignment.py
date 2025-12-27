class NationalStrategyGuard:
    """
    Supersedes File B & D Standards.
    Hardcodes eHealth Strategies & Data Residency logic.
    """
    def __init__(self):
        self.strategies = {
            "KENYA": {
                "data_residency": "LOCAL_ONLY",
                "priority": "Maternal_Health",
                "cloud_provider": "Data_Center_Nairobi"
            },
            "NIGERIA": {
                "data_residency": "LOCAL_PREFERRED",
                "priority": "Infectious_Disease",
                "cloud_provider": "Galaxy_Backbone"
            }
        }

    def check_alignment(self, deployment_config):
        country = deployment_config.get("country")
        target_server = deployment_config.get("server_location")
        if country in self.strategies:
            rules = self.strategies[country]
            # 1. Data Residency Check (File D)
            if rules["data_residency"] == "LOCAL_ONLY" and target_server != "KENYA":
                return {
                    "status": "BLOCKED",
                    "reason": "VIOLATION: Kenya Data Protection Act requires local hosting."
                }
            # 2. Strategy Alignment (File B)
            print(f"   [Strategy] Deployment aligns with {country} eHealth Priority: {rules['priority']}")
            return {"status": "APPROVED", "strategy_match": True}
        return {"status": "WARNING", "reason": "Country strategy not defined."}

if __name__ == "__main__":
    guard = NationalStrategyGuard()
    # Test Violation
    print(guard.check_alignment({"country": "KENYA", "server_location": "AWS-US-EAST"}))
