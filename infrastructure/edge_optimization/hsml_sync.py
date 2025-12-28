import hashlib
import json

class HSMLSyncAgent:
    """
    Hierarchical State Machine Layer (HSML) Sync.
    Reconciles edge data with the Nexus using Merkle Trees.
    """
    def compute_merkle_root(self, data_list):
        """
        Computes the root hash of local data to detect differences efficiently.
        """
        hashes = [hashlib.sha256(json.dumps(d).encode()).hexdigest() for d in data_list]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1]) # Duplicate last if odd
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i+1]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            hashes = new_hashes
        return hashes[0] if hashes else None

    def reconcile(self, local_data, nexus_root_hash):
        """
        Compares local root vs nexus root. If mismatch, syncs diffs.
        """
        local_root = self.compute_merkle_root(local_data)
        if local_root == nexus_root_hash:
            return "SYNC_STATUS: ALIGNED (No Data Transfer Needed)"
        else:
            return f"SYNC_STATUS: DRIFT DETECTED. Initiating IP-09 Protocol to push {len(local_data)} records."

if __name__ == "__main__":
    agent = HSMLSyncAgent()
    mock_data = [{"patient": "A"}, {"patient": "B"}]
    print(agent.reconcile(mock_data, "wrong_hash_123"))
