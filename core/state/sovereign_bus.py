import json
import os

class SovereignBus:
    """
    Ensures state persistence across Ports 8501, 8502, and 8503.
    """
    def __init__(self, state_file="core/state/system_state.json"):
        self.state_file = state_file
        self.last_hash = None
        if not os.path.exists(self.state_file):
            self.save_state({"status": "ORACLE_STABLE", "security": "IRON_DOME_ACTIVE", "nodes": 50})

    def get_state(self):
        with open(self.state_file, 'r') as f:
            return json.load(f)

    def save_state(self, data):
        # Prevent React Error #185 by checking for data identity
        new_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
        if new_hash != self.last_hash:
        with open(self.state_file, 'w') as f:
                json.dump(data, f)
            self.last_hash = new_hash
            return True
        return False # No change, no write, no re-render trigger

bus = SovereignBus()
