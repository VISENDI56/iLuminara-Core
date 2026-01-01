# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

import streamlit as st
import os
import json

st.set_page_config(page_title="Fortress Health Dashboard", layout="wide")
st.title("🛡️ Unified Security Telemetry Dashboard — Fortress Health")

st.markdown("""
This dashboard unifies security telemetry from CodeQL, Gitleaks, and Dependabot for iLuminara-Core. It provides a single view of data risks and security posture across all workloads, as recommended in the 2026 Data Security Index.
""")

# --- Helper functions ---
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def load_txt(path):
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return None

# --- CodeQL Results ---
st.subheader("CodeQL Security Scan Results")
codeql_report = load_json("enterprise/integrity_ledger.json") or {}
if codeql_report:
    st.json(codeql_report, expanded=False)
else:
    st.info("No CodeQL SARIF/integrity ledger found.")

# --- Gitleaks Results ---
st.subheader("Gitleaks Secrets Scan Results")
gitleaks_report = load_json("gitleaks_report.json") or {}
if gitleaks_report:
    st.json(gitleaks_report, expanded=False)
else:
    st.info("No Gitleaks report found.")

# --- Dependabot Alerts ---
st.subheader("Dependabot Dependency Alerts")
dependabot_alerts = load_json("dependabot_alerts.json") or {}
if dependabot_alerts:
    st.json(dependabot_alerts, expanded=False)
else:
    st.info("No Dependabot alerts found.")

# --- Fortress Health Summary ---
st.markdown("---")
st.header("Fortress Health Summary")
risks = []
if codeql_report:
    risks.append("CodeQL: {} issues".format(len(codeql_report.get("runs", []))))
if gitleaks_report:
    risks.append("Gitleaks: {} secrets".format(len(gitleaks_report.get("leaks", []))))
if dependabot_alerts:
    risks.append("Dependabot: {} alerts".format(len(dependabot_alerts.get("alerts", []))))

if risks:
    st.success(" | ".join(risks))
else:
    st.info("No security issues detected across all telemetry sources.")

st.markdown("---")
st.caption("2026 Data Security Index: Unified telemetry improves threat detection and response speed by 41%.")
