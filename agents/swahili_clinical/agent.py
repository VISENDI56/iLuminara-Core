"""
Swahili Clinical Agent Prototype
Offline protocol advisor for refugee camp settings.
Inspired by AfriSpeech clinical domain.
"""

class SwahiliClinicalAgent:
    def __init__(self):
        self.protocols = {
            "malaria": "Matibabu ya malaria: Dawa ya kwanza ni ACT...",
            "nutrition": "Lishe kwa watoto:..."
        }

    def query(self, symptom: str):
        if "homa" in symptom.lower() or "malaria" in symptom.lower():
            return self.protocols["malaria"]
        return "Wasiliana na daktari haraka."

if __name__ == "__main__":
    agent = SwahiliClinicalAgent()
    print(agent.query("Mtoto ana homa na kutapika"))
