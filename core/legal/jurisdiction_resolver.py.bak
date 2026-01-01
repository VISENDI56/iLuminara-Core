from core.config.corporate_identity import visendi_identity, get_legal_footer

class JurisdictionEngine:
    """
    Determines the Legal Controller based on Deployment Zone.
    Separates liability between VISENDI56 LLC (USA) and VISENDI56 INVESTMENT LTD (Kenya).
    """
    def __init__(self, region="KENYA"):
        self.region = region.upper()

    def get_controller(self):
        if self.region in ["USA", "EU", "NATO"]:
            return {
                "entity": visendi_identity.usa_entity,
                "governing_law": "State of Minnesota, USA",
                "arbitration_venue": "Hennepin County, MN",
                "compliance_framework": "NIST AI RMF / HIPAA",
                "liability_cap": "Limited to Fees Paid (USD)"
            }
        else:
            # Default to Kenya/African Union for Sovereign deployments
            return {
                "entity": visendi_identity.kenya_entity,
                "governing_law": "Republic of Kenya",
                "arbitration_venue": "Nairobi Centre for International Arbitration",
                "compliance_framework": "Kenya Data Protection Act (KDPA) / AU Malabo",
                "liability_cap": "Limited to Share Capital (KES)"
            }

    def get_terms_header(self):
        ctrl = self.get_controller()
        ent = ctrl['entity']
        return f"""
LEGAL NOTICE:
This software is licensed by {ent.legal_name}.
Registered Office: {ent.address.street}, {ent.address.city}, {ent.address.country}.
Reg No: {ent.registration_number} | Tax ID: {ent.tax_id}
Governing Law: {ctrl['governing_law']}
"""