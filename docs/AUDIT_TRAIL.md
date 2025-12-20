# Tamper-proof Audit Trail

## Overview

The Tamper-proof Audit Trail is a cryptographically-secured ledger system for iLuminara-Core that provides:

1. **Immutability**: Audit entries are cryptographically chained and signed using Google Cloud KMS
2. **High-throughput**: Google Cloud Bigtable for write-heavy audit logging with sub-10ms latency
3. **Cross-region synchronization**: Google Cloud Spanner for globally consistent audit metadata
4. **Sovereign key management**: Google Cloud KMS with HSM-backed keys that never leave their region

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Tamper-proof Audit Trail                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Bigtable    │  │   Spanner    │  │   Cloud KMS  │    │
│  │   Ledger     │  │ Sync Engine  │  │   Manager    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                 │                  │             │
│         │                 │                  │             │
│         v                 v                  v             │
│  ┌───────────────────────────────────────────────┐        │
│  │         AuditEntry (Cryptographic)            │        │
│  │  - timestamp, event_type, actor, resource    │        │
│  │  - previous_hash (chain linkage)             │        │
│  │  - entry_hash (SHA-256)                      │        │
│  │  - signature (KMS asymmetric key)            │        │
│  └───────────────────────────────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Features

### 1. Cryptographic Chain of Custody
Each audit entry contains:
- **SHA-256 hash** of its content
- **Previous entry hash** creating an immutable chain
- **KMS signature** for non-repudiation

Any tampering breaks the chain and can be detected cryptographically.

### 2. High-Throughput Storage (Bigtable)
- Sub-10ms write latency
- Petabyte-scale capacity
- Automatic replication and failover
- Time-ordered row keys for efficient range scans

### 3. Global Consistency (Cloud Spanner)
- External consistency with TrueTime
- Multi-region ACID transactions
- Cross-continental data replication
- Strong consistency guarantees

### 4. Sovereign Key Management (Cloud KMS)
- HSM-backed cryptographic keys
- Keys never leave sovereign region
- Automatic key rotation
- Audit logging of all key operations

## Usage

### Basic Example

```python
from governance_kernel.audit_trail import (
    TamperProofAuditTrail,
    AuditEventType
)

# Initialize audit trail (simulation mode for development)
trail = TamperProofAuditTrail(simulate=True)

# Log an event
entry = trail.log_event(
    event_type=AuditEventType.DATA_ACCESS,
    actor="user@example.com",
    resource="patient_record_12345",
    action="read_phi_data",
    jurisdiction="GDPR_EU",
    outcome="SUCCESS",
    metadata={
        "ip_address": "192.168.1.100",
        "reason": "clinical review"
    }
)

print(f"Audit entry created: {entry.entry_hash}")
print(f"Signed with KMS: {entry.signature[:20]}...")
```

### Integration with SovereignGuardrail

```python
from governance_kernel.vector_ledger import SovereignGuardrail

# Enable tamper-proof audit trail
guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)

# All validation actions are now automatically logged
result = guardrail.validate_action(
    action_type='High_Risk_Inference',
    payload={
        'actor': 'ml_system',
        'resource': 'patient_diagnosis_ai',
        'explanation': 'SHAP values: [0.8, 0.1, 0.1]',
        'confidence_score': 0.95,
        'evidence_chain': ['fever', 'cough', 'lab_positive'],
        'consent_token': 'valid_token_12345',
        'consent_scope': 'diagnosis'
    },
    jurisdiction='EU_AI_ACT'
)

# Retrieve audit history
history = guardrail.get_tamper_proof_audit_history(limit=10)
for entry in history:
    print(f"{entry['timestamp']}: {entry['event_type']} - {entry['outcome']}")

# Verify chain integrity
integrity = guardrail.verify_audit_chain_integrity()
if integrity['chain_valid']:
    print("✅ Audit chain is cryptographically valid")
else:
    print("❌ Audit chain integrity compromised!")
    print(f"Details: {integrity['details']}")
```

### Retrieving Audit History

```python
# Get recent audit entries
entries = trail.get_audit_history(limit=100)

for entry in entries:
    print(f"Time: {entry.timestamp}")
    print(f"Event: {entry.event_type}")
    print(f"Actor: {entry.actor}")
    print(f"Outcome: {entry.outcome}")
    print(f"Hash: {entry.entry_hash}")
    print(f"Signature: {entry.signature[:20]}...")
    print("---")
```

### Verifying Chain Integrity

```python
# Get audit entries
entries = trail.get_audit_history(limit=1000)

# Verify cryptographic integrity
result = trail.verify_chain_integrity(entries)

print(f"Total entries: {result['total_entries']}")
print(f"Valid entries: {result['valid_entries']}")
print(f"Chain valid: {result['chain_valid']}")

if not result['chain_valid']:
    print("❌ Tampering detected!")
    for detail in result['details']:
        print(f"  Entry {detail['index']}: {detail['error']}")
```

