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
Example Usage: Ethical Engine and Humanitarian Margin Calculator
═════════════════════════════════════════════════════════════════════════════

Demonstrates the use of the EthicalEngine class for validating humanitarian
constraints on health system actions.
"""

from governance_kernel.ethical_engine import EthicalEngine, HumanitarianViolationError


def example_conflict_zone_response():
    """Example: Medical response in a conflict zone."""
    print("=" * 80)
    print("Example 1: Medical Response in Conflict Zone")
    print("=" * 80)
    
    engine = EthicalEngine(use_cloud_secrets=False)
    
    action = {
        'type': 'field_hospital',
        'scope': 'conflict_zone',
        'estimated_civilian_impact': 0.5,
        'medical_benefit': 0.95
    }
    
    context = {
        'conflict_zone': True,
        'outbreak_suspected': False,
        'civilian_population': 50000,
        'healthcare_capacity': 0.3  # Collapsed infrastructure
    }
    
    try:
        result = engine.apply_constraints(action, context)
        
        print(f"\n✅ Action Approved")
        print(f"   Constraints Applied: {', '.join(result['constraints_applied'])}")
        print(f"   Humanitarian Margin: {result['humanitarian_margin']['margin']:.2%}")
        print(f"   Interpretation: {result['humanitarian_margin']['interpretation']}")
        print(f"\n   Civilian Protection Measures:")
        for measure in result['action'].get('civilian_protection_measures', []):
            print(f"   - {measure}")
        
    except HumanitarianViolationError as e:
        print(f"\n❌ Action Rejected: {e}")


def example_outbreak_response():
    """Example: Cholera outbreak response in refugee camp."""
    print("\n" + "=" * 80)
    print("Example 2: Cholera Outbreak Response in Dadaab Refugee Camp")
    print("=" * 80)
    
    engine = EthicalEngine(use_cloud_secrets=False)
    
    action = {
        'type': 'cholera_response',
        'scope': 'refugee_camp',
        'estimated_civilian_impact': 0.3,
        'medical_benefit': 0.85,
        'attack_rate': 0.4,  # 4% attack rate
        'r_effective': 2.8,   # Rapid spread
        'severity_score': 0.75
    }
    
    context = {
        'conflict_zone': False,
        'outbreak_suspected': True,
        'civilian_population': 200000,
        'healthcare_capacity': 0.5  # Limited capacity
    }
    
    try:
        result = engine.apply_constraints(action, context)
        
        print(f"\n✅ Action Approved")
        print(f"   Constraints Applied: {', '.join(result['constraints_applied'])}")
        print(f"   Humanitarian Margin: {result['humanitarian_margin']['margin']:.2%}")
        print(f"   Interpretation: {result['humanitarian_margin']['interpretation']}")
        
        print(f"\n   Duration: {result['action']['duration_days']} days")
        print(f"   Review Required: {result['action']['review_required']}")
        print(f"   Review Interval: {result['action']['review_interval_days']} days")
        
        print(f"\n   Alternatives Considered:")
        for alt in result['action'].get('alternatives_considered', []):
            print(f"   - {alt}")
        
    except HumanitarianViolationError as e:
        print(f"\n❌ Action Rejected: {e}")


def example_disproportionate_action():
    """Example: Disproportionate action that violates Geneva Convention."""
    print("\n" + "=" * 80)
    print("Example 3: Disproportionate Action (Should be Rejected)")
    print("=" * 80)
    
    engine = EthicalEngine(use_cloud_secrets=False)
    
    action = {
        'type': 'forced_relocation',
        'scope': 'entire_city',
        'estimated_civilian_impact': 0.9,  # Very high harm
        'medical_benefit': 0.1  # Low benefit
    }
    
    context = {
        'conflict_zone': True,
        'healthcare_capacity': 0.5
    }
    
    try:
        result = engine.apply_constraints(action, context)
        print(f"\n✅ Action Approved (unexpected)")
        
    except HumanitarianViolationError as e:
        print(f"\n❌ Action Rejected (as expected)")
        print(f"   Reason: {str(e)[:200]}...")


def example_combined_crisis():
    """Example: Combined conflict zone + outbreak scenario."""
    print("\n" + "=" * 80)
    print("Example 4: Combined Crisis (Conflict Zone + Outbreak)")
    print("=" * 80)
    
    engine = EthicalEngine(use_cloud_secrets=False)
    
    action = {
        'type': 'emergency_response',
        'scope': 'regional',
        'estimated_civilian_impact': 0.15,
        'medical_benefit': 0.85,
        'attack_rate': 0.3,
        'r_effective': 1.8,
        'severity_score': 0.8
    }
    
    context = {
        'conflict_zone': True,
        'outbreak_suspected': True,
        'civilian_population': 50000,
        'healthcare_capacity': 0.4
    }
    
    try:
        result = engine.apply_constraints(action, context)
        
        print(f"\n✅ Action Approved")
        print(f"   Constraints Applied: {len(result['constraints_applied'])} constraints")
        for constraint in result['constraints_applied']:
            print(f"   - {constraint}")
        
        print(f"\n   Humanitarian Margin Analysis:")
        margin = result['humanitarian_margin']
        print(f"   - Base Margin: {margin['base']:.2%}")
        print(f"   - Final Margin: {margin['margin']:.2%}")
        print(f"   - Multipliers Applied:")
        for mult in margin['multipliers']:
            print(f"     • {mult}")
        print(f"   - Interpretation: {margin['interpretation']}")
        
    except HumanitarianViolationError as e:
        print(f"\n❌ Action Rejected: {e}")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "ETHICAL ENGINE - HUMANITARIAN MARGIN CALCULATOR" + " " * 16 + "║")
    print("╚" + "=" * 78 + "╝")
    
    example_conflict_zone_response()
    example_outbreak_response()
    example_disproportionate_action()
    example_combined_crisis()
    
    print("\n" + "=" * 80)
    print("Examples Complete")
    print("=" * 80)
    print("\nFor more information, see:")
    print("- Geneva Convention Article 3: https://www.icrc.org/en/doc/resources/documents/article/other/armed-conflict-article-170308.htm")
    print("- WHO IHR (2005): https://www.who.int/publications/i/item/9789241580496")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
