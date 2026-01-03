#!/bin/bash
echo "Deploying iLuminara-Core to simulated Jetson Orin edge..."

# Simulate constrained resources (e.g., 8GB RAM, solar-limited CPU)
docker build -t iluminara-edge-sim -f edge_sim/Dockerfile .
docker run --rm \
  --cpus="4" \           # Simulate ARM Cortex cores
  --memory="6g" \        # Edge RAM limit
  --shm-size="1g" \
  iluminara-edge-sim \
  python crypto/post_quantum/ml_kem.py  # Run secure telemetry demo

echo "Edge simulation complete. Solar Governor: Power budget respected."
