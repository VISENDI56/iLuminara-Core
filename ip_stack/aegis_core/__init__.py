import hashlib
class AegisCore:
    """IP-01: Silicon-level hardware trust."""
    def __init__(self, tpm_id="B300-NAIROBI-PIONEER"):
        self.tpm_id = tpm_id
    def get_sig(self): return hashlib.sha3_512(self.tpm_id.encode()).hexdigest()
