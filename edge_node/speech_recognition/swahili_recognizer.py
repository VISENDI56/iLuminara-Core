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
Swahili Speech Recognition Module for iLuminara
================================================

Integrates Google Cloud Speech-to-Text API for Swahili (sw-KE) language support.
This module is part of the FRENASA engine for processing voice alerts from 
Community Health Volunteers (CHVs) in East Africa.

Key Features:
- Real-time speech-to-text transcription in Swahili
- Support for both streaming and batch audio processing
- Integration with FRENASA symptom extraction pipeline
- Compliance with GDPR/KDPA data sovereignty requirements

Usage:
    recognizer = SwahiliRecognizer()
    text = recognizer.transcribe_audio("chv_alert.wav")
"""

from google.cloud import speech
from typing import Optional, Dict, Any, List
import io
import json
from datetime import datetime


class SwahiliRecognizer:
    """
    Speech-to-Text recognizer optimized for Swahili language (Kenya dialect).
    
    Attributes:
        language_code: Primary language code (sw-KE for Kenya)
        alternative_codes: Fallback language codes (sw-TZ for Tanzania)
        client: Google Cloud Speech client
    """
    
    def __init__(
        self, 
        language_code: str = "sw-KE",
        enable_automatic_punctuation: bool = True,
        enable_word_time_offsets: bool = False
    ):
        """
        Initialize Swahili speech recognizer.
        
        Args:
            language_code: BCP-47 language code (default: sw-KE)
            enable_automatic_punctuation: Add punctuation to transcripts
            enable_word_time_offsets: Include timing info for each word
        """
        self.language_code = language_code
        self.alternative_codes = ["sw-TZ"]  # Tanzania Swahili as fallback
        self.enable_automatic_punctuation = enable_automatic_punctuation
        self.enable_word_time_offsets = enable_word_time_offsets
        
        # Initialize Google Cloud Speech client
        self.client = speech.SpeechClient()
        
    def transcribe_audio(
        self, 
        audio_file_path: str,
        encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz: int = 16000
    ) -> Dict[str, Any]:
        """
        Transcribe audio file to text in Swahili.
        
        Args:
            audio_file_path: Path to audio file (WAV, FLAC, MP3)
            encoding: Audio encoding format
            sample_rate_hertz: Audio sample rate
            
        Returns:
            Dictionary containing:
                - transcript: Full transcription text
                - confidence: Confidence score (0.0 to 1.0)
                - language_code: Detected language code
                - timestamp: Processing timestamp
                - word_timestamps: Optional word-level timing info
        """
        # Read audio file
        with io.open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()
            
        audio = speech.RecognitionAudio(content=content)
        
        # Configure recognition settings
        config = speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=self.language_code,
            alternative_language_codes=self.alternative_codes,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
            enable_word_time_offsets=self.enable_word_time_offsets,
            model="default",  # Use default model for Swahili
        )
        
        # Perform recognition
        response = self.client.recognize(config=config, audio=audio)
        
        # Process results
        if not response.results:
            return {
                "transcript": "",
                "confidence": 0.0,
                "language_code": self.language_code,
                "timestamp": datetime.utcnow().isoformat(),
                "error": "No speech detected in audio"
            }
        
        # Extract best result
        result = response.results[0]
        alternative = result.alternatives[0]
        
        output = {
            "transcript": alternative.transcript,
            "confidence": alternative.confidence,
            "language_code": self.language_code,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Add word-level timestamps if enabled
        if self.enable_word_time_offsets and alternative.words:
            output["word_timestamps"] = [
                {
                    "word": word_info.word,
                    "start_time": word_info.start_time.total_seconds(),
                    "end_time": word_info.end_time.total_seconds(),
                }
                for word_info in alternative.words
            ]
        
        return output
    
    def transcribe_streaming(
        self,
        audio_generator,
        encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz: int = 16000
    ):
        """
        Perform streaming speech recognition for real-time transcription.
        
        Args:
            audio_generator: Generator yielding audio chunks
            encoding: Audio encoding format
            sample_rate_hertz: Audio sample rate
            
        Yields:
            Partial and final transcription results
        """
        # Configure streaming recognition
        config = speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz,
            language_code=self.language_code,
            alternative_language_codes=self.alternative_codes,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
        )
        
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True  # Return intermediate results
        )
        
        # Create request generator
        def request_generator():
            # First request contains streaming config
            yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
            
            # Subsequent requests contain audio content
            for audio_chunk in audio_generator:
                yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)
        
        # Perform streaming recognition
        responses = self.client.streaming_recognize(request_generator())
        
        # Process and yield results
        for response in responses:
            for result in response.results:
                alternative = result.alternatives[0]
                
                yield {
                    "transcript": alternative.transcript,
                    "is_final": result.is_final,
                    "confidence": alternative.confidence if result.is_final else None,
                    "timestamp": datetime.utcnow().isoformat(),
                }
    
    def extract_health_keywords(self, transcript: str) -> List[str]:
        """
        Extract common health-related keywords from Swahili transcript.
        
        This is a simple keyword extraction for integration with FRENASA engine.
        More sophisticated NLP is handled by the symptom extraction model.
        
        Args:
            transcript: Swahili transcription text
            
        Returns:
            List of detected health keywords
        """
        # Common Swahili health keywords
        health_keywords = {
            "homa": "fever",
            "kikohozi": "cough",
            "kuhara": "diarrhea",
            "kutapika": "vomiting",
            "maumivu": "pain",
            "kichwa": "head",
            "tumbo": "stomach",
            "kifua": "chest",
            "ugonjwa": "illness",
            "damu": "blood",
            "jasho": "sweating",
            "dhaifu": "weakness",
            "kichefuchefu": "nausea",
        }
        
        transcript_lower = transcript.lower()
        detected = []
        
        for swahili_word, english_translation in health_keywords.items():
            if swahili_word in transcript_lower:
                detected.append({
                    "swahili": swahili_word,
                    "english": english_translation
                })
        
        return detected


def recognize_swahili_audio(audio_file_path: str) -> Dict[str, Any]:
    """
    Convenience function for quick Swahili transcription.
    
    Args:
        audio_file_path: Path to audio file
        
    Returns:
        Transcription result dictionary
    """
    recognizer = SwahiliRecognizer()
    return recognizer.transcribe_audio(audio_file_path)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        print(f"🎤 Transcribing: {audio_file}")
        
        result = recognize_swahili_audio(audio_file)
        
        print("\n" + "="*60)
        print("TRANSCRIPTION RESULT")
        print("="*60)
        print(f"Text: {result['transcript']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Language: {result['language_code']}")
        print("="*60)
    else:
        print("Usage: python swahili_recognizer.py <audio_file.wav>")
