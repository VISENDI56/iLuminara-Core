# iLuminara-Core: Agentic Operating System for Health Security

[![License: Polyform Shield](https://img.shields.io/badge/License-Polyform_Shield-blue.svg)](LICENSE)
[![Compliance: ISO 42001 / IEC 62304](https://img.shields.io/badge/Compliance-ISO_42001%20%2F%20IEC_62304-green.svg)](compliance/SECURITY.md)
[![Logic: Z3 Verified](https://img.shields.io/badge/Logic-Z3_Verified-orange.svg)](core/governance/contracts/pcc_gate.py)
[![Substrate: NVIDIA Blackwell Optimized](https://img.shields.io/badge/Substrate-NVIDIA_Blackwell-76b900.svg)](core/research/nvidia_bionemo)
[![Docs: Mintlify](https://img.shields.io/badge/Docs-Mintlify-black.svg)](https://visendi56.mintlify.app/)

**iLuminara-Core** is a modular, agentic operating system designed for health security applications, with a focus on humanitarian contexts such as outbreak surveillance, personalized genomics, and logistics in underserved areas (e.g., refugee settlements). It integrates advanced AI reasoning, formal verification, and hardware-optimized inference to support resilient, low-latency decision-making.

## Key Features
- **Recursive Reasoning Architecture**: Energy-based models (JEPA-MPC) with System-2 style deliberation for complex clinical and governance tasks.
- **Formal Verification**: Z3 solver integration for compliance across multiple global regulatory frameworks.
- **Hardware Optimization**: Targeted for NVIDIA Blackwell-series GPUs, Holoscan for edge processing, BioNeMo for generative biology, and cuOpt for logistics.
- **Geospatial Intelligence**: ESRI Native SDK integration for offline-capable mapping and anomaly detection.
- **Security and Privacy**: Post-quantum hardening (ML-KEM), federated learning patterns, and secure aggregation.
- **Low-Latency Inference**: Optimized pipelines targeting high-throughput, real-time performance.
- **Modular Design**: Extensive directories for agents, inference, governance, genomics, surveillance, and deployment.

## Architecture Overview
The system is structured around a core governance kernel with specialized modules:
- **Cognitive Core**: Tiny Recursive Model (TRM) for efficient reasoning.
- **Input Layers**: Direct pixel/multimodal processing for robustness.
- **Explainability**: Gradient-based saliency for clinical transparency.
- **Deployment Flexibility**: Supports hybrid cloud-edge setups with burst compute options.

For detailed blueprints, see [`CORE_PATENT_BLUEPRINT.md`](CORE_PATENT_BLUEPRINT.md) and [`architecture_manifest_2026.md`](architecture_manifest_2026.md).

## Quick Start
```bash
# Clone the repository
git clone https://github.com/VISENDI56/iLuminara-Core.git
cd iLuminara-Core

# Set up environment (requires Python 3.10+ and NVIDIA tools)
make setup  # Or pip install -r requirements.txt

# Run basic tests
make test

# Launch demo dashboard
make run
```

Detailed guides:
 * COMPLETE_LAUNCH_GUIDE.md
 * QUICKSTART_DEMO.md

## Installation
 * Prerequisites: NVIDIA CUDA toolkit, Docker (optional for containerized deployment), and access to relevant cloud providers (GCP/Azure recommended).
 * Review environment templates: .env.template.
 * For edge deployment: See deployment/ and Jetson/Blackwell scripts.

## Usage
 * Local Development: Use streamlit_app.py or dashboard launchers.
 * API Access: Start services via start_all_services.py.
 * Simulations: Run outbreak/logistics scenarios in simulation_engine/.
 * Examples in examples/.

## Compliance and Security
 * Formal compliance artifacts: compliance_artifacts/
 * Security policy: SECURITY.md
 * Software Bill of Materials (SBOM): SBOM_2026_HARDENED.txt

## Contributing
Contributions are welcome via pull requests. Please review CONTRIBUTING.md and open issues for discussion. Focus areas include module enhancements, testing, and documentation.

## License
This project is licensed under the Polyform Shield License - see LICENSE for details.

Built to support resilient health infrastructure in challenging environments.
