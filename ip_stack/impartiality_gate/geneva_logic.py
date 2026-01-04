class GenevaGuard:
    """Common Article 3: Impartiality & Neutrality Gate."""
    def __init__(self):
        self.non_combatant_protection = True

    def redact_location_data(self, record, status="Protected"):
        """IASC 2021: Location redaction for vulnerable populations."""
        if status == "Protected" or status == "Refugee":
            # Strip GPS, maintain only region-level aggregate
            record['gps_lat'] = "REDACTED_GENEVA_ART3"
            record['gps_long'] = "REDACTED_GENEVA_ART3"
            print("[Geneva-Guard] GPS Redacted for Protected Person.")
        return record
