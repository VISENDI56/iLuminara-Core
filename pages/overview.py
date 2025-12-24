"""Overview page for iLuminara demo dashboard"""
import streamlit as st

def render():
    st.title("🏠 Welcome to iLuminara")
    
    st.markdown("""
    ## The Sovereign Health Intelligence Platform
    
    iLuminara is a **self-governing compliance system** that transforms health data management
    through autonomous regulatory intelligence, quantum-inspired analytics, and offline-first architecture.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>⚖️ Self-Governing Law</h3>
            <p><strong>7 Legal Frameworks</strong></p>
            <p>Autonomous compliance with EU AI Act, IHR 2005, GDPR, HIPAA, Malabo Convention, CSDDD, and IFRS S2</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🔮 Quantum Intelligence</h3>
            <p><strong>ECF Signal Fusion</strong></p>
            <p>Transforms vague symptoms into correlated health intelligence using quantum-inspired algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔐 Offline Identity</h3>
            <p><strong>Somatic Triad Auth</strong></p>
            <p>Biometric + Behavioral + Contextual authentication without cloud dependency</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎯 Explore the Demo Modules")
    
    st.markdown("""
    ### ⚖️ Compliance Simulator
    Watch the Regenerative Compliance Oracle (RCO) detect regulatory drift in real-time,
    automatically generate compliance hotfixes, and predict future regulatory amendments.
    
    ### 🔐 Authentication Demo  
    Experience the Somatic Triad Authentication system scoring biometric, behavioral,
    and contextual factors to create a composite authentication score.
    
    ### 🔮 Signal Fusion
    Input vague health symptoms and see Entangled Correlation Fusion (ECF) transform
    them into actionable intelligence with risk scoring and alert generation.
    
    ### 📊 49-Law Audit Dashboard
    Real-time monitoring of all 7 active legal frameworks with liveness testing,
    compliance health scoring, and framework roll call verification.
    
    ### 🌐 Network Propagation
    Visualize how health alerts spread through networks using the Viral Symbiotic
    API Infusion (VSAI) epidemiological SIR model.
    """)
    
    st.markdown("---")
    
    st.info("👈 **Use the sidebar to navigate between demo modules**")
    
    # System Architecture
    st.subheader("🏗️ System Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Nuclear IP Stack:**
        - 🔐 STA: Somatic Triad Authentication  
        - 🔮 ECF: Entangled Correlation Fusion
        - 🎨 ASF: Adaptive Serenity Flow
        - 🌐 VSAI: Viral Symbiotic API Infusion
        """)
    
    with col2:
        st.markdown("""
        **Governance Kernel:**
        - ⚖️ RCO: Regenerative Compliance Oracle
        - 🛡️ Sovereign Guardrail v3.0
        - 🔗 Quantum Nexus (Law Harmonization)
        - 📋 45-Law Registry (7 frameworks active)
        """)
