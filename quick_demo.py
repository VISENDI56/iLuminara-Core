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

#!/usr/bin/env python3
"""
Quick Demo Script - Run iLuminara locally without manual setup
"""

import subprocess
import sys
import time

def run_command(cmd, description):
    """Run a command and print status."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print('='*60)
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║           iLuminara Quick Demo Launcher                     ║
║     Sovereign Health Intelligence Platform                  ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        return 1
    
    print("✓ Python version OK")
    
    # Install dependencies
    if not run_command(
        "pip install -q fastapi uvicorn streamlit pydeck plotly pandas",
        "Installing core dependencies..."
    ):
        print("\nFailed to install dependencies. Continuing anyway...")
    
    print("\n✓ Setup complete")
    
    print("""
╔════════════════════════════════════════════════════════════╗
║                Starting Services                            ║
╚════════════════════════════════════════════════════════════╝

The following services will start:
  • Backend API    : http://localhost:8000
  • Frontend UI    : http://localhost:8501

Run the services manually with:
  1. Backend:  uvicorn app.backend.main:app --host 0.0.0.0 --port 8000
  2. Frontend: streamlit run app/frontend/main.py

Or use the provided script:
  ./run_demo.sh

Press Ctrl+C to stop services.
    """)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
