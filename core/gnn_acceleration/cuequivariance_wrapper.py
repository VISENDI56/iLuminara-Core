import torch
try:
    import cuequivariance as cue
except ImportError:
    cue = None

class GeometricAccelerator:
    """Blackwell-native geometric speeds via cuEquivariance."""
    pass
