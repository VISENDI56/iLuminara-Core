#!/bin/bash
# iLuminara Live Ingestor - Type your SMS signal below
mkdir -p logs audit
echo "--- iLuminara Ingestor Active ---"
while true; do
    read -p "Enter SMS/EMR Signal: " signal
    echo "[$(date)] SIGNAL: $signal" >> logs/ingressor.log
    echo "✅ Signal Synced to Nexus."
done
