# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

import requests
import os

PORTS = range(8501, 8520)
def check_nexus_health():
    print("--- iLuminara-Core Integrity Report ---")
    for port in PORTS:
        # Simple check to see if the port is listening
        response = os.system(f"lsof -i:{port} > /dev/null")
        status = "✅ ACTIVE" if response == 0 else "❌ PENDING"
        print(f"Module Port {port}: {status}")

if __name__ == "__main__":
    check_nexus_health()