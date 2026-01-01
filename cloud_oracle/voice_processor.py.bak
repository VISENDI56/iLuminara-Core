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
Voice Note Processor - Cloud Functions with Edge Fallback
═════════════════════════════════════════════════════════════════════════════

Trigger-based processing for voice notes using Cloud Functions architecture.
Includes edge fallback simulation for sovereignty-compliant local processing.

Architecture:
- Cloud Functions for scalable processing
- Edge fallback for offline/sovereign scenarios
- Integration with governance kernel for compliance
- Asynchronous processing with pub/sub triggers

Philosophy: "Process at the edge when sovereign, cloud when optimal."
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json
import base64


@dataclass
class ProcessingResult:
    """Result from voice note processing."""
    success: bool
    voice_note_id: str
    transcription: Dict[str, Any]
    extracted_symptoms: Dict[str, Any]
    golden_thread_record: Optional[Dict[str, Any]] = None
    processing_time_ms: float = 0.0
    processing_location: str = "unknown"  # "cloud", "edge", "hybrid"
    sovereignty_status: str = "compliant"
    error_message: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "voice_note_id": self.voice_note_id,
            "transcription": self.transcription,
            "extracted_symptoms": self.extracted_symptoms,
            "golden_thread_record": self.golden_thread_record,
            "processing_time_ms": self.processing_time_ms,
            "processing_location": self.processing_location,
            "sovereignty_status": self.sovereignty_status,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class VoiceNoteProcessor:
    """
    Cloud Functions-based voice note processor with edge fallback.
    
    Processes voice notes through the complete pipeline:
    1. Audio reception (Cloud Storage trigger)
    2. Transcription (Cloud Speech-to-Text)
    3. Symptom extraction (Vertex AI)
    4. Data fusion (Golden Thread)
    5. Governance validation (Sovereign Guardrail)
    
    Usage:
        processor = VoiceNoteProcessor(
            mode="edge",  # or "cloud" or "hybrid"
            enable_sovereignty_checks=True
        )
        
        result = processor.process_voice_note(
            audio_data=audio_bytes,
            metadata={"location": "Dadaab", "chv_id": "CHV_001"}
        )
    """
    
    def __init__(
        self,
        mode: str = "edge",
        enable_sovereignty_checks: bool = True,
        credentials_path: Optional[str] = None,
        jurisdiction: str = "KDPA_KE",
    ):
        """
        Initialize voice note processor.
        
        Args:
            mode: Processing mode ("cloud", "edge", "hybrid")
            enable_sovereignty_checks: Whether to enforce sovereignty validation
            credentials_path: Path to Google Cloud credentials
            jurisdiction: Legal jurisdiction for governance (e.g., "KDPA_KE", "GDPR_EU")
        """
        self.mode = mode
        self.enable_sovereignty_checks = enable_sovereignty_checks
        self.credentials_path = credentials_path
        self.jurisdiction = jurisdiction
        
        # Initialize components
        self._initialize_components()
        
        # Processing statistics
        self.processing_stats = {
            "total_processed": 0,
            "cloud_processed": 0,
            "edge_processed": 0,
            "sovereignty_violations": 0,
            "average_processing_time_ms": 0.0
        }
    
    def _initialize_components(self):
        """Initialize all processing components."""
        try:
            from edge_node.frenasa_engine.voice_transcription import SwahiliTranscriber
            from edge_node.frenasa_engine.symptom_extraction import FRENASASymptomExtractor
            from edge_node.sync_protocol.golden_thread import GoldenThread
            from governance_kernel.vector_ledger import SovereignGuardrail
            
            # Initialize transcriber
            self.transcriber = SwahiliTranscriber(
                credentials_path=self.credentials_path,
                language_code="sw-KE"
            )
            
            # Initialize symptom extractor
            self.extractor = FRENASASymptomExtractor(
                credentials_path=self.credentials_path
            )
            
            # Initialize Golden Thread
            self.golden_thread = GoldenThread()
            
            # Initialize sovereignty guardrail
            self.guardrail = SovereignGuardrail() if self.enable_sovereignty_checks else None
            
            print(f"✅ Voice note processor initialized (mode: {self.mode})")
            
        except Exception as e:
            print(f"❌ Failed to initialize components: {e}")
            raise
    
    def process_voice_note(
        self,
        audio_data: bytes,
        metadata: Optional[Dict[str, Any]] = None,
        patient_id: Optional[str] = None,
    ) -> ProcessingResult:
        """
        Process a voice note through the complete pipeline.
        
        Args:
            audio_data: Raw audio bytes
            metadata: Additional metadata (location, CHV ID, etc.)
            patient_id: Patient identifier (optional)
        
        Returns:
            ProcessingResult with complete processing outcome
        """
        start_time = datetime.utcnow()
        voice_note_id = self._generate_voice_note_id(metadata)
        
        try:
            # Step 1: Sovereignty validation (if enabled)
            if self.enable_sovereignty_checks:
                self._validate_sovereignty(audio_data, metadata)
            
            # Step 2: Transcription
            print(f"🎤 Transcribing voice note {voice_note_id}...")
            transcription_result = self.transcriber.transcribe_audio(audio_data)
            
            # Step 3: Symptom extraction
            print(f"🔬 Extracting symptoms from transcription...")
            location = metadata.get("location") if metadata else None
            extracted_symptoms = self.extractor.extract_symptoms(
                transcription_result.text,
                location=location
            )
            
            # Step 4: Golden Thread data fusion
            print(f"🧵 Fusing with Golden Thread...")
            golden_thread_record = self._fuse_with_golden_thread(
                extracted_symptoms,
                metadata,
                patient_id or "UNKNOWN"
            )
            
            # Calculate processing time
            end_time = datetime.utcnow()
            processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Determine processing location
            processing_location = self._determine_processing_location()
            
            # Update statistics
            self._update_statistics(processing_time_ms, processing_location)
            
            return ProcessingResult(
                success=True,
                voice_note_id=voice_note_id,
                transcription=transcription_result.to_dict(),
                extracted_symptoms=extracted_symptoms.to_dict(),
                golden_thread_record=golden_thread_record.to_dict() if golden_thread_record else None,
                processing_time_ms=processing_time_ms,
                processing_location=processing_location,
                sovereignty_status="compliant",
                timestamp=end_time
            )
            
        except Exception as e:
            print(f"❌ Voice note processing failed: {e}")
            
            end_time = datetime.utcnow()
            processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            return ProcessingResult(
                success=False,
                voice_note_id=voice_note_id,
                transcription={},
                extracted_symptoms={},
                processing_time_ms=processing_time_ms,
                processing_location=self.mode,
                sovereignty_status="error",
                error_message=str(e),
                timestamp=end_time
            )
    
    def _validate_sovereignty(self, audio_data: bytes, metadata: Optional[Dict[str, Any]]):
        """
        Validate sovereignty compliance before processing.
        
        Enforces:
        - PHI data stays in sovereign territory
        - Consent validation
        - Data processing lawfulness
        """
        if not self.guardrail:
            return
        
        # Validate high-risk inference action (voice processing involves PHI)
        payload = {
            "data_type": "PHI",
            "destination": "Edge_Node" if self.mode == "edge" else "Cloud_Function",
            "consent_token": metadata.get("consent_token", "IMPLICIT_CHV_CONSENT"),
            "consent_scope": ["health_surveillance", "outbreak_detection"],
            "action": "voice_transcription_and_symptom_extraction",
            "explanation": "Voice-based symptom reporting from community health volunteer",
            "confidence_score": 0.85,
            "evidence_chain": ["audio_input", "transcription", "symptom_extraction", "data_fusion"]
        }
        
        try:
            self.guardrail.validate_action(
                action_type="High_Risk_Inference",
                payload=payload,
                jurisdiction=self.jurisdiction
            )
        except Exception as e:
            self.processing_stats["sovereignty_violations"] += 1
            raise Exception(f"Sovereignty violation: {e}")
    
    def _fuse_with_golden_thread(
        self,
        extracted_symptoms,
        metadata: Optional[Dict[str, Any]],
        patient_id: str
    ):
        """Integrate extracted symptoms with Golden Thread data fusion."""
        # Create CBS signal from voice note
        cbs_signal = {
            "location": extracted_symptoms.location or "UNKNOWN",
            "symptom": ", ".join([s.symptom_name for s in extracted_symptoms.symptoms]),
            "symptoms": [s.to_dict() for s in extracted_symptoms.symptoms],
            "timestamp": extracted_symptoms.timestamp.isoformat(),
            "source": "CHV_Voice_Alert",
            "chv_id": metadata.get("chv_id") if metadata else None,
            "urgency": extracted_symptoms.urgency_level,
            "disease_suspicion": extracted_symptoms.disease_suspicion
        }
        
        # Fuse with Golden Thread
        fused_record = self.golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            patient_id=patient_id
        )
        
        return fused_record
    
    def _generate_voice_note_id(self, metadata: Optional[Dict[str, Any]]) -> str:
        """Generate unique voice note ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        chv_id = metadata.get("chv_id", "UNKNOWN") if metadata else "UNKNOWN"
        return f"VN-{chv_id}-{timestamp}"
    
    def _determine_processing_location(self) -> str:
        """Determine where processing occurred."""
        if self.mode == "edge":
            return "edge"
        elif self.mode == "cloud":
            # Check if cloud services were actually used
            if self.transcriber.client is None and self.extractor.client is None:
                return "edge_fallback"
            return "cloud"
        else:  # hybrid
            return "hybrid"
    
    def _update_statistics(self, processing_time_ms: float, location: str):
        """Update processing statistics."""
        self.processing_stats["total_processed"] += 1
        
        if location in ["cloud", "hybrid"]:
            self.processing_stats["cloud_processed"] += 1
        else:
            self.processing_stats["edge_processed"] += 1
        
        # Update average processing time
        total = self.processing_stats["total_processed"]
        current_avg = self.processing_stats["average_processing_time_ms"]
        new_avg = ((current_avg * (total - 1)) + processing_time_ms) / total
        self.processing_stats["average_processing_time_ms"] = new_avg
    
    def get_statistics(self) -> Dict[str, Any]:
        """Return processing statistics."""
        return self.processing_stats.copy()


# ═════════════════════════════════════════════════════════════════════════════
# Cloud Functions Entry Points
# ═════════════════════════════════════════════════════════════════════════════

def cloud_function_handler(event, context):
    """
    Google Cloud Functions entry point for voice note processing.
    
    Triggered by Cloud Storage upload event.
    
    Args:
        event: Cloud Storage event data
        context: Cloud Functions context
    
    Returns:
        HTTP response with processing result
    """
    print(f"Processing voice note from Cloud Storage trigger...")
    print(f"Event: {event}")
    
    try:
        # Extract audio data from Cloud Storage
        bucket_name = event.get("bucket")
        file_name = event.get("name")
        
        # Initialize processor in cloud mode
        processor = VoiceNoteProcessor(
            mode="cloud",
            enable_sovereignty_checks=True,
            jurisdiction="KDPA_KE"
        )
        
        # Download audio from Cloud Storage
        # (In production, would use google-cloud-storage)
        # audio_data = download_from_gcs(bucket_name, file_name)
        audio_data = b""  # Placeholder
        
        # Extract metadata from file name or Cloud Storage metadata
        metadata = {
            "location": event.get("metadata", {}).get("location", "UNKNOWN"),
            "chv_id": event.get("metadata", {}).get("chv_id", "UNKNOWN"),
            "consent_token": "CLOUD_STORAGE_UPLOAD_CONSENT"
        }
        
        # Process voice note
        result = processor.process_voice_note(audio_data, metadata)
        
        print(f"✅ Processing complete: {result.voice_note_id}")
        
        return {
            "statusCode": 200,
            "body": result.to_json()
        }
        
    except Exception as e:
        print(f"❌ Cloud function error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def edge_fallback_handler(audio_data: bytes, metadata: Dict[str, Any]) -> ProcessingResult:
    """
    Edge fallback handler for offline/sovereign scenarios.
    
    Processes voice notes locally without cloud connectivity.
    
    Args:
        audio_data: Raw audio bytes
        metadata: Voice note metadata
    
    Returns:
        ProcessingResult
    """
    print("🔒 Using edge fallback (sovereignty mode)...")
    
    processor = VoiceNoteProcessor(
        mode="edge",
        enable_sovereignty_checks=True,
        jurisdiction="KDPA_KE"
    )
    
    return processor.process_voice_note(audio_data, metadata)


# ═════════════════════════════════════════════════════════════════════════════
# Example Usage / Testing
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 80)
    print("Voice Note Processor - Cloud Functions with Edge Fallback")
    print("═" * 80)
    
    # Test with edge mode (no cloud connectivity required)
    print("\n📦 Testing Edge Fallback Mode...\n")
    
    # Create sample audio
    from edge_node.frenasa_engine.voice_transcription import create_sample_audio
    audio = create_sample_audio(duration_seconds=2.0)
    
    # Create metadata
    metadata = {
        "location": "Dadaab, Ifo Camp",
        "chv_id": "CHV_AMINA_HASSAN",
        "timestamp": datetime.utcnow().isoformat(),
        "consent_token": "CHV_IMPLICIT_CONSENT"
    }
    
    # Process voice note
    processor = VoiceNoteProcessor(mode="edge", enable_sovereignty_checks=True)
    result = processor.process_voice_note(audio, metadata, patient_id="PATIENT_TEST_001")
    
    print("=" * 80)
    print("Processing Result:")
    print("=" * 80)
    print(f"Success: {result.success}")
    print(f"Voice Note ID: {result.voice_note_id}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    print(f"Processing Location: {result.processing_location}")
    print(f"Sovereignty Status: {result.sovereignty_status}")
    print(f"\nTranscription: {result.transcription.get('text', 'N/A')}")
    print(f"Symptoms Extracted: {len(result.extracted_symptoms.get('symptoms', []))}")
    print(f"Urgency: {result.extracted_symptoms.get('urgency', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("Full JSON Output:")
    print("=" * 80)
    print(result.to_json())
    
    print("\n" + "=" * 80)
    print("Processing Statistics:")
    print("=" * 80)
    stats = processor.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "═" * 80)
