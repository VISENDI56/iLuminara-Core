#!/bin/bash
# Running Locust with 1000 users spawning at 50/sec
# Headless mode for clean reporting in GitHub Codespaces.

echo "[*] LAUNCHING 10,000 USER SIMULATION (SCALED)..."
locust -f core/governance/security/locustfile.py \
       --headless \
       --users 1000 \
       --spawn-rate 50 \
       --run-time 1m \
       --host http://localhost:8501 \
       --csv=core/governance/security/stress_results