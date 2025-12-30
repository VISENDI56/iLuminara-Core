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

#!/usr/bin/env python3
"""
Sample Audio Generator for Voice Processing Tests
═════════════════════════════════════════════════════════════════════════════

Generates a simple WAV file for testing the voice processing endpoint.

In production, this would be replaced with actual voice recordings from CHVs.
"""

import wave
import struct
import random
import math


def generate_test_audio(filename: str, duration_seconds: float = 2.0, sample_rate: int = 16000):
    """
    Generate a test audio file with random noise.
    
    Args:
        filename: Output WAV filename
        duration_seconds: Length of audio in seconds
        sample_rate: Sample rate in Hz
    """
    print(f"Generating test audio: {filename}")
    print(f"  Duration: {duration_seconds}s")
    print(f"  Sample rate: {sample_rate} Hz")
    
    # Open WAV file for writing
    with wave.open(filename, 'wb') as wav_file:
        # Set parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate audio frames
        num_frames = int(sample_rate * duration_seconds)
        
        # Generate simple sine wave with noise (simulates speech)
        frames = []
        for i in range(num_frames):
            # Base sine wave (simulates voice fundamental frequency)
            t = i / sample_rate
            frequency = 150 + 50 * math.sin(2 * math.pi * 2 * t)  # Varying pitch
            amplitude = 3000 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.5 * t))  # Varying volume
            
            # Sine wave
            value = amplitude * math.sin(2 * math.pi * frequency * t)
            
            # Add noise for realism
            noise = random.gauss(0, 300)
            
            # Combine and clip
            sample = int(value + noise)
            sample = max(-32768, min(32767, sample))
            
            frames.append(struct.pack('h', sample))
        
        # Write frames
        wav_file.writeframes(b''.join(frames))
    
    print(f"✓ Generated: {filename}")
    return filename


def generate_swahili_symptom_audio():
    """Generate a sample audio file simulating a Swahili symptom report."""
    filename = "swahili-symptom.wav"
    
    # Generate 3 seconds of audio (longer for "speech")
    generate_test_audio(filename, duration_seconds=3.0)
    
    print(f"\nUsage:")
    print(f"  curl -X POST http://localhost:8080/process-voice \\")
    print(f"    -H 'Content-Type: audio/wav' \\")
    print(f"    --data-binary @{filename}")
    
    return filename


if __name__ == "__main__":
    print("═" * 80)
    print("iLuminara Test Audio Generator")
    print("═" * 80)
    print("")
    
    # Generate sample audio files
    generate_swahili_symptom_audio()
    
    print("")
    print("=" * 80)
    print("Test audio files generated successfully!")
    print("=" * 80)
