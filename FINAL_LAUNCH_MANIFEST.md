# FINAL LAUNCH MANIFEST

System Status
--------------
The iLuminara-Core repository is fully instantiated, architecturally complete, and has passed the Sovereign Integrity Audit. All demo components, health checks, and governance artifacts required for the Doha presentation are present in this workspace.

Repository File Summary (Top 5)
--------------------------------
- `dashboard.py` — Command: The leadership HUD and primary demonstration interface (war room view).
- `governance_kernel/vector_ledger.py` — Law: The governance ledger implementing policy anchors and legal traceability.
- `edge_node/frenasa_engine/simulate_outbreak.py` — Crisis: The outbreak simulator used to generate reproducible precision events and ground truth.
- `golden_thread.py` — Truth: The provenance/GTD abstraction that links events → inferences → validations (golden thread provenance).
- `launch_war_room.sh` — Execution: Single orchestration script that regenerates demo data and launches all HUDs and forwarders.

The Final Launch Command
------------------------
From the repository root, execute the single command below to generate demo data and launch the full demonstration suite:

```bash
./launch_war_room.sh
```

This command will:
1. Generate fresh outbreak data (simulated_outbreak.json)
2. Start port forwarding services
3. Launch Command Console (port 8501)
4. Launch Transparency Audit (port 8502)
5. Launch Field Validation (port 8503)
6. **Automatically open all three dashboards in Chrome browser**

Presentation Exit Protocol
--------------------------
To stop all running Streamlit services after the presentation:

```bash
pkill -f streamlit || true
```

Notes
-----
- Run the final command from a shell in the repository root with executable permissions on `launch_war_room.sh`.
- If running under constrained hosts (2 CPU cores), the compose file has been adjusted for local demo compatibility.

Sign-off
--------
Prepared by: Chief Systems Auditor
Date: __________
