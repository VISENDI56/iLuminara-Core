# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

"""
Swahili Medical Q&A System
═════════════════════════════════════════════════════════════════════════════

Medical question-answering system using Gemini Pro.
Provides evidence-based medical information in Swahili.

Usage:
    qa_system = SwahiliMedicalQA(api_key="YOUR_GEMINI_API_KEY")
    result = qa_system.ask("Je, dalili za malaria ni zipi?")
"""

from typing import Dict, List
from governance_kernel.vector_ledger import SovereignGuardrail

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  google-generativeai not installed. Install with: pip install google-generativeai")


class SwahiliMedicalQA:
    """
    Medical question-answering system using Gemini Pro.
    Provides evidence-based medical information in Swahili.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Swahili Medical Q&A system.
        
        Args:
            api_key: Gemini API key
        """
        self.guardrail = SovereignGuardrail()
        
        if GEMINI_AVAILABLE and api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_gemini = True
        else:
            self.use_gemini = False
            print("⚠️  Gemini not available. Using knowledge base responses.")
        
        # System prompt for medical context
        self.system_prompt = """
        Wewe ni mshauri wa afya wa AI unayezungumza Kiswahili na Kiingereza kwa ufasaha.
        (You are an AI health advisor fluent in Swahili and English.)
        
        Kanuni:
        1. Toa majibu ya kitaalamu yakijumuisha vyanzo vya kisayansi
        2. Kumbuka kuweka onyo kwa dalili hatari
        3. Pendekeza kutembelea daktari kwa hali mbaya
        4. Usitoe diagnosis za moja kwa moja - eleza uwezekano tu
        5. Zingatia hali za Kenya na Afrika Mashariki
        
        Rules:
        1. Provide evidence-based answers with scientific sources
        2. Always include warnings for serious symptoms
        3. Recommend seeing a doctor for severe conditions
        4. Don't give definitive diagnoses - explain possibilities only
        5. Consider context of Kenya and East Africa
        """
        
        # Knowledge base for offline mode
        self.knowledge_base = {
            "malaria": {
                "symptoms": "Dalili za malaria ni pamoja na homa, kichefuchefu, maumivu ya kichwa, na jasho baridi.",
                "treatment": "Dawa za malaria (ACT) zinapatikana hospitalini. Tembelea daktari kwa diagnosis sahihi.",
                "prevention": "Tumia chandarua cha kulala na ondoa maji yaliyosimama karibu na nyumba."
            },
            "homa": {
                "advice": "Pumzika, nywa maji mengi, na tumia kitambaa cha baridi. Kama homa ni juu ya 38.5°C au inaendelea zaidi ya siku 3, tembelea daktari."
            },
            "kifua kikuu": {
                "symptoms": "Dalili ni pamoja na kikohozi chenye damu, homa ya jioni, na kupungua uzito.",
                "action": "⚠️ Tafuta msaada wa haraka. Kifua kikuu ni hatari na kinahitaji matibabu ya haraka."
            }
        }
    
    def ask(self, question: str) -> Dict[str, any]:
        """
        Answer medical question in Swahili.
        
        Args:
            question: Medical question in Swahili
        
        Returns:
            {
                "answer": "...",
                "sources": ["WHO", "CDC"],
                "safety_notice": "...",
                "confidence": 0.85
            }
        """
        
        # Validate sovereignty (no PHI in question)
        if self._contains_phi(question):
            return {
                "answer": "Samahani, siwezi kuchakata maswali yenye taarifa za kibinafsi. Tafadhali uliza swali la jumla.",
                "sources": [],
                "safety_notice": "Privacy protection active",
                "confidence": 0.0
            }
        
        if self.use_gemini:
            return self._ask_with_gemini(question)
        else:
            return self._ask_with_knowledge_base(question)
    
    def _ask_with_gemini(self, question: str) -> Dict[str, any]:
        """Generate response using Gemini Pro."""
        try:
            full_prompt = f"{self.system_prompt}\n\nSwali la Mgonjwa: {question}\n\nJibu:"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.3,  # Lower temperature for medical accuracy
                    "top_p": 0.8,
                    "max_output_tokens": 1024
                },
                safety_settings={
                    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
                }
            )
            
            answer_text = response.text
            sources = self._extract_sources(answer_text)
            
            return {
                "answer": answer_text,
                "sources": sources,
                "safety_notice": self._generate_safety_notice(question),
                "confidence": 0.85
            }
            
        except Exception as e:
            print(f"⚠️  Gemini error: {e}. Using knowledge base.")
            return self._ask_with_knowledge_base(question)
    
    def _ask_with_knowledge_base(self, question: str) -> Dict[str, any]:
        """Answer using offline knowledge base."""
        question_lower = question.lower()
        
        # Search knowledge base
        for topic, info in self.knowledge_base.items():
            if topic in question_lower:
                # Build response from knowledge base
                answer_parts = []
                if "symptoms" in info:
                    answer_parts.append(info["symptoms"])
                if "treatment" in info:
                    answer_parts.append(info["treatment"])
                if "prevention" in info:
                    answer_parts.append(info["prevention"])
                if "advice" in info:
                    answer_parts.append(info["advice"])
                if "action" in info:
                    answer_parts.append(info["action"])
                
                answer = " ".join(answer_parts)
                
                return {
                    "answer": answer,
                    "sources": ["iLuminara Knowledge Base"],
                    "safety_notice": self._generate_safety_notice(question),
                    "confidence": 0.7
                }
        
        # Default response if topic not found
        return {
            "answer": "Samahani, sina taarifa kamili kuhusu swali lako. Tafadhali tembelea daktari kwa ushauri zaidi. / Sorry, I don't have complete information about your question. Please visit a doctor for more advice.",
            "sources": [],
            "safety_notice": "Taarifa hii ni ya elimu tu. Tembelea daktari kwa diagnosis sahihi.",
            "confidence": 0.3
        }
    
    def _contains_phi(self, text: str) -> bool:
        """Check if text contains Protected Health Information."""
        phi_indicators = [
            "jina langu",  # my name
            "naitwa",      # I am called
            "ID",
            "nambari ya simu",  # phone number
            "email",
            "tarehe ya kuzaliwa"  # date of birth
        ]
        
        return any(indicator in text.lower() for indicator in phi_indicators)
    
    def _extract_sources(self, text: str) -> List[str]:
        """Extract cited sources from generated text."""
        sources = []
        if "WHO" in text or "Shirika la Afya Duniani" in text:
            sources.append("World Health Organization")
        if "CDC" in text:
            sources.append("Centers for Disease Control")
        if "Kenya" in text or "MoH" in text or "Wizara ya Afya" in text:
            sources.append("Kenya Ministry of Health")
        
        return sources if sources else ["Medical Knowledge Base"]
    
    def _generate_safety_notice(self, question: str) -> str:
        """Generate appropriate safety notice based on question."""
        emergency_keywords = ["ajali", "damu nyingi", "kukosa pumzi", "kifua kikuu", "emergency"]
        
        for keyword in emergency_keywords:
            if keyword in question.lower():
                return "⚠️ DHARURA: Tafuta msaada wa haraka! / EMERGENCY: Seek immediate help!"
        
        return "Taarifa hii ni ya elimu tu. Tembelea daktari kwa diagnosis sahihi. / This information is for education only. Visit a doctor for accurate diagnosis."
