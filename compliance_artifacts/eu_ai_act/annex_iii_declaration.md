# EU AI Act: High-Risk Classification Declaration
**Regulation (EU) 2024/1689**

## 1. System Classification
**Category:** Annex III, Paragraph 5(a) - AI systems intended to be used by emergency medical services for triage.
**Risk Level:** HIGH

## 2. Conformity Assessment Procedure
This system follows the internal control procedure set out in Annex VI.
- **Data Governance:** Enforced via `context_distillation.py`.
- **Human Oversight:** Enforced via `dashboard.py` (Override Button).
- **Cybersecurity:** Enforced via `blockchain_logger.py` and `quantize_deploy.py`.

## 3. Systemic Risk (GPAI)
**Current FLOPs:** < 10^25 (Monitored by `flop_counter.py`).
**Status:** Non-Systemic. Notification to EU Commission NOT required at this time.
