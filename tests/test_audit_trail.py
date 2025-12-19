"""
Tests for Tamper-proof Audit Trail
════════════════════════════════════════════════════════════════════════════

Tests the complete audit trail system including:
- BigtableLedger: High-throughput storage
- SpannerSyncEngine: Cross-region synchronization
- CloudKMSManager: Cryptographic signing
- TamperProofAuditTrail: End-to-end integration
"""

import pytest
from datetime import datetime
from governance_kernel.audit_trail import (
    AuditEntry,
    AuditEventType,
    BigtableLedger,
    SpannerSyncEngine,
    CloudKMSManager,
    TamperProofAuditTrail
)


class TestAuditEntry:
    """Test AuditEntry creation and integrity."""
    
    def test_audit_entry_creation(self):
        """Test basic audit entry creation."""
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type=AuditEventType.SOVEREIGNTY_CHECK.value,
            actor="user@example.com",
            resource="patient_record_12345",
            action="validate_sovereignty",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            metadata={"reason": "data transfer validation"},
            previous_hash="0" * 64
        )
        
        assert entry.timestamp == "2025-01-15T10:00:00Z"
        assert entry.event_type == "sovereignty_check"
        assert entry.actor == "user@example.com"
        assert len(entry.entry_hash) == 64  # SHA-256 produces 64 hex chars
        assert entry.entry_hash != ""
    
    def test_audit_entry_hash_computation(self):
        """Test that hash is computed correctly."""
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GLOBAL_DEFAULT",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        # Verify hash is deterministic
        hash1 = entry._compute_hash()
        hash2 = entry._compute_hash()
        assert hash1 == hash2
        assert hash1 == entry.entry_hash
    
    def test_audit_entry_integrity_verification(self):
        """Test integrity verification."""
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GLOBAL_DEFAULT",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        # Should pass integrity check
        assert entry.verify_integrity() is True
        
        # Tamper with entry
        original_hash = entry.entry_hash
        entry.outcome = "FAILURE"  # Modify data
        
        # Should fail integrity check (hash doesn't match modified data)
        assert entry.verify_integrity() is False
        
        # Restore and recompute
        entry.outcome = "SUCCESS"
        entry.entry_hash = entry._compute_hash()
        assert entry.verify_integrity() is True
    
    def test_audit_entry_chain_linkage(self):
        """Test that entries link to previous entries."""
        entry1 = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="event1",
            actor="actor1",
            resource="resource1",
            action="action1",
            jurisdiction="GLOBAL_DEFAULT",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        # Second entry links to first
        entry2 = AuditEntry(
            timestamp="2025-01-15T10:01:00Z",
            event_type="event2",
            actor="actor2",
            resource="resource2",
            action="action2",
            jurisdiction="GLOBAL_DEFAULT",
            outcome="SUCCESS",
            metadata={},
            previous_hash=entry1.entry_hash
        )
        
        assert entry2.previous_hash == entry1.entry_hash
        assert entry2.entry_hash != entry1.entry_hash


class TestBigtableLedger:
    """Test Bigtable ledger storage (simulation mode)."""
    
    def test_bigtable_initialization_simulation(self):
        """Test Bigtable initialization in simulation mode."""
        ledger = BigtableLedger(simulate=True)
        assert ledger.simulate is True
        assert len(ledger._simulated_store) == 0
    
    def test_bigtable_write_entry(self):
        """Test writing entries to Bigtable."""
        ledger = BigtableLedger(simulate=True)
        
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GLOBAL_DEFAULT",
            outcome="SUCCESS",
            metadata={"test": "data"},
            previous_hash="0" * 64
        )
        
        result = ledger.write_entry(entry)
        assert result is True
        assert len(ledger._simulated_store) == 1
    
    def test_bigtable_read_entries(self):
        """Test reading entries from Bigtable."""
        ledger = BigtableLedger(simulate=True)
        
        # Write multiple entries
        for i in range(5):
            entry = AuditEntry(
                timestamp=f"2025-01-15T10:0{i}:00Z",
                event_type=f"event_{i}",
                actor="test_actor",
                resource=f"resource_{i}",
                action=f"action_{i}",
                jurisdiction="GLOBAL_DEFAULT",
                outcome="SUCCESS",
                metadata={"index": i},
                previous_hash="0" * 64
            )
            ledger.write_entry(entry)
        
        # Read entries
        entries = ledger.read_entries(limit=10)
        assert len(entries) == 5
        
        # Should be in reverse chronological order (most recent first)
        assert entries[0].metadata["index"] == 4
        assert entries[4].metadata["index"] == 0
    
    def test_bigtable_row_key_generation(self):
        """Test row key generation for time-ordered scanning."""
        ledger = BigtableLedger(simulate=True)
        
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GLOBAL_DEFAULT",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        row_key = ledger._generate_row_key(entry)
        
        # Row key should be string with reversed timestamp
        assert isinstance(row_key, str)
        assert "#" in row_key
        parts = row_key.split("#")
        assert len(parts) == 2
        assert len(parts[0]) == 16  # Reversed timestamp (16 digits)


