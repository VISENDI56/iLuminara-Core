# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

# IP-02: Crypto Shredder — Post-Quantum Edition

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
try:
    from oqs import KeyEncapsulation
    POST_QUANTUM = True
except ImportError:
    POST_QUANTUM = False
import os

class CryptoShredder:
    def __init__(self):
        self.key = os.urandom(32)
        if POST_QUANTUM:
            self.kem = KeyEncapsulation('Kyber1024')

    def encrypt(self, data: bytes) -> bytes:
        if POST_QUANTUM:
            pk, sk = self.kem.generate_keypair()
            ciphertext, shared_secret = self.kem.encapsulate(pk)
            aesgcm = AESGCM(shared_secret[:32])
            nonce = os.urandom(12)
            return nonce + aesgcm.encrypt(nonce, data, None)
        else:
            aesgcm = AESGCM(self.key)
            nonce = os.urandom(12)
            return nonce + aesgcm.encrypt(nonce, data, None)

    def shred(self):
        self.key = None
        if POST_QUANTUM:
            self.kem = None
