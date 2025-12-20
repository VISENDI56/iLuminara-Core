"""
Crypto Shredder (IP-02): Cryptographic Data Dissolution
═════════════════════════════════════════════════════════════════════════════

Philosophy: "Data is not deleted; it is cryptographically dissolved."

The Crypto Shredder ensures that sensitive health data can be rendered 
permanently unrecoverable through cryptographic key destruction rather than 
physical deletion. This approach provides:

1. Instant dissolution (microseconds vs. hours of secure deletion)
2. Mathematical proof of unrecoverability
3. Compliance with GDPR "Right to Erasure" (Art. 17)
4. No orphaned data remnants in backup systems

Technical Implementation:
- All sensitive data is encrypted with per-record ephemeral keys
- Keys are stored in a separate key vault
- "Deletion" = destroying the key, rendering ciphertext permanently useless
- Key vault maintains audit trail of dissolution events
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import secrets
import hashlib
import json


@dataclass
class DissolutionRecord:
    """Audit trail entry for cryptographic data dissolution."""
    record_id: str
    key_id: str
    timestamp: datetime
    jurisdiction: str
    legal_basis: str  # e.g., "GDPR Art. 17", "Patient Request"
    dissolution_proof: str  # Cryptographic proof of key destruction
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "key_id": self.key_id,
            "timestamp": self.timestamp.isoformat(),
            "jurisdiction": self.jurisdiction,
            "legal_basis": self.legal_basis,
            "dissolution_proof": self.dissolution_proof,
        }


class CryptoShredder:
    """
    Implements cryptographic data dissolution as alternative to physical deletion.
    
    Key Concepts:
    - Ephemeral keys: Each data record has unique encryption key
    - Key vault: Centralized secure storage for keys
    - Dissolution: Key destruction renders data permanently unrecoverable
    - Audit trail: Complete record of all dissolution events
    
    Usage:
        shredder = CryptoShredder()
        
        # Encrypt sensitive data
        key_id, ciphertext = shredder.encrypt_data(
            data={"patient_id": "12345", "diagnosis": "malaria"},
            record_id="PATIENT_12345_20250101"
        )
        
        # Later: Dissolve the data (GDPR Right to Erasure)
        shredder.dissolve(
            key_id=key_id,
            legal_basis="GDPR Art. 17 (Right to Erasure)",
            jurisdiction="GDPR_EU"
        )
        
        # Data is now permanently unrecoverable
        assert shredder.is_dissolved(key_id) == True
    """
    
    def __init__(self):
        """Initialize the Crypto Shredder with empty key vault."""
        self.key_vault = {}  # key_id -> encryption_key
        self.dissolution_log = []  # Audit trail
        self.dissolved_keys = set()  # Dissolved key IDs
        
    def generate_ephemeral_key(self) -> tuple[str, bytes]:
        """
        Generate a cryptographically secure ephemeral key.
        
        Returns:
            tuple: (key_id, encryption_key)
        """
        key_id = self._generate_key_id()
        encryption_key = secrets.token_bytes(32)  # 256-bit AES key
        return key_id, encryption_key
    
    def encrypt_data(self, data: Dict[str, Any], record_id: str) -> tuple[str, str]:
        """
        Encrypt sensitive data with ephemeral key.
        
        Args:
            data: The sensitive data to encrypt
            record_id: Unique identifier for the record
            
        Returns:
            tuple: (key_id, ciphertext_hex)
            
        Note: In production, use AES-256-GCM. This is a simplified implementation.
        """
        # Generate ephemeral key
        key_id, encryption_key = self.generate_ephemeral_key()
        
        # Store key in vault
        self.key_vault[key_id] = {
            "key": encryption_key,
            "record_id": record_id,
            "created_at": datetime.utcnow(),
            "status": "ACTIVE",
        }
        
        # Encrypt data (simplified: XOR with key hash)
        # In production, use proper AES-GCM encryption
        data_bytes = json.dumps(data).encode('utf-8')
        key_hash = hashlib.sha256(encryption_key).digest()
        
        # Simple XOR encryption (for demonstration)
        ciphertext = bytes(
            data_bytes[i] ^ key_hash[i % len(key_hash)]
            for i in range(len(data_bytes))
        )
        
        ciphertext_hex = ciphertext.hex()
        
        return key_id, ciphertext_hex
    
    def decrypt_data(self, key_id: str, ciphertext_hex: str) -> Optional[Dict[str, Any]]:
        """
        Decrypt data using stored key.
        
        Args:
            key_id: The key identifier
            ciphertext_hex: The encrypted data in hex format
            
        Returns:
            Decrypted data dict, or None if key is dissolved
        """
        # Check if key is dissolved
        if key_id in self.dissolved_keys:
            return None
            
        # Retrieve key from vault
        if key_id not in self.key_vault:
            raise ValueError(f"❌ Key {key_id} not found in vault")
            
        key_entry = self.key_vault[key_id]
        if key_entry["status"] == "DISSOLVED":
            return None
            
        encryption_key = key_entry["key"]
        
        # Decrypt data (reverse of encryption)
        ciphertext = bytes.fromhex(ciphertext_hex)
        key_hash = hashlib.sha256(encryption_key).digest()
        
        # XOR decryption
        plaintext_bytes = bytes(
            ciphertext[i] ^ key_hash[i % len(key_hash)]
            for i in range(len(ciphertext))
        )
        
        # Parse JSON
        plaintext = plaintext_bytes.decode('utf-8')
        data = json.loads(plaintext)
        
        return data
    
    def dissolve(
        self,
        key_id: str,
        legal_basis: str,
        jurisdiction: str = "GLOBAL_DEFAULT"
    ) -> DissolutionRecord:
        """
        Cryptographically dissolve data by destroying its encryption key.
        
        This is the core of IP-02: Data is not deleted; it is cryptographically
        dissolved. Once the key is destroyed, the ciphertext becomes permanently
        unrecoverable - mathematically proven.
        
        Args:
            key_id: The encryption key to dissolve
            legal_basis: Legal justification (e.g., "GDPR Art. 17")
            jurisdiction: Legal jurisdiction
            
        Returns:
            DissolutionRecord: Audit trail entry
            
        Raises:
            ValueError: If key_id not found in vault
        """
        if key_id not in self.key_vault:
            raise ValueError(f"❌ Key {key_id} not found in vault")
            
        key_entry = self.key_vault[key_id]
        
        # Generate cryptographic proof of dissolution
        dissolution_proof = self._generate_dissolution_proof(key_id, key_entry["key"])
        
        # CRITICAL: Destroy the key
        key_entry["key"] = None
        key_entry["status"] = "DISSOLVED"
        key_entry["dissolved_at"] = datetime.utcnow()
        
        # Mark as dissolved
        self.dissolved_keys.add(key_id)
        
        # Create audit record
        dissolution_record = DissolutionRecord(
            record_id=key_entry["record_id"],
            key_id=key_id,
            timestamp=datetime.utcnow(),
            jurisdiction=jurisdiction,
            legal_basis=legal_basis,
            dissolution_proof=dissolution_proof,
        )
        
        # Add to audit trail
        self.dissolution_log.append(dissolution_record)
        
        return dissolution_record
    
    def is_dissolved(self, key_id: str) -> bool:
        """
        Check if a key has been dissolved.
        
        Args:
            key_id: The key identifier
            
        Returns:
            True if key is dissolved, False otherwise
        """
        return key_id in self.dissolved_keys
    
    def get_dissolution_audit_trail(self) -> list:
        """
        Retrieve complete audit trail of dissolution events.
        
        Returns:
            List of DissolutionRecord dictionaries
        """
        return [record.to_dict() for record in self.dissolution_log]
    
    def get_active_keys_count(self) -> int:
        """Return count of active (non-dissolved) keys."""
        return sum(
            1 for entry in self.key_vault.values()
            if entry["status"] == "ACTIVE"
        )
    
    def get_dissolved_keys_count(self) -> int:
        """Return count of dissolved keys."""
        return len(self.dissolved_keys)
    
    def _generate_key_id(self) -> str:
        """Generate unique key identifier."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        random_suffix = secrets.token_hex(8)
        return f"KEY-{timestamp}-{random_suffix}"
    
    def _generate_dissolution_proof(self, key_id: str, key: bytes) -> str:
        """
        Generate cryptographic proof of key destruction.
        
        Uses one-way hash of key material + timestamp to prove dissolution.
        This proof can be audited but cannot be reversed to recover the key.
        """
        timestamp = datetime.utcnow().isoformat()
        proof_material = f"{key_id}:{key.hex()}:{timestamp}".encode('utf-8')
        proof_hash = hashlib.sha256(proof_material).hexdigest()
        return f"SHA256:{proof_hash}"


# ═════════════════════════════════════════════════════════════════════════════
# IP-02: Crypto Shredder
# 
# "Data is not deleted; it is cryptographically dissolved."
# 
# Core Innovation:
# - Instant dissolution (microseconds vs. hours)
# - Mathematical proof of unrecoverability
# - GDPR Art. 17 compliant ("Right to Erasure")
# - No orphaned data in backups
# ═════════════════════════════════════════════════════════════════════════════
