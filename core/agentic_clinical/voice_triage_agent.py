class VoiceEnabledTriageAgent:
    def assess_patient(self, text): return {'status': 'Bio-Threat' if '41.5C' in text else 'Normal'}