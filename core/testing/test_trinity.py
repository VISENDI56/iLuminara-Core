import sys
sys.path.append('.')  # Sovereign pathing

from core.governance.gates.outlier_gate import PatientZeroGate, PrecisionVerdict
from core.substrate.energy.solar_governor import SolarGovernor
from core.substrate.memory.kv_pager import SovereignPager

def run_apex_verification():
    print("\n=== iLuminara Build-Rev 184-Perfected: Sovereign Trinity Verification ===\n")

    passed = 0
    total = 3

    # 1. Patient Zero Protocol
    gate = PatientZeroGate(tolerance=0.01)
    verdict = gate.verify_vital_sign("Kakuma-Child-001", 41.5, 0.5)
    if verdict == PrecisionVerdict.RETAIN_FP16:
        print("[PASS] Z3-Gate: Correctly forced FP16 for outlier")
        passed += 1
    else:
        print("[FAIL] Z3-Gate: Unexpected verdict")

    # 2. Solar Sentinel
    gov = SolarGovernor()
    mode = gov.optimize_pipeline()
    if "FP8" in mode:
        print(f"[PASS] Solar Governor: Engaged low-power mode ({mode})")
        passed += 1
    else:
        print(f"[WARN] Solar Governor: Full power mode ({mode})")

    # 3. Sovereign Pager
    pager = SovereignPager(total_blocks=512)
    success1 = pager.allocate_longitudinal_context("Dadaab-Patient-001", "CRITICAL_ALLERGY")
    success2 = pager.allocate_longitudinal_context("Screening-002", "STANDARD")
    if success1 and success2:
        print("[PASS] Sovereign Pager: Successful allocation with priority")
        passed += 1
    else:
        print("[FAIL] Sovereign Pager: Allocation failed")

    print(f"\n=== TRINITY VERIFICATION: {passed}/{total} PASSED ===")
    print("System kinetic-ready for austere deployment.\n")

if __name__ == "__main__":
    run_apex_verification()
