# Disaster Recovery Procedures

## 1. Database Point-in-Time Recovery (PITR)
- **Protocol:** WAL archiving to S3 enabled.
- **RPO:** 5 minutes.
- **RTO:** 15 minutes.

## 2. Biological Containment Failure
- **Protocol:** "Code Red" Isolation.
- **Action:** IGX Safety Island triggers physical lock on bio-synthesis module.
- **Data:** BioNeMo weights purged from edge cache immediately.