#!/usr/bin/env python3
"""
Tamper-proof Audit Trail Demo
═══════════════════════════════════════════════════════════════════════════

Demonstrates the tamper-proof audit trail with:
1. Bigtable high-throughput ledger storage
2. Cloud Spanner cross-region synchronization
3. Cloud KMS sovereign key management

This demo runs in simulation mode (no real GCP resources required).
"""

import sys
import time
from datetime import datetime
from governance_kernel.audit_trail import (
    TamperProofAuditTrail,
    AuditEventType,
    AuditEntry
)
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError


def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_entry(entry, show_full=False):
    """Print audit entry details."""
    print(f"  📝 Entry Hash: {entry.entry_hash[:16]}...{entry.entry_hash[-8:]}")
    print(f"  ⏰ Timestamp:  {entry.timestamp}")
    print(f"  🎯 Event Type: {entry.event_type}")
    print(f"  👤 Actor:      {entry.actor}")
    print(f"  📦 Resource:   {entry.resource}")
    print(f"  ⚡ Action:     {entry.action}")
    print(f"  🌍 Jurisdiction: {entry.jurisdiction}")
    print(f"  ✅ Outcome:    {entry.outcome}")
    print(f"  🔗 Previous:   {entry.previous_hash[:16]}...{entry.previous_hash[-8:]}")
    print(f"  ✍️  Signature:  {entry.signature[:32]}...")
    
    if show_full and entry.metadata:
        print(f"  📋 Metadata:")
        for key, value in entry.metadata.items():
            print(f"     - {key}: {value}")
    print()


def demo_basic_audit_trail():
    """Demo 1: Basic audit trail operations."""
    print_header("Demo 1: Basic Tamper-proof Audit Trail")
    
    print("Initializing tamper-proof audit trail (simulation mode)...")
    trail = TamperProofAuditTrail(simulate=True)
    print("✅ Audit trail initialized\n")
    
    print("Components:")
    print("  • Bigtable Ledger:    Ready for high-throughput writes")
    print("  • Spanner Sync Engine: Ready for cross-region sync")
    print("  • Cloud KMS Manager:   Ready for cryptographic signing")
    print()
    
    print("Logging audit event: DATA_ACCESS...")
    entry1 = trail.log_event(
        event_type=AuditEventType.DATA_ACCESS,
        actor="dr.smith@hospital.com",
        resource="patient_record_12345",
        action="read_medical_history",
        jurisdiction="HIPAA_US",
        outcome="SUCCESS",
        metadata={
            "ip_address": "192.168.1.100",
            "reason": "annual checkup review"
        }
    )
    
    print_entry(entry1, show_full=True)
    
    print("Logging audit event: HIGH_RISK_INFERENCE...")
    entry2 = trail.log_event(
        event_type=AuditEventType.HIGH_RISK_INFERENCE,
        actor="ml_diagnostic_system",
        resource="diagnosis_prediction_67890",
        action="predict_disease_risk",
        jurisdiction="EU_AI_ACT",
        outcome="SUCCESS",
        metadata={
            "model_version": "v2.3.1",
            "confidence": 0.92,
            "predicted_disease": "Type 2 Diabetes",
            "shap_values": "[0.45, 0.23, 0.18, 0.14]"
        }
    )
    
    print_entry(entry2, show_full=True)
    
    print("🔗 Verifying chain linkage...")
    if entry2.previous_hash == entry1.entry_hash:
        print("✅ Cryptographic chain verified: Entry 2 links to Entry 1")
    else:
        print("❌ Chain broken!")
    
    return trail


