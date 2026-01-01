import os

class HardwareAbstractionLayer:
    """
    Foolproof Supply Chain Strategy.
    Detects available silicon and routes compute accordingly.
    Reduces dependence on top-tier H100s.
    """
    def detect_and_route(self):
        # 1. Check for NVIDIA GPU
        if self._check_nvidia():
            return "CUDA_BACKEND"
            
        # 2. Check for AMD GPU (ROCm)
        if self._check_amd():
            return "ROCM_BACKEND"
            
        # 3. Fallback to CPU (OpenVINO / ONNX)
        return "CPU_OPTIMIZED_BACKEND"

    def _check_nvidia(self):
        # Simulated check
        return True 

    def _check_amd(self):
        return False