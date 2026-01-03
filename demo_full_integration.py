"""
Full Integration Demo
Chains: Ingestion → Lattice → EITV → Provenance → Charter Alignment
"""

from core.lattice.core import LatticeCore
from governance.solar_governor.eitv_mode import SolarGovernor
from security.logic_scrubber.provenance_audit import ProvenanceAuditor
from agents.charter_alignment.supervisor import CharterAlignmentAgent

print("iLuminara-Core Full Sovereign Reasoning Demo")
lattice = LatticeCore()
lattice.build_lattice(".")
impact = lattice.predict_impact("Z3-Gate")

governor = SolarGovernor()
governor.apply_change_with_eitv("Refactor Z3-Gate for new protocol")

auditor = ProvenanceAuditor()
auditor.audit_data("WHO_Protocols", "Malaria update")

agent = CharterAlignmentAgent()
agent.check_alignment("Telemetry update", impact)

print("Full chain complete: Sovereign change approved.")
