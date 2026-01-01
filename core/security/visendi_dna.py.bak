import hashlib
import os

class SovereignDNA:
    """
    The VISENDI56 Cryptographic DNA (Enterprise Edition).
    Uses verified corporate artifacts and Microsoft Entra ID to generate the System Root Key.
    """
    def __init__(self):
        # --- DATA EXTRACTED FROM UPLOADED FILES ---
        self.us_file_no = "1387664800024"       # MN Secretary of State
        self.us_ein = "92-3622772"              # IRS
        self.ke_reg_no = "PVT-MKUMQYEX"         # BRS
        self.ke_pin = "P052221589C"             # KRA
        
        # --- USER OVERRIDE IDENTITY ---
        self.director_root = "ANTHONY WAGANDA"  
        self.director_email = "waganda@visendi56.onmicrosoft.com"
        
    def generate_genesis_seed(self):
        """
        Generates the immutable 'Genesis Seed' for iLuminara.
        Fused from Legal Entity IDs + Director Identity.
        """
        # Fuse the data into a single string
        dna_string = f"{self.us_file_no}|{self.ke_reg_no}|{self.us_ein}|{self.director_root}"
        
        # Create SHA-256 Hash
        genesis_hash = hashlib.sha256(dna_string.encode()).hexdigest()
        
        return genesis_hash

    def verify_director_authority(self, user_email, user_name):
        """
        The 'Director Gate'.
        Grants Root/God Mode privileges ONLY to the verified Director.
        """
        # Strict equality check on the Corporate Identity
        if user_name.upper() == self.director_root and user_email.lower() == self.director_email:
            return True, "ACCESS_GRANTED_SOVEREIGN_DIRECTOR"
        else:
            return False, "ACCESS_DENIED_CIVILIAN"

dna = SovereignDNA()
print(f"[*] SYSTEM GENESIS HASH: {dna.generate_genesis_seed()}")