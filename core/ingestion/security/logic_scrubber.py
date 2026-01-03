import re
class LogicScrubber:
    """Build-Rev 214: Scrubbing transcripts for logic-bombs."""
    def audit(self, text):
        forbidden = [r"DROP", r"DELETE", r"eval", r"exec"]
        return not any(re.search(p, text, re.I) for p in forbidden)
