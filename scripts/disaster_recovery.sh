#!/bin/bash
# Automated failover DNS switch using Cloudflare API (example)
# Usage: ./scripts/disaster_recovery.sh <primary_health_url> <cloudflare_token> <zone_id> <record_id> <failover_ip>

PRIMARY_HEALTH_URL="$1"
CF_TOKEN="$2"
ZONE_ID="$3"
RECORD_ID="$4"
FAILOVER_IP="$5"

if ! curl -fs $PRIMARY_HEALTH_URL > /dev/null; then
  echo "[!] Primary region down. Initiating DNS failover..."
  curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
    -H "Authorization: Bearer $CF_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"content":"'$FAILOVER_IP'"}'
  echo "[+] DNS failover complete."
else
  echo "[+] Primary region healthy. No action taken."
fi
