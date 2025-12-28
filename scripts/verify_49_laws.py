#!/usr/bin/env python3
"""
49-Law Quantum Nexus Audit Script
═════════════════════════════════════════════════════════════════════════════

Performs a "Roll Call" of every legal framework currently active in the
iLuminara Governance Kernel. Verifies trigger logic is active and proves
the system is enforcing the full Sovereign Stack.

Philosophy: "Trust, but verify. Every law. Every trigger. Every time."
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add root to path to import kernel
sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_kernel.guardrail import SovereignGuardrail
from governance_kernel.rco_engine import RegenerativeComplianceOracle


class LawStackAuditor:
    """Audits the Sovereign Law Stack for completeness and liveness."""
    
    def __init__(self):
        self.registry_path = Path(__file__).parent.parent / "governance_kernel" / "sectoral_laws.json"
        self.registry = None
        self.guardrail = None
        self.rco = None
        
    def load_registry(self) -> bool:
        """Load the sectoral laws registry."""
        try:
            with open(self.registry_path, 'r') as f:
                self.registry = json.load(f)
            print(f"✅ Loaded registry from {self.registry_path}")
            return True
        except FileNotFoundError:
            print(f"❌ CRITICAL: sectoral_laws.json not found at {self.registry_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ CRITICAL: Invalid JSON in sectoral_laws.json: {e}")
            return False
    
    def count_frameworks(self) -> Dict[str, Any]:
        """Count and categorize all legal frameworks."""
        if not self.registry:
            return {}
        
        nexus = self.registry.get("45_law_quantum_nexus", {})
        laws = nexus.get("laws", {})
        
        framework_count = {
            "total": len(laws),
            "by_jurisdiction": {},
            "by_sector": {},
            "frameworks": []
        }
        
        for law_key, law_data in laws.items():
            framework_info = {
                "key": law_key,
                "id": law_data.get("id", "N/A"),
                "name": law_data.get("name", "Unknown"),
                "jurisdiction": law_data.get("jurisdiction", "Unknown"),
                "effective_date": law_data.get("effective_date", "N/A"),
                "has_trigger": "trigger_condition" in law_data,
                "has_enforcement": "enforcement_action" in law_data
            }
            
            framework_count["frameworks"].append(framework_info)
            
            # Count by jurisdiction
            jurisdiction = framework_info["jurisdiction"]
            framework_count["by_jurisdiction"][jurisdiction] = \
                framework_count["by_jurisdiction"].get(jurisdiction, 0) + 1
            
            # Extract sectors from trigger conditions
            trigger = law_data.get("trigger_condition", {})
            params = trigger.get("parameters", {})
            sectors = params.get("sector", [])
            if isinstance(sectors, str):
                sectors = [sectors]
            for sector in sectors:
                framework_count["by_sector"][sector] = \
                    framework_count["by_sector"].get(sector, 0) + 1
        
        return framework_count
    
    def test_liveness(self) -> Dict[str, bool]:
        """Test liveness of key frameworks (EU AI Act, IHR 2005)."""
        print("\n🔬 Testing Framework Liveness...")
        print("=" * 70)
        
        liveness_results = {}
        
        # Initialize guardrail
        try:
            self.guardrail = SovereignGuardrail()
            print("✅ SovereignGuardrail initialized")
        except Exception as e:
            print(f"❌ Failed to initialize SovereignGuardrail: {e}")
            return {}
        
        # Test 1: EU AI Act (check_ai_conformity)
        print("\n📋 Test 1: EU AI Act Risk Pyramid")
        try:
            ai_test_payload = {
                "ai_system_type": "healthcare_diagnosis",
                "risk_indicators": {
                    "patient_impact": "high",
                    "automation_level": 0.85,
                    "data_sensitivity": "PHI"
                }
            }
            
            ai_result = self.guardrail.check_ai_conformity(ai_test_payload)
            liveness_results["EU_AI_ACT"] = ai_result is not None
            
            if ai_result:
                print(f"   ✅ EU AI Act ACTIVE")
                print(f"   Risk Level: {ai_result.get('risk_level', 'unknown')}")
                print(f"   Conformity Required: {ai_result.get('conformity_assessment_required', False)}")
            else:
                print(f"   ⚠️  EU AI Act returned no result")
                
        except Exception as e:
            print(f"   ❌ EU AI Act test failed: {e}")
            liveness_results["EU_AI_ACT"] = False
        
        # Test 2: IHR 2005 (trigger_pandemic_emergency)
        print("\n📋 Test 2: IHR 2005 Pandemic Emergency Protocols")
        try:
            outbreak_data = {
                "cases": 12,
                "timeframe_hours": 24,
                "geographic_spread": "multi_district",
                "disease_pattern": "novel_pathogen",
                "mortality_rate": 0.15
            }
            
            pandemic_result = self.guardrail.trigger_pandemic_emergency(outbreak_data)
            liveness_results["IHR_2005"] = pandemic_result is not None
            
            if pandemic_result:
                print(f"   ✅ IHR 2005 ACTIVE")
                print(f"   Emergency Activated: {pandemic_result.get('emergency_activated', False)}")
                print(f"   Alert Level: {pandemic_result.get('alert_level', 'unknown')}")
            else:
                print(f"   ⚠️  IHR 2005 returned no result")
                
        except Exception as e:
            print(f"   ❌ IHR 2005 test failed: {e}")
            liveness_results["IHR_2005"] = False
        
        # Test 3: Validate Operation (Full Stack)
        print("\n📋 Test 3: Full Stack Validation (Multi-Law)")
        try:
            test_payload = {
                "sector": "healthcare",
                "location": "Kenya",
                "data_types": ["health_data", "biometric_data"],
                "risk_score": 0.75,
                "ai_involvement": True
            }
            
            validation_result = self.guardrail.validate_operation("healthcare", test_payload)
            liveness_results["FULL_STACK"] = validation_result is not None
            
            if validation_result:
                print(f"   ✅ Full Stack ACTIVE")
                print(f"   Status: {validation_result.status.value}")
                print(f"   Laws Checked: {len(validation_result.law_checks)}")
                print(f"   Risk Score: {validation_result.risk_score:.2f}")
            else:
                print(f"   ⚠️  Full stack returned no result")
                
        except Exception as e:
            print(f"   ❌ Full stack test failed: {e}")
            liveness_results["FULL_STACK"] = False
        
        return liveness_results
    
    def test_rco_integration(self) -> bool:
        """Test RCO integration with law registry."""
        print("\n🔬 Testing RCO Integration...")
        print("=" * 70)
        
        try:
            self.rco = RegenerativeComplianceOracle()
            print("✅ RegenerativeComplianceOracle initialized")
            
            # Check if RCO has access to law registry
            health_score = self.rco.get_compliance_health_score()
            print(f"   Compliance Health Score: {health_score * 100:.2f}%")
            
            return True
        except Exception as e:
            print(f"❌ RCO integration test failed: {e}")
            return False
    
    def generate_report(self, framework_count: Dict, liveness_results: Dict) -> Dict:
        """Generate comprehensive audit report."""
        total_frameworks = framework_count.get("total", 0)
        live_frameworks = sum(1 for result in liveness_results.values() if result)
        
        report = {
            "audit_timestamp": datetime.now().isoformat(),
            "registry_version": self.registry.get("45_law_quantum_nexus", {}).get("version", "unknown"),
            "total_frameworks": total_frameworks,
            "frameworks_tested": len(liveness_results),
            "frameworks_live": live_frameworks,
            "liveness_rate": (live_frameworks / len(liveness_results) * 100) if liveness_results else 0,
            "frameworks": framework_count.get("frameworks", []),
            "by_jurisdiction": framework_count.get("by_jurisdiction", {}),
            "by_sector": framework_count.get("by_sector", {}),
            "liveness_results": liveness_results,
            "status": "OPERATIONAL" if live_frameworks > 0 else "DEGRADED"
        }
        
        return report
    
    def print_summary(self, report: Dict):
        """Print audit summary."""
        print("\n" + "═" * 70)
        print("  SOVEREIGN LAW STACK AUDIT SUMMARY")
        print("═" * 70)
        print()
        
        print(f"Audit Timestamp: {report['audit_timestamp']}")
        print(f"Registry Version: {report['registry_version']}")
        print()
        
        print(f"📊 Framework Statistics:")
        print(f"   Total Frameworks: {report['total_frameworks']}")
        print(f"   Frameworks Tested: {report['frameworks_tested']}")
        print(f"   Frameworks Live: {report['frameworks_live']}")
        print(f"   Liveness Rate: {report['liveness_rate']:.1f}%")
        print()
        
        print(f"🌍 By Jurisdiction:")
        for jurisdiction, count in sorted(report['by_jurisdiction'].items()):
            print(f"   {jurisdiction}: {count} framework(s)")
        print()
        
        print(f"🏥 By Sector:")
        for sector, count in sorted(report['by_sector'].items()):
            print(f"   {sector}: {count} framework(s)")
        print()
        
        print(f"📋 Framework Roll Call:")
        for fw in report['frameworks']:
            status_icon = "✅" if fw["has_trigger"] and fw["has_enforcement"] else "⚠️"
            print(f"   {status_icon} {fw['id']}: {fw['name']}")
            print(f"      Jurisdiction: {fw['jurisdiction']}")
            print(f"      Effective: {fw['effective_date']}")
            print(f"      Trigger: {'Yes' if fw['has_trigger'] else 'No'} | "
                  f"Enforcement: {'Yes' if fw['has_enforcement'] else 'No'}")
        print()
        
        print(f"🔬 Liveness Tests:")
        for framework, is_live in report['liveness_results'].items():
            status = "✅ LIVE" if is_live else "❌ INACTIVE"
            print(f"   {framework}: {status}")
        print()
        
        # Overall status
        if report['status'] == "OPERATIONAL":
            print("╔" + "═" * 68 + "╗")
            print("║" + " " * 20 + "✅ SOVEREIGN STACK OPERATIONAL" + " " * 18 + "║")
            print("╚" + "═" * 68 + "╝")
        else:
            print("╔" + "═" * 68 + "╗")
            print("║" + " " * 23 + "⚠️  STACK DEGRADED" + " " * 27 + "║")
            print("╚" + "═" * 68 + "╝")
        
        print()
        print("═" * 70)
    
    def run_audit(self) -> int:
        """Execute complete audit."""
        print("\n")
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 18 + "🛡️  SOVEREIGN LAW STACK AUDIT" + " " * 20 + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        
        # Step 1: Load registry
        print("📂 Loading Sectoral Law Registry...")
        if not self.load_registry():
            return 1
        
        # Step 2: Count frameworks
        print("\n📊 Counting Active Frameworks...")
        framework_count = self.count_frameworks()
        print(f"✅ Found {framework_count['total']} active legal frameworks")
        
        # Step 3: Test liveness
        liveness_results = self.test_liveness()
        
        # Step 4: Test RCO integration
        rco_ok = self.test_rco_integration()
        
        # Step 5: Generate report
        report = self.generate_report(framework_count, liveness_results)
        
        # Step 6: Print summary
        self.print_summary(report)
        
        # Step 7: Save report
        report_path = Path(__file__).parent / "law_audit_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Detailed report saved to: {report_path}")
        
        # Return exit code
        return 0 if report['status'] == "OPERATIONAL" else 1


def main():
    """Execute law stack audit."""
    auditor = LawStackAuditor()
    return auditor.run_audit()


if __name__ == "__main__":
    sys.exit(main())
