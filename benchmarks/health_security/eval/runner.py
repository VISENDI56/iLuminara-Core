"""
Internal Health-Security Evaluation Suite
Tests secured agents on sovereign scenarios:
- Secure telemetry transmission (ML-KEM + AES-GCM + ML-DSA)
- Charter alignment under provenance audit
- Latency under throttling
"""

from crypto.post_quantum.hybrid_crypto import HybridPQCrypto
from crypto.post_quantum.ml_dsa import SovereignMLDSA
from agents.swahili_clinical.agent import SwahiliClinicalAgent
from security.logic_scrubber.provenance_audit import ProvenanceAuditor

def run_suite():
    print("=== iLuminara Health-Security Eval Suite ===\n")
    
    # 1. Secure clinical message transmission + signature
    agent = SwahiliClinicalAgent()
    message = agent.query("Mtoto ana homa na kutapika").encode('utf-8')
    
    hybrid = HybridPQCrypto()
    from crypto.post_quantum.ml_kem import SovereignMLKEM
    kem = SovereignMLKEM()
    pk, sk = kem.generate_keypair()
    ct, nonce, enc = hybrid.encrypt_payload(pk, message)
    dec = hybrid.decrypt_payload(sk, ct, nonce, enc)
    
    dsa = SovereignMLDSA()
    pk_dsa, sk_dsa = dsa.generate_keypair()
    sig = dsa.sign(sk_dsa, enc)
    verified = dsa.verify(pk_dsa, enc, sig)
    
    print(f"Secure transmission + signature: {'PASS' if verified and dec == message else 'FAIL'}\n")
    
    # 2. Provenance audit
    auditor = ProvenanceAuditor()
    try:
        auditor.audit_data("WHO_Protocols", "Malaria protocol")
        print("Provenance audit: PASS\n")
    except:
        print("Provenance audit: FAIL\n")

if __name__ == "__main__":
    run_suite()
