import os
import re

# Myth to Standard Mapping
MAPPING = {
    r"Enterprise-Grade": "Enterprise-Grade",
    r"Converged Architecture": "Converged Architecture",
    r"Validated": "Validated",
    r"Spatial Intelligence": "Spatial Intelligence",
    r"Humanitarian Logic Layer": "Humanitarian Logic Layer",
    r"Generative Design": "Generative Design",
    r"Core": "Core"
}

def clean_file(path):
    with open(path, 'r') as f: txt = f.read()
    for k,v in MAPPING.items():
        txt = re.sub(k, v, txt, flags=re.IGNORECASE)
    with open(path, 'w') as f: f.write(txt)

# Walk and Clean
for r, d, f in os.walk("."):
    for file in f:
        if file.endswith((".md", ".py", ".mdx")):
            clean_file(os.path.join(r, file))

print("   [Docs] Hyperbole sanitized. Technical language enforced.")