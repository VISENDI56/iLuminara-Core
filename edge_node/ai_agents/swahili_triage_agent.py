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
Swahili Medical Triage Agent
═════════════════════════════════════════════════════════════════════════════

Conversational AI agent for Swahili medical symptom triage using Dialogflow CX.
Integrates with iLuminara Edge Node for CBS reporting.

Usage:
    agent = SwahiliTriageAgent(
        project_id="iluminara-production",
        agent_id="swahili-triage-agent-id"
    )
    
    response = agent.triage_symptom("homa na kichefuchefu")
"""

from typing import Dict, Optional
import uuid
from datetime import datetime

try:
    from google.cloud import dialogflowcx_v3 as dialogflow
    DIALOGFLOW_AVAILABLE = True
except ImportError:
    DIALOGFLOW_AVAILABLE = False
    print("⚠️  google-cloud-dialogflow-cx not installed. Install with: pip install google-cloud-dialogflow-cx")


class SwahiliTriageAgent:
    """
    Conversational AI agent for Swahili medical symptom triage.
    Integrates with iLuminara Edge Node for CBS reporting.
    """
    
    def __init__(
        self, 
        project_id: str,
        location: str = "europe-west4",
        agent_id: str = None
    ):
        """
        Initialize the Swahili triage agent.
        
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region
            agent_id: Dialogflow CX agent ID (optional)
        """
        self.project_id = project_id
        self.location = location
        self.agent_id = agent_id
        
        if DIALOGFLOW_AVAILABLE and agent_id:
            self.use_dialogflow = True
            self.session_client = dialogflow.SessionsClient()
            self.agent_path = f"projects/{project_id}/locations/{location}/agents/{agent_id}"
        else:
            self.use_dialogflow = False
            print("⚠️  Dialogflow not available. Using rule-based triage.")
        
        # Rule-based triage logic for offline mode
        self.triage_rules = {
            # Emergency symptoms
            "emergency": {
                "keywords": ["kukosa pumzi", "damu nyingi", "kifua kikuu", "ajali"],
                "response": "⚠️ DHARURA! Tafuta msaada wa haraka. Nenda hospitali mara moja. / EMERGENCY! Seek immediate help. Go to hospital now.",
                "priority": "HIGH"
            },
            # Serious symptoms
            "urgent": {
                "keywords": ["homa kali", "kutapika", "kuhara kwa siku nyingi", "maumivu ya kifua"],
                "response": "Dalili zako ni za kuhitajika. Tembelea kliniki leo. / Your symptoms require attention. Visit clinic today.",
                "priority": "MEDIUM"
            },
            # Common symptoms
            "routine": {
                "keywords": ["homa", "kichefuchefu", "maumivu ya kichwa", "kikohozi"],
                "response": "Pumzika na kunywa maji mengi. Kama homa haipungui baada ya siku 3, tembelea daktari. / Rest and drink plenty of water. If fever persists after 3 days, see a doctor.",
                "priority": "LOW"
            }
        }
    
    def detect_intent(
        self, 
        text: str, 
        session_id: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Send user query to Dialogflow agent and get response.
        
        Args:
            text: Swahili medical query
            session_id: Unique session identifier
        
        Returns:
            {
                "response_text": "...",
                "intent": "report_symptom",
                "parameters": {...},
                "confidence": 0.95
            }
        """
        
        if self.use_dialogflow:
            return self._detect_with_dialogflow(text, session_id)
        else:
            return self._detect_with_rules(text)
    
    def _detect_with_dialogflow(self, text: str, session_id: str = None) -> Dict[str, any]:
        """Detect intent using Dialogflow CX."""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session_path = f"{self.agent_path}/sessions/{session_id}"
        
        try:
            # Prepare query
            text_input = dialogflow.TextInput(text=text)
            query_input = dialogflow.QueryInput(
                text=text_input,
                language_code="sw"
            )
            
            # Send request
            request = dialogflow.DetectIntentRequest(
                session=session_path,
                query_input=query_input
            )
            
            response = self.session_client.detect_intent(request=request)
            query_result = response.query_result
            
            # Parse response
            return {
                "response_text": query_result.response_messages[0].text.text[0] if query_result.response_messages else "",
                "intent": query_result.intent.display_name if query_result.intent else "unknown",
                "parameters": dict(query_result.parameters) if query_result.parameters else {},
                "confidence": query_result.intent_detection_confidence if query_result.intent else 0.0,
                "session_id": session_id
            }
            
        except Exception as e:
            print(f"⚠️  Dialogflow error: {e}. Falling back to rules.")
            return self._detect_with_rules(text)
    
    def _detect_with_rules(self, text: str) -> Dict[str, any]:
        """Detect intent using rule-based logic (offline mode)."""
        text_lower = text.lower()
        
        # Check emergency first
        for severity, rule in self.triage_rules.items():
            for keyword in rule["keywords"]:
                if keyword in text_lower:
                    return {
                        "response_text": rule["response"],
                        "intent": f"report_symptom_{severity}",
                        "parameters": {"symptom": keyword, "severity": severity},
                        "confidence": 0.8,
                        "priority": rule["priority"]
                    }
        
        # Default response
        return {
            "response_text": "Asante kwa kuripoti. Daktari atakutembelea. / Thank you for reporting. A doctor will visit you.",
            "intent": "report_symptom_general",
            "parameters": {},
            "confidence": 0.5,
            "priority": "LOW"
        }
    
    def triage_symptom(self, symptom: str, log_to_cbs: bool = True) -> str:
        """
        Triage a reported symptom and provide guidance.
        
        Args:
            symptom: Swahili symptom description
            log_to_cbs: Whether to log to Community-Based Surveillance
        
        Returns:
            Triage advice in Swahili
        """
        
        query = f"Nina {symptom}"  # "I have {symptom}"
        result = self.detect_intent(query)
        
        # Log to CBS if requested
        if log_to_cbs:
            self._log_to_cbs(symptom, result)
        
        return result["response_text"]
    
    def _log_to_cbs(self, symptom: str, triage_result: Dict):
        """Log symptom to Community-Based Surveillance system."""
        try:
            from edge_node.sync_protocol.golden_thread import GoldenThread
            
            gt = GoldenThread()
            
            cbs_record = {
                'location': 'Unknown',  # Would be geo-tagged in production
                'symptom': symptom,
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'dialogflow_triage',
                'priority': triage_result.get('priority', 'LOW')
            }
            
            # Log CBS signal (privacy-preserving, no patient ID)
            print(f"📊 CBS Log: {symptom} | Priority: {cbs_record['priority']}")
            # In production: gt.log_cbs_signal(cbs_record)
            
        except Exception as e:
            print(f"⚠️  CBS logging failed: {e}")