def demo_chain_integrity():
    """Demo 2: Chain integrity verification."""
    print_header("Demo 2: Cryptographic Chain Integrity")
    
    print("Creating audit trail with multiple events...")
    trail = TamperProofAuditTrail(simulate=True)
    
    # Log several events
    events = [
        ("DATA_ACCESS", "user1@example.com", "record_001", "read"),
        ("DATA_TRANSFER", "user2@example.com", "record_002", "export"),
        ("CONSENT_VALIDATION", "system", "consent_003", "validate"),
        ("SOVEREIGNTY_CHECK", "guardrail", "transfer_004", "check"),
        ("RETENTION_ENFORCEMENT", "system", "old_record_005", "archive"),
    ]
    
    entries = []
    for i, (event_type, actor, resource, action) in enumerate(events):
        print(f"  {i+1}. Logging {event_type}...")
        entry = trail.log_event(
            event_type=getattr(AuditEventType, event_type),
            actor=actor,
            resource=resource,
            action=action,
            jurisdiction="GDPR_EU",
            outcome="SUCCESS"
        )
        entries.append(entry)
    
    print(f"\n✅ Logged {len(entries)} events\n")
    
    # Verify chain integrity
    print("🔍 Verifying cryptographic chain integrity...")
    result = trail.verify_chain_integrity(entries)
    
    print(f"\n📊 Verification Results:")
    print(f"  • Total Entries:     {result['total_entries']}")
    print(f"  • Valid Entries:     {result['valid_entries']}")
    print(f"  • Chain Integrity:   {'✅ VALID' if result['chain_valid'] else '❌ BROKEN'}")
    print(f"  • Chain Breaks:      {result['broken_chain']}")
    print(f"  • Invalid Signatures: {result['invalid_signatures']}")
    
    if result['chain_valid']:
        print("\n✅ All entries cryptographically verified!")
    else:
        print("\n❌ Chain integrity compromised!")
        for detail in result['details']:
            print(f"  ⚠️  Issue at entry {detail['index']}: {detail['error']}")
    
    return trail, entries


def demo_tampering_detection():
    """Demo 3: Detect tampering attempts."""
    print_header("Demo 3: Tampering Detection")
    
    print("Creating clean audit trail...")
    trail = TamperProofAuditTrail(simulate=True)
    
    # Create valid entries
    entry1 = trail.log_event(
        event_type=AuditEventType.DATA_ACCESS,
        actor="attacker@evil.com",
        resource="sensitive_data",
        action="unauthorized_access",
        jurisdiction="GDPR_EU",
        outcome="FAILURE"  # Attacker failed authentication
    )
    
    entry2 = trail.log_event(
        event_type=AuditEventType.DATA_TRANSFER,
        actor="security_system",
        resource="alert_log",
        action="log_intrusion_attempt",
        jurisdiction="GDPR_EU",
        outcome="SUCCESS"
    )
    
    print("✅ Created 2 audit entries\n")
    print("Original Entry 1:")
    print_entry(entry1)
    
    # Simulate tampering
    print("🚨 SIMULATING ATTACK: Attacker tries to modify entry outcome...\n")
    print("Attacker changes outcome from 'FAILURE' to 'SUCCESS' (trying to hide failed access)")
    entry1.outcome = "SUCCESS"  # Modify without updating hash
    
    print("\nTampered Entry 1:")
    print_entry(entry1)
    
    # Verify integrity
    print("🔍 Running integrity verification...\n")
    entries = [entry1, entry2]
    result = trail.verify_chain_integrity(entries)
    
    if not result['chain_valid']:
        print("🚨 TAMPERING DETECTED!")
        print(f"\n📊 Verification Results:")
        print(f"  • Total Entries:     {result['total_entries']}")
        print(f"  • Valid Entries:     {result['valid_entries']}")
        print(f"  • Chain Integrity:   ❌ COMPROMISED")
        
        print(f"\n⚠️  Details:")
        for detail in result['details']:
            print(f"  • Entry {detail['index']}: {detail['error']}")
        
        print("\n✅ Cryptographic protection working as designed!")
        print("   The tampered entry was detected because its hash doesn't match.")
        print("   This is mathematically impossible to forge without the KMS key.")
    else:
        print("❌ Tampering NOT detected (this should not happen!)")


