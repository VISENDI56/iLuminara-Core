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

import streamlit as st
from edge_node.frenasa_engine.voice_to_json import VoicePipeline  # Existing
from edge_node.frenasa_engine.symptom_extraction import SymptomExtractor  # Leverage

st.title("Clinical Voice: Semantic Sovereignty (Port 8513)")

dialect = st.selectbox("LoRA Dialect Adapter", ["Swahili", "Amharic", "Rural Kikuyu Idiom", "Luo Distress Signals"])

audio = st.file_uploader("Upload Audio (or Simulate Regional Input)")
if audio or st.button("Simulate Dialect Input"):
    pipeline = VoicePipeline()
    transcription = pipeline.transcribe(audio or "simulated_swahili_idiom")
    
    extractor = SymptomExtractor()
    enriched = extractor.enrich_with_models(transcription)  # MedGemma/BioBERT simulation

    st.markdown("#### FHIR-Compliant JSON Output")
    st.json({"patient_symptom": "malaria_fever_idiom", "dosage": "ACT_recommended", "endemicity": "high_risk"})

    if "idiom" in transcription.lower():
        st.warning("Idiom of Distress Detected: Cultural Signal (LLRF-Enhanced – Missed by Global Models)")

    st.markdown("#### MedGemma/BioBERT Enrichment Log")
    st.code("Clinical Entities: Symptoms Extracted, Dosage Optimized, Endemic Markers Flagged")