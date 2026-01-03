# iLuminara Sovereign Health Platform

## Overview
iLuminara is a comprehensive Sovereign Health Intelligence Platform built with Python and Streamlit. It provides sovereign health intelligence through command orchestration, decision support, regulatory compliance, and AI-driven field validation.

## Project Structure
- `streamlit_app.py` - Main entry point for the unified Streamlit application
- `Home.py` - Alternative home page with sovereign OS features
- `core/` - Core platform modules including UI, governance, and services
- `governance/` - Governance kernel and compliance modules
- `certification/` - Living certification and compliance engine
- `edge_node/` - Edge node AI agents and processing
- `docs/` - Documentation and API references

## Technology Stack
- **Frontend**: Streamlit (Python)
- **Data**: Pandas, NumPy
- **Visualization**: Plotly
- **Security**: Cryptography, PyOpenSSL, Python-JOSE
- **Validation**: Z3-Solver, Pydantic

## Running the Application
The application runs on port 5000 using Streamlit:
```bash
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=5000 --server.headless=true
```

## Configuration
- `.streamlit/config.toml` - Streamlit theme and server configuration

## Recent Changes
- 2026-01-03: Initial import and setup in Replit environment
- Fixed config.toml boolean case issue (False -> false)
- Added missing os import to Home.py
