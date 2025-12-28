# Privacy Impact Assessment Template
## ISO 27701 Compliance Template

**PIA ID:** PIA-[PROJECT]-[DATE]
**Version:** 1.0
**Assessment Date:** [DATE]
**Assessor:** [NAME], Privacy Officer
**Review Date:** [DATE + 6 months]

---

## 1. Executive Summary

### 1.1 Purpose
This Privacy Impact Assessment (PIA) evaluates the privacy risks associated with [PROJECT/SYSTEM NAME] and ensures compliance with ISO 27701 Privacy Information Management standards, GDPR, and relevant African data protection regulations (KDPA, POPIA, etc.).

### 1.2 Scope
- **System/Service:** [SYSTEM NAME]
- **Data Processing Activities:** [LIST ACTIVITIES]
- **Data Subjects:** [LIST CATEGORIES: patients, healthcare workers, etc.]
- **Geographic Scope:** [COUNTRIES/REGIONS]

### 1.3 Key Findings
- **High Risk Areas:** [LIST]
- **Recommended Controls:** [LIST]
- **Residual Risk Level:** [HIGH/MEDIUM/LOW]

---

## 2. Data Processing Description

### 2.1 Processing Purpose
Describe the purpose of the data processing activity:
- Primary Purpose: [DESCRIPTION]
- Secondary Purposes: [DESCRIPTION]
- Legal Basis: [LEGAL BASIS UNDER APPLICABLE LAW]

### 2.2 Data Categories
List all categories of personal data processed:

| Data Category | Description | Source | Retention Period | Legal Basis |
|---------------|-------------|--------|------------------|-------------|
| Health Data | Medical records, diagnostic data | Healthcare providers, patients | 7 years | Consent, vital interests |
| Biometric Data | Facial recognition, voice patterns | Device sensors | 2 years | Legitimate interest |
| Location Data | GPS coordinates, facility locations | Mobile devices | 1 year | Consent |
| Contact Data | Names, emails, phone numbers | User registration | Indefinite | Contract |

### 2.3 Data Subjects
Identify categories of data subjects:

- **Patients:** Individuals receiving healthcare services
- **Healthcare Workers:** Medical professionals using the system
- **Facility Staff:** Administrative and support personnel
- **Emergency Contacts:** Designated contacts for patients
- **Legal Representatives:** Guardians, next of kin

### 2.4 Processing Activities
Detail the processing operations:

1. **Collection:** Data gathered from medical devices, user inputs, and integrations
2. **Storage:** Encrypted storage in compliant cloud infrastructure
3. **Processing:** AI analysis, risk assessment, and decision support
4. **Sharing:** Controlled sharing with authorized healthcare providers
5. **Deletion:** Secure deletion upon retention period expiry

---

## 3. Legal and Regulatory Compliance

### 3.1 Applicable Laws and Regulations
- **ISO 27701:** Privacy Information Management Systems
- **GDPR:** General Data Protection Regulation (if applicable)
- **African Regulations:**
  - Kenya Data Protection Act (KDPA)
  - Protection of Personal Information Act (POPIA) - South Africa
  - Nigeria Data Protection Regulation
  - Other relevant national laws

### 3.2 Controller/Processor Analysis
Based on privacy/controller_processor_matrix.json:

- **Controller:** [ENTITY NAME] - Determines purposes and means of processing
- **Processor:** [ENTITY NAME] - Processes data on behalf of controller
- **Joint Controllers:** [IF APPLICABLE]

### 3.3 Data Protection Officer
- **Contact:** [NAME], Data Protection Officer
- **Email:** [EMAIL]
- **Responsibilities:** Privacy compliance oversight and advice

---

## 4. Privacy Risk Assessment

### 4.1 Risk Identification
Identify potential privacy risks:

| Risk ID | Risk Description | Likelihood | Impact | Risk Level |
|---------|------------------|------------|--------|------------|
| PR-001 | Unauthorized access to health data | Medium | High | High |
| PR-002 | Data breach during transmission | Low | High | Medium |
| PR-003 | Inadequate consent mechanisms | Medium | Medium | Medium |
| PR-004 | Bias in AI processing affecting privacy | Low | High | Medium |
| PR-005 | Data subject rights not properly implemented | Medium | Medium | Medium |

### 4.2 Risk Analysis
For each high-risk item, provide detailed analysis:

#### PR-001: Unauthorized Access to Health Data
- **Description:** Potential for unauthorized personnel to access sensitive health information
- **Threat Sources:** Insider threats, external hackers, system misconfigurations
- **Vulnerabilities:** Weak access controls, inadequate authentication
- **Current Controls:** RBAC, MFA, encryption
- **Residual Risk:** Medium (after controls)

#### PR-002: Data Breach During Transmission
- **Description:** Risk of data interception during network transmission
- **Threat Sources:** Man-in-the-middle attacks, network eavesdropping
- **Vulnerabilities:** Unencrypted channels, weak TLS configurations
- **Current Controls:** TLS 1.3, certificate pinning
- **Residual Risk:** Low (after controls)

### 4.3 Risk Evaluation
- **High Risk:** Requires immediate mitigation
- **Medium Risk:** Requires monitoring and planned mitigation
- **Low Risk:** Acceptable with current controls

---

## 5. Privacy Controls and Safeguards

### 5.1 Technical Controls
- **Encryption:** AES-256 encryption at rest and in transit
- **Access Control:** Role-based access with principle of least privilege
- **Audit Logging:** Comprehensive audit trails of all data access
- **Data Minimization:** Collection limited to necessary data only
- **Pseudonymization:** Use of pseudonyms where possible

