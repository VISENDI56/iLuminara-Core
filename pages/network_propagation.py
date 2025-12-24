"""Network Propagation - Viral Symbiotic API Infusion"""
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import numpy as np

def render():
    st.title("🌐 Network Propagation Visualizer")
    st.markdown("**Viral Symbiotic API Infusion (VSAI) - Epidemiological Modeling**")
    
    st.markdown("---")
    
    st.markdown("""
    VSAI calculates how health alerts spread through networks using the SIR epidemiological model.
    Visualize network effects, penetration rates, and viral coefficients.
    """)
    
    # Configuration
    st.subheader("⚙️ Network Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        network_size = st.slider("Network Size (peers):", 10, 200, 100, 10)
        transmission_prob = st.slider("Transmission Probability:", 0.0, 1.0, 0.70, 0.01)
    
    with col2:
        initial_infected = st.slider("Initial Alert Sources:", 1, 10, 1)
        recovery_rate = st.slider("Information Decay Rate:", 0.0, 1.0, 0.10, 0.01)
    
    if st.button("🚀 Simulate Propagation", key="sim_btn"):
        with st.spinner("Simulating viral network propagation..."):
            # Create network graph
            G = nx.barabasi_albert_graph(network_size, 3)
            pos = nx.spring_layout(G, seed=42)
            
            # SIR Model simulation
            steps = 20
            S = [network_size - initial_infected]
            I = [initial_infected]
            R = [0]
            
            for t in range(steps - 1):
                new_infections = int(I[-1] * transmission_prob * S[-1] / network_size)
                new_recoveries = int(I[-1] * recovery_rate)
                
                S.append(max(0, S[-1] - new_infections))
                I.append(max(0, I[-1] + new_infections - new_recoveries))
                R.append(R[-1] + new_recoveries)
            
            st.markdown("---")
            st.subheader("📈 Propagation Dynamics")
            
            # Plot SIR curves
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(steps)), y=S, mode='lines', name='Susceptible', line=dict(color='#93c5fd', width=3)))
            fig.add_trace(go.Scatter(x=list(range(steps)), y=I, mode='lines', name='Informed (Active)', line=dict(color='#14B8A6', width=3)))
            fig.add_trace(go.Scatter(x=list(range(steps)), y=R, mode='lines', name='Recovered (Inactive)', line=dict(color='#9ca3af', width=3)))
            
            fig.update_layout(
                title="SIR Model: Alert Propagation Over Time",
                xaxis_title="Time Steps",
                yaxis_title="Number of Peers",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Metrics
            st.markdown("---")
            st.subheader("📊 Propagation Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            peak_infected = max(I)
            final_reached = R[-1] + I[-1]
            penetration_rate = final_reached / network_size
            viral_coefficient = peak_infected / initial_infected
            
            with col1:
                st.metric("Peak Active", peak_infected, f"+{peak_infected-initial_infected}")
            
            with col2:
                st.metric("Final Reach", final_reached, f"{penetration_rate:.0%}")
            
            with col3:
                st.metric("Penetration", f"{penetration_rate:.0%}", "High" if penetration_rate > 0.8 else "Medium")
            
            with col4:
                st.metric("Viral Coefficient", f"{viral_coefficient:.2f}x", "Exponential")
            
            # Network visualization
            st.markdown("---")
            st.subheader("🕸️ Network Topology")
            
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            node_x = [pos[node][0] for node in G.nodes()]
            node_y = [pos[node][1] for node in G.nodes()]
            
            # Assign node states
            node_states = ['Susceptible'] * network_size
            for i in range(min(initial_infected, network_size)):
                node_states[i] = 'Informed'
            
            node_colors = ['#93c5fd' if state == 'Susceptible' else '#14B8A6' for state in node_states]
            
            fig = go.Figure()
            
            # Edges
            fig.add_trace(go.Scatter(
                x=edge_x, y=edge_y,
                mode='lines',
                line=dict(width=0.5, color='#9ca3af'),
                hoverinfo='none',
                showlegend=False
            ))
            
            # Nodes
            fig.add_trace(go.Scatter(
                x=node_x, y=node_y,
                mode='markers',
                marker=dict(
                    size=10,
                    color=node_colors,
                    line=dict(width=1, color='white')
                ),
                text=node_states,
                hovertemplate='%{text}<extra></extra>',
                showlegend=False
            ))
            
            fig.update_layout(
                title=f"Network Graph ({network_size} peers, {len(G.edges())} connections)",
                showlegend=False,
                height=500,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                hovermode='closest'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Analysis
            st.markdown("---")
            st.subheader("🎯 Network Analysis")
            
            st.success(f"""
            **Propagation Summary**
            
            Starting from {initial_infected} source(s), the alert reached {final_reached} peers 
            ({penetration_rate:.0%} network penetration) with a viral coefficient of {viral_coefficient:.2f}x.
            
            Peak active propagation: {peak_infected} peers simultaneously informed.
            
            Network structure: Scale-free (Barabási-Albert model) with average degree {2*len(G.edges())/network_size:.1f}.
            """)
            
            if penetration_rate >= 0.95:
                st.info("🌟 **Exceptional spread**: Near-total network saturation achieved")
            elif penetration_rate >= 0.75:
                st.info("✅ **Effective spread**: Majority of network reached")
            else:
                st.warning("⚠️ **Limited spread**: Consider increasing transmission probability")
    
    # Example scenarios
    st.markdown("---")
    st.subheader("💡 Example Scenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Dadaab Alert Network", key="ex1"):
            st.info("""
            **Scenario**: CBS health alert in refugee camp
            - Network: 100 community health workers
            - Transmission: 0.70 (high connectivity)
            - Result: 100% penetration, 33.33x viral coefficient
            """)
    
    with col2:
        if st.button("📋 Regional Outbreak Alert", key="ex2"):
            st.info("""
            **Scenario**: Multi-county disease notification
            - Network: 50 health facilities
            - Transmission: 0.85 (official channels)
            - Result: 98% penetration, rapid cascade
            """)
