# iLuminara Transcendence Protocol

## Overview

The Transcendence Protocol is a unified launch system for the iLuminara platform that provides a single entry point to the complete iLuminara experience.

## Components

### 1. `portal.py`
A unified Streamlit interface that combines three critical views:
- **🛡️ Command Console**: Leadership dashboard with real-time outbreak monitoring
- **📊 Transparency Audit**: Protocol validation and decision reasoning console
- **📱 Field Validation**: Mobile-optimized interface for community health workers

### 2. `transcendence_protocol.sh`
Automated launch script that:
1. Cleans up any zombie Streamlit processes
2. Regenerates simulation data using Active Inference Engine
3. Launches the unified portal interface

## Usage

### Quick Start

```bash
./transcendence_protocol.sh
```

This single command will:
1. Kill any existing Streamlit processes
2. Run the outbreak simulation (`edge_node/frenasa_engine/simulate_outbreak.py`)
3. Launch the portal on `http://0.0.0.0:8501`

### Manual Execution

If you prefer to run steps individually:

```bash
# Step 1: Clean up
pkill -f streamlit

# Step 2: Generate simulation data
python3 edge_node/frenasa_engine/simulate_outbreak.py

# Step 3: Launch portal
streamlit run portal.py --server.port 8501 --server.address 0.0.0.0
```

## Features

### Command Console
- Real-time Z-Score monitoring
- Parametric bond status tracking
- CBS (Community-Based Surveillance) and EMR (Electronic Medical Records) signal counting
- Geographic visualization with risk heat mapping
- Golden Thread timeline showing data fusion

### Transparency Audit
- SHAP-based decision reasoning
- 4.2-second alert transmission speed metrics
- Precision alert timeline
- Governance Kernel compliance status (14 active protocols)
- Legal vector check (GDPR, KDPA, HIPAA, etc.)

### Field Validation
- Mobile-optimized data entry for community health workers
- Real-time alert verification
- Water source status reporting
- Priority scoring system
- LoRaWAN mesh security confirmation

## Data Flow

```
simulate_outbreak.py
    ↓
simulated_outbreak.json
precision_alert_sequence.json
    ↓
portal.py (Streamlit Interface)
    ↓
User Interface (Browser)
```

## System Requirements

- Python 3.8+
- Streamlit
- Pandas
- PyDeck
- Plotly Express
- JSON support

## Data Format

The portal supports the comprehensive outbreak simulation format:

```json
{
  "simulation_metadata": {...},
  "events": [...],
  "z_score_timeline": [...],
  "parametric_bond_trigger": {...},
  "golden_thread_examples": [...],
  "geographic_data": [...]
}
```

## Navigation

Use the sidebar to switch between views:
- Command Console: Overview and metrics
- Transparency Audit: Decision explanations
- Field Validation: Data entry and verification

The time slider allows you to explore the outbreak progression across all 72 hours of the simulation.

## Architecture

The portal implements the iLuminara philosophy:
> "Transform preventable suffering from statistical inevitability to historical anomaly."

It demonstrates:
- **Data Sovereignty**: All processing happens locally
- **Governance Compliance**: 14 legal frameworks enforced
- **Golden Thread**: CBS + EMR data fusion
- **Transparency**: Explainable AI decisions
- **Field-First Design**: CHW-optimized interfaces

## Notes

- Portal runs on port 8501 by default
- Accessible at `http://0.0.0.0:8501` or your machine's IP
- Data is regenerated on each protocol execution
- All interfaces use the same underlying simulation data
