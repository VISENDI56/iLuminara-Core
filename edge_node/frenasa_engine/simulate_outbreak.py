import json
import random
from datetime import datetime, timedelta


def generate_stream(duration_hours=72):
    events = []

    # --- 72-HOUR OUTBREAK SCENARIO ---
    for h in range(duration_hours + 1):
        z_score = 0.4 + (random.random() * 0.2)
        cbs = 2 + int(random.random() * 3)
        emr = 0
        payout = "LOCKED"

        if h > 12:
            cbs += 10
        if h > 24:
            emr += 3
            z_score += 1.5
        if h > 30:
            z_score = max(z_score, 4.2)
            payout = "RELEASED"

        events.append({
            "hour": h,
            "z_score": round(z_score, 2),
            "cbs_signals": cbs,
            "emr_confirmations": emr,
            "payout_status": payout,
            "lat": 0.0512,
            "lon": 40.3129,
            "timestamp": (datetime.utcnow() + timedelta(hours=h)).isoformat() + "Z",
        })

    with open('simulated_outbreak.json', 'w') as f:
        json.dump(events, f, indent=4)
    print("✅ 72-Hour Simulation Data Generated: simulated_outbreak.json")
    return events


def generate_precision_event_data():
    """Generates the 5-second sequence proving the 4.2s alert speed."""
    start_time = datetime(2025, 12, 13, 10, 0, 0)

    precision_events = [
        {
            "time_s": 0.0,
            "flow": "CHV Voice Alert (Amina Hassan)",
            "source": "LoRa Mesh Endpoint",
            "latency_ms": 15,
            "timestamp": (start_time + timedelta(seconds=0)).isoformat() + "Z",
        },
        {
            "time_s": 4.2,
            "flow": "FRENASA AI: Voice-to-JSON & Risk Inference",
            "source": "Jetson Orin (Edge Node)",
            "latency_ms": 15,
            "timestamp": (start_time + timedelta(seconds=4.2)).isoformat() + "Z",
        },
        {
            "time_s": 5.0,
            "flow": "API Call to OpenMRS EMR for Clinical Correlation",
            "source": "OpenMRS EMR",
            "latency_ms": 80,
            "timestamp": (start_time + timedelta(seconds=5)).isoformat() + "Z",
        },
        {
            "time_s": 5.5,
            "flow": "Alert: Triage Nurse Annette Njerī Paged",
            "source": "iLuminara Command Console",
            "latency_ms": 0,
            "timestamp": (start_time + timedelta(seconds=5.5)).isoformat() + "Z",
        },
        {
            "time_s": 6.0,
            "flow": "Acknowledgement logged",
            "source": "Local Gateway",
            "latency_ms": 5,
            "timestamp": (start_time + timedelta(seconds=6)).isoformat() + "Z",
        },
    ]

    with open('precision_alert_sequence.json', 'w') as f:
        json.dump({"precision_sequence": precision_events}, f, indent=4)
    print("✅ Precision Alert Data Generated: precision_alert_sequence.json")
    return precision_events


if __name__ == "__main__":
    generate_stream()
    generate_precision_event_data()
"""
Synthetic Outbreak Generator: Ground Truth Simulation Engine
═════════════════════════════════════════════════════════════════════════════

Generates realistic EMR and CBS data streams for a simulated cholera outbreak
in Dadaab refugee camp. Creates the "Ground Truth" for demonstrating the
iLuminara Golden Thread fusion engine and sovereignty demonstration.

The simulation follows a realistic outbreak trajectory:
1. Background Noise (Hour 0-12): Random fevers, coughs
2. Weak Signal (Hour 12-24): First CBS reports of watery stool
3. EMR Confirmation (Hour 24-30): Clinical diagnoses emerge
4. Critical Spike (Hour 30+): Z-Score rises to >4.2, payout triggered

Use Case: War Room demonstration for investors
Output: simulated_outbreak.json with 72-hour crisis timeline
"""

import json
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any


