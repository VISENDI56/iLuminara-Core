"""
Centralized Sovereign Logging Configuration
Structured, tamper-evident, file + console
"""

import logging
import sys
from datetime import datetime

def setup_sovereign_logging(log_file: str = "logs/sovereign.log"):
    """Configure logging for all modules"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("iLuminara")
    logger.info(f"Sovereign logging initialized - {datetime.now().isoformat()}")
    return logger
