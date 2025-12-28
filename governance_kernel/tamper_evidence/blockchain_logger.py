import hashlib
import json
import time
import os

class SovereignChain:
    """
    Implements a localized SHA-256 Hash Chain.
    Ensures 'Tamper Evidence' for audit trails (Article 12).
    """
    def __init__(self, chain_file="sovereign_ledger.jsonl"):
        self.chain_file = chain_file
        self.last_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        self._load_last_hash()

    def _load_last_hash(self):
        if os.path.exists(self.chain_file):
            with open(self.chain_file, "r") as f:
                lines = f.readlines()
                if lines:
                    last_block = json.loads(lines[-1])
                    self.last_hash = last_block["current_hash"]

    def log_event(self, event_type, payload):
        timestamp = time.time()
        # Create the block content
        block_content = {
            "prev_hash": self.last_hash,
            "timestamp": timestamp,
            "event": event_type,
            "payload": payload
        }
        # Calculate Hash (PoW simulation not needed for private chain, just integrity)
        block_string = json.dumps(block_content, sort_keys=True)
        current_hash = hashlib.sha256(block_string.encode()).hexdigest()
        # Append Hash to Block
        block_content["current_hash"] = current_hash
        # Write to Immutable Ledger
        with open(self.chain_file, "a") as f:
            f.write(json.dumps(block_content) + "\n")
        # Update pointer
        self.last_hash = current_hash
        return current_hash

if __name__ == "__main__":
    chain = SovereignChain()
    tx_hash = chain.log_event("SYSTEM_BOOT", {"version": "Omega_1.0"})
    print(f"✅ Event Locked on Chain. Hash: {tx_hash}")
