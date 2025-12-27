class CommunityOracle:
    """
    The Ground Truth Channel.
    Allows Community Health Workers (CHWs) to override AI Risk Scores.
    """
    def __init__(self):
        self.disputes = []

    def receive_sms_report(self, sender_role, location, message):
        """
        Parses incoming SMS feedback.
        """
        print(f"   📱 [Oracle] SMS from {sender_role} @ {location}: '{message}'")
        if "WATER BAD" in message.upper() or "PEOPLE SICK" in message.upper():
            return self._trigger_override(location, message)
        return "LOGGED"

    def _trigger_override(self, location, evidence):
        """
        Injects a High-Priority Interrupt to the C2 Nexus.
        """
        override_event = {
            "type": "HUMAN_OVERRIDE",
            "location": location,
            "evidence": evidence,
            "action": "FORCE_RISK_LEVEL_CRITICAL"
        }
        print(f"   🚨 [Oracle] OVERRIDE TRIGGERED for {location}. AI Risk Score ignored.")
        return override_event

if __name__ == "__main__":
    oracle = CommunityOracle()
    oracle.receive_sms_report("CHW-Leader", "District-B", "AI says water safe but people sick!")