class TestSpannerSyncEngine:
    """Test Spanner cross-region synchronization (simulation mode)."""
    
    def test_spanner_initialization_simulation(self):
        """Test Spanner initialization in simulation mode."""
        sync_engine = SpannerSyncEngine(simulate=True)
        assert sync_engine.simulate is True
        assert len(sync_engine._simulated_metadata) == 0
    
    def test_spanner_sync_entry_metadata(self):
        """Test syncing entry metadata across regions."""
        sync_engine = SpannerSyncEngine(simulate=True)
        
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        regions = ["us-east1", "eu-west1", "asia-southeast1"]
        result = sync_engine.sync_entry_metadata(entry, regions)
        
        assert result is True
        assert entry.entry_hash in sync_engine._simulated_metadata
        assert sync_engine._simulated_metadata[entry.entry_hash]["sync_regions"] == regions
    
    def test_spanner_verify_cross_region_consistency(self):
        """Test cross-region consistency verification."""
        sync_engine = SpannerSyncEngine(simulate=True)
        
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        regions = ["us-east1", "eu-west1"]
        sync_engine.sync_entry_metadata(entry, regions)
        
        # Verify consistency
        result = sync_engine.verify_cross_region_consistency(entry.entry_hash)
        
        assert result["status"] == "CONSISTENT"
        assert result["regions"] == regions
        assert "verification_time" in result
    
    def test_spanner_verify_nonexistent_entry(self):
        """Test verification of non-existent entry."""
        sync_engine = SpannerSyncEngine(simulate=True)
        
        result = sync_engine.verify_cross_region_consistency("nonexistent_hash")
        
        assert result["status"] == "NOT_FOUND"


class TestCloudKMSManager:
    """Test Cloud KMS key management (simulation mode)."""
    
    def test_kms_initialization_simulation(self):
        """Test KMS initialization in simulation mode."""
        kms = CloudKMSManager(simulate=True)
        assert kms.simulate is True
    
    def test_kms_sign_entry(self):
        """Test signing audit entries."""
        kms = CloudKMSManager(simulate=True)
        
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        signature = kms.sign_entry(entry)
        
        assert signature != ""
        assert len(signature) > 0
        # Base64 encoded signature
        import base64
        try:
            base64.b64decode(signature)
            assert True
        except Exception:
            assert False, "Signature should be valid base64"
    
    def test_kms_verify_signature(self):
        """Test signature verification."""
        kms = CloudKMSManager(simulate=True)
        
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        signature = kms.sign_entry(entry)
        
        # Verify correct signature
        assert kms.verify_signature(entry, signature) is True
        
        # Verify incorrect signature
        assert kms.verify_signature(entry, "invalid_signature") is False
    
    def test_kms_signature_deterministic(self):
        """Test that signatures are deterministic for same entry."""
        kms = CloudKMSManager(simulate=True)
        
        entry = AuditEntry(
            timestamp="2025-01-15T10:00:00Z",
            event_type="test_event",
            actor="test_actor",
            resource="test_resource",
            action="test_action",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            metadata={},
            previous_hash="0" * 64
        )
        
        sig1 = kms.sign_entry(entry)
        sig2 = kms.sign_entry(entry)
        
        # Same entry should produce same signature
        assert sig1 == sig2
    
    def test_kms_key_rotation(self):
        """Test key rotation capability."""
        kms = CloudKMSManager(simulate=True)
        
        result = kms.rotate_key()
        
        assert result["status"] == "ROTATED"
        assert "new_version" in result
        assert "timestamp" in result


