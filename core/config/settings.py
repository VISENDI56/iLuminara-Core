from pydantic_settings import BaseSettings
from typing import Literal

class GlobalSettings(BaseSettings):
    ENV_STATE: Literal["dev", "staging", "prod"] = "dev"
    
    # Feature Flags
    ENABLE_HSTPU_PREDICTION: bool = True
    ENABLE_AZURE_BRIDGE: bool = False
    
    # Performance Targets
    MAX_LATENCY_MS: int = 52
    ANXIETY_REDUCTION_TARGET: float = 0.316  # 31.6%
    
    # WFP Vulnerability Weights
    EQUITY_WEIGHT_VULNERABLE: float = 1.5
    EQUITY_WEIGHT_STANDARD: float = 1.0

    class Config:
        env_file = ".env"

settings = GlobalSettings()