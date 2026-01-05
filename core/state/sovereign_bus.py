import json
from pathlib import Path
from datetime import datetime

STATE_FILE = Path("core/state/state.json")
DEFAULT_STATE = {
    "schema_version": "2026.01",
    "status": "BOOT",
    "mode": "INIT",
    "version": "1.0",
    "last_updated": None
}

class SovereignBus:
    def __init__(self):
        self.state_file = STATE_FILE
        self._state = DEFAULT_STATE.copy()
        self.load()

    def load(self):
        if self.state_file.exists():
            try:
                self._state.update(json.loads(self.state_file.read_text()))
            except:
                self._state = DEFAULT_STATE.copy()
        self._state["last_updated"] = datetime.utcnow().isoformat()

    def save(self):
        self.state_file.write_text(json.dumps(self._state, indent=2))

    def get(self, key):
        return self._state.get(key)

    def set(self, key, value):
        self._state[key] = value
        self._state["last_updated"] = datetime.utcnow().isoformat()
        self.save()

bus = SovereignBus()
