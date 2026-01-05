import logging
import os
from datetime import datetime

os.makedirs("iluminara-nexus/logs", exist_ok=True)
log_filename = f"iluminara-nexus/logs/nexus_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(module)s | %(message)s'
)

def log_audit(event_type, message, context=None):
    payload = f"[{event_type}] {message}"
    if context:
        payload += f" | META: {str(context)}"
    logging.info(payload)
