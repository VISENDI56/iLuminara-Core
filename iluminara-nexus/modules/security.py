import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class SecurityGate:
    @staticmethod
    def get_secret(key):
        val = os.getenv(key)
        if not val:
            raise EnvironmentError(f"CRITICAL: Missing Security Key [{key}]")
        return val

    @staticmethod
    def verify_role(required_role="OPERATOR"):
        current_role = os.getenv("SYSTEM_ROLE", "OBSERVER")
        if current_role != required_role:
            st.error(f"⛔ ACCESS DENIED: Role '{current_role}' insufficient.")
            st.stop()
        return True
