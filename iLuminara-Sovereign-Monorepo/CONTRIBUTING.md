# Contributing to iLuminara Sovereign Systems

Welcome to the Nairobi-Nexus development team. This is a **polyglot monorepo** designed for maximum transparency and compliance.

## 🛠 Technology Matrix
| Component | Language | Primary Responsibility |
| :--- | :--- | :--- |
| **IMS Kernel** | Python 3.12+ | Ethical AI, Evidence Locking, Audit Oracles |
| **Mobile Agents** | Dart (Flutter) | Edge-side PII encryption, Human-Oversight UI |
| **Orchestration** | Bash / Shell | Sovereign Guardrail deployment, Hardware Hardening |

## 🏗 Directory Rules
- **Logic Isolation:** Do not implement business rules in `mobile/`. All core governance must live in `core/`.
- **Atomic Commits:** Changes affecting multiple layers MUST be submitted in a single atomic Pull Request.
- **Evidence Requirement:** Every PR must trigger a `compliance_oracle` scan before merging.