class TestTamperProofAuditTrail:
    """Test complete tamper-proof audit trail system."""
    
    def test_audit_trail_initialization(self):
        """Test initialization of complete audit trail."""
        trail = TamperProofAuditTrail(simulate=True)
        
        assert trail.simulate is True
        assert trail.bigtable is not None
        assert trail.spanner is not None
        assert trail.kms is not None
    
    def test_audit_trail_log_event(self):
        """Test logging events to audit trail."""
        trail = TamperProofAuditTrail(simulate=True)
        
        entry = trail.log_event(
            event_type=AuditEventType.SOVEREIGNTY_CHECK,
            actor="user@example.com",
            resource="patient_record_12345",
            action="validate_data_transfer",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            metadata={"reason": "cross-border transfer validation"}
        )
        
        assert entry is not None
        assert entry.event_type == AuditEventType.SOVEREIGNTY_CHECK.value
        assert entry.actor == "user@example.com"
        assert entry.signature != ""
        assert len(entry.entry_hash) == 64
    
    def test_audit_trail_chain_creation(self):
        """Test that audit entries form a chain."""
        trail = TamperProofAuditTrail(simulate=True)
        
        # Log multiple events
        entry1 = trail.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            actor="user1@example.com",
            resource="resource1",
            action="read",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS"
        )
        
        entry2 = trail.log_event(
            event_type=AuditEventType.DATA_TRANSFER,
            actor="user2@example.com",
            resource="resource2",
            action="transfer",
            jurisdiction="KDPA_KE",
            outcome="SUCCESS"
        )
        
        entry3 = trail.log_event(
            event_type=AuditEventType.CONSENT_VALIDATION,
            actor="user3@example.com",
            resource="resource3",
            action="validate",
            jurisdiction="HIPAA_US",
            outcome="SUCCESS"
        )
        
        # Verify chain linkage
        assert entry2.previous_hash == entry1.entry_hash
        assert entry3.previous_hash == entry2.entry_hash
    
    def test_audit_trail_get_history(self):
        """Test retrieving audit history."""
        trail = TamperProofAuditTrail(simulate=True)
        
        # Log some events
        for i in range(5):
            trail.log_event(
                event_type=AuditEventType.SYSTEM_CONFIGURATION,
                actor=f"admin{i}@example.com",
                resource=f"config_{i}",
                action="update",
                jurisdiction="GLOBAL_DEFAULT",
                outcome="SUCCESS",
                metadata={"index": i}
            )
        
        # Get history
        history = trail.get_audit_history(limit=10)
        
        assert len(history) == 5
        # Most recent should be first
        assert history[0].metadata["index"] == 4
    
    def test_audit_trail_verify_chain_integrity(self):
        """Test verifying chain integrity."""
        trail = TamperProofAuditTrail(simulate=True)
        
        # Create valid chain
        for i in range(3):
            trail.log_event(
                event_type=AuditEventType.HIGH_RISK_INFERENCE,
                actor=f"ml_system_{i}",
                resource=f"prediction_{i}",
                action="inference",
                jurisdiction="EU_AI_ACT",
                outcome="SUCCESS"
            )
        
        # Get entries and verify
        entries = trail.get_audit_history(limit=10)
        result = trail.verify_chain_integrity(entries)
        
        assert result["total_entries"] == 3
        assert result["valid_entries"] == 3
        assert result["chain_valid"] is True
        assert result["broken_chain"] is False
        assert result["invalid_signatures"] == 0
    
    def test_audit_trail_detect_tampering(self):
        """Test detection of tampered entries."""
        trail = TamperProofAuditTrail(simulate=True)
        
        # Create chain
        entry1 = trail.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            actor="user@example.com",
            resource="resource1",
            action="read",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS"
        )
        
        entry2 = trail.log_event(
            event_type=AuditEventType.DATA_TRANSFER,
            actor="user@example.com",
            resource="resource2",
            action="transfer",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS"
        )
        
        # Tamper with entry1 (simulate attack)
        entries = [entry1, entry2]
        entries[0].outcome = "FAILURE"  # Modify outcome without updating hash
        
        # Verify should detect tampering
        result = trail.verify_chain_integrity(entries)
        
        assert result["chain_valid"] is False
        assert len(result["details"]) > 0
    
    def test_audit_trail_verify_cross_region_sync(self):
        """Test cross-region synchronization verification."""
        trail = TamperProofAuditTrail(simulate=True)
        
        entry = trail.log_event(
            event_type=AuditEventType.BREACH_NOTIFICATION,
            actor="security_system",
            resource="breach_alert_12345",
            action="notify",
            jurisdiction="GDPR_EU",
            outcome="SUCCESS",
            sync_regions=["us-east1", "eu-west1", "asia-southeast1"]
        )
        
        # Verify cross-region sync
        result = trail.verify_cross_region_sync(entry.entry_hash)
        
        assert result["status"] == "CONSISTENT"
        assert "us-east1" in result["regions"]
        assert "eu-west1" in result["regions"]
        assert "asia-southeast1" in result["regions"]
    
    def test_audit_trail_different_event_types(self):
        """Test logging various event types."""
        trail = TamperProofAuditTrail(simulate=True)
        
        event_types = [
            AuditEventType.SOVEREIGNTY_CHECK,
            AuditEventType.DATA_ACCESS,
            AuditEventType.DATA_TRANSFER,
            AuditEventType.HIGH_RISK_INFERENCE,
            AuditEventType.CONSENT_VALIDATION,
            AuditEventType.KEY_ROTATION,
            AuditEventType.BREACH_NOTIFICATION,
            AuditEventType.RETENTION_ENFORCEMENT,
        ]
        
        for event_type in event_types:
            entry = trail.log_event(
                event_type=event_type,
                actor="system",
                resource="test_resource",
                action="test_action",
                jurisdiction="GLOBAL_DEFAULT",
                outcome="SUCCESS"
            )
            assert entry.event_type == event_type.value