### 5.2 Organizational Controls
- **Privacy Training:** Mandatory privacy training for all personnel
- **Data Protection Impact Assessment:** Regular DPIA reviews
- **Incident Response:** Privacy incident response procedures
- **Vendor Management:** Privacy requirements in vendor contracts

### 5.3 Procedural Controls
- **Consent Management:** Clear consent mechanisms for data processing
- **Data Subject Rights:** Procedures for handling access, rectification, erasure requests
- **Data Mapping:** Regular mapping of data flows and processing activities
- **Retention Schedules:** Defined retention periods with automated deletion

---

## 6. Data Subject Rights Implementation

### 6.1 Right to Information
- **Implementation:** Privacy notices provided at data collection points
- **Evidence:** privacy/impact_assessment_template.md
- **Verification:** Annual review of privacy notices

### 6.2 Right of Access
- **Implementation:** Self-service portal for data access requests
- **Timeline:** Response within 30 days
- **Evidence:** Access request logs

### 6.3 Right to Rectification
- **Implementation:** Data correction procedures through user interface
- **Timeline:** Corrections within 30 days
- **Evidence:** Rectification request logs

### 6.4 Right to Erasure
- **Implementation:** Secure deletion procedures
- **Timeline:** Deletion within 90 days of request
- **Evidence:** Deletion logs and certificates

### 6.5 Right to Data Portability
- **Implementation:** Data export in machine-readable format
- **Timeline:** Export within 30 days
- **Evidence:** Portability request logs

### 6.6 Right to Object
- **Implementation:** Objection handling procedures
- **Timeline:** Response within 30 days
- **Evidence:** Objection logs

### 6.7 Automated Decision Making
- **Implementation:** Human oversight for high-risk AI decisions
- **Evidence:** AI decision audit trails
- **Verification:** Regular bias and fairness assessments

---

## 7. International Data Transfers

### 7.1 Transfer Analysis
- **Recipient Countries:** [LIST COUNTRIES]
- **Transfer Mechanisms:** [SCCs, BCRs, etc.]
- **Adequacy Decisions:** [COUNTRIES WITH ADEQUACY]

### 7.2 Transfer Risk Assessment
- **High Risk Transfers:** Transfers to countries without adequacy
- **Mitigation Measures:** Standard Contractual Clauses, BCRs
- **Residual Risk:** [ASSESSMENT]

### 7.3 African Data Residency
Based on governance_kernel/national_strategy_guard.py:
- **Local Storage:** Data stored in African jurisdictions
- **Processing Location:** Processing occurs within approved jurisdictions
- **Transfer Controls:** Cryptographic verification of data location

---

## 8. Monitoring and Review

### 8.1 Ongoing Monitoring
- **Privacy Metrics:** Regular monitoring of privacy KPIs
- **Incident Tracking:** Privacy incident logging and analysis
- **Audit Reviews:** Annual privacy audits

### 8.2 Review Triggers
- **Significant Changes:** Changes to processing activities
- **New Regulations:** Updates to applicable privacy laws
- **Incidents:** Privacy breaches or near-misses
- **Technological Changes:** New technologies affecting privacy

### 8.3 Review Process
- **Frequency:** Annual review, or as triggered
- **Responsible Party:** Privacy Officer
- **Documentation:** Updated PIA with change log

---

## 9. Residual Risk and Recommendations

### 9.1 Residual Risk Summary
After implementing recommended controls, the residual privacy risks are:

| Risk Category | Residual Risk Level | Mitigation Status |
|---------------|-------------------|-------------------|
| Unauthorized Access | Low | Acceptable |
| Data Breach | Low | Acceptable |
| Consent Issues | Low | Acceptable |
| AI Bias | Medium | Requires monitoring |
| Rights Implementation | Low | Acceptable |

### 9.2 Recommendations
1. **Implement Enhanced Monitoring:** Deploy advanced privacy monitoring tools
2. **Conduct Regular Audits:** Annual third-party privacy audits
3. **Staff Training:** Ongoing privacy awareness training
4. **Technology Updates:** Regular updates to privacy-enhancing technologies
5. **Incident Response Testing:** Regular testing of privacy incident response procedures

---

## 10. Approval and Sign-off

### 10.1 Privacy Officer Review
**Name:** [PRIVACY OFFICER NAME]
**Date:** [DATE]
**Recommendation:** [APPROVE/CONDITIONAL APPROVAL/REJECT]
**Comments:** [COMMENTS]

### 10.2 Data Controller Approval
**Name:** [DATA CONTROLLER NAME]
**Date:** [DATE]
**Approval:** [APPROVED]
**Conditions:** [ANY CONDITIONS]

### 10.3 Legal Review
**Name:** [LEGAL COUNSEL NAME]
**Date:** [DATE]
**Approval:** [APPROVED]
**Comments:** [LEGAL COMMENTS]

---

## 11. Appendices

### Appendix A: Data Flow Diagrams
[Insert data flow diagrams showing data processing activities]

### Appendix B: Risk Assessment Details
[Detailed risk assessment worksheets]

### Appendix C: Control Implementation Evidence
[Links to evidence of control implementation]

### Appendix D: Related Documents
- privacy/controller_processor_matrix.json
- governance/isms_handbook.md
- certification/audit_bundle_generator.py

---

*This PIA template is auto-generated and maintained by the Living Certification Oracle system.*