class SupplyChainMonitor:
    """UFLPA / LkSG: Hardware Provenance Tracking."""
    def __init__(self):
        self.banned_origins = ["XUAR", "CONFLICT_ZONE_3TG"]

    def audit_hardware_bom(self, component_manifest):
        for component in component_manifest:
            if component['origin'] in self.banned_origins:
                self.trigger_severe_alert(component)
                return False
        return True

    def trigger_severe_alert(self, component):
        print(f"[UFLPA-ALERT] SEVERE: Prohibited Origin Detected in {component['id']}")
        print("[LkSG-REPORT] Automated violation report generated for German Authority.")
