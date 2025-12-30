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

import datetime
from typing import Dict, List, Optional

class SovereignPricingModel:
    """
    The Official 2026 Sovereign Pricing Matrix.
    Defines the 4 Tiers of the iLuminara Civilization OS.
    """
    _tiers: Dict[str, Dict] = {
        "SOVEREIGN_NODE": {
            "role": "Clinic / NGO Edge Node",
            "price_monthly_usd": 99,
            "hardware_target": "NVIDIA Jetson Orin Nano (67 TOPS Generative AI Capable)",
            "core_ai_engine": "Tiny Recursive Model (TRM) – Offline-First Active Inference",
            "infrastructure": "Hyperledger Besu (Air-Gapped Private Network)",
            "compliance_level": "ZKP Identity + Omni-Law Lite",
            "geospatial": "Esri GeoGhost Offline Mapping"
        },
        "BIO_FOUNDRY": {
            "role": "Field Hospital / Genomic Lab",
            "price_monthly_usd": 999,
            "hardware_target": "NVIDIA IGX Orin (Industrial-Grade Safety Certified)",
            "core_ai_engine": "BioNeMo Evo 2 (FP8 Optimized Genomic Foundation Model)",
            "infrastructure": "IGX Safety Island Root-of-Trust",
            "compliance_level": "Omni-Law Standard",
            "geospatial": "NVIDIA Holoscan Real-Time Sensor Fusion"
        },
        "CIVILIZATION": {
            "role": "Municipality / Refugee Camp / Disaster Zone",
            "price_monthly_usd": 4999,
            "hardware_target": "IGX Orin Server Cluster (Multi-Node Redundancy)",
            "core_ai_engine": "JEPA-MPC Architecture (Predictive World Model + Model-Predictive Control)",
            "infrastructure": "6G Ghost-Mesh Fabric (Ad-Hoc Resilient Networking)",
            "compliance_level": "Omni-Law Standard + Active Interceptor",
            "geospatial": "NVIDIA Modulus Physics-Informed ML"
        },
        "PLANETARY_NEXUS": {
            "role": "Nation State / UN Agency / Global Coalition",
            "price_monthly_usd": 41666,  # Equivalent to ~$500,000 annual baseline
            "hardware_target": "H100/H200 Cloud Fleet + Sovereign Edge Federation",
            "core_ai_engine": "Nebius Cloud Distillation + BioNeMo Evo 2 Ensemble",
            "infrastructure": "PABS Federated Network (Pathogen Access & Benefit-Sharing Compliant)",
            "compliance_level": "Constitutional Customization + 47-Framework Enforcement",
            "geospatial": "NVIDIA Omniverse Digital Twin Platform"
        }
    }

    def __init__(self):
        self.current_year = datetime.datetime.now().year

    @classmethod
    def list_tiers(cls) -> List[str]:
        """Return ascending order of sovereign evolution"""
        return list(cls._tiers.keys())

    def get_tier_details(self, tier: str) -> Optional[Dict]:
        return self._tiers.get(tier.upper())

    def generate_quote(
        self,
        tier: str,
        node_count: int = 1,
        bio_credits: float = 0.0,
        annual: bool = False
    ) -> Dict:
        """
        Quantum-Entangled Quote Generator.
        Incorporates Bio-Credit Sovereignty Subsidies (1% per 10,000 credits, capped at 20%).
        Supports monthly or annual projection.
        """
        tier_key = tier.upper()
        if tier_key not in self._tiers:
            return {"error": "Invalid Sovereign Tier – Ascension Path Not Found"}

        sku = self._tiers[tier_key]
        base_monthly = sku["price_monthly_usd"] * node_count
        multiplier = 12 if annual else 1
        base_total = base_monthly * multiplier

        # Bio-Credit Subsidy Alchemy: Max 20% sovereign discount
        discount_percent = min(0.20, bio_credits / 10000.0)
        final_total = base_total * (1.0 - discount_percent)

        return {
            "tier": tier_key.replace("_", " ").title(),
            "role": sku["role"],
            "node_count": node_count,
            "hardware_target": sku["hardware_target"],
            "core_ai_engine": sku["core_ai_engine"],
            "infrastructure": sku["infrastructure"],
            "base_total_usd": f"${base_total:,.2f} {'/ year' if annual else '/ month'}",
            "bio_credit_subsidy_applied": f"{discount_percent * 100:.1f}%",
            "final_total_usd": f"${final_total:,.2f} {'/ year' if annual else '/ month'}",
            "quote_generated": datetime.datetime.utcnow().isoformat() + "Z",
            "sovereign_note": "Data Never Leaves Jurisdiction – Only Gradients Flow"
        }

    def calculate_outcome_subsidy(self, prediction_error):
        """
        Calculates a 'Precision Subsidy' for the customer.
        The better the JEPA World Model performs, the more the customer saves.
        """
        # Lower error = Higher subsidy for the host government
        subsidy_rate = max(0, 0.20 - (prediction_error * 0.5))
        return subsidy_rate