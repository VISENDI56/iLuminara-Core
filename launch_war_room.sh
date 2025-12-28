#!/bin/bash
# iLuminara Doha Investor Demo Launch Script
# ═════════════════════════════════════════════════════════════════════════════
# Complete automated launch of the War Room experience:
# - Field Validation Form (CHW Mobile Interface)
# - Transparency Audit View (Clinical Staff)
# - Command Console (Leadership Dashboard)
# ═════════════════════════════════════════════════════════════════════════════

# Help flag
if [ "$1" == "--help" ]; then
    echo "================================================"
    echo "🛡️  iLUMINARA SOVEREIGN COMMAND SUITE LAUNCHER"
    echo "================================================"
    echo ""
    echo "OVERVIEW (Mintlify-Aligned):"
    echo "  Quickstart: Launch War Room for immediate sovereignty demonstration"
    echo "  Architecture: Command Console - Real-time decision orchestration"
    echo "  Governance Kernel: Transparency Audit - Regulatory compliance monitoring"
    echo "  AI Agents: Field Validation - Human-in-the-loop clinical verification"
    echo "  Security: All apps enforce Class-5 defensive protocols"
    echo "  Deployment: Streamlit Cloud hosted for global access"
    echo "  API: RESTful endpoints for external integrations"
    echo ""
    echo "USAGE:"
    echo "  ./launch_war_room.sh          # Launch all apps"
    echo "  ./launch_war_room.sh --help   # Show this help"
    echo ""
    echo "APPS LAUNCHED:"
    echo "  - Command Console:    http://localhost:8501"
    echo "  - Transparency Audit: http://localhost:8502"
    echo "  - Field Validation:   http://localhost:8503"
    echo ""
    echo "For full documentation: https://visendi56.mintlify.app/"
    exit 0
fi

echo "================================================"
echo "🛡️  LAUNCHING iLUMINARA SOVEREIGN COMMAND SUITE"
echo "================================================"
echo ""

# 1. Generate fresh outbreak data
echo "1. Generating Fresh Outbreak Data..."
python3 edge_node/frenasa_engine/simulate_outbreak.py
echo ""

# 2. Start port forwarder (maps external ports to Streamlit apps)
echo "2. Starting Port Forwarder..."
nohup python3 tools/port_forwarder.py > /dev/null 2>&1 &
sleep 1

# 3. Launch the three core apps in the background

# Command Console (The Main View for Leadership) - Port 8501
echo "3. Launching COMMAND CONSOLE (http://0.0.0.0:8501)..."
nohup streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 > logs/dashboard.log 2>&1 &
sleep 2

# Transparency View (The Audit View for Clinical Staff) - Port 8502
echo "4. Launching TRANSPARENCY AUDIT (http://0.0.0.0:8502)..."
nohup streamlit run transparency_view.py --server.port 8502 --server.address 0.0.0.0 > logs/transparency.log 2>&1 &
sleep 2

# Field Validation Form (The Mobile Input for CHWs) - Port 8503
echo "5. Launching FIELD VALIDATION (http://0.0.0.0:8503)..."
nohup streamlit run field_validation_form.py --server.port 8503 --server.address 0.0.0.0 > logs/field_validation.log 2>&1 &
sleep 2

echo ""
echo "================================================"
echo "✅ LAUNCH SUCCESSFUL"
echo "================================================"
echo ""

# 6. Auto-open all dashboards in Chrome
echo "6. Opening dashboards in Chrome..."
python3 tools/open_dashboards.py
sleep 1

echo ""
echo "🌐 Dashboards are now open in Chrome:"
echo ""
echo "   Tab 1 (COMMAND CONSOLE):"
echo "   http://0.0.0.0:8501"
echo ""
echo "   Tab 2 (TRANSPARENCY AUDIT):"
echo "   http://0.0.0.0:8502"
echo ""
echo "   Tab 3 (FIELD VALIDATION):"
echo "   http://0.0.0.0:8503"
echo ""
echo "💡 Demo Flow:"
echo "   1. Use the Hour Slider in the Command Console (Tab 1)"
echo "   2. Watch the Field Validation KPI change from PENDING→COMPLETED at Hour 40"
echo "   3. View the Transparency Audit in Tab 2 for clinical staff view"
echo "   4. Submit field validation in Tab 3 to close the Human-in-the-Loop"
echo ""
echo "================================================"
echo "Quote: 'Transform preventable suffering from statistical inevitability to historical anomaly.'"
echo "================================================"
