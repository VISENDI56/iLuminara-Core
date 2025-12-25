import re

class SovereignGuardrail:
    def __init__(self):
        self.genai_leak_patterns = [
            r"(patient|user|person|name|ssn|dob|address|phone|email|mrn|medical record|diagnosis|icd-10|phi|pii)",
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",  # Email
        ]
        self.anomalous_activity_threshold = 5  # Example: 5+ GenAI calls/min triggers alert
        self.activity_log = []

    def leak_filter(self, prompt: str) -> bool:
        """Return True if prompt is safe, False if it leaks sensitive data."""
        for pattern in self.genai_leak_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return False
        return True

    def detect_anomalous_activity(self, user_id: str) -> bool:
        """Detects if user exceeds GenAI usage threshold."""
        self.activity_log.append((user_id, 'genai_call'))
        recent = [x for x in self.activity_log[-10:] if x[0] == user_id]
        return len(recent) > self.anomalous_activity_threshold

# Example usage:
# guardrail = SovereignGuardrail()
# if not guardrail.leak_filter(prompt):
#     raise Exception("Sensitive data leak detected!")
# if guardrail.detect_anomalous_activity(user_id):
#     alert_admin(user_id)