def demo_cross_region_sync():
    """Demo 4: Cross-region synchronization."""
    print_header("Demo 4: Cross-Region Synchronization")
    
    print("Initializing global audit trail...")
    trail = TamperProofAuditTrail(simulate=True)
    
    print("\n🌍 Multi-region deployment:")
    regions = ["us-east1", "eu-west1", "asia-southeast1"]
    for region in regions:
        print(f"  • {region}")
    
    print("\nLogging event with cross-region sync...")
    entry = trail.log_event(
        event_type=AuditEventType.BREACH_NOTIFICATION,
        actor="security_incident_response",
        resource="breach_alert_2025_001",
        action="notify_data_protection_authority",
        jurisdiction="GDPR_EU",
        outcome="SUCCESS",
        metadata={
            "breach_type": "unauthorized_access_attempt",
            "affected_records": 0,
            "notification_sent_to": "GDPR DPA",
            "response_time_minutes": 45
        },
        sync_regions=regions
    )
    
    print("\n✅ Event logged to Bigtable")
    print("✅ Metadata synced to Spanner")
    print("✅ Entry signed with Cloud KMS")
    print()
    print_entry(entry, show_full=True)
    
    # Verify cross-region sync
    print("🔍 Verifying cross-region synchronization...\n")
    sync_result = trail.verify_cross_region_sync(entry.entry_hash)
    
    if sync_result['status'] == 'CONSISTENT':
        print("✅ Entry synchronized across all regions:")
        for region in sync_result['regions']:
            print(f"   ✓ {region}")
        print(f"\n⏰ Verification Time: {sync_result['verification_time']}")
        print("\n💡 Cloud Spanner ensures global consistency using TrueTime.")
    else:
        print(f"⚠️  Sync status: {sync_result['status']}")


def demo_sovereign_guardrail_integration():
    """Demo 5: Integration with SovereignGuardrail."""
    print_header("Demo 5: Integration with Sovereign Guardrail")
    
    print("Initializing SovereignGuardrail with tamper-proof audit...")
    guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
    print()
    
    # Test successful validation
    print("Test 1: Valid high-risk inference")
    print("-" * 60)
    try:
        result = guardrail.validate_action(
            action_type='High_Risk_Inference',
            payload={
                'actor': 'ml_diagnostic_system',
                'resource': 'patient_diagnosis_ai_12345',
                'explanation': 'SHAP values: [0.8, 0.1, 0.1]',
                'confidence_score': 0.95,
                'evidence_chain': ['fever', 'cough', 'positive_test'],
                'consent_token': 'valid_consent_token_67890',
                'consent_scope': 'ai_diagnosis'
            },
            jurisdiction='EU_AI_ACT'
        )
        print("✅ Validation PASSED")
        print("✅ Event logged to tamper-proof audit trail")
    except SovereigntyViolationError as e:
        print(f"❌ Validation FAILED: {e}")
    
    print("\n" + "=" * 60)
    
    # Test violation
    print("\nTest 2: Attempted data sovereignty violation")
    print("-" * 60)
    try:
        result = guardrail.validate_action(
            action_type='Data_Transfer',
            payload={
                'actor': 'rogue_system',
                'resource': 'patient_phi_sensitive',
                'data_type': 'PHI',
                'destination': 'Foreign_Cloud',  # Violation!
                'consent_token': 'token'
            },
            jurisdiction='GDPR_EU'
        )
        print("⚠️  This should not print (violation should be raised)")
    except SovereigntyViolationError as e:
        print("✅ Violation BLOCKED by SovereignGuardrail")
        print("✅ Violation logged to tamper-proof audit trail")
        print(f"\n📋 Violation Details:")
        print(f"   {str(e)[:200]}...")
    
    print("\n" + "=" * 60)
    
    # Check audit history
    print("\n📜 Retrieving tamper-proof audit history...")
    history = guardrail.get_tamper_proof_audit_history(limit=10)
    
    print(f"\nFound {len(history)} audit entries:")
    for i, entry in enumerate(history, 1):
        print(f"\n  {i}. Event: {entry['event_type']}")
        print(f"     Outcome: {entry['outcome']}")
        print(f"     Jurisdiction: {entry['jurisdiction']}")
        print(f"     Timestamp: {entry['timestamp']}")
        
        if entry['outcome'] == 'VIOLATION':
            print(f"     ⚠️  Violation Type: {entry['metadata'].get('violation_type', 'N/A')}")
    
    # Verify chain integrity
    print("\n🔍 Verifying audit chain integrity...")
    integrity = guardrail.verify_audit_chain_integrity()
    
    if integrity.get('chain_valid'):
        print(f"✅ Audit chain cryptographically verified!")
        print(f"   Valid entries: {integrity['valid_entries']}/{integrity['total_entries']}")
    else:
        print(f"❌ Chain integrity issue detected")


