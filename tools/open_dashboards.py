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

# Dashboard URLs
DASHBOARDS = [
    ("http://0.0.0.0:8501", "Command Console"),
    ("http://0.0.0.0:8502", "Transparency Audit"),
    ("http://0.0.0.0:8503", "Field Validation"),
]

def open_dashboards_in_chrome():
    """Open all three dashboards in Chrome browser tabs"""
    print("🌐 Opening iLuminara dashboards in Chrome...")
    print("")
    
    # Try to find Chrome executable
    chrome_paths = [
        'google-chrome',
        'chrome',
        'chromium-browser',
        'chromium',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium-browser',
    ]
    
    chrome_cmd = None
    for path in chrome_paths:
        try:
            # Check if command exists
            result = subprocess.run(['which', path], capture_output=True, text=True)
            if result.returncode == 0:
                chrome_cmd = path
                break
        except Exception:
            continue
    
    if not chrome_cmd:
        print("❌ ERROR: Chrome/Chromium not found on system")
        print("   Please install Chrome or Chromium to use this feature")
        return False
    
    # Open all dashboards in Chrome
    # First dashboard opens a new window, subsequent ones open as new tabs
    for i, (url, name) in enumerate(DASHBOARDS):
        try:
            if i == 0:
                # Open first dashboard in new window
                subprocess.Popen([chrome_cmd, '--new-window', url], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                print(f"   ✅ Opened {name}: {url}")
                time.sleep(0.5)  # Small delay to ensure window opens first
            else:
                # Open subsequent dashboards as new tabs
                subprocess.Popen([chrome_cmd, '--new-tab', url], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                print(f"   ✅ Opened {name}: {url}")
                time.sleep(0.3)  # Small delay between tabs
        except Exception as e:
            print(f"   ❌ Failed to open {name}: {e}")
            return False
    
    print("")
    print("✅ All dashboards opened in Chrome!")
    return True

if __name__ == "__main__":
    success = open_dashboards_in_chrome()
    sys.exit(0 if success else 1)
