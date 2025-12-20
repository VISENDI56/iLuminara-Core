"""
Voice-to-JSON Pipeline Integration Module
═════════════════════════════════════════════════════════════════════════════

End-to-end pipeline for transforming Swahili voice notes into structured JSON.
Integrates all components: transcription, symptom extraction, and data fusion.

Complete Pipeline:
1. Audio Input → Swahili Transcription (Cloud Speech-to-Text)
2. Transcription → Symptom Extraction (Vertex AI / FRENASA)
3. Symptoms → Golden Thread Data Fusion
4. Governance Validation (Sovereign Guardrail)
5. Structured JSON Output

Philosophy: "From voice to verified intelligence in seconds."
"""

from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import os


@dataclass
class VoiceToJSONResult:
    """Complete result from voice-to-JSON transformation."""
    pipeline_id: str
    success: bool
    
    # Input
    audio_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Stage 1: Transcription
    transcription: Optional[Dict[str, Any]] = None
    transcription_time_ms: float = 0.0
    
    # Stage 2: Symptom Extraction
    symptoms: Optional[Dict[str, Any]] = None
    extraction_time_ms: float = 0.0
    
    # Stage 3: Data Fusion
    golden_thread_record: Optional[Dict[str, Any]] = None
    fusion_time_ms: float = 0.0
    
    # Stage 4: Governance
    governance_status: str = "pending"
    sovereignty_compliant: bool = True
    
    # Overall
    total_time_ms: float = 0.0
    processing_mode: str = "unknown"
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pipeline_id": self.pipeline_id,
            "success": self.success,
            "audio_metadata": self.audio_metadata,
            "transcription": self.transcription,
            "transcription_time_ms": self.transcription_time_ms,
            "symptoms": self.symptoms,
            "extraction_time_ms": self.extraction_time_ms,
            "golden_thread_record": self.golden_thread_record,
            "fusion_time_ms": self.fusion_time_ms,
            "governance_status": self.governance_status,
            "sovereignty_compliant": self.sovereignty_compliant,
            "total_time_ms": self.total_time_ms,
            "processing_mode": self.processing_mode,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat()
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, filepath: str):
        """Save result to JSON file."""
        with open(filepath, 'w') as f:
            f.write(self.to_json())
        print(f"💾 Saved pipeline result to: {filepath}")


