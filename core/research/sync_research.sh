#!/bin/bash
echo "[*] PULSING THE RESEARCH BRIDGE..."
git submodule update --init --recursive --remote

echo "[*] VERIFYING EXTERNAL CODE AGAINST STBK..."
# Ensure the new code doesn't introduce vulnerabilities before merging.
python3 core/governance/security/dependabot_fixer.py

echo "✅ R&D ORGANS SYNCHRONIZED."
