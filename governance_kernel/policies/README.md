
# OPA Policy-as-Code

## Supported Frameworks (50)

- GDPR (EU)
- LGPD (Brazil)
- HIPAA (US)
- CCPA (California)
- POPIA (South Africa)
- NIST (US)
- ISO (Global)
- SOC (Global)
- EU AI Act (EU)
- PIPEDA (Canada)
- DPA (General)
- IHR (WHO)
- HITECH (US)
- BR Law (Brazil)
- Kenya DPA 2019 (Kenya)
- ZA PAI (South Africa)
- CA Privacy Act (Canada)
- EU Digital Services Act (EU)
- SG PDPA (Singapore)
- AU Privacy Act (Australia)
- IN DPDP (India)
- JP APPI (Japan)
- KR PIPA (South Korea)
- FR CNIL (France)
- DE BDSD (Germany)
- UK DPA 2018 (UK)
- CH FADP (Switzerland)
- RU FZ 152 (Russia)
- AE DP (UAE)
- SA PDPL (Saudi Arabia)
- NG NDPR (Nigeria)
- MX FDPL (Mexico)
- AR PDPA (Argentina)
- CL LPD (Chile)
- UA DP (Ukraine)
- PH DPA (Philippines)
- TH PDPA (Thailand)
- ID PDPA (Indonesia)
- MY PDPA (Malaysia)
- EG DP (Egypt)
- MA DP (Morocco)
- ET DP (Ethiopia)
- GH DP (Ghana)
- ZM DP (Zambia)
- TN DP (Tunisia)
- KE DP (Kenya)
- MW DP (Malawi)
- BW DP (Botswana)
- UG DP (Uganda)

## Usage

- Place Rego policies in this directory, one per framework.
- OpaGuardrail class in guardrail.py calls OPA REST API for dynamic law enforcement.
- Update policies by pushing new .rego files—no redeploy required.

## Compliance Matrix

| Framework | Region | Policy File |
|-----------|--------|-------------|
| GDPR      | EU     | gdpr.rego   |
| LGPD      | BR     | lgpd.rego   |
| HIPAA     | US     | hipaa.rego  |
| ...       | ...    | ...         |

