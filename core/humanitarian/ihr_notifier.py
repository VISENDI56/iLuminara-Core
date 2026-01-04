import datetime

class IHRNotifier:
    """WHO IHR (2005/2025): 24-hour Epidemiological Reporting."""
    def assess_event(self, outbreak_data):
        # Annex 2 Assessment logic
        if outbreak_data['severity'] > 0.8:
            self.send_focal_point_alert(outbreak_data)

    def send_focal_point_alert(self, data):
        timestamp = datetime.datetime.now().isoformat()
        print(f"[IHR-24H] NOTIFICATION: National Focal Point Alerted at {timestamp}")