### Cross-Region Synchronization

```python
# Log event with specific regions
entry = trail.log_event(
    event_type=AuditEventType.BREACH_NOTIFICATION,
    actor="security_system",
    resource="breach_alert_12345",
    action="notify_authorities",
    jurisdiction="GDPR_EU",
    outcome="SUCCESS",
    sync_regions=["us-east1", "eu-west1", "asia-southeast1"]
)

# Verify cross-region consistency
sync_result = trail.verify_cross_region_sync(entry.entry_hash)

if sync_result['status'] == 'CONSISTENT':
    print(f"✅ Entry synchronized across: {sync_result['regions']}")
else:
    print(f"❌ Synchronization issue: {sync_result['status']}")
```

## Event Types

The system supports various auditable events:

- `SOVEREIGNTY_CHECK`: Sovereignty validation checks
- `DATA_ACCESS`: Data access operations
- `DATA_TRANSFER`: Data transfer/export operations
- `HIGH_RISK_INFERENCE`: AI/ML high-risk inferences
- `CONSENT_VALIDATION`: Consent verification events
- `KEY_ROTATION`: Cryptographic key rotation
- `BREACH_NOTIFICATION`: Security breach notifications
- `RETENTION_ENFORCEMENT`: Data retention policy enforcement
- `SYSTEM_CONFIGURATION`: System configuration changes

## Production Deployment

### Prerequisites

```bash
# Install Google Cloud SDK dependencies
pip install google-cloud-bigtable google-cloud-spanner google-cloud-kms
```

### Configuration

```python
from governance_kernel.audit_trail import TamperProofAuditTrail

# Production configuration
trail = TamperProofAuditTrail(
    bigtable_config={
        'project_id': 'iluminara-sovereign',
        'instance_id': 'audit-ledger-prod',
        'table_id': 'tamper_proof_trail'
    },
    spanner_config={
        'project_id': 'iluminara-sovereign',
        'instance_id': 'global-audit-sync-prod',
        'database_id': 'audit_metadata'
    },
    kms_config={
        'project_id': 'iluminara-sovereign',
        'location_id': 'us-east1',  # Sovereign region
        'key_ring_id': 'audit-signing-prod',
        'key_id': 'audit-master-key'
    },
    simulate=False  # Use real GCP services
)
```

### Infrastructure Setup

#### 1. Create Bigtable Instance

```bash
gcloud bigtable instances create audit-ledger-prod \
    --display-name="Audit Ledger Production" \
    --cluster-config=id=audit-cluster,zone=us-east1-b,nodes=3 \
    --instance-type=PRODUCTION

gcloud bigtable tables create tamper_proof_trail \
    --instance=audit-ledger-prod \
    --column-families=audit_data
```

#### 2. Create Cloud Spanner Instance

```bash
gcloud spanner instances create global-audit-sync-prod \
    --config=nam-eur-asia1 \
    --description="Global Audit Sync" \
    --nodes=3

gcloud spanner databases create audit_metadata \
    --instance=global-audit-sync-prod
```

Create the schema:

```sql
CREATE TABLE audit_metadata (
  entry_hash STRING(64) NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  event_type STRING(50) NOT NULL,
  jurisdiction STRING(50) NOT NULL,
  sync_regions ARRAY<STRING(50)>,
  verification_status STRING(20) NOT NULL,
) PRIMARY KEY (entry_hash);

CREATE INDEX idx_timestamp ON audit_metadata(timestamp DESC);
CREATE INDEX idx_jurisdiction ON audit_metadata(jurisdiction);
```

#### 3. Create Cloud KMS Keys

```bash
# Create key ring
gcloud kms keyrings create audit-signing-prod \
    --location=us-east1

# Create asymmetric signing key (HSM-backed)
gcloud kms keys create audit-master-key \
    --keyring=audit-signing-prod \
    --location=us-east1 \
    --purpose=asymmetric-signing \
    --default-algorithm=ec-sign-p256-sha256 \
    --protection-level=hsm
```

## Security Considerations

### 1. Key Sovereignty
- KMS keys are HSM-backed and never leave their configured region
- Keys cannot be exported or extracted
- All cryptographic operations are performed within the HSM

### 2. Tamper Detection
- Any modification to an audit entry invalidates its hash
- Chain breaks are immediately detectable
- Invalid signatures indicate compromised entries

### 3. Non-Repudiation
- All entries are signed with KMS asymmetric keys
- Signatures provide cryptographic proof of authenticity
- Cannot deny actions logged with valid signatures

### 4. Audit Trail Immutability
- Bigtable provides append-only semantics
- No delete operations on audit logs
- Historical entries preserved indefinitely