class TestAuditTrailIntegration:
    """Integration tests for audit trail with governance kernel."""
    
    def test_audit_trail_with_sovereign_guardrail(self):
        """Test integration with SovereignGuardrail."""
        from governance_kernel.vector_ledger import SovereignGuardrail
        
        # Initialize guardrail with tamper-proof audit
        guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
        
        assert guardrail.tamper_proof_audit_enabled is True
        assert guardrail.tamper_proof_trail is not None
    
    def test_audit_trail_logs_successful_validation(self):
        """Test that successful validations are logged."""
        from governance_kernel.vector_ledger import SovereignGuardrail
        
        guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
        
        # Perform a validation
        result = guardrail.validate_action(
            action_type='High_Risk_Inference',
            payload={
                'actor': 'ml_system',
                'resource': 'patient_diagnosis',
                'explanation': 'SHAP values: [0.8, 0.1, 0.1]',
                'confidence_score': 0.95,
                'evidence_chain': ['symptom_fever', 'symptom_cough', 'lab_positive'],
                'consent_token': 'valid_token_12345',
                'consent_scope': 'diagnosis'
            },
            jurisdiction='EU_AI_ACT'
        )
        
        assert result is True
        
        # Check audit trail
        history = guardrail.get_tamper_proof_audit_history(limit=10)
        assert len(history) > 0
        assert history[0]['outcome'] == "SUCCESS"
    
    def test_audit_trail_logs_violations(self):
        """Test that violations are logged to audit trail."""
        from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError
        
        guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
        
        # Attempt a violation
        with pytest.raises(SovereigntyViolationError):
            guardrail.validate_action(
                action_type='Data_Transfer',
                payload={
                    'actor': 'system',
                    'resource': 'patient_phi',
                    'data_type': 'PHI',
                    'destination': 'Foreign_Cloud',
                    'consent_token': 'token'
                },
                jurisdiction='GDPR_EU'
            )
        
        # Check that violation was logged
        history = guardrail.get_tamper_proof_audit_history(limit=10)
        assert len(history) > 0
        
        # Find the violation entry
        violation_entries = [e for e in history if e['outcome'] == 'VIOLATION']
        assert len(violation_entries) > 0
        assert violation_entries[0]['metadata']['violation_type'] == 'DATA_SOVEREIGNTY'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
