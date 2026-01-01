# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

import random
import time
import json

class LiveDataHarness:
    """
    Simulates the chaotic real-world inputs for the Omni-Law Matrix.
    """
    def generate_financial_event(self):
        # 5% chance of Sanctioned Entity
        payee = "Global-Supplies-Ltd" if random.random() > 0.5 else "SC-9982"
        amount = random.randint(5000, 50000)
        return {"context": "FINANCE", "payload": {"payee_id": payee, "amount": amount}}

    def generate_supply_chain_event(self):
        # 10% chance of Forced Labor Region
        origin = "Shenzhen" if random.random() > 0.1 else "XUAR"
        material = random.choice(["Silicon", "Gold", "Cotton"])
        return {"context": "SUPPLY_CHAIN", "payload": {"origin": origin, "material": material}}

    def generate_esg_event(self):
        # Random logistics emissions
        return {
            "context": "LOGISTICS",
            "payload": {
                "destination": "EU",
                "distance_km": random.randint(100, 5000),
                "weight_kg": random.randint(50, 1000)
            }
        }

    def get_next_event(self):
        """Randomly selects a sector event to stream."""
        generators = [self.generate_financial_event, self.generate_supply_chain_event, self.generate_esg_event]
        return random.choice(generators)()
