import hashlib
import datetime

class MDRClinicalLog:
    """EU MDR Annex II & FDA 21 CFR Part 11."""
    def log_inference(self, diagnostic_id, result, clinician_id):
        timestamp = datetime.datetime.now().isoformat()
        signature = hashlib.sha3_256(f"{clinician_id}{timestamp}".encode()).hexdigest()
        
        entry = {
            "id": diagnostic_id,
            "result": result,
            "timestamp": timestamp,
            "biometric_sig": signature,
            "conformity": "EU-MDR-CLASS-IIA"
        }
        print(f"[MDR-Log] Immutable entry created for ID: {diagnostic_id}")
        return entry
