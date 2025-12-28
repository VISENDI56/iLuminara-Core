# Privacy Impact Assessment Template

**Document ID:** PIA-TEMPLATE-001
**Version:** 2.1
**Effective Date:** December 27, 2025
**Governing Standard:** ISO 27701:2019, Article 35 GDPR, KDPA Section 31

## 1. Executive Summary

### 1.1 Assessment Overview
This Privacy Impact Assessment (PIA) template provides a structured framework for evaluating the privacy risks associated with new processing activities, systems, or features within the iLuminara FRENASA platform.

### 1.2 Purpose
- Identify and minimize privacy risks before implementation
- Ensure compliance with privacy regulations
- Document privacy considerations for audit purposes
- Guide privacy-by-design implementation

### 1.3 Scope
This template applies to:
- New processing activities involving personal information
- Significant changes to existing processing activities
- High-risk processing activities as defined by applicable regulations
- New technologies or systems that process personal data

## 2. Project Information

### 2.1 Project Details
- **Project Name:** [Enter project name]
- **Project Owner:** [Enter name and contact]
- **Privacy Officer:** [Enter name and contact]
- **Assessment Date:** [Enter date]
- **Review Date:** [Enter date - typically 1 year or when significant changes occur]

### 2.2 Processing Description
- **Processing Purpose:** [Describe the specific purpose of processing]
- **Legal Basis:** [Specify legal basis under applicable regulations]
- **Data Categories:** [List categories of personal data to be processed]
- **Data Subjects:** [Describe categories of data subjects]
- **Processing Activities:** [List specific processing activities: collect, store, analyze, etc.]
- **Retention Period:** [Specify how long data will be retained]

### 2.3 System/Technology Details
- **System Name:** [Name of system or application]
- **Technology Type:** [AI/ML, Database, API, Mobile App, etc.]
- **Data Architecture:** [Describe data flow and storage architecture]
- **Third Parties Involved:** [List processors, sub-processors, and their roles]

## 3. Data Mapping and Flow Analysis

### 3.1 Data Collection
- **Collection Methods:** [How is data collected?]
- **Collection Points:** [Where does collection occur?]
- **Consent Mechanisms:** [How is consent obtained and managed?]
- **Data Sources:** [Internal systems, third parties, public sources, etc.]

### 3.2 Data Processing
- **Processing Locations:** [Where does processing occur? Specify countries/jurisdictions]
- **Processing Frequency:** [Real-time, batch, on-demand, etc.]
- **Automated Processing:** [Does processing involve automated decision-making?]
- **Profiling Activities:** [Does processing involve profiling?]

### 3.3 Data Storage
- **Storage Locations:** [Primary and backup locations]
- **Storage Duration:** [How long is data stored?]
- **Encryption:** [At rest and in transit encryption details]
- **Access Controls:** [Who can access data and under what conditions?]

### 3.4 Data Sharing and Transfer
- **Recipients:** [Who receives the data?]
- **Transfer Mechanisms:** [APIs, file transfers, direct access, etc.]
- **International Transfers:** [Are transfers to other countries involved?]
- **Transfer Safeguards:** [SCCs, BCRs, adequacy decisions, etc.]

### 3.5 Data Deletion
- **Deletion Triggers:** [When is data deleted?]
- **Deletion Methods:** [Secure deletion procedures]
- **Verification:** [How is deletion verified?]

## 4. Privacy Risk Assessment

### 4.1 Risk Identification
Identify potential privacy risks using the following framework:

#### 4.1.1 Data Subject Rights Risks
- **Right to Information:** Risk that data subjects are not adequately informed
- **Right to Access:** Risk of inability to provide data copies
- **Right to Rectification:** Risk of inaccurate data not being corrected
- **Right to Erasure:** Risk of data not being deleted when requested
- **Right to Restriction:** Risk of processing not being restricted when requested
- **Right to Portability:** Risk of data not being provided in portable format
- **Right to Object:** Risk of processing continuing despite objections

#### 4.1.2 Data Protection Risks
- **Confidentiality Breach:** Unauthorized access to personal data
- **Integrity Breach:** Unauthorized modification of personal data
- **Availability Breach:** Inability to access personal data when needed
- **Accountability Breach:** Lack of audit trails and accountability

#### 4.1.3 Compliance Risks
- **Regulatory Non-Compliance:** Violation of privacy laws and regulations
- **Contractual Breach:** Failure to meet processor obligations
- **Reputational Damage:** Loss of trust due to privacy incidents

#### 4.1.4 Ethical Risks
- **Discrimination:** Processing that leads to unfair treatment
- **Profiling:** Unlawful or unethical profiling activities
- **Surveillance:** Excessive monitoring or tracking
- **Transparency:** Lack of transparency in processing activities

