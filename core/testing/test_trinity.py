from core.governance.gates.outlier_gate import PatientZeroGate
from core.substrate.energy.solar_governor import SolarGovernor
from core.substrate.memory.kv_pager import SovereignPager

def run_apex_check():
    print("--- iLuminara Build-Rev 184 Trinity Check ---")
    
    # 1. Test Patient Zero Protocol (Kakuma Child Scenario)
    gate = PatientZeroGate(tolerance=0.01)
    # Scale factor 0.5 results in error 0.25 (>0.01) -> Should Force FP16
    verdict = gate.verify_vital_sign("Kakuma-Child-001", 41.0, 0.5)
    print(f"Patient Zero Verdict: {verdict}")
    
    # 2. Test Solar Sentinel (Polio Scenario)
    gov = SolarGovernor()
    mode = gov.optimize_pipeline()
    print(f"Solar Mode: {mode}")

    # 3. Test Sovereign Pager (TB History Scenario)
    pager = SovereignPager()
    alloc = pager.allocate_longitudinal_context("Dadaab-TB-Patient-05", "CRITICAL_ALLERGY")
    print(f"Longitudinal Allocation: {alloc}")

if __name__ == "__main__":
    run_apex_check()
