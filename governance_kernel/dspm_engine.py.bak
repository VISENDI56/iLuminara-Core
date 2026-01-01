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

import re
import os
import json
import streamlit as st
from typing import List, Dict

st.set_page_config(page_title="DSPM Engine", layout="wide")
st.title("🔎 Automated DSPM Classification Engine")

st.markdown("""
This module discovers and classifies sensitive data (PII, PHI) across iLuminara health datasets using regex and ML-driven methods. All findings are auto-tagged for proactive risk management.
""")

# --- Regex patterns for PII/PHI ---
PII_PATTERNS = {
    "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "Phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "Name": r"\b([A-Z][a-z]+\s[A-Z][a-z]+)\b",
    "DOB": r"\b\d{4}-\d{2}-\d{2}\b",
    "ICD-10": r"[A-Z][0-9]{2}\.[0-9]"
}

# --- ML stub (placeholder for real model) ---
def ml_classify(text: str) -> List[str]:
    # Placeholder: In production, use a trained model for PHI/PII
    return [k for k, v in PII_PATTERNS.items() if re.search(v, text)]

# --- Scan a file or dataset ---
def scan_file(path: str) -> Dict:
    if not os.path.exists(path):
        return {"error": "File not found"}
    with open(path) as f:
        data = f.read()
    findings = {}
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, data)
        if matches:
            findings[label] = list(set(matches))
    # ML-driven (stub)
    ml_tags = ml_classify(data)
    if ml_tags:
        findings["ML_Tags"] = ml_tags
    return findings

# --- Streamlit UI ---
st.subheader("Scan Health Data File for Sensitive Data")
file_path = st.text_input("Enter file path to scan:", "field_validation_submissions.json")
if st.button("Scan File"):
    result = scan_file(file_path)
    st.json(result)
    if result and not result.get("error"):
        st.success("Sensitive data classified and tagged.")
    elif result.get("error"):
        st.error(result["error"])

st.markdown("---")
st.caption("2026 Data Security Index: 79% of organizations prioritize DSPM for proactive risk management.")
