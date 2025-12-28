import json
import datetime

class FHIRAdapter:
    """
    Framework 14: FHIR R4 Compliant Data Exchange.
    Ensures iLuminara speaks 'Ministry of Health' language.
    """
    def to_fhir_observation(self, internal_data):
        """
        Converts internal symptom data to FHIR Observation Resource.
        """
        return {
            "resourceType": "Observation",
            "id": "example-observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "8867-4",
                    "display": "Heart rate"
                }]
            },
            "subject": {"reference": f"Patient/{internal_data.get('patient_hash')}"},
            "valueQuantity": {
                "value": internal_data.get("value"),
                "unit": "beats/minute",
                "system": "http://unitsofmeasure.org",
                "code": "/min"
            },
            "effectiveDateTime": datetime.datetime.now().isoformat()
        }

if __name__ == "__main__":
    adapter = FHIRAdapter()
    fhir_json = adapter.to_fhir_observation({"patient_hash": "abc-123", "value": 80})
    print(json.dumps(fhir_json, indent=2))
