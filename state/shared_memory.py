import streamlit as st
from typing import Any, Dict

class SovereignSharedMemory:
    def __init__(self):
        if 'shared' not in st.session_state:
            st.session_state.shared = {
                "outbreak_context": {},
                "ethical_logs": [],
                "user_session": {"role": "guest", "authenticated": False},
                "golden_thread": [],
                "rco_proposals": []
            }

    def get(self, key: str, default: Any = None) -> Any:
        return st.session_state.shared.get(key, default)

    def set(self, key: str, value: Any):
        st.session_state.shared[key] = value

    def update(self, updates: Dict):
        st.session_state.shared.update(updates)

    def clear(self):
        st.session_state.shared = {}

    def load_state(self) -> Dict:
        return st.session_state.shared

# Singleton sovereign instance
shared_memory = SovereignSharedMemory()

def load_state():
    return shared_memory.load_state()

def get_shared(key, default=None):
    return shared_memory.get(key, default)

def set_shared(key, value):
    shared_memory.set(key, value)
