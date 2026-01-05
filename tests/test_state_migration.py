import pytest
import json
from core.state.migration import load_state

def test_migration_legacy(tmp_path):
    legacy = {"old_key": "value"}
    path = tmp_path / "state.json"
    path.write_text(json.dumps(legacy))
    state = load_state(str(path))
    assert state["schema_version"] == "2026.01"
    assert "old_key" in state

def test_migration_corrupt(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("invalid json")
    state = load_state(str(path))
    assert state["schema_version"] == "2026.01"  # Defaults used
