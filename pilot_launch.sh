#!/bin/bash
set -e
echo "Launching Sovereign Pilot - Dadaab Node"
docker-compose -f docker-compose.ims.yml up -d
echo "Pilot active. Monitoring ethical drift and compliance..."
echo "Feedback loop open - awaiting real operator input"
