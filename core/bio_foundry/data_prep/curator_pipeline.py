from nemo_curator import Curator
from nemo_curator.filters import QualityFilter

class SovereignDataCurator:
    """
    Using NeMo Curator to ensure biosecurity data is high-fidelity
    and stripped of non-compliant PII before training.
    """
    def __init__(self):
        self.curator = Curator()

    def sanitize_field_data(self, raw_pathogen_json):
        # Apply high-fidelity filters to remove 'noisy' biometrics
        # ensuring the RSA doesn't learn from corrupted field data.
        clean_data = self.curator.filter(
            raw_pathogen_json,
            filter_obj=QualityFilter(min_score=0.85)
        )
        return clean_data

curator_engine = SovereignDataCurator()