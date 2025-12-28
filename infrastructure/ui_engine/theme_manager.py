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

def get_theme_context():
    """
    Provides theme and physics metadata for the iLuminara Nexus.
    Ensures all keys required by dashboard.py (like time_lag_h) are present.
    """
    now = datetime.datetime.now()
    hour = now.hour

    # Physics constants for Circadian alignment
    physics_metadata = {
        "time_lag_h": 0.5,  # 30-minute lag for circadian shift processing
        "refresh_rate_ms": 1000,
        "solar_angle": 15.0 * (hour - 12) # Approximation
    }

    theme = "light" if 6 <= hour < 18 else "dark"

    return {
        "theme": theme,
        "physics": physics_metadata,
        "timestamp": now.isoformat()
    }