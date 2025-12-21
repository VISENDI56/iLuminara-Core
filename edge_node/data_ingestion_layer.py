iLuminara Data Ingestion Layer v2.0
Scientific Kernel: Spatio-Temporal Decay & Source Weighting (Rift Valley Fever Model)


import random
import math
from datetime import datetime, timedelta

class IngestionEngine:
    def __init__(self):
        # Simulated Data Lake
        self.data_lake = {"EMR": [], "CBS": [], "IDSR": []}

    def _generate_coords(self):
        """Generates random coords near Dadaab (0.0512, 40.3129)"""
        lat = 0.0512 + random.uniform(-0.01, 0.01)
        lon = 40.3129 + random.uniform(-0.01, 0.01)
        return (lat, lon)

    def fetch_emr_data(self):
        """SOURCE 1: EMR (Clinical Truth)"""
        record = {
            "source": "CLINIC_BLOCK_B4",
            "type": "LAB_RESULT",
            "patient_id": f"P-{random.randint(1000,9999)}",
            "diagnosis": "Vibrio cholerae 01",
            "confirmed": True,
            "timestamp": datetime.now(),
            "coords": self._generate_coords()
        }
        self.data_lake["EMR"].append(record)
        return record

    def fetch_cbs_data(self):
        """SOURCE 2: CBS (Community Rumors)"""
        # Simulate a slight time lag (1-3 days ago)
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

        # 1. Temporal Decay (Lambda based on Cholera incubation ~5 days)
        # Formula: e^(-0.5 * (delta_days / 5)^2)
        delta_t_days = (emr['timestamp'] - cbs['timestamp']).total_seconds() / 86400
        temporal_weight = math.exp(-0.5 * (abs(delta_t_days) / 5)**2)

        # 2. Spatial Weight (Inverse Distance)
        dist_km = self._calculate_haversine(emr['coords'], cbs['coords'])
        # Weight degrades rapidly after 2km (slum density)
        spatial_weight = 1 / (1 + (dist_km * 2))

        # 3. Base Confidence
        base_conf = 0.98 if emr['confirmed'] else 0.4

        # Final Fusion Score
        fusion_score = base_conf * temporal_weight * spatial_weight
        
        # Determine Narrative
        if fusion_score > 0.8:
            note = f"CRITICAL CONVERGENCE ({dist_km:.2f}km radius). Lab & Field match."
        elif fusion_score > 0.5:
            note = f"Moderate Correlation. Spatio-temporal decay active ({delta_t_days:.1f} day lag)."
        else:
            note = "Weak Signal Correlation. Sources likely independent."

        return {
            "fusion_score": round(fusion_score, 4),
            "fusion_note": note,
            "live_feeds": [emr, cbs, idsr],
            "physics": {"dist_km": round(dist_km, 2), "time_lag_h": round(delta_t_days*24, 1)}
        }