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

# iLuminara Data Ingestion Layer v2.0 (FINAL)
# Scientific Kernel: Spatio-Temporal Decay & Source Weighting
# Reference: Rift Valley Fever Vector Models (Linthicum et al.)


import random
import math
from datetime import datetime, timedelta

class IngestionEngine:
    def __init__(self):
        self.data_lake = {"EMR": [], "CBS": [], "IDSR": []}

    def _generate_coords(self):
        """Generates random coords near Dadaab (0.512, 40.3129)"""
        lat = 0.512 + random.uniform(-0.1, 0.1)
        lon = 40.3129 + random.uniform(-0.1, 0.1)
        return (lat, lon)

    def fetch_emr_data(self):
        """SOURCE 1: EMR (Clinical Truth)"""
        record = {
            "source": "CLINIC_BLOCK_B4",
            "type": "LAB_RESULT",
            "patient_id": f"P-{random.randint(1000,9999)}",
            "diagnosis": "Vibrio cholerae 1",
            "confirmed": True,
            "timestamp": datetime.now(),
            "coords": self._generate_coords()
        }
        self.data_lake["EMR"].append(record)
        return record

    def fetch_cbs_data(self):
        """SOURCE 2: CBS (Community Rumors)"""
        # Simulate lag (Community reports are often delayed)
        lag = random.randint(0, 72)
        signal = {
            "source": "SENTRY_AMINA",
            "type": "SYMPTOM_REPORT",
            "observation": "Acute Watery Diarrhea",
            "count": random.randint(1, 5),
            "timestamp": datetime.now() - timedelta(hours=lag),
            "coords": self._generate_coords()
        }
        self.data_lake["CBS"].append(signal)
        return signal

    def fetch_idsr_data(self):
        """SOURCE 3: IDSR (National Context)"""
        alert = {
            "source": "MINISTRY_HEALTH_KENYA",
            "region_risk": "HIGH",
            "alert_level": "PHASE_2",
            "advisory": "Flood waters increasing vector breeding."
        }
        self.data_lake["IDSR"].append(alert)
        return alert

    def _calculate_haversine(self, coord1, coord2):
        """Returns distance in km between two lat/lon tuples"""
        R = 6371  # Earth radius in km
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    def fuse_data_streams(self):
        """
        THE GOLDEN THREAD CALCULUS
        Prob(Truth) = Base_Conf * Temporal_Decay * Spatial_Weight
        """
        emr = self.fetch_emr_data()
        cbs = self.fetch_cbs_data()
        idsr = self.fetch_idsr_data()

        # 1. Temporal Decay: e^(-0.5 * (delta_days / 5)^2)
        # 5 days is the serial interval for Cholera
        delta_t_days = (emr['timestamp'] - cbs['timestamp']).total_seconds() / 86400
        temporal_weight = math.exp(-0.5 * (abs(delta_t_days) / 5)**2)

        # 2. Spatial Weight: Inverse Distance
        dist_km = self._calculate_haversine(emr['coords'], cbs['coords'])
        spatial_weight = 1 / (1 + (dist_km * 2)) # Degrades fast after 2km

        # 3. Base Confidence
        base_conf = 0.98 if emr['confirmed'] else 0.4

        # Final Fusion Score
        fusion_score = base_conf * temporal_weight * spatial_weight
        
        if fusion_score > 0.8:
            note = f"CRITICAL CONVERGENCE ({dist_km:.2f}km radius). Lab & Field match."
        elif fusion_score > 0.5:
            note = f"Moderate Correlation. Spatio-temporal decay active ({delta_t_days:.1f}d lag)."
        else:
            note = "Weak Signal Correlation. Sources likely independent."

        return {
            "fusion_score": round(fusion_score, 4),
            "fusion_note": note,
            "live_feeds": [emr, cbs, idsr],
            "physics": {"dist_km": round(dist_km, 2), "time_lag_h": round(delta_t_days*24, 1)}
        }