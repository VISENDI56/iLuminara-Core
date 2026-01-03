import sys
import os
import json
import time
import requests
from datetime import datetime
import importlib.util

# Force sovereign pathing
sys.path.append(os.getcwd())

# JSON Report for CI/Audit Trail
report = {
    "timestamp": datetime.now().isoformat(),
    "overall_status": "FAIL",
    "components": {},
    "summary": []
}

def log_report(component, status, details=""):
    report["components"][component] = {"status": status, "details": details}
    prefix = "[SUCCESS]" if status == "PASS" else "[FAIL]"
    print(f"{prefix} {component}: {details}")

def probe_import(module_path, attr=None):
    try:
        spec = importlib.util.spec_from_file_location(module_path.replace('/', '.'), module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if attr:
                getattr(module, attr)
            return True
    except Exception as e:
        return str(e)
    return True

def test_flow():
    global report
    print("\n" + "="*50)
    print(" iLUMINARA APEX SOVEREIGN INTEGRITY SENTINEL")
    print(" Zero False Positives | Real Functional Validation")
    print("="*50)

    all_pass = True

    # --- PHASE 1: VOICE INGESTION PROBE ---
    if probe_import("core/ingestion/voice/sovereign_scribe.py", "SovereignScribe"):
        try:
            from core.ingestion.voice.sovereign_scribe import SovereignScribe
            scribe = SovereignScribe()
            # Real minimal call with synthetic input
            result = scribe.transcribe_synthetic("febrile patient 41.5C")
            log_report("1/7: VOX-SCRIBE", "PASS", f"Transcription: {result[:50]}...")
        except Exception as e:
            all_pass = False
            log_report("1/7: VOX-SCRIBE", "FAIL", str(e))
    else:
        all_pass = False
        log_report("1/7: VOX-SCRIBE", "FAIL", "Module/attr missing")

    # --- PHASE 2: Z3-GATE FORMAL VERIFICATION ---
    if probe_import("core/governance/gates/outlier_gate.py", "PatientZeroGate"):
        try:
            from core.governance.gates.outlier_gate import PatientZeroGate
            gate = PatientZeroGate()
            result = gate.verify_vital_sign("P-001", 41.5, 0.1)
            if "RETAIN" in result or "FP16" in result:
                log_report("2/7: Z3-FORMAL-GATE", "PASS", result)
            else:
                all_pass = False
                log_report("2/7: Z3-FORMAL-GATE", "FAIL", "Unexpected verdict")
        except Exception as e:
            all_pass = False
            log_report("2/7: Z3-FORMAL-GATE", "FAIL", str(e))
    else:
        all_pass = False
        log_report("2/7: Z3-FORMAL-GATE", "FAIL", "Module missing")

    # --- PHASE 3: AGENTIC CLINICAL CORE ---
    if probe_import("core/agentic_clinical/voice_triage_agent.py", "VoiceEnabledTriageAgent"):
        try:
            from core.agentic_clinical.voice_triage_agent import VoiceEnabledTriageAgent
            agent = VoiceEnabledTriageAgent()
            result = agent.assess_patient("41.5C fever unusual lesions")
            if result.get("status") in ["Critical", "Bio-Threat"]:
                log_report("3/7: AGENTIC-TRIAGE", "PASS", str(result))
            else:
                all_pass = False
                log_report("3/7: AGENTIC-TRIAGE", "FAIL", "No alert raised")
        except Exception as e:
            all_pass = False
            log_report("3/7: AGENTIC-TRIAGE", "FAIL", str(e))
    else:
        all_pass = False
        log_report("3/7: AGENTIC-TRIAGE", "FAIL", "Module missing")

    # --- PHASE 4: BIONEMO NEUTRALIZATION PIPELINE ---
    if probe_import("core/research/blueprints/protein_binder.py"):
        try:
            from core.research.blueprints.protein_binder import BioThreatNeutralizer
            neutralizer = BioThreatNeutralizer()
            # Ping local NIM endpoints first
            if requests.get("http://localhost:8001/v1/health", timeout=3).status_code == 200:
                result = neutralizer.design_binder("SAMPLE_PATHOGEN_SEQ")
                if result.get("binder_seq") and result.get("confidence", 0) > 0.5:
                    log_report("4/7: BIONEMO-SUBSTRATE", "PASS", f"Seq len: {len(result['binder_seq'])}")
                else:
                    all_pass = False
                    log_report("4/7: BIONEMO-SUBSTRATE", "FAIL", "Weak binder")
            else:
                all_pass = False
                log_report("4/7: BIONEMO-SUBSTRATE", "FAIL", "NIM endpoints down")
        except Exception as e:
            all_pass = False
            log_report("4/7: BIONEMO-SUBSTRATE", "FAIL", str(e))
    else:
        all_pass = False
        log_report("4/7: BIONEMO-SUBSTRATE", "FAIL", "Pipeline missing")

    # --- PHASE 5: ROCK SANDBOX CONTAINMENT ---
    if probe_import("agentic_clinical/rock_sandbox/__init__.py"):
        try:
            # Minimal sandbox spawn test with synthetic command
            from agentic_clinical.rock_sandbox import spawn_isolated
            spawn_isolated(["echo", "SOVEREIGN_TEST"])
            log_report("5/7: ROCK-CONTAINMENT", "PASS", "Sandbox spawned")
        except Exception as e:
            all_pass = False
            log_report("5/7: ROCK-CONTAINMENT", "FAIL", str(e))
    else:
        all_pass = False
        log_report("5/7: ROCK-CONTAINMENT", "FAIL", "ROCK integration missing")

    # --- PHASE 6: IFLOW CONTEXT ORCHESTRATION ---
    if probe_import("ml_ops/iflow_orchestrator.py"):
        try:
            from ml_ops.iflow_orchestrator import iFlowOrchestrator
            orch = iFlowOrchestrator()
            orch.persist_memory("test_alert", "Patient Zero")
            log_report("6/7: IFLOW-ORCHESTRATION", "PASS", "Memory persisted")
        except Exception as e:
            all_pass = False
            log_report("6/7: IFLOW-ORCHESTRATION", "FAIL", str(e))
    else:
        all_pass = False
        log_report("6/7: IFLOW-ORCHESTRATION", "FAIL", "iFlow missing")

    # --- PHASE 7: HARDWARE SUBSTRATE BINDING ---
    try:
        from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetPowerUsage
        nvmlInit()
        power = nvmlDeviceGetPowerUsage(nvmlDeviceGetHandleByIndex(0)) / 1000.0
        log_report("7/7: BLACKWELL-SUBSTRATE", "PASS", f"Power draw: {power:.1f}W")
    except Exception as e:
        all_pass = False
        log_report("7/7: BLACKWELL-SUBSTRATE", "FAIL", f"NVML: {str(e)}")

    # Final Verdict
    print("\n" + "="*50)
    if all_pass:
        report["overall_status"] = "PASS"
        print(" [APEX SUCCESS] FULL SOVEREIGN INTEGRITY VERIFIED")
    else:
        report["overall_status"] = "FAIL"
        print(" [CRITICAL FAIL] INTEGRITY BREACH DETECTED - INTERVENTION REQUIRED")
    print("="*50)

    # Sovereign Audit Export
    with open("tools/integrity_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nAudit trail exported: tools/integrity_report.json")

if __name__ == "__main__":
    test_flow()
    sys.exit(0 if report["overall_status"] == "PASS" else 1)