## Compliance Mapping

The tamper-proof audit trail supports compliance with:

| Framework | Requirement | How We Meet It |
|-----------|-------------|----------------|
| **GDPR Art. 30** | Records of Processing | Complete audit trail of all data processing |
| **HIPAA §164.312** | Audit Controls | Cryptographically-secured audit logs |
| **SOC 2** | Security Monitoring | Real-time audit logging with integrity verification |
| **ISO 27001 A.12.4** | Logging and Monitoring | Comprehensive event logging across all systems |
| **NIST CSF** | Detect Function | Continuous audit monitoring and anomaly detection |
| **EU AI Act §12** | Record Keeping | Immutable logs of all high-risk AI operations |

## Performance Characteristics

### Bigtable Performance
- Write latency: **< 10ms** (p99)
- Read latency: **< 6ms** (p99)
- Throughput: **10,000+ writes/second** per node
- Storage: **Petabyte-scale**

### Spanner Performance
- Global consistency: **TrueTime-synchronized**
- Cross-region latency: **< 100ms** (p99)
- Transaction throughput: **1,000+ TPS** per node
- Storage: **Multi-petabyte**

### KMS Performance
- Signing operations: **< 100ms** (p99)
- Key rotation: **Zero downtime**
- Geographic constraint: **Guaranteed sovereign custody**

## Monitoring and Alerts

### Key Metrics to Monitor

```python
# Example monitoring integration
from governance_kernel.audit_trail import TamperProofAuditTrail

trail = TamperProofAuditTrail(simulate=False)

# Monitor chain integrity
integrity = trail.verify_chain_integrity(trail.get_audit_history(limit=1000))
if not integrity['chain_valid']:
    # Alert: Audit chain compromised
    send_alert("CRITICAL", "Audit chain integrity violation detected")

# Monitor cross-region sync
# Check that recent entries are synchronized
recent_entries = trail.get_audit_history(limit=10)
for entry in recent_entries:
    sync_status = trail.verify_cross_region_sync(entry.entry_hash)
    if sync_status['status'] != 'CONSISTENT':
        send_alert("WARNING", f"Cross-region sync failure: {entry.entry_hash}")
```

### Recommended Alerts

1. **Chain Integrity Violation** (Critical)
   - Trigger: `verify_chain_integrity()` returns `chain_valid=False`
   - Action: Immediate investigation, potential security incident

2. **Cross-Region Sync Failure** (High)
   - Trigger: Entry not synchronized within 5 minutes
   - Action: Check Spanner replication status

3. **KMS Signing Failure** (High)
   - Trigger: `sign_entry()` returns empty signature
   - Action: Verify KMS key permissions and availability

4. **High Write Latency** (Medium)
   - Trigger: Bigtable write latency > 50ms (p99)
   - Action: Check Bigtable node capacity

## Testing

Run the comprehensive test suite:

```bash
# Run all audit trail tests
pytest tests/test_audit_trail.py -v

# Run specific test class
pytest tests/test_audit_trail.py::TestTamperProofAuditTrail -v

# Run with coverage
pytest tests/test_audit_trail.py --cov=governance_kernel.audit_trail --cov-report=html
```

## Troubleshooting

### Issue: Simulation mode not working

**Solution**: Check that imports are successful:
```python
try:
    from governance_kernel.audit_trail import TamperProofAuditTrail
    print("✅ Audit trail module loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
```

### Issue: GCP credentials not found

**Solution**: Set up application default credentials:
```bash
gcloud auth application-default login
```

Or use service account key:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Issue: Bigtable connection timeout

**Solution**: Check firewall rules and VPC configuration:
```bash
gcloud compute firewall-rules list
gcloud bigtable instances describe audit-ledger-prod
```

### Issue: KMS permission denied

**Solution**: Grant required IAM roles:
```bash
gcloud kms keys add-iam-policy-binding audit-master-key \
    --location=us-east1 \
    --keyring=audit-signing-prod \
    --member=serviceAccount:SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com \
    --role=roles/cloudkms.signerVerifier
```

## References

- [Google Cloud Bigtable Documentation](https://cloud.google.com/bigtable/docs)
- [Google Cloud Spanner Documentation](https://cloud.google.com/spanner/docs)
- [Google Cloud KMS Documentation](https://cloud.google.com/kms/docs)
- [GDPR Article 30 - Records of Processing](https://gdpr-info.eu/art-30-gdpr/)
- [HIPAA Security Rule §164.312](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)
- [SOC 2 Trust Services Criteria](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome)

---

**Last Updated**: December 19, 2025  
**Status**: Production-Ready  
**Compliance**: GDPR, HIPAA, SOC 2, ISO 27001, EU AI Act ✅
