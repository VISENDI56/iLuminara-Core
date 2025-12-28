import datetime

def apply_circadian_theme():
    """
    Applies Dark/Light mode based on the local time of the Edge Node.
    Supports ISO 42001 'Human Factors' requirements.
    """
    hour = datetime.datetime.now().hour
    if 6 <= hour < 18:
        print("   [Theme] Circadian Shift: LIGHT_MODE (Daytime Ops)")
        return "light"
    else:
        print("   [Theme] Circadian Shift: DARK_MODE (Nighttime Ops)")
        return "dark"