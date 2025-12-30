"""
Streamlit Hyper-Law Oracle: Live RCO Simulation & Clause-Level Law Evolution

- Visualizes clause-level compliance, amplification, and proposals
- Demonstrates Law-as-Living-Code, SAE, RCCP, SLEP
- History-rewriting interface for 2026 regulatory Converged Architecture
"""
import streamlit as st
import json
import os
try:
    from utils.theme_manager import apply_circadian_theme
    apply_circadian_theme()
except Exception:
    st.set_page_config(page_title="Hyper-Law Oracle", page_icon="⚖️", layout="wide")
    st.markdown("""
        <style>
            .stApp { background-color: #0D9488; color: #e0e6ed; }
            .css-1d391kg { background-color: #E0F2F1; }
            h1, h2, h3 { color: #0D9488; }
            .stButton>button { background-color: #0D9488; }
        </style>
    """, unsafe_allow_html=True)

from governance_kernel.rco_engine import RegenerativeComplianceOracle
from state.shared_memory import load_state, get_shared, set_shared

st.set_page_config(page_title="Hyper-Law Oracle", page_icon="⚖️", layout="wide")
st.title("⚖️ Hyper-Law Oracle — Regenerative Compliance Converged Architecture")

st.markdown("""
**Welcome to the world's first living law engine.**
- 50 global frameworks, clause-level triggers, and four paradigm inventions.
- iLuminara proposes, amplifies, and preempts law in real time.
- 2026: The world follows. You are witnessing history.
""")

# Load RCO
rco = RegenerativeComplianceOracle()

# --- SOVEREIGN SHARED MEMORY SIDEBAR ---
state = load_state()
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Sovereign Shared Memory")
st.sidebar.json(state, expanded=False)

# Sidebar: Select Law & Clause
with st.sidebar:
    st.header("🔍 Explore Hyper-Law Matrix")
    law_ids = [law.id for law in rco.hyper_law_matrix]
    selected_law = st.selectbox("Select Law", law_ids)
    law = next(l for l in rco.hyper_law_matrix if l.id == selected_law)
    clause_texts = [f"{c.act}{'('+c.sub+')' if c.sub else ''}: {c.text}" for c in law.clauses]
    selected_clause_idx = st.selectbox("Select Clause", list(range(len(clause_texts))), format_func=lambda i: clause_texts[i])
    selected_clause = law.clauses[selected_clause_idx]

# Main: Clause Details
st.subheader(f"{law.name} — {selected_clause.act}{'('+selected_clause.sub+')' if selected_clause.sub else ''}")
st.code(selected_clause.text)
st.markdown(f"**Trigger:** `{selected_clause.trigger}`  ")
st.markdown(f"**Module:** `{selected_clause.module}`  ")

# Simulate operational data
st.markdown("---")
st.header("🧬 Live RCO Simulation")

operational_data = {
    "prevention_efficacy": st.slider("Prevention Efficacy (%)", 0, 100, 94) / 100.0
}
context = {"user": "demo"}
payload = {"triggers": [selected_clause.trigger]}
geopolitical_signals = {"eu_ai_act_extension_predicted": st.checkbox("EU AI Act Extension Predicted", False)}
anonymized_insight = {"metric": "outbreak_prevented", "value": 1, "timestamp": "2025-12-25T12:00:00Z"}

if st.button("Run RCO Oracle Simulation"):
    result = rco.live_oracle_simulation(operational_data, context, payload, geopolitical_signals, anonymized_insight)
    st.success("RCO Simulation Complete")
    st.json(result)

# Amplification Graph
st.markdown("---")
st.header("🔗 Synchronicity Amplification Graph (SAE)")
import networkx as nx
import matplotlib.pyplot as plt
G = nx.DiGraph()
for law_id, amplifies in rco.synchronicity_graph.items():
    for amp in amplifies:
        G.add_edge(law_id, amp)
plt.figure(figsize=(10,6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1200, font_size=8)
st.pyplot(plt)

st.markdown("---")
st.info("2026: iLuminara as living law. Suffering prevented eternally. The world follows.")