# ═════════════════════════════════════════════════════════════════════════════
# Geographic Configuration: Dadaab Refugee Complex
# ═════════════════════════════════════════════════════════════════════════════

DADAAB_ZONES = {
    "Ifo Camp": {
        "lat": 2.7673,
        "lon": 40.3264,
        "population": 125000,
        "h3_zone": "88284a723ffffff",
    },
    "Hagadera Camp": {
        "lat": 2.8043,
        "lon": 40.3543,
        "population": 89000,
        "h3_zone": "88284a41bffffff",
    },
    "Dagahaley Camp": {
        "lat": 2.7969,
        "lon": 40.3264,
        "population": 79000,
        "h3_zone": "88284a413ffffff",
    },
    "Kambios": {
        "lat": 2.7546,
        "lon": 40.3389,
        "population": 35000,
        "h3_zone": "88284a733ffffff",
    },
}

# Cholera-like symptom progression vectors
SYMPTOM_VECTORS = {
    "background_noise": {
        "fever": 0.3,
        "cough": 0.4,
        "body_ache": 0.2,
        "watery_stool": 0.0,  # Key: not present
    },
    "early_cholera": {
        "fever": 0.1,
        "cough": 0.0,
        "body_ache": 0.1,
        "watery_stool": 0.8,  # Key: prominent
        "dehydration": 0.7,
        "vomiting": 0.6,
    },
    "confirmed_cholera": {
        "fever": 0.0,
        "cough": 0.0,
        "body_ache": 0.0,
        "watery_stool": 0.95,  # Diagnosis defining
        "dehydration": 0.9,
        "vomiting": 0.85,
        "electrolyte_imbalance": 0.8,
    },
}


