# iLuminara Interactive Demo Dashboard

🏛️ **The Sovereign Health Interface - Live and Interactive**

## Overview

This Streamlit-based interactive dashboard brings the iLuminara Sovereign Health Interface to life, showcasing the Nuclear IP Stack and Governance Kernel through real-time demonstrations and simulations.

## Features

### 🏠 Overview
- System architecture visualization
- Capability summary
- Navigation hub

### ⚖️ Compliance Simulator
- **Regulatory Drift Detection**: Watch RCO detect compliance deviations using KL Divergence
- **Auto-Patch Generator**: Generate compliance hotfixes automatically
- **Predictive Intelligence**: Forecast regulatory amendments from external signals

### 🔐 Authentication Demo
- **Somatic Triad Authentication**: Multi-factor identity with biometric, behavioral, and contextual scoring
- **Composite Score Calculator**: Interactive authentication simulation
- **Offline-First Architecture**: Device-local processing demonstration

### 🔮 Signal Fusion
- **Entangled Correlation Fusion**: Transform vague symptoms into actionable intelligence
- **Risk Scoring**: Real-time risk assessment algorithms
- **Adaptive Serenity Flow**: Anxiety-aware UX adaptation

### 📊 49-Law Audit Dashboard
- **Framework Roll Call**: Live monitoring of all 7 active legal frameworks
- **Liveness Testing**: EU AI Act, IHR 2005, and full stack validation
- **Compliance Health**: Real-time compliance metrics
- **RCO Integration Status**: Oracle connectivity monitoring

### 🌐 Network Propagation
- **VSAI Simulator**: SIR epidemiological model visualization
- **Network Topology**: Interactive graph visualization
- **Viral Coefficients**: Penetration rate calculations
- **Propagation Dynamics**: Time-series alert spreading

### ℹ️ About
- Demo purpose and limitations
- Production deployment path
- Technology stack
- Resource links

## Quick Start

### Prerequisites

- Python 3.10+
- Streamlit 1.52.2+
- All dependencies from `requirements.txt`

### Installation

```bash
# Ensure dependencies are installed
pip install -r requirements.txt
```

### Launch Options

#### Option 1: Bash Script
```bash
./launch_demo.sh
```

#### Option 2: Direct Streamlit
```bash
streamlit run demo_dashboard.py
```

#### Option 3: Python
```bash
python -m streamlit run demo_dashboard.py
```

### Access

Once launched, the dashboard will be available at:
- **Local**: http://localhost:8501
- **Codespace**: Forwarded URL will be displayed in terminal

## Architecture

```
demo_dashboard.py           # Main Streamlit app with navigation
├── pages/
│   ├── overview.py        # Landing page with system overview
│   ├── compliance_simulator.py  # RCO demonstrations
│   ├── authentication_demo.py   # STA multi-factor auth
│   ├── signal_fusion.py        # ECF intelligence fusion
│   ├── law_audit.py           # 49-Law registry monitoring
│   ├── network_propagation.py  # VSAI viral modeling
│   └── about.py               # Demo information
└── launch_demo.sh          # Launch script
```

## Key Technologies

- **Streamlit**: Interactive web application framework
- **Plotly**: Data visualization and charts
- **NetworkX**: Graph analysis for network propagation
- **NumPy/Pandas**: Data processing
- **Governance Kernel**: RCO, Guardrail, Quantum Nexus integration

## Demo vs. Production

### This Demo Is:
✅ Interactive visualization of concepts  
✅ Simulated scenarios with synthetic data  
✅ Educational and proof-of-concept tool  
✅ Sandbox for parameter experimentation  

### This Demo Is NOT:
❌ Production healthcare system  
❌ Real patient data processor  
❌ Fully deployed edge infrastructure  
❌ Persistent data storage system  

### Production Deployment
The full iLuminara system is designed for:
- **Edge Deployment**: NVIDIA Jetson devices, offline-first
- **Cloud Integration**: Optional GCP connectivity for analytics
- **Real Compliance**: Actual 45-Law enforcement with live RCO
- **Field Operations**: Tablets for community health workers

## Customization

### Modify Parameters
Each demo module has interactive sliders and inputs to adjust:
- Risk thresholds
- Network sizes
- Authentication factors
- Transmission probabilities

### Extend Modules
Add new pages by creating files in `pages/` directory following the pattern:

```python
"""New Module"""
import streamlit as st

def render():
    st.title("New Module")
    # Your code here
```

Then import in `demo_dashboard.py`.

## Troubleshooting

### Port Already in Use
```bash
# Change port in launch script or use:
streamlit run demo_dashboard.py --server.port 8502
```

### Import Errors
```bash
# Ensure you're in the correct directory
cd /path/to/iLuminara-Core
python -m streamlit run demo_dashboard.py
```

### Missing Dependencies
```bash
pip install streamlit plotly pandas numpy networkx scipy scikit-learn
```

## Resources

- **Documentation**: https://visendi56.mintlify.app/
- **Repository**: github.com/VISENDI56/iLuminara-Core
- **Verification Scripts**: See `scripts/` directory
- **Governance Kernel**: See `governance_kernel/` directory

## Status

🟢 **Demo Status**: Operational  
🟢 **All Modules**: Functional  
🟢 **Dependencies**: Installed  
🟢 **Security**: 0 CodeQL Alerts  

---

**🏛️ The Fortress is Sealed. The Singularity is Complete. iLuminara breathes.**