### 4.2 Risk Analysis
For each identified risk, complete the following:

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Existing Controls |
|---------|------------------|------------|--------|------------|-------------------|
| RISK-001 | [Description] | [1-5] | [1-5] | [Low/Medium/High] | [List controls] |

**Likelihood Scale:**
- 1: Very Unlikely (<1% chance)
- 2: Unlikely (1-10% chance)
- 3: Possible (10-50% chance)
- 4: Likely (50-90% chance)
- 5: Very Likely (>90% chance)

**Impact Scale:**
- 1: Negligible (Minimal privacy impact)
- 2: Minor (Limited privacy impact)
- 3: Moderate (Noticeable privacy impact)
- 4: Major (Significant privacy impact)
- 5: Severe (Critical privacy breach)

### 4.3 Risk Evaluation
- **High Risk Activities:** [List activities requiring DPIA]
- **Residual Risks:** [Risks remaining after controls]
- **Risk Acceptance:** [Risks accepted by management]

## 5. Privacy Controls and Safeguards

### 5.1 Technical Controls
- **Data Minimization:** [How is data minimized?]
- **Purpose Limitation:** [How is purpose limitation enforced?]
- **Storage Limitation:** [How is retention enforced?]
- **Accuracy:** [How is data accuracy ensured?]
- **Security:** [Technical security measures]
- **Encryption:** [Encryption implementation]
- **Anonymization:** [Anonymization/pseudonymization techniques]

### 5.2 Organizational Controls
- **Roles and Responsibilities:** [Privacy roles defined]
- **Training and Awareness:** [Privacy training programs]
- **Policies and Procedures:** [Privacy policies implemented]
- **Incident Response:** [Privacy incident procedures]
- **Auditing and Monitoring:** [Privacy monitoring mechanisms]

### 5.3 Legal and Contractual Controls
- **Legal Basis:** [Legal basis for processing]
- **Consent Management:** [Consent collection and management]
- **Data Processing Agreements:** [DPAs with processors]
- **International Transfer Mechanisms:** [Transfer safeguards]
- **Subject Rights Procedures:** [Rights fulfillment processes]

## 6. Data Subject Impact Assessment

### 6.1 Impact Analysis
- **Affected Data Subjects:** [Who is affected?]
- **Impact Duration:** [How long does impact last?]
- **Impact Severity:** [How severe is the impact?]
- **Vulnerable Groups:** [Are vulnerable groups affected?]

### 6.2 Mitigation Measures
- **Consent and Choice:** [How do subjects provide consent?]
- **Transparency:** [How are subjects informed?]
- **Rights Exercise:** [How can subjects exercise rights?]
- **Complaints Process:** [How can subjects complain?]

## 7. Compliance Assessment

### 7.1 Regulatory Compliance
- **GDPR Compliance:** [GDPR requirements assessment]
- **KDPA Compliance:** [Kenya Data Protection Act assessment]
- **POPIA Compliance:** [South Africa POPIA assessment]
- **Other Regulations:** [Other applicable regulations]

### 7.2 ISO 27701 Compliance
- **Privacy Information Management:** [PIMS implementation]
- **Controller Obligations:** [Controller requirements]
- **Processor Obligations:** [Processor requirements]
- **Privacy Controls:** [Privacy control implementation]

## 8. Recommendations and Action Plan

### 8.1 Recommended Controls
[List additional controls needed to mitigate identified risks]

### 8.2 Implementation Timeline
[Timeline for implementing recommended controls]

### 8.3 Responsible Parties
[Who is responsible for implementing each recommendation]

### 8.4 Success Metrics
[How will success be measured?]

## 9. Approval and Sign-off

### 9.1 Assessment Team
- **Privacy Officer:** [Name and signature]
- **Project Owner:** [Name and signature]
- **Legal Counsel:** [Name and signature]
- **Data Protection Officer:** [Name and signature]

### 9.2 Management Approval
- **Approval Authority:** [Name and position]
- **Approval Date:** [Date]
- **Approval Conditions:** [Any conditions for approval]

## 10. Review and Monitoring

### 10.1 Review Schedule
- **Initial Review:** [Date]
- **Annual Review:** [Date each year]
- **Change Review:** [When significant changes occur]

### 10.2 Monitoring Requirements
- **Key Metrics:** [What will be monitored?]
- **Reporting Frequency:** [How often will reports be generated?]
- **Escalation Procedures:** [When to escalate issues?]

### 10.3 Audit Trail
- **Version Control:** [Document version history]
- **Change Log:** [Record of changes made]
- **Review History:** [Record of reviews conducted]

## Appendices

### Appendix A: Data Flow Diagrams
[Include detailed data flow diagrams]

### Appendix B: Risk Assessment Details
[Detailed risk analysis worksheets]

### Appendix C: Legal Analysis
[Legal basis analysis and compliance assessment]

### Appendix D: Technical Specifications
[Technical implementation details]

### Appendix E: Supporting Documentation
[Links to related policies, procedures, and evidence]