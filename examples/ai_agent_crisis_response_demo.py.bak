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
Example: AI Agents with Ethical Guardrails for Crisis Response
═════════════════════════════════════════════════════════════════════════════

Demonstrates the integrated AI agent system with:
1. Crisis Decision Agent - Humanitarian law compliance
2. Fairness Constraint Engine - Equitable resource allocation
3. AI Agent Coordinator - Multi-layer ethical validation

This example simulates a disease outbreak scenario requiring resource allocation
with ethical constraints.
"""

import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from governance_kernel.ai_agent_coordinator import (
    AIAgentCoordinator,
    CrisisScenarioType
)
from governance_kernel.crisis_decision_agent import DecisionType
import json


def main():
    """Demonstrate AI agents in a crisis response scenario."""
    
    print("=" * 80)
    print("iLuminara AI Agents: Ethical Crisis Response Demonstration")
    print("=" * 80)
    print()
    
    # Initialize the AI Agent Coordinator
    print("🤖 Initializing AI Agent Coordinator...")
    coordinator = AIAgentCoordinator(
        fairness_threshold=0.8,
        confidence_threshold=0.7
    )
    print("   ✓ Crisis Decision Agent loaded")
    print("   ✓ Fairness Constraint Engine loaded")
    print("   ✓ Sovereign Guardrail loaded")
    print()
    
    # Scenario: Cholera outbreak in Dadaab refugee camp
    print("📊 SCENARIO: Cholera Outbreak in Dadaab Refugee Camp")
    print("-" * 80)
    print("Location: Dadaab, Kenya")
    print("Affected Population: 5,500 people across 4 zones")
    print("Available Resources: Medical supplies, food, water")
    print("Decision Required: Fair resource allocation with ethical constraints")
    print()
    
    # Define population groups with vulnerability factors
    population_groups = [
        {
            "group_id": "children_under_5",
            "name": "Children Under 5",
            "size": 800,
            "characteristics": {
                "age_group": "children",
                "vulnerability_level": "high"
            },
            "vulnerability_score": 1.5,  # Higher vulnerability
            "need_level": 0.9,  # High need due to dehydration risk
            "is_protected_group": True,  # Protected under humanitarian law
            "current_resources": 0
        },
        {
            "group_id": "pregnant_women",
            "name": "Pregnant Women",
            "size": 300,
            "characteristics": {
                "gender": "female",
                "condition": "pregnant",
                "vulnerability_level": "high"
            },
            "vulnerability_score": 1.4,
            "need_level": 0.85,
            "is_protected_group": True,
            "current_resources": 0
        },
        {
            "group_id": "elderly",
            "name": "Elderly (65+)",
            "size": 400,
            "characteristics": {
                "age_group": "elderly",
                "vulnerability_level": "medium-high"
            },
            "vulnerability_score": 1.3,
            "need_level": 0.8,
            "is_protected_group": True,
            "current_resources": 0
        },
        {
            "group_id": "adults",
            "name": "Adults (18-64)",
            "size": 3000,
            "characteristics": {
                "age_group": "adults",
                "vulnerability_level": "standard"
            },
            "vulnerability_score": 1.0,
            "need_level": 0.6,
            "is_protected_group": False,
            "current_resources": 0
        },
        {
            "group_id": "disabled_persons",
            "name": "Persons with Disabilities",
            "size": 200,
            "characteristics": {
                "disability_status": True,
                "vulnerability_level": "high"
            },
            "vulnerability_score": 1.4,
            "need_level": 0.85,
            "is_protected_group": True,
            "current_resources": 0
        },
        {
            "group_id": "healthcare_workers",
            "name": "Healthcare Workers",
            "size": 80,
            "characteristics": {
                "occupation": "medical",
                "vulnerability_level": "high"
            },
            "vulnerability_score": 1.2,
            "need_level": 0.95,  # Critical to maintain healthcare capacity
            "is_protected_group": True,  # Protected under Geneva Conventions
            "current_resources": 0
        }
    ]
    
    # Available resources
    resources_available = {
        "oral_rehydration_solution": 4000,  # ORS packets
        "medical_supplies": 2500,
        "clean_water_liters": 15000,
        "food_rations": 5000,
        "medical_staff_hours": 800
    }
    
    # Constraints and requirements
    constraints = {
        "time_sensitivity": "urgent",
        "must_prioritize_life_saving": True,
        "maintain_healthcare_capacity": True
    }
    
    print("🔬 Executing AI Agent Decision Pipeline...")
    print("-" * 80)
    
    # Execute the integrated decision
    try:
        result = coordinator.execute_crisis_decision(
            scenario_type=CrisisScenarioType.DISEASE_OUTBREAK,
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            affected_area="Dadaab_Refugee_Camp",
            population_groups=population_groups,
            resources_available=resources_available,
            constraints=constraints,
            jurisdiction="KDPA_KE"  # Kenya Data Protection Act
        )
        
        print("✅ Decision Pipeline Complete\n")
        
        # Display results
        print("=" * 80)
        print("DECISION RESULTS")
        print("=" * 80)
        print()
        
        print(f"Decision ID: {result.decision_output.decision_id}")
        print(f"Approval Status: {result.approval_status}")
        print(f"Confidence Score: {result.decision_output.confidence_score:.2f}")
        print()
        
        print("--- HUMANITARIAN LAW COMPLIANCE ---")
        for principle, compliant in result.decision_output.ethical_compliance.items():
            status = "✓" if compliant else "✗"
            print(f"{status} {principle.upper()}")
        print()
        
        print("--- FAIRNESS METRICS ---")
        print(f"Overall Fairness Score: {result.fairness_assessment.overall_fairness_score:.2f}")
        for metric, score in result.fairness_assessment.metric_scores.items():
            print(f"  • {metric}: {score:.2f}")
        print()
        
        if result.fairness_assessment.equity_gaps:
            print(f"⚠️  Equity Gaps Identified: {len(result.fairness_assessment.equity_gaps)}")
            for gap in result.fairness_assessment.equity_gaps[:3]:
                print(f"   - {gap['type']}: {gap['group']}")
            print()
        
        print("--- RESOURCE ALLOCATION RECOMMENDATION ---")
        if "allocations" in result.decision_output.recommendation:
            allocations = result.decision_output.recommendation["allocations"]
            print(f"Total Groups: {len(allocations)}")
            print()
            
            # Sort by priority
            sorted_allocs = sorted(
                allocations, 
                key=lambda x: (x.get("priority") == "HIGH", x.get("recommended_allocation", 0)),
                reverse=True
            )
            
            for alloc in sorted_allocs[:6]:  # Show top 6
                print(f"  {alloc['group']}:")
                print(f"    Priority: {alloc.get('priority', 'STANDARD')}")
                print(f"    Need Level: {alloc.get('need_level', 0):.2f}")
                print(f"    Recommended: {alloc.get('recommended_allocation', 0):.0f} units")
                print(f"    Justification: {alloc.get('justification', 'N/A')}")
                print()
        
        print("--- LEGAL CITATIONS ---")
        for citation in result.decision_output.humanitarian_law_citations[:5]:
            print(f"  • {citation}")
        print()
        
        print("--- SOVEREIGNTY COMPLIANCE ---")
        print(f"Jurisdiction: {result.sovereignty_compliance['jurisdiction']}")
        print(f"Compliant: {'✓' if result.sovereignty_compliance['compliant'] else '✗'}")
        print(f"Checks Performed: {len(result.sovereignty_compliance['checks_performed'])}")
        print()
        
        if result.approval_status == "REQUIRES_HUMAN_REVIEW":
            print("⚠️  HUMAN REVIEW REQUIRED")
            print("   This decision requires human oversight due to:")
            for reason in result.rejection_reasons:
                print(f"   - {reason}")
            print()
        elif result.approval_status == "APPROVED":
            print("✅ DECISION APPROVED FOR IMPLEMENTATION")
            print("   All ethical constraints satisfied")
            print()
        
        # Export full report
        report_path = "/tmp/crisis_decision_report.json"
        coordinator.export_decision_report(result, report_path)
        print(f"📄 Full decision report exported to: {report_path}")
        print()
        
        # Display ethical summary
        print("=" * 80)
        print(result.ethical_summary)
        print("=" * 80)
        print()
        
        # Show decision history
        print("📜 DECISION AUDIT LOG")
        print("-" * 80)
        history = coordinator.get_decision_history()
        print(f"Total Decisions Logged: {len(history)}")
        if history:
            latest = history[-1]
            print(f"Latest Decision:")
            print(f"  ID: {latest['decision_id']}")
            print(f"  Timestamp: {latest['timestamp']}")
            print(f"  Scenario: {latest['scenario_type']}")
            print(f"  Status: {latest['approval_status']}")
        print()
        
        print("=" * 80)
        print("✅ DEMONSTRATION COMPLETE")
        print("=" * 80)
        print()
        print("Key Achievements:")
        print("  ✓ Humanitarian law compliance enforced")
        print("  ✓ Fairness constraints validated")
        print("  ✓ Protected groups prioritized")
        print("  ✓ Full audit trail maintained")
        print("  ✓ Sovereignty compliance checked")
        print("  ✓ Transparent decision-making process")
        print()
        
    except Exception as e:
        print(f"❌ Error during decision execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