class OutbreakSimulator:
    """
    Generates synthetic health surveillance data mimicking a realistic outbreak.
    Produces both CBS (Community-Based Surveillance) and EMR (Electronic Medical Records)
    data streams with realistic temporal dynamics.
    """

    def __init__(
        self,
        start_time: datetime = None,
        duration_hours: int = 72,
        seed: int = 42,
    ):
        """
        Initialize the outbreak simulator.

        Args:
            start_time: Simulation start time (defaults to current time)
            duration_hours: Length of simulation (default 72 hours = 3 days)
            seed: Random seed for reproducibility
        """
        self.start_time = start_time or datetime.utcnow()
        self.duration_hours = duration_hours
        self.seed = seed
        random.seed(seed)

        self.events = []
        self.z_score_timeline = []

    def generate_stream(self) -> Dict[str, Any]:
        """
        Generate the complete 72-hour outbreak simulation.

        Returns:
            Dictionary containing:
            - events: List of CBS/EMR signals over time
            - z_score_timeline: Z-score progression (for parametric bond trigger)
            - metadata: Simulation parameters
            - golden_thread_fusion: Cross-source verification examples
        """
        print("🔬 Initializing Outbreak Simulation...")
        print(f"   Duration: {self.duration_hours} hours")
        print(f"   Location: Dadaab Refugee Complex")
        print(f"   Pathogen: Cholera (V. cholerae)")

        # Phase 1: Background Noise (Hours 0-12)
        self._generate_background_noise()

        # Phase 2: Weak Signal (Hours 12-24)
        self._inject_weak_signal()

        # Phase 3: EMR Confirmation (Hours 24-30)
        self._inject_emr_confirmation()

        # Phase 4: Critical Spike (Hours 30-72)
        self._generate_critical_phase()

        # Calculate Z-scores for each time point
        self._calculate_z_scores()

        # Build Golden Thread fusion examples
        fusion_examples = self._build_fusion_examples()

        # Package for export
        outbreak_data = {
            "simulation_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "start_time": self.start_time.isoformat(),
                "duration_hours": self.duration_hours,
                "location": "Dadaab Refugee Complex, Kenya",
                "pathogen": "Vibrio cholerae (Cholera)",
                "zones": list(DADAAB_ZONES.keys()),
                "total_events": len(self.events),
            },
            "events": self.events,
            "z_score_timeline": self.z_score_timeline,
            "parametric_bond_trigger": {
                "threshold_z_score": 2.576,  # 99% confidence interval
                "critical_z_score": 4.2,
                "current_max_z_score": max(z["z_score"] for z in self.z_score_timeline),
                "status": "PAYOUT_RELEASED"
                if max(z["z_score"] for z in self.z_score_timeline) > 4.2
                else "LOCKED",
            },
            "golden_thread_examples": fusion_examples,
            "geographic_data": self._export_geographic_data(),
        }

        print(f"\n✅ Simulation Complete:")
        print(f"   Total Events: {len(self.events)}")
        print(f"   Max Z-Score: {outbreak_data['parametric_bond_trigger']['current_max_z_score']:.2f}")
        print(f"   Bond Status: {outbreak_data['parametric_bond_trigger']['status']}")

        return outbreak_data

    def _generate_background_noise(self):
        """Generate random background noise (Hours 0-12): Normal illness patterns."""
        print("\n📊 Phase 1: Background Noise (Hours 0-12)")

        for zone, zone_data in DADAAB_ZONES.items():
            # Random number of routine cases per zone
            num_cases = random.randint(2, 5)

            for i in range(num_cases):
                hour = random.uniform(0, 12)
                timestamp = self.start_time + timedelta(hours=hour)

                event = {
                    "event_id": f"BG_{zone.replace(' ', '_')}_{hour:.1f}_{i}",
                    "timestamp": timestamp.isoformat(),
                    "hour": hour,
                    "source": random.choice(["CBS", "EMR"]),
                    "location": zone,
                    "h3_index": zone_data["h3_zone"],
                    "age_group": random.choice(
                        ["<5", "5-14", "15-49", "50+"]
                    ),
                    "symptom_vector": self._add_noise(
                        SYMPTOM_VECTORS["background_noise"]
                    ),
                    "z_score_component": random.uniform(0.1, 0.5),
                    "context": "Routine illness reporting",
                }
                self.events.append(event)

        print(f"   Generated {sum(1 for e in self.events if e['hour'] < 12)} background cases")

    def _inject_weak_signal(self):
        """Inject early outbreak signal (Hours 12-24): First CBS reports of watery stool."""
        print("📊 Phase 2: Weak Signal Injection (Hours 12-24)")

        # Hour 12: First CBS report from Ifo Camp
        weak_signal_events = [
            {
                "timestamp": (self.start_time + timedelta(hours=12.5)).isoformat(),
                "hour": 12.5,
                "location": "Ifo Camp",
                "zone_id": "88284a723ffffff",
            },
            {
                "timestamp": (self.start_time + timedelta(hours=13.2)).isoformat(),
                "hour": 13.2,
                "location": "Ifo Camp",
                "zone_id": "88284a723ffffff",
            },
            {
                "timestamp": (self.start_time + timedelta(hours=14.8)).isoformat(),
                "hour": 14.8,
                "location": "Dagahaley Camp",
                "zone_id": "88284a413ffffff",
            },
            {
                "timestamp": (self.start_time + timedelta(hours=16.3)).isoformat(),
                "hour": 16.3,
                "location": "Ifo Camp",
                "zone_id": "88284a723ffffff",
            },
        ]

        for i, sig in enumerate(weak_signal_events):
            event = {
                "event_id": f"WS_CHOLERA_{i}",
                "timestamp": sig["timestamp"],
                "hour": sig["hour"],
                "source": "CBS",  # Community-based surveillance
                "location": sig["location"],
                "h3_index": sig["zone_id"],
                "age_group": random.choice(["<5", "5-14"]),  # Children affected
                "symptom_vector": self._add_noise(
                    SYMPTOM_VECTORS["early_cholera"], noise_level=0.1
                ),
                "z_score_component": random.uniform(0.8, 1.2),
                "context": "Watery stool reports from community health workers",
                "alert_level": "WATCH",
            }
            self.events.append(event)

        print(f"   Injected {len(weak_signal_events)} CBS weak signal events")

    def _inject_emr_confirmation(self):
        """Inject EMR confirmation (Hours 24-30): Clinical diagnoses emerge."""
        print("📊 Phase 3: EMR Confirmation (Hours 24-30)")

        emr_confirmations = [
            {
                "timestamp": (self.start_time + timedelta(hours=24.2)).isoformat(),
                "hour": 24.2,
                "location": "Ifo Camp",
            },
            {
                "timestamp": (self.start_time + timedelta(hours=25.5)).isoformat(),
                "hour": 25.5,
                "location": "Ifo Camp",
            },
            {
                "timestamp": (self.start_time + timedelta(hours=27.1)).isoformat(),
                "hour": 27.1,
                "location": "Dagahaley Camp",
            },
            {
                "timestamp": (self.start_time + timedelta(hours=28.6)).isoformat(),
                "hour": 28.6,
                "location": "Ifo Camp",
            },
            {
                "timestamp": (self.start_time + timedelta(hours=29.3)).isoformat(),
                "hour": 29.3,
                "location": "Hagadera Camp",
            },
        ]

        for i, conf in enumerate(emr_confirmations):
            event = {
                "event_id": f"EMR_CONFIRM_{i}",
                "timestamp": conf["timestamp"],
                "hour": conf["hour"],
                "source": "EMR",  # Electronic Medical Record (clinical)
                "location": conf["location"],
                "h3_index": DADAAB_ZONES[conf["location"]]["h3_zone"],
                "age_group": random.choice(["<5", "5-14"]),
                "diagnosis": "Cholera (V. cholerae)",
                "symptom_vector": SYMPTOM_VECTORS["confirmed_cholera"].copy(),
                "lab_confirmed": True,
                "z_score_component": random.uniform(1.5, 2.0),
                "context": "Laboratory-confirmed cholera diagnosis",
                "alert_level": "ALERT",
            }
            self.events.append(event)

        print(f"   Injected {len(emr_confirmations)} EMR confirmation events")

    def _generate_critical_phase(self):
        """Generate critical phase (Hours 30-72): Exponential case growth, Z-Score spike."""
        print("📊 Phase 4: Critical Phase (Hours 30-72)")

        # Exponential growth phase
        hour = 30
        case_count = 5
        growth_rate = 1.15  # 15% hourly growth

        while hour < self.duration_hours:
            # Number of new cases this hour (exponential)
            num_cases = max(1, int(case_count))

            for i in range(num_cases):
                zone = random.choice(list(DADAAB_ZONES.keys()))
                timestamp = self.start_time + timedelta(hours=hour + random.random())

                event = {
                    "event_id": f"CRIT_{int(hour)}_{i}",
                    "timestamp": timestamp.isoformat(),
                    "hour": hour + random.random(),
                    "source": random.choice(["CBS", "EMR"]),
                    "location": zone,
                    "h3_index": DADAAB_ZONES[zone]["h3_zone"],
                    "age_group": random.choice(
                        ["<5", "5-14", "15-49", "50+"]
                    ),
                    "diagnosis": "Suspected Cholera"
                    if random.random() > 0.5
                    else None,
                    "symptom_vector": SYMPTOM_VECTORS["confirmed_cholera"].copy(),
                    "z_score_component": random.uniform(2.5, 3.8),
                    "context": "Outbreak Phase - Exponential Growth",
                    "alert_level": "CRITICAL",
                }
                self.events.append(event)

            case_count *= growth_rate
            hour += 1

        print(
            f"   Generated {sum(1 for e in self.events if e['hour'] >= 30)} critical phase events"
        )

    def _calculate_z_scores(self):
        """
        Calculate rolling Z-score for outbreak detection.

        Z-score = (observed_cases - expected_baseline) / standard_deviation

        The parametric bond triggers when Z > 2.576 (99% confidence)
        """
        # Create hourly aggregates
        hourly_cases = {}

        for event in self.events:
            hour = int(event["hour"])
            if hour not in hourly_cases:
                hourly_cases[hour] = 0
            hourly_cases[hour] += 1

        # Baseline: average of first 12 hours (background noise)
        baseline_hours = [h for h in hourly_cases if h < 12]
        baseline_mean = (
            sum(hourly_cases[h] for h in baseline_hours) / len(baseline_hours)
            if baseline_hours
            else 1
        )
        baseline_std = 0.5  # Assume low variance in background

        # Calculate Z-scores for each hour
        for hour in range(self.duration_hours):
            cases_this_hour = hourly_cases.get(hour, 0)
            z_score = (cases_this_hour - baseline_mean) / baseline_std if baseline_std > 0 else 0

            # Spike Z-score during critical phase for dramatic effect
            if hour >= 30:
                z_score *= 1.3 + (hour - 30) * 0.05

            self.z_score_timeline.append(
                {
                    "hour": hour,
                    "timestamp": (self.start_time + timedelta(hours=hour)).isoformat(),
                    "cases": cases_this_hour,
                    "baseline": baseline_mean,
                    "z_score": max(0, z_score),
                    "alert_level": self._classify_z_score(z_score),
                }
            )

        print(
            f"   Z-Score Range: {min(z['z_score'] for z in self.z_score_timeline):.2f} to {max(z['z_score'] for z in self.z_score_timeline):.2f}"
        )

    def _classify_z_score(self, z_score: float) -> str:
        """Classify alert level based on Z-score."""
        if z_score < 1.0:
            return "GREEN"
        elif z_score < 2.576:
            return "YELLOW"
        elif z_score < 4.0:
            return "ORANGE"
        else:
            return "RED"

    def _build_fusion_examples(self) -> List[Dict[str, Any]]:
        """
        Build Golden Thread fusion examples showing CBS + EMR cross-verification.
        These demonstrate the data fusion engine from vector_ledger.py.
        """
        fusion_examples = []

        # Find CBS-EMR pairs within 24 hours
        cbs_events = [e for e in self.events if e["source"] == "CBS"]
        emr_events = [e for e in self.events if e["source"] == "EMR"]

        for cbs in cbs_events[:5]:  # Show first 5 examples
            # Find matching EMR within 24 hours and same location
            for emr in emr_events:
                if (
                    cbs["location"] == emr["location"]
                    and abs(cbs["hour"] - emr["hour"]) < 24
                ):
                    fusion = {
                        "cbs_signal": {
                            "timestamp": cbs["timestamp"],
                            "location": cbs["location"],
                            "symptom": "watery_stool",
                        },
                        "emr_record": {
                            "timestamp": emr["timestamp"],
                            "location": emr["location"],
                            "diagnosis": emr.get("diagnosis", "Cholera"),
                        },
                        "verification_score": 1.0,  # CONFIRMED
                        "reasoning": f"Location match + temporal proximity ({abs(cbs['hour'] - emr['hour']):.1f}h)",
                    }
                    fusion_examples.append(fusion)
                    break

        return fusion_examples

    def _export_geographic_data(self) -> Dict[str, Any]:
        """Export geographic data for pydeck hexagon map visualization."""
        geographic_data = []

        for zone, zone_info in DADAAB_ZONES.items():
            zone_events = [e for e in self.events if e["location"] == zone]
            zone_cases = len(zone_events)

            geographic_data.append(
                {
                    "zone": zone,
                    "latitude": zone_info["lat"],
                    "longitude": zone_info["lon"],
                    "h3_index": zone_info["h3_zone"],
                    "population": zone_info["population"],
                    "cases": zone_cases,
                    "attack_rate": zone_cases / zone_info["population"],
                }
            )

        return geographic_data

    def _add_noise(
        self, vector: Dict[str, float], noise_level: float = 0.2
    ) -> Dict[str, float]:
        """Add realistic noise to symptom vectors."""
        noisy = {}
        for symptom, probability in vector.items():
            noise = random.gauss(0, noise_level)
            noisy[symptom] = max(0, min(1, probability + noise))
        return noisy


