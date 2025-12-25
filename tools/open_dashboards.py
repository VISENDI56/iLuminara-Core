#!/usr/bin/env python3
"""
Open all iLuminara dashboards in Chrome browser
This script opens three tabs in Chrome for the complete War Room experience:
- Command Console (Leadership Dashboard)
- Transparency Audit (Clinical Staff View)
- Field Validation (CHW Mobile Interface)
"""
import subprocess
import sys
import time

# Dashboard URLs (using localhost for browser compatibility)
DASHBOARDS = [
    ("http://localhost:8501", "Command Console"),
    ("http://localhost:8502", "Transparency Audit"),
    ("http://localhost:8503", "Field Validation"),
]

def open_dashboards_in_browser():
    """Open all three dashboards in the default browser"""
    print("🌐 Opening iLuminara dashboards in default browser...")
    print("")
    
    for url, name in DASHBOARDS:
        try:
            # Use $BROWSER environment variable for dev container compatibility
            subprocess.run(['bash', '-c', f'$BROWSER "{url}"'], 
                         capture_output=True, check=True)
            print(f"   ✅ Opened {name}: {url}")
            time.sleep(0.5)  # Brief delay between opens
        except Exception as e:
            print(f"   ❌ Failed to open {name}: {e}")
    
    print("")
    print("✅ All dashboards opened in browser!")
    return True

if __name__ == "__main__":
    success = open_dashboards_in_browser()
    sys.exit(0 if success else 1)