class VoiceToJSONPipeline:
    """
    Complete pipeline for Swahili voice note to structured JSON transformation.
    
    Orchestrates the entire workflow from audio input to verified JSON output,
    with sovereignty compliance validation at every step.
    
    Usage:
        pipeline = VoiceToJSONPipeline(mode="edge")
        result = pipeline.process(
            audio_data=audio_bytes,
            patient_id="PATIENT_001",
            location="Dadaab"
        )
        print(result.to_json())
    """
    
    def __init__(
        self,
        mode: str = "edge",
        credentials_path: Optional[str] = None,
        jurisdiction: str = "KDPA_KE",
        enable_logging: bool = True,
    ):
        """
        Initialize voice-to-JSON pipeline.
        
        Args:
            mode: Processing mode ("edge", "cloud", "hybrid")
            credentials_path: Path to Google Cloud credentials
            jurisdiction: Legal jurisdiction for governance
            enable_logging: Enable detailed logging
        """
        self.mode = mode
        self.credentials_path = credentials_path
        self.jurisdiction = jurisdiction
        self.enable_logging = enable_logging
        
        self._initialize_components()
        
        # Pipeline statistics
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "average_time_ms": 0.0
        }
    
    def _initialize_components(self):
        """Initialize all pipeline components."""
        try:
            from edge_node.frenasa_engine.voice_transcription import SwahiliTranscriber
            from edge_node.frenasa_engine.symptom_extraction import FRENASASymptomExtractor
            from edge_node.sync_protocol.golden_thread import GoldenThread
            from governance_kernel.vector_ledger import SovereignGuardrail
            
            if self.enable_logging:
                print("🔧 Initializing Voice-to-JSON Pipeline Components...")
            
            # Transcriber
            self.transcriber = SwahiliTranscriber(
                credentials_path=self.credentials_path,
                language_code="sw-KE"
            )
            
            # Symptom Extractor
            self.extractor = FRENASASymptomExtractor(
                credentials_path=self.credentials_path
            )
            
            # Golden Thread
            self.golden_thread = GoldenThread()
            
            # Sovereignty Guardrail
            self.guardrail = SovereignGuardrail()
            
            if self.enable_logging:
                print(f"✅ Pipeline initialized (mode: {self.mode}, jurisdiction: {self.jurisdiction})")
            
        except Exception as e:
            print(f"❌ Pipeline initialization failed: {e}")
            raise
    
    def process(
        self,
        audio_data: bytes,
        patient_id: str = "UNKNOWN",
        location: Optional[str] = None,
        chv_id: Optional[str] = None,
        consent_token: Optional[str] = None,
        audio_format: str = "LINEAR16",
        sample_rate: int = 16000,
    ) -> VoiceToJSONResult:
        """
        Process voice note through complete pipeline.
        
        Args:
            audio_data: Raw audio bytes
            patient_id: Patient identifier
            location: Geographic location
            chv_id: Community Health Volunteer ID
            consent_token: Patient consent token
            audio_format: Audio encoding format
            sample_rate: Audio sample rate in Hz
        
        Returns:
            VoiceToJSONResult with complete transformation result
        """
        pipeline_id = self._generate_pipeline_id()
        start_time = datetime.utcnow()
        
        # Audio metadata
        audio_metadata = {
            "size_bytes": len(audio_data),
            "format": audio_format,
            "sample_rate": sample_rate,
            "location": location,
            "chv_id": chv_id,
            "patient_id": patient_id
        }
        
        if self.enable_logging:
            print(f"\n{'═' * 80}")
            print(f"Pipeline {pipeline_id} - Starting Processing")
            print(f"{'═' * 80}")
        
        try:
            # ═════════════════════════════════════════════════════════════════
            # STAGE 0: Governance Pre-Check
            # ═════════════════════════════════════════════════════════════════
            if self.enable_logging:
                print("\n🛡️  Stage 0: Governance Pre-Check")
            
            self._validate_governance_precheck(
                audio_metadata,
                consent_token or "IMPLICIT_CHV_CONSENT"
            )
            
            # ═════════════════════════════════════════════════════════════════
            # STAGE 1: Swahili Transcription
            # ═════════════════════════════════════════════════════════════════
            if self.enable_logging:
                print("\n🎤 Stage 1: Swahili Transcription")
            
            stage1_start = datetime.utcnow()
            transcription_result = self.transcriber.transcribe_audio(
                audio_data,
                sample_rate_hertz=sample_rate,
                encoding=audio_format
            )
            stage1_time = (datetime.utcnow() - stage1_start).total_seconds() * 1000
            
            if self.enable_logging:
                print(f"   ✓ Transcribed: \"{transcription_result.text}\"")
                print(f"   ✓ Confidence: {transcription_result.confidence:.2%}")
                print(f"   ✓ Time: {stage1_time:.2f}ms")
            
            # ═════════════════════════════════════════════════════════════════
            # STAGE 2: FRENASA Symptom Extraction
            # ═════════════════════════════════════════════════════════════════
            if self.enable_logging:
                print("\n🔬 Stage 2: FRENASA Symptom Extraction")
            
            stage2_start = datetime.utcnow()
            extracted_symptoms = self.extractor.extract_symptoms(
                transcription_result.text,
                location=location
            )
            stage2_time = (datetime.utcnow() - stage2_start).total_seconds() * 1000
            
            if self.enable_logging:
                print(f"   ✓ Symptoms identified: {len(extracted_symptoms.symptoms)}")
                for symptom in extracted_symptoms.symptoms:
                    print(f"      - {symptom.symptom_name} ({symptom.severity})")
                print(f"   ✓ Urgency: {extracted_symptoms.urgency_level}")
                print(f"   ✓ Disease suspicion: {extracted_symptoms.disease_suspicion or 'None'}")
                print(f"   ✓ Time: {stage2_time:.2f}ms")
            
            # ═════════════════════════════════════════════════════════════════
            # STAGE 3: Golden Thread Data Fusion
            # ═════════════════════════════════════════════════════════════════
            if self.enable_logging:
                print("\n🧵 Stage 3: Golden Thread Data Fusion")
            
            stage3_start = datetime.utcnow()
            golden_thread_record = self._fuse_with_golden_thread(
                transcription_result,
                extracted_symptoms,
                patient_id,
                chv_id
            )
            stage3_time = (datetime.utcnow() - stage3_start).total_seconds() * 1000
            
            if self.enable_logging:
                print(f"   ✓ Record ID: {golden_thread_record.record_id}")
                print(f"   ✓ Verification score: {golden_thread_record.verification_score}")
                print(f"   ✓ Retention status: {golden_thread_record.retention_status}")
                print(f"   ✓ Time: {stage3_time:.2f}ms")
            
            # ═════════════════════════════════════════════════════════════════
            # STAGE 4: Final Governance Validation
            # ═════════════════════════════════════════════════════════════════
            if self.enable_logging:
                print("\n🛡️  Stage 4: Final Governance Validation")
            
            self._validate_governance_postcheck(golden_thread_record)
            
            if self.enable_logging:
                print("   ✓ All sovereignty checks passed")
            
            # Calculate total time
            total_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Update statistics
            self._update_stats(True, total_time)
            
            if self.enable_logging:
                print(f"\n{'═' * 80}")
                print(f"✅ Pipeline Complete - Total Time: {total_time:.2f}ms")
                print(f"{'═' * 80}")
            
            return VoiceToJSONResult(
                pipeline_id=pipeline_id,
                success=True,
                audio_metadata=audio_metadata,
                transcription=transcription_result.to_dict(),
                transcription_time_ms=stage1_time,
                symptoms=extracted_symptoms.to_dict(),
                extraction_time_ms=stage2_time,
                golden_thread_record=golden_thread_record.to_dict(),
                fusion_time_ms=stage3_time,
                governance_status="compliant",
                sovereignty_compliant=True,
                total_time_ms=total_time,
                processing_mode=self.mode,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            if self.enable_logging:
                print(f"\n❌ Pipeline failed: {e}")
            
            total_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            self._update_stats(False, total_time)
            
            return VoiceToJSONResult(
                pipeline_id=pipeline_id,
                success=False,
                audio_metadata=audio_metadata,
                total_time_ms=total_time,
                processing_mode=self.mode,
                sovereignty_compliant=False,
                governance_status="failed",
                error_message=str(e),
                timestamp=datetime.utcnow()
            )
    
    def _validate_governance_precheck(self, audio_metadata: Dict[str, Any], consent_token: str):
        """Pre-processing governance validation."""
        payload = {
            "data_type": "PHI",
            "destination": "Edge_Node" if self.mode == "edge" else "Cloud_Function",
            "consent_token": consent_token,
            "consent_scope": ["health_surveillance", "voice_transcription"],
            "action": "voice_note_processing"
        }
        
        self.guardrail.validate_action(
            action_type="Data_Transfer",
            payload=payload,
            jurisdiction=self.jurisdiction
        )
    
    def _validate_governance_postcheck(self, golden_thread_record):
        """Post-processing governance validation."""
        payload = {
            "data_type": "PHI",
            "destination": "Local_Database",
            "consent_token": "FUSED_RECORD_CONSENT",
            "explanation": f"Golden Thread fusion with verification score {golden_thread_record.verification_score}",
            "confidence_score": golden_thread_record.verification_score,
            "evidence_chain": golden_thread_record.confidence_chain,
            "record_date": golden_thread_record.timestamp.isoformat()
        }
        
        self.guardrail.validate_action(
            action_type="High_Risk_Inference",
            payload=payload,
            jurisdiction=self.jurisdiction
        )
    
    def _fuse_with_golden_thread(
        self,
        transcription_result,
        extracted_symptoms,
        patient_id: str,
        chv_id: Optional[str]
    ):
        """Integrate results with Golden Thread."""
        # Create CBS signal from voice note
        cbs_signal = {
            "location": extracted_symptoms.location or "UNKNOWN",
            "symptom": ", ".join([s.symptom_name for s in extracted_symptoms.symptoms]),
            "symptoms": [s.to_dict() for s in extracted_symptoms.symptoms],
            "timestamp": extracted_symptoms.timestamp.isoformat(),
            "source": "CHV_Voice_Alert",
            "chv_id": chv_id or "UNKNOWN_CHV",
            "urgency": extracted_symptoms.urgency_level,
            "disease_suspicion": extracted_symptoms.disease_suspicion,
            "transcription": transcription_result.text,
            "transcription_confidence": transcription_result.confidence
        }
        
        # Fuse with Golden Thread
        return self.golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            patient_id=patient_id
        )
    
    def _generate_pipeline_id(self) -> str:
        """Generate unique pipeline ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        return f"PIPELINE-V2J-{timestamp}"
    
    def _update_stats(self, success: bool, time_ms: float):
        """Update pipeline statistics."""
        self.stats["total_processed"] += 1
        if success:
            self.stats["successful"] += 1
        else:
            self.stats["failed"] += 1
        
        # Update average time
        total = self.stats["total_processed"]
        current_avg = self.stats["average_time_ms"]
        new_avg = ((current_avg * (total - 1)) + time_ms) / total
        self.stats["average_time_ms"] = new_avg
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        return self.stats.copy()


# ═════════════════════════════════════════════════════════════════════════════
# Convenience Functions
# ═════════════════════════════════════════════════════════════════════════════

def process_voice_file(
    filepath: str,
    patient_id: str = "UNKNOWN",
    location: Optional[str] = None,
    mode: str = "edge"
) -> VoiceToJSONResult:
    """
    Process a voice file through the pipeline.
    
    Args:
        filepath: Path to audio file
        patient_id: Patient identifier
        location: Geographic location
        mode: Processing mode ("edge", "cloud", "hybrid")
    
    Returns:
        VoiceToJSONResult
    """
    with open(filepath, 'rb') as f:
        audio_data = f.read()
    
    pipeline = VoiceToJSONPipeline(mode=mode)
    return pipeline.process(audio_data, patient_id=patient_id, location=location)


# ═════════════════════════════════════════════════════════════════════════════
# Example Usage / Demo
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 80)
    print("Voice-to-JSON Pipeline - Complete Integration Demo")
    print("═" * 80)
    
    # Create sample audio
    from edge_node.frenasa_engine.voice_transcription import create_sample_audio
    
    print("\n📢 Creating sample Swahili voice note...")
    audio = create_sample_audio(duration_seconds=3.0)
    
    # Initialize pipeline
    print("\n🔧 Initializing pipeline...")
    pipeline = VoiceToJSONPipeline(
        mode="edge",
        jurisdiction="KDPA_KE",
        enable_logging=True
    )
    
    # Process voice note
    result = pipeline.process(
        audio_data=audio,
        patient_id="PATIENT_DEMO_001",
        location="Dadaab, Ifo Camp",
        chv_id="CHV_AMINA_HASSAN",
        consent_token="DEMO_CONSENT_TOKEN"
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("FINAL JSON OUTPUT")
    print("=" * 80)
    print(result.to_json())
    
    # Save to file
    output_file = "/tmp/voice_to_json_result.json"
    result.save_to_file(output_file)
    
    # Display statistics
    print("\n" + "=" * 80)
    print("PIPELINE STATISTICS")
    print("=" * 80)
    stats = pipeline.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "═" * 80)
    print("✅ Demo Complete!")
    print("═" * 80)
