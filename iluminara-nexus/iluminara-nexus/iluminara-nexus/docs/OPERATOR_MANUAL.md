# iLuminara-Core: Operator Manual v1.0

## 🚦 System Lifecycle
1. **BOOT**: The system validates the `.env` security keys and hardware integrity.
2. **READY**: The Governance Kernel is loaded. Policy anchors are active.
3. **ACTIVE**: Real-time signal ingestion and predictive monitoring is enabled.

## 📥 Ingesting Data
- Ensure the **Location** matches one of the four designated camp zones: Ifo, Dagahaley, Hagadera, or Kalobeyei.
- **Severity Scores** range from 1 (Monitoring) to 5 (Immediate Intervention Required).

## 📑 Accessing the Ledger
- Navigate to the **Local Ledger** tab to view all persistent records.
- Records are stored locally in `data/sovereign_records.db` to ensure data residency.

## 🚨 Troubleshooting
- **Access Denied**: Ensure your `.env` file has `SYSTEM_ROLE=OPERATOR`.
- **Validation Error**: Check that the `Symptom Code` is between 3-10 characters.
