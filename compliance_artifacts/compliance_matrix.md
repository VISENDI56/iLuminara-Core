# iLuminara Compliance Matrix (Omni-Law, 29 Frameworks)

| Framework / Law                | Code/Artifact(s)                                  | Key Controls/Features                                                                                 | Status  |
|-------------------------------|--------------------------------------------------|------------------------------------------------------------------------------------------------------|---------|
| GDPR (EU)                     | Free Access Portal, Crypto Shredder, blockchain_logger.py, compliance_compiler.py | Data subject rights, erasure, audit trail, risk management                                           | ✅      |
| HIPAA/HITECH (US)             | sovereign_guardrail.py, blockchain_logger.py      | Clinical security, breach notification, audit logging                                                | ✅      |
| KDPA (Kenya), POPIA (SA), PIPEDA (CA) | Data localization logic, sovereign_guardrail.py | Data sovereignty, minimization, adequacy enforcement                                                 | ✅      |
| CCPA/CPRA (California)        | sovereign_guardrail.py, Crypto Shredder           | Right to limit use, right to delete, Do Not Sell, Data Dividends                                     | ✅      |
| LGPD (Brazil)                 | Free Access Portal, cot_reasoning.py, Crypto Shredder | Automated decision review, health protection exception, transparency                                 | ✅      |
| EU AI Act (2024/1689)         | compliance_compiler.py, context_distillation.py, cot_reasoning.py, quantize_deploy.py, hsml_sync.py, dashboard.py | High-risk AI, risk management, data governance, human oversight, cybersecurity                       | ✅      |
| UFLPA (USA)                   | sectoral_laws.json, sovereign_guardrail.py        | Supply chain origin block, forced labor prevention                                                   | ✅      |
| Dodd-Frank 1502 (USA)         | sectoral_laws.json, sovereign_guardrail.py        | Conflict minerals, audit proof enforcement                                                          | ✅      |
| CBAM (EU)                     | sectoral_laws.json, sovereign_guardrail.py        | Carbon border adjustment, emissions calculation                                                      | ✅      |
| OFAC (USA)                    | sectoral_laws.json, sovereign_guardrail.py        | Sanctions screening, transaction freeze                                                              | ✅      |
| EU MDR (2017/745)             | sectoral_laws.json, sovereign_guardrail.py        | Post-market surveillance for clinical outputs                                                        | ✅      |
| NDPR (Nigeria)                | sectoral_laws.json, sovereign_guardrail.py        | Data transfer adequacy, privacy alerts                                                               | ✅      |
| FHIR R4 (HL7)                 | fhir_adapter.py                                  | Health data interoperability, Ministry of Health compliance                                          | ✅      |
| ... (15+ more sectoral laws)  | sectoral_laws.json, sovereign_guardrail.py        | ESG, finance, pharma, privacy, supply chain, etc.                                                    | ✅      |

**Status:** All 29 frameworks are integrated, enforced, and auditable in the codebase.

---

## Documentation
- All legal artifacts, policies, and technical controls are in `compliance_artifacts/`.
- Sectoral law triggers and actions are defined in `governance_kernel/sectoral_laws.json`.
- The universal enforcer logic is in `governance_kernel/sovereign_guardrail.py`.
- FHIR interoperability is in `infrastructure/interoperability/fhir_adapter.py`.
- Automated compliance reporting: `compliance_compiler.py`.
- All modules are tested and validated for regulatory review.
