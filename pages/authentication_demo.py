"""Authentication Demo - Somatic Triad Authentication"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render():
    st.title("🔐 Authentication Demo")
    st.markdown("**Somatic Triad Authentication (STA) - Offline-First Multi-Factor Identity**")
    
    st.markdown("---")
    
    st.markdown("""
    STA combines three independent authentication factors to create a composite security score:
    - **Biometric**: Fingerprint/Face recognition  
    - **Behavioral**: Typing patterns, device interaction  
    - **Contextual**: Location, time, device trust
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Authentication Factors")
        
        # Biometric score
        biometric_score = st.slider("Biometric Confidence:", 0.0, 1.0, 0.94, 0.01, key="bio")
        st.caption("Fingerprint match quality")
        
        # Behavioral score
        behavioral_score = st.slider("Behavioral Confidence:", 0.0, 1.0, 0.87, 0.01, key="behav")
        st.caption("Typing pattern analysis")
        
        # Contextual score
        contextual_score = st.slider("Contextual Confidence:", 0.0, 1.0, 0.91, 0.01, key="context")
        st.caption("Location + device trust")
        
        # Calculate composite score
        composite_score = (biometric_score + behavioral_score + contextual_score) / 3
        
    with col2:
        st.subheader("Composite Score")
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=composite_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Authentication"},
            gauge={
                'axis': {'range': [None, 1]},
                'bar': {'color': "#14B8A6"},
                'steps': [
                    {'range': [0, 0.5], 'color': "#fee2e2"},
                    {'range': [0.5, 0.75], 'color': "#fef3c7"},
                    {'range': [0.75, 1], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0.75
                }
            }
        ))
        fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
        if composite_score >= 0.75:
            st.success(f"✅ **AUTHENTICATED** ({composite_score:.3f})")
        else:
            st.error(f"❌ **DENIED** ({composite_score:.3f})")
    
    st.markdown("---")
    
    # Detailed breakdown
    st.subheader("Factor Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🧬 Biometric", f"{biometric_score:.2f}", f"{(biometric_score-0.75)*100:.0f}%")
        st.caption("Fingerprint sensor + liveness detection")
    
    with col2:
        st.metric("⚡ Behavioral", f"{behavioral_score:.2f}", f"{(behavioral_score-0.75)*100:.0f}%")
        st.caption("Keystroke dynamics + mouse patterns")
    
    with col3:
        st.metric("🌍 Contextual", f"{contextual_score:.2f}", f"{(contextual_score-0.75)*100:.0f}%")
        st.caption("Geolocation + device fingerprint")
    
    # Simulate authentication attempt
    st.markdown("---")
    st.subheader("🧪 Simulate Authentication")
    
    user_profile = st.selectbox(
        "Select User Profile:",
        ["Dr. Sarah Kimani (Field Worker)", "Admin User (Office)", "Guest (Untrusted Device)"]
    )
    
    if st.button("🚀 Authenticate User", key="auth_btn"):
        profiles = {
            "Dr. Sarah Kimani (Field Worker)": (0.94, 0.87, 0.91),
            "Admin User (Office)": (0.98, 0.95, 0.88),
            "Guest (Untrusted Device)": (0.72, 0.65, 0.45)
        }
        
        bio, behav, ctx = profiles[user_profile]
        comp = (bio + behav + ctx) / 3
        
        with st.spinner("Authenticating..."):
            st.markdown("---")
            st.code(f"""
Authentication Flow:
==================
User: {user_profile}
Timestamp: 2025-12-24T10:26:15Z
Device: Edge Node (Offline Mode)

Factor Analysis:
- Biometric:   {bio:.3f} ({'✓' if bio >= 0.75 else '✗'})
- Behavioral:  {behav:.3f} ({'✓' if behav >= 0.75 else '✗'})
- Contextual:  {ctx:.3f} ({'✓' if ctx >= 0.75 else '✗'})

Composite Score: {comp:.3f}
Decision: {'GRANT ACCESS' if comp >= 0.75 else 'DENY ACCESS'}
            """)
            
            if comp >= 0.75:
                st.success(f"✅ **ACCESS GRANTED** - Composite Score: {comp:.3f}")
                st.info("🔒 Session encrypted | Offline mode active | Biometric data never leaves device")
            else:
                st.error(f"❌ **ACCESS DENIED** - Composite Score: {comp:.3f} (Threshold: 0.750)")
                st.warning("⚠️ Recommend: Re-attempt with biometric recalibration")
    
    st.markdown("---")
    st.info("""
    **🔐 Offline-First Security**: All authentication happens on-device. Biometric data never 
    transmitted to cloud. Perfect for field workers in remote areas with no connectivity.
    """)
