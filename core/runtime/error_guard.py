import streamlit as st
import logging
import traceback
from pathlib import Path

LOG_FILE = Path("iluminara.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("iLuminara.Runtime")


def guard(fn):
    """Decorator for crash-proof Streamlit execution."""
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.exception("Unhandled application error")
            st.error("⚠️ A system error occurred. The incident has been logged.")
            st.stop()
    return wrapped
