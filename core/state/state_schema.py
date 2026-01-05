"""
Canonical Sovereign State Schema
Versioned, validated, migration-safe
"""

SCHEMA_VERSION = "2026.01"

CANONICAL_STATE = {
    "schema_version": SCHEMA_VERSION,
    "status": "INITIALIZING",
    "mode": "SAFE",
    "version": "0.1.0",
    "last_updated": None,
}

INVARIANT_KEYS = set(CANONICAL_STATE.keys())
