"""
Post-Quantum Hybrid: ML-KEM + AES-256-GCM
- ML-KEM establishes shared secret
- Derive AES-256 key via HKDF
- Encrypt/authenticate clinical payload with AES-GCM
Pure Python (cryptography lib for AES-GCM - widely trusted, minimal dep)
"""

from kyber import ML_KEM_768
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class HybridPQCrypto:
    def __init__(self):
        self.kem = ML_KEM_768()

    def encrypt_payload(self, pk, plaintext: bytes):
        ct, ss = self.kem.encaps(pk)
        # Derive AES-256 key
        hkdf = HKDF(algorithm=SHA256(), length=32, salt=None, info=b'iLuminara telemetry')
        aes_key = hkdf.derive(ss)
        
        nonce = os.urandom(12)
        aesgcm = AESGCM(aes_key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        
        print(f"Hybrid encrypted payload ({len(plaintext)} → {len(ciphertext)} bytes)")
        return ct, nonce, ciphertext

    def decrypt_payload(self, sk, ct, nonce, ciphertext):
        ss = self.kem.decaps(sk, ct)
        hkdf = HKDF(algorithm=SHA256(), length=32, salt=None, info=b'iLuminara telemetry')
        aes_key = hkdf.derive(ss)
        
        aesgcm = AESGCM(aes_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        print("Hybrid decrypted successfully")
        return plaintext

if __name__ == "__main__":
    from crypto.post_quantum.ml_kem import SovereignMLKEM
    from agents.swahili_clinical.agent import SwahiliClinicalAgent
    
    kem = SovereignMLKEM()
    pk, sk = kem.generate_keypair()
    
    agent = SwahiliClinicalAgent()
    message = agent.query("Mtoto ana homa na kutapika").encode('utf-8')
    
    hybrid = HybridPQCrypto()
    ct, nonce, enc_payload = hybrid.encrypt_payload(pk, message)
    dec_payload = hybrid.decrypt_payload(sk, ct, nonce, enc_payload)
    print(f"Round-trip match: {dec_payload.decode('utf-8')}")
