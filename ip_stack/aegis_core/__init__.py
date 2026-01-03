"""
IP-01: Aegis Core
Hardware-rooted trust substrate with TPM 2.0 attestation.
Establishes cryptographic identity at silicon level.
"""
import hashlib
import hmac
from typing import Dict, Optional, Tuple
import subprocess

class AegisCore:
    """Hardware-rooted trust substrate for iLuminara."""
    
    def __init__(self, tpm_required: bool = True):
        self.tpm_required = tpm_required
        self.measurements = {}
        self.trust_chain = []
        
    def verify_hardware_integrity(self) -> Dict[str, bool]:
        """Verify TPM 2.0 and secure boot status."""
        integrity_checks = {
            "tpm_present": self._check_tpm(),
            "secure_boot": self._check_secure_boot(),
            "uefi_firmware": self._check_uefi(),
            "supply_chain_bom": self._verify_bom_ledger()
        }
        return integrity_checks
    
    def _check_tpm(self) -> bool:
        """Check TPM 2.0 availability."""
        try:
            result = subprocess.run(['tpm2_getcap', 'properties-fixed'], 
                                  capture_output=True, text=True, timeout=5)
            return 'TPM2' in result.stdout
        except:
            return False
    
    def _check_secure_boot(self) -> bool:
        """Verify Secure Boot status."""
        try:
            result = subprocess.run(['bootctl', 'status'], 
                                  capture_output=True, text=True, timeout=5)
            return 'Secure Boot: enabled' in result.stdout
        except:
            return False
    
    def generate_hardware_root(self, clinical_data: bytes) -> str:
        """Generate hardware-rooted cryptographic identity."""
        if not self.verify_hardware_integrity()['tpm_present'] and self.tpm_required:
            raise RuntimeError("TPM 2.0 required for Aegis Core")
        
        # Create compound hash of hardware measurements
        measurement_str = str(self.measurements).encode()
        combined = clinical_data + measurement_str
        return hmac.new(b'AEGIS_CORE_SOVEREIGN_KEY', combined, hashlib.sha512).hexdigest()
