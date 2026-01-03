class VoiceEnabledTriageAgent:
    """Refined in Rev 202 to fix attribute errors during Shadow Triage."""
    def __init__(self):
        self.active_status = "READY"

    def assess_patient(self, transcription_data):
        # Fix: Ensure logic handles both raw strings and dict objects
        text = transcription_data if isinstance(transcription_data, str) else transcription_data.get('data', '')
        
        if "41" in text or "fever" in text.lower():
            return {"status": "CRITICAL_TRIAGE", "action": "IMMEDIATE_ISOLATION"}
        return {"status": "STABLE", "action": "OBSERVE"}
