import json
from datetime import datetime

class HSMLLogger:
    """
        Human Security Markup Language (HSML).
            Standardizes Audit Logs for the Blockchain/Transparency Portal.
                """
                    def log_decision(self, actor, action, compliance_verdict):
                            log_entry = {
                                    "timestamp": datetime.utcnow().isoformat(),
                                        "actor_role": actor, # CHW, Supervisor, Donor
                                            "action": action,
                                                "compliance": compliance_verdict, # NIST AI RMF Level 3
                                                    "sovereignty_tag": "KENYA_DADAAB_NODE_01"
                            }
                    return json.dumps(log_entry)