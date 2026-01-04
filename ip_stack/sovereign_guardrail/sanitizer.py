import re

class POPIASanitizer:
    """Section 14: Automated pseudonymization for cross-border flows."""
    def __init__(self):
        self.phi_patterns = [
            r'\b\d{13}\b', # South African ID pattern
            r'\b0\d{9}\b', # Phone numbers
        ]

    def redact_telemetry(self, data_packet, is_cross_border=True):
        if not is_cross_border:
            return data_packet
        
        redacted = data_packet
        for pattern in self.phi_patterns:
            redacted = re.sub(pattern, "[REDACTED-POPIA-S14]", redacted)
        return redacted
