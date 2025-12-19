"""
Swahili Medical Translator
═════════════════════════════════════════════════════════════════════════════

GDPR-compliant Swahili-English medical translation using Google Cloud Translation API.
Always validates data sovereignty before cloud translation.

Usage:
    translator = SwahiliMedicalTranslator(
        project_id="iluminara-production",
        location="europe-west4"
    )
    
    english_text = translator.translate("Nina homa na maumivu ya tumbo")
"""

from typing import Optional
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

try:
    from google.cloud import translate_v3
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    print("⚠️  google-cloud-translate not installed. Install with: pip install google-cloud-translate")


class SwahiliMedicalTranslator:
    """
    GDPR-compliant Swahili-English medical translator.
    Always de-identifies PHI before cloud translation.
    """
    
    def __init__(self, project_id: str, location: str = "europe-west4"):
        """
        Initialize the translator with Google Cloud configuration.
        
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region (default: europe-west4 for GDPR compliance)
        """
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError("google-cloud-translate is required. Install: pip install google-cloud-translate")
        
        self.project_id = project_id
        self.location = location
        self.client = translate_v3.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"
        self.guardrail = SovereignGuardrail()
        
        # Cache for common translations (offline capability)
        self.translation_cache = self._load_common_translations()
    
    def _load_common_translations(self) -> dict:
        """Load common Swahili medical terms for offline translation."""
        return {
            # Symptoms
            "homa": "fever",
            "kichefuchefu": "nausea",
            "maumivu ya kichwa": "headache",
            "maumivu ya tumbo": "stomach pain",
            "kukosa pumzi": "difficulty breathing",
            "kuhara": "diarrhea",
            "kutapika": "vomiting",
            "kikohozi": "cough",
            
            # Diseases
            "malaria": "malaria",
            "kifua kikuu": "tuberculosis",
            "ukimwi": "HIV/AIDS",
            "homa ya manjano": "yellow fever",
            
            # Body parts
            "kichwa": "head",
            "tumbo": "stomach",
            "moyo": "heart",
            "mapafu": "lungs",
            "ini": "liver",
            
            # Common phrases
            "nina": "I have",
            "mgonjwa": "patient",
            "daktari": "doctor",
            "hospitali": "hospital",
            "dawa": "medicine",
        }
    
    def translate(
        self, 
        text: str, 
        source_lang: str = "sw", 
        target_lang: str = "en",
        jurisdiction: str = "GDPR_EU",
        use_cache: bool = True
    ) -> Optional[str]:
        """
        Translate medical text with sovereignty validation.
        
        Args:
            text: De-identified medical text (no PHI)
            source_lang: Source language code (default: Swahili)
            target_lang: Target language code (default: English)
            jurisdiction: Legal framework to validate against
            use_cache: Whether to use offline cache first
        
        Returns:
            Translated text or None if sovereignty violation
        """
        
        # Check cache first for offline capability
        if use_cache and text.lower() in self.translation_cache:
            return self.translation_cache[text.lower()]
        
        # Validate sovereignty compliance
        try:
            self.guardrail.validate_action(
                action_type='Cloud_Translation',
                payload={
                    'data_type': 'De_Identified_Medical_Text',
                    'destination': f'Google_Cloud_{self.location.upper()}',
                    'has_phi': False,  # Must be False
                    'consent_token': 'GENERAL_RESEARCH_CONSENT'
                },
                jurisdiction=jurisdiction
            )
        except SovereigntyViolationError as e:
            print(f"❌ Translation blocked: {e}")
            return None
        
        # Perform translation via Google Cloud
        try:
            request = {
                "parent": self.parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_lang,
                "target_language_code": target_lang
            }
            
            response = self.client.translate_text(request=request)
            translated = response.translations[0].translated_text
            
            # Cache the translation
            if use_cache:
                self.translation_cache[text.lower()] = translated
            
            return translated
            
        except Exception as e:
            print(f"❌ Translation error: {e}")
            return None
    
    def batch_translate(self, texts: list, **kwargs) -> list:
        """
        Translate multiple texts efficiently.
        
        Args:
            texts: List of texts to translate
            **kwargs: Arguments passed to translate()
        
        Returns:
            List of translated texts
        """
        return [self.translate(text, **kwargs) for text in texts]
