class GenevaGate:
    """IHL Common Article 3 Compliance."""
    def verify_neutrality(self, patient_metadata):
        # Prevent prioritization based on non-medical indicators
        forbidden_keys = ['affiliation', 'combatant_status', 'political_rank']
        for key in forbidden_keys:
            if key in patient_metadata:
                print("[GenevaGate] VIOLATION: Non-neutral metadata detected. Blocking.")
                return False
        return True

    def iasc_redaction(self, location_data, population_type="REFUGEE"):
        if population_type == "REFUGEE":
            # Redact to 2 decimal places (approx 1.1km) to prevent targeting
            return round(location_data, 2)
        return location_data
