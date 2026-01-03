from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class GeoBoundary(BaseModel):
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float

class HSML_Log(BaseModel):
    """
        The Immutable Audit Trail Schema.
            Enforces 'Golden Rule Algorithm' constraints.
                """
                    trace_id: str = Field(..., description="Blockchain-logged Chain-of-Thought ID")
                        timestamp: datetime
                            actor_role: str
                                action_type: str
                                    
                                        # Mathematical Fairness Constraints
                                            wfp_vulnerability_index: float = Field(..., ge=0.0, le=1.0)
                                                equity_score: float
                                                    
                                                        # Sovereignty Enforcement
                                                            geo_context: GeoBoundary
                                                                
                                                                    @validator('equity_score')
                                                                        def enforce_golden_rule(cls, v, values):
                                                                                """
                                                                                        Golden Rule Algorithm:
                                                                                                Resources must prioritize vulnerability.
                                                                                                        If Equity Score < WFP Index, the action is UNETHICAL.
                                                                                                                """
                                                                                                                        if 'wfp_vulnerability_index' in values and v < values['wfp_vulnerability_index']:
                                                                                                                                raise ValueError("Golden Rule Violation: Equity Score below Vulnerability Index.")
                                                                                                                                        return v