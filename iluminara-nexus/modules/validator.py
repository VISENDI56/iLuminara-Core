from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional

class ClinicalSignal(BaseModel):
    source_id: str = Field(..., min_length=3)
    location: str = Field(..., pattern=r"^(Ifo|Dagahaley|Hagadera|Kalobeyei)$")
    symptom_code: str = Field(..., min_length=3)
    severity_score: int = Field(..., ge=1, le=5)
    timestamp: Optional[str] = None

def validate_input(data_dict):
    try:
        if not data_dict.get('timestamp'):
            data_dict['timestamp'] = datetime.now().isoformat()
        signal = ClinicalSignal(**data_dict)
        return True, signal
    except ValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return False, errors
