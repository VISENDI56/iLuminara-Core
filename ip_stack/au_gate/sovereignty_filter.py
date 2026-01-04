class AfricanSovereigntyGate:
    """AU Malabo & Nigeria NDPR Compliance."""
    def verify_regional_transfer(self, target_country, data_type="HEALTH"):
        # Enforce AU-specific SCCs
        authorized_regions = ['ECOWAS', 'SADC', 'EAC', 'MAGHREB']
        if target_country in authorized_regions:
            return True
        print(f"[AU-Gate] ALERT: Transfer to {target_country} requires Ministerial Approval.")
        return False

    def get_ndpr_consent_lang(self, region):
        langs = {"Lagos": "Yoruba", "Kano": "Hausa", "Enugu": "Igbo"}
        return langs.get(region, "English")
