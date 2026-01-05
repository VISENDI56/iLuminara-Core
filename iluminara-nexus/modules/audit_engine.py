import pandas as pd
import os
from datetime import datetime

class EvidenceLocker:
    def __init__(self, path="audit/ip09_locker.csv"):
        self.path = path
        if not os.path.exists(self.path):
            df = pd.DataFrame(columns=["Timestamp", "IP_Module", "Action", "Status", "Nexus_Location"])
            df.to_csv(self.path, index=False)

    def commit(self, event, ip_module, status, location="Dadaab-Dagahaley"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = pd.DataFrame([[timestamp, ip_module, event, status, location]])
        log_entry.to_csv(self.path, mode='a', header=False, index=False)
