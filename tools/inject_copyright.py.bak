import os

LICENSE_HEADER = """# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------
"""

def stamp_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Avoid double-stamping
    if "Polyform Shield License" in content:
        return
        
    with open(filepath, 'w') as f:
        f.write(LICENSE_HEADER + "\n" + content)
    print(f"   [Copyright] Stamped: {filepath}")

# Walk and Stamp
for root, dirs, files in os.walk("."):
    if "venv" in root or ".git" in root: continue
    for file in files:
        if file.endswith(".py"):
            stamp_file(os.path.join(root, file))