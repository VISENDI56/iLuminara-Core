class SovereignPricingModel:
    """
    The Official 2026 Sovereign Pricing Matrix.
    Defines the 4 Tiers of the iLuminara Civilization OS.
    """
    def __init__(self):
        self.tiers = {
            "SOVEREIGN_NODE": {
                "role": "Clinic / NGO Edge",
                "price_monthly": 99,
                "currency": "USD",
                "hardware": "NVIDIA Jetson Orin Nano",
                "core_ai": "Tiny Recursive Model (TRM)",
                "infra": "Hyperledger Besu (Offline)"
            },
            "BIO_FOUNDRY": {
                "role": "Field Hospital / Lab",
                "price_monthly": 999,
                "currency": "USD",
                "hardware": "NVIDIA IGX Orin (Industrial)",
                "core_ai": "BioNeMo Evo 2 (FP8)",
                "infra": "IGX Safety Island Root"
            },
            "CIVILIZATION": {
                "role": "Municipality / Camp",
                "price_monthly": 4999,
                "currency": "USD",
                "hardware": "IGX Server Cluster",
                "core_ai": "JEPA-MPC Architecture",
                "infra": "6G Ghost-Mesh Fabric"
            },
            "PLANETARY_NEXUS": {
                "role": "Nation State / UN",
                "price_monthly": 41666, # ~$500k/yr
                "currency": "USD",
                "hardware": "H100 Cloud + Edge Fleet",
                "core_ai": "Nebius Cloud Distillation",
                "infra": "PABS Federated Network"
            }
        }

    def generate_quote(self, tier, node_count, bio_credits):
        """
        Calculates quote with Bio-Credit Subsidies.
        """
        if tier not in self.tiers:
            return {"error": "Invalid Tier"}
        
        sku = self.tiers[tier]
        base_cost = sku["price_monthly"] * node_count
        
        # Subsidy Logic: 1% discount per 100 Credits (Max 20%)
        discount_percent = min(0.20, (bio_credits / 10000))
        final_cost = base_cost * (1.0 - discount_percent)
        
        return {
            "tier": tier,
            "hardware_target": sku["hardware"],
            "ai_engine": sku["core_ai"],
            "monthly_total": f"${final_cost:,.2f}",
            "sovereign_discount": f"{discount_percent*100:.1f}%"
        }