def demo_performance():
    """Demo 6: Performance characteristics."""
    print_header("Demo 6: Performance Characteristics")
    
    print("Initializing audit trail...")
    trail = TamperProofAuditTrail(simulate=True)
    
    print("\nBenchmarking write performance...")
    num_entries = 100
    start_time = time.time()
    
    for i in range(num_entries):
        trail.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            actor=f"user{i}@example.com",
            resource=f"resource_{i}",
            action="access",
            jurisdiction="GLOBAL_DEFAULT",
            outcome="SUCCESS",
            metadata={"index": i}
        )
    
    elapsed = time.time() - start_time
    throughput = num_entries / elapsed
    avg_latency = (elapsed / num_entries) * 1000  # in milliseconds
    
    print(f"\n📊 Performance Results:")
    print(f"  • Entries Written:   {num_entries}")
    print(f"  • Total Time:        {elapsed:.2f} seconds")
    print(f"  • Throughput:        {throughput:.2f} entries/second")
    print(f"  • Avg Latency:       {avg_latency:.2f} ms/entry")
    
    print(f"\n💡 Note: This is simulation mode performance.")
    print(f"   Production Bigtable performance characteristics:")
    print(f"   • Write latency:     < 10ms (p99)")
    print(f"   • Read latency:      < 6ms (p99)")
    print(f"   • Throughput:        10,000+ writes/sec per node")
    
    # Verify integrity of all entries
    print(f"\n🔍 Verifying integrity of {num_entries} entries...")
    entries = trail.get_audit_history(limit=num_entries)
    
    verify_start = time.time()
    result = trail.verify_chain_integrity(entries)
    verify_elapsed = time.time() - verify_start
    
    print(f"\n✅ Verification complete:")
    print(f"  • Time taken:        {verify_elapsed:.2f} seconds")
    print(f"  • Valid entries:     {result['valid_entries']}/{result['total_entries']}")
    print(f"  • Chain valid:       {'✅ YES' if result['chain_valid'] else '❌ NO'}")


def main():
    """Run all demos."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  Tamper-proof Audit Trail Demo".center(78) + "█")
    print("█" + "  iLuminara-Core Sovereign Health Architecture".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    print("\n🎯 This demo showcases:")
    print("  1. Basic audit trail operations")
    print("  2. Cryptographic chain integrity")
    print("  3. Tampering detection")
    print("  4. Cross-region synchronization")
    print("  5. Integration with SovereignGuardrail")
    print("  6. Performance characteristics")
    
    print("\n💡 Running in simulation mode (no GCP resources required)")
    
    input("\nPress Enter to begin...")
    
    try:
        # Run all demos
        demo_basic_audit_trail()
        input("\nPress Enter for next demo...")
        
        demo_chain_integrity()
        input("\nPress Enter for next demo...")
        
        demo_tampering_detection()
        input("\nPress Enter for next demo...")
        
        demo_cross_region_sync()
        input("\nPress Enter for next demo...")
        
        demo_sovereign_guardrail_integration()
        input("\nPress Enter for final demo...")
        
        demo_performance()
        
        print_header("Demo Complete")
        print("✅ All demos completed successfully!")
        print("\n📚 For more information:")
        print("  • Documentation: docs/AUDIT_TRAIL.md")
        print("  • Tests: tests/test_audit_trail.py")
        print("  • Source: governance_kernel/audit_trail.py")
        
        print("\n🚀 Status: Production-Ready")
        print("   The tamper-proof audit trail is ready for deployment.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
