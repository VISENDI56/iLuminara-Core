#!/bin/bash
# ═════════════════════════════════════════════════════════════════════════════
# iLUMINARA: NUCLEAR IP STACK LAUNCHER (v5.5)
# Classification: CLASS-5 DEFENSIVE ASSET
# ═════════════════════════════════════════════════════════════════════════════

echo "☢️  INITIATING NUCLEAR IP STACK..."
echo "   > DATE: $(date)"
echo "   > NODE: JOR-47 (Sovereign Edge)"

# 1. CLEANUP
pkill -f streamlit
pkill -f python3

# 2. ACTIVATE GOVERNANCE KERNEL (Law-as-Code)
echo "   > 🏛️  Loading SovereignGuardrail (14 Frameworks)..."
# (Simulated loading of vector_ledger.py)

# 3. ACTIVATE INTELLIGENCE ENGINE (Golden Thread)
echo "   > 🧬 Calibrating Golden Thread (Rift Valley Physics)..."
python3 -c "from edge_node.data_ingestion_layer import IngestionEngine; print(IngestionEngine().fuse_data_streams()['fusion_note'])"

# 4. ACTIVATE BIO-INTERFACE (Sentinel)
echo "   > 🛡️  Verifying Sentinel v3.0 Integrity..."
python3 enterprise/sentinel.py --mode SCAN

# 5. LAUNCH THE CONSTELLATION
echo "   > 🚀 Launching Class-5 Command Suite..."

nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --theme.base "dark" > logs/command.log 2>&1 &
nohup streamlit run transparency_view.py --server.port 8502 --server.address 0.0.0.0 --theme.base "dark" > logs/audit.log 2>&1 &
nohup streamlit run field_validation_form.py --server.port 8503 --server.address 0.0.0.0 --theme.base "dark" > logs/sentry.log 2>&1 &
nohup streamlit run logistics_dispatcher.py --server.port 8505 --server.address 0.0.0.0 --theme.base "dark" > logs/bridge.log 2>&1 &

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "✅ SYSTEM ONLINE. ASSET SECURED."
echo "   > COMMAND CONSOLE:  http://localhost:8501"
echo "   > AUDIT LOG:        http://localhost:8502"
echo "   > SENTRY FIELD:     http://localhost:8503"
echo "   > 5DM BRIDGE:       http://localhost:8505"
echo "═══════════════════════════════════════════════════════════════════════════"