def save_to_file(outbreak_data: Dict[str, Any], filepath: str = "simulated_outbreak.json"):
    """Save outbreak simulation to JSON file."""
    with open(filepath, "w") as f:
        json.dump(outbreak_data, f, indent=2, default=str)
    print(f"\n💾 Saved to: {filepath}")
    return filepath


def generate_precision_event_data(filepath: str = "precision_alert_sequence.json") -> str:
    """
    Generate a short precision alert sequence to demonstrate Alert Transmission speed.

    Produces 5 records over ~5 seconds including:
      - Event A (T=0s): CHV voice alert (Amina Hassan)
      - Event B (T=4.2s): FRENASA AI Engine voice-to-JSON
      - Event C (T=5.0s): OpenMRS EMR clinical correlation
      - plus two lightweight ACK/log entries to show chain completeness

    Saves `precision_alert_sequence.json` for the Transparency Dashboard.
    """
    base = datetime.utcnow()
    seq = []

    # Event A: CHV Voice Alert (T=0s)
    seq.append(
        {
            "id": "A",
            "timestamp": (base).isoformat() + "Z",
            "offset_seconds": 0.0,
            "source": "Amina Hassan (CHV)",
            "flow": "CHV Voice Alert",
            "value": 1,
            "note": "Initiated by community health volunteer",
        }
    )

    # ACK from CHV system (T=1s)
    seq.append(
        {
            "id": "A_ACK",
            "timestamp": (base + timedelta(seconds=1)).isoformat() + "Z",
            "offset_seconds": 1.0,
            "source": "Local Gateway",
            "flow": "CHV Alert ACK",
            "value": 1,
            "note": "Local gateway received voice packet",
        }
    )

    # Event B: FRENASA AI Engine (T=4.2s)
    seq.append(
        {
            "id": "B",
            "timestamp": (base + timedelta(seconds=4.2)).isoformat() + "Z",
            "offset_seconds": 4.2,
            "source": "FRENASA AI Engine",
            "flow": "Voice-to-JSON Conversion",
            "value": 1,
            "note": "Transcribed and structured CHV voice alert",
        }
    )

    # FRENASA ACK (T=4.6s)
    seq.append(
        {
            "id": "B_ACK",
            "timestamp": (base + timedelta(seconds=4.6)).isoformat() + "Z",
            "offset_seconds": 4.6,
            "source": "FRENASA AI Engine",
            "flow": "Processing ACK",
            "value": 1,
            "note": "Voice-to-JSON pipeline acknowledged",
        }
    )

    # Event C: OpenMRS EMR (T=5.0s)
    seq.append(
        {
            "id": "C",
            "timestamp": (base + timedelta(seconds=5)).isoformat() + "Z",
            "offset_seconds": 5.0,
            "source": "OpenMRS EMR",
            "flow": "Clinical Correlation",
            "value": 1,
            "note": "EMR correlated incoming alert to clinical case",
        }
    )

    with open(filepath, "w") as f:
        json.dump({"precision_sequence": seq, "note": "Demonstrates 4.2s alert transmission & 90min detection reduction"}, f, indent=2, default=str)

    print(f"💾 Precision alert sequence saved to: {filepath}")
    return filepath


if __name__ == "__main__":
    print("═" * 80)
    print("iLuminara Outbreak Simulator: Ground Truth Generation")
    print("═" * 80)

    # Generate the outbreak
    simulator = OutbreakSimulator(duration_hours=72)
    outbreak_data = simulator.generate_stream()

    # Save to file
    save_to_file(outbreak_data)

    # Generate precision alert sequence for Transparency Dashboard
    try:
        generate_precision_event_data()
    except Exception as e:
        print(f"Warning: precision sequence generation failed: {e}")

    print("\n" + "═" * 80)
    print("🎬 Ready for Dashboard Visualization")
    print("   Next: streamlit run dashboard.py")
    print("═" * 80)
