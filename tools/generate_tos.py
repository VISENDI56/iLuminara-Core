from core.legal.jurisdiction_resolver import JurisdictionEngine
import datetime

def generate_agreement(region):
    engine = JurisdictionEngine(region)
    ctrl = engine.get_controller()
    ent = ctrl['entity']
    
    tos_text = f"""
Terms of Service (Sovereign License)
====================================
Last Updated: {datetime.date.today()}

1. PARTIES
This agreement is between You ("Licensee") and {ent.legal_name} ("Licensor"), 
a company registered in {ent.address.country} under number {ent.registration_number}.

2. ADDRESS FOR SERVICE
USA: 5200 Wilson Rd, Ste 150, Edina, MN 55424
KENYA: The Billows, Ring Rd, Kilimani, PO Box 35827-00200, Nairobi

3. GOVERNING LAW
This agreement shall be governed by the laws of {ctrl['governing_law']}. 
Disputes shall be settled in {ctrl['arbitration_venue']}.

4. IP OWNERSHIP
The "Nuclear IP Stack" (BioNeMo, JEPA, Omni-Law) remains the sole property 
of VISENDI56. Use is strictly limited to Humanitarian/Sovereign purposes 
unless a Commercial License is granted.
"""
    
    filename = f"docs/legal/TERMS_{region}.txt"
    with open(filename, "w") as f:
        f.write(tos_text)
    print(f"✅ Generated ToS for {region}: {filename}")

if __name__ == "__main__":
    generate_agreement("USA")
    generate_agreement("KENYA")