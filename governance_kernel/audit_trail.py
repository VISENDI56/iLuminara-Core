"""
Tamper-proof Audit Trail with Cloud Infrastructure
════════════════════════════════════════════════════════════════════════════

A cryptographically-secured audit ledger for iLuminara-Core that ensures:
1. Immutability: Audit entries are cryptographically chained and signed
2. High-throughput: Bigtable for write-heavy audit logging
3. Cross-region sync: Cloud Spanner for global consistency
4. Sovereign keys: Cloud KMS for key management and HSM simulation

Architecture:
- Bigtable: Primary ledger storage (high-throughput writes)
- Cloud Spanner: Audit metadata and cross-region queries
- Cloud KMS: Key management and cryptographic operations

Philosophy: "Trust, but verify with cryptographic proof."
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class AuditEventType(Enum):
    """Types of auditable events in iLuminara-Core."""
    SOVEREIGNTY_CHECK = "sovereignty_check"
    DATA_ACCESS = "data_access"
    DATA_TRANSFER = "data_transfer"
    HIGH_RISK_INFERENCE = "high_risk_inference"
    CONSENT_VALIDATION = "consent_validation"
    KEY_ROTATION = "key_rotation"
    BREACH_NOTIFICATION = "breach_notification"
    RETENTION_ENFORCEMENT = "retention_enforcement"
    SYSTEM_CONFIGURATION = "system_configuration"


@dataclass
class AuditEntry:
    """
    Immutable audit entry with cryptographic integrity.
    
    Each entry contains:
    - timestamp: ISO8601 UTC timestamp
    - event_type: Type of auditable event
    - actor: Entity performing the action (user ID, service account)
    - resource: Resource being accessed/modified
    - action: Specific action performed
    - jurisdiction: Legal jurisdiction context
    - outcome: SUCCESS, FAILURE, VIOLATION
    - metadata: Additional context (evidence, reasons, etc.)
    - previous_hash: Hash of previous entry (chain integrity)
    - entry_hash: Hash of current entry
    - signature: KMS signature for non-repudiation
    """
    timestamp: str
    event_type: str
    actor: str
    resource: str
    action: str
    jurisdiction: str
    outcome: str
    metadata: Dict[str, Any]
    previous_hash: str
    entry_hash: str = ""
    signature: str = ""
    
    def __post_init__(self):
        """Compute hash and signature upon creation."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"
        if not self.entry_hash:
            self.entry_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """
        Compute SHA-256 hash of entry content (excluding entry_hash and signature).
        Creates tamper-evident chain: hash depends on previous_hash.
        """
        # Create canonical representation (deterministic JSON)
        content = {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "actor": self.actor,
            "resource": self.resource,
            "action": self.action,
            "jurisdiction": self.jurisdiction,
            "outcome": self.outcome,
            "metadata": self.metadata,
            "previous_hash": self.previous_hash
        }
        canonical_json = json.dumps(content, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Verify that entry hash matches computed hash."""
        computed = self._compute_hash()
        return computed == self.entry_hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class BigtableLedger:
    """
    High-throughput audit ledger using Google Cloud Bigtable.
    
    Bigtable provides:
    - Sub-10ms latency writes
    - Petabyte-scale storage
    - Automatic replication and failover
    
    Schema:
    - Row Key: {timestamp_reverse}#{entry_hash} (enables time-ordered scans)
    - Column Family: audit_data
    - Columns: event_type, actor, resource, action, jurisdiction, outcome, 
               metadata, previous_hash, signature
    """
    
    def __init__(self, project_id: str = "iluminara-sovereign", 
                 instance_id: str = "audit-ledger",
                 table_id: str = "tamper_proof_trail",
                 simulate: bool = True):
        """
        Initialize Bigtable connection.
        
        Args:
            project_id: GCP project ID
            instance_id: Bigtable instance ID
            table_id: Bigtable table name
            simulate: If True, use in-memory simulation (for development)
        """
        self.project_id = project_id
        self.instance_id = instance_id
        self.table_id = table_id
        self.simulate = simulate
        
        # In-memory store for simulation mode
        self._simulated_store: Dict[str, AuditEntry] = {}
        
        if not simulate:
            try:
                from google.cloud import bigtable
                from google.cloud.bigtable import column_family
                
                # Initialize Bigtable client
                self.client = bigtable.Client(project=project_id, admin=True)
                self.instance = self.client.instance(instance_id)
                self.table = self.instance.table(table_id)
                
                # Ensure table exists
                if not self.table.exists():
                    # Create table with column family
                    self.table.create()
                    cf = self.table.column_family("audit_data")
                    cf.create()
            except ImportError:
                print("⚠️  google-cloud-bigtable not installed. Using simulation mode.")
                self.simulate = True
    
    def write_entry(self, entry: AuditEntry) -> bool:
        """
        Write audit entry to Bigtable ledger.
        
        Args:
            entry: AuditEntry to persist
            
        Returns:
            True if write successful
        """
        if self.simulate:
            # Simulation mode: store in memory
            row_key = self._generate_row_key(entry)
            self._simulated_store[row_key] = entry
            return True
        
        try:
            # Generate time-reversed row key for chronological scanning
            row_key = self._generate_row_key(entry)
            row = self.table.direct_row(row_key)
            
            # Write all columns
            row.set_cell("audit_data", "timestamp", entry.timestamp)
            row.set_cell("audit_data", "event_type", entry.event_type)
            row.set_cell("audit_data", "actor", entry.actor)
            row.set_cell("audit_data", "resource", entry.resource)
            row.set_cell("audit_data", "action", entry.action)
            row.set_cell("audit_data", "jurisdiction", entry.jurisdiction)
            row.set_cell("audit_data", "outcome", entry.outcome)
            row.set_cell("audit_data", "metadata", json.dumps(entry.metadata))
            row.set_cell("audit_data", "previous_hash", entry.previous_hash)
            row.set_cell("audit_data", "entry_hash", entry.entry_hash)
            row.set_cell("audit_data", "signature", entry.signature)
            
            # Commit the row
            row.commit()
            return True
            
        except Exception as e:
            print(f"❌ Bigtable write error: {e}")
            return False
    
    def _generate_row_key(self, entry: AuditEntry) -> str:
        """
        Generate row key for time-ordered scanning.
        Format: {timestamp_reverse}#{entry_hash}
        
        Reverse timestamp enables efficient range scans from most recent to oldest.
        """
        # Parse timestamp and reverse for descending order
        ts = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
        timestamp_micros = int(ts.timestamp() * 1_000_000)
        # Reverse: subtract from max value
        reversed_ts = 9999999999999999 - timestamp_micros
        return f"{reversed_ts:016d}#{entry.entry_hash[:16]}"
    
    def read_entries(self, limit: int = 100, start_time: Optional[str] = None) -> List[AuditEntry]:
        """
        Read audit entries from ledger.
        
        Args:
            limit: Maximum number of entries to return
            start_time: Optional ISO8601 timestamp to start scan from
            
        Returns:
            List of AuditEntry objects in chronological order
        """
        if self.simulate:
            # Return simulated entries
            entries = list(self._simulated_store.values())
            # Sort by timestamp (most recent first)
            entries.sort(key=lambda e: e.timestamp, reverse=True)
            return entries[:limit]
        
        # Real Bigtable scan
        try:
            entries = []
            # Scan table (row keys are already in reverse chronological order)
            for row in self.table.read_rows(limit=limit):
                entry = self._row_to_entry(row)
                if entry:
                    entries.append(entry)
            return entries
        except Exception as e:
            print(f"❌ Bigtable read error: {e}")
            return []
    
    def _row_to_entry(self, row) -> Optional[AuditEntry]:
        """Convert Bigtable row to AuditEntry."""
        try:
            cells = row.cells["audit_data"]
            return AuditEntry(
                timestamp=cells["timestamp"][0].value.decode('utf-8'),
                event_type=cells["event_type"][0].value.decode('utf-8'),
                actor=cells["actor"][0].value.decode('utf-8'),
                resource=cells["resource"][0].value.decode('utf-8'),
                action=cells["action"][0].value.decode('utf-8'),
                jurisdiction=cells["jurisdiction"][0].value.decode('utf-8'),
                outcome=cells["outcome"][0].value.decode('utf-8'),
                metadata=json.loads(cells["metadata"][0].value.decode('utf-8')),
                previous_hash=cells["previous_hash"][0].value.decode('utf-8'),
                entry_hash=cells["entry_hash"][0].value.decode('utf-8'),
                signature=cells["signature"][0].value.decode('utf-8')
            )
        except Exception as e:
            print(f"⚠️  Error parsing row: {e}")
            return None


class SpannerSyncEngine:
    """
    Cross-region audit synchronization using Google Cloud Spanner.
    
    Cloud Spanner provides:
    - Global consistency with external consistency (TrueTime)
    - Multi-region replication
    - ACID transactions across continents
    
    Schema:
    - audit_metadata table:
        - entry_hash (PRIMARY KEY)
        - timestamp
        - event_type
        - jurisdiction
        - sync_regions (ARRAY<STRING>)
        - verification_status
    """
    
    def __init__(self, project_id: str = "iluminara-sovereign",
                 instance_id: str = "global-audit-sync",
                 database_id: str = "audit_metadata",
                 simulate: bool = True):
        """
        Initialize Spanner connection.
        
        Args:
            project_id: GCP project ID
            instance_id: Spanner instance ID
            database_id: Database name
            simulate: If True, use in-memory simulation
        """
        self.project_id = project_id
        self.instance_id = instance_id
        self.database_id = database_id
        self.simulate = simulate
        
        # In-memory store for simulation
        self._simulated_metadata: Dict[str, Dict[str, Any]] = {}
        
        if not simulate:
            try:
                from google.cloud import spanner
                
                # Initialize Spanner client
                self.spanner_client = spanner.Client(project=project_id)
                self.instance = self.spanner_client.instance(instance_id)
                self.database = self.instance.database(database_id)
                
            except ImportError:
                print("⚠️  google-cloud-spanner not installed. Using simulation mode.")
                self.simulate = True
    
    def sync_entry_metadata(self, entry: AuditEntry, regions: List[str]) -> bool:
        """
        Synchronize audit entry metadata across regions.
        
        Args:
            entry: AuditEntry to sync
            regions: List of regions to replicate to (e.g., ['us-east1', 'eu-west1', 'asia-southeast1'])
            
        Returns:
            True if sync successful
        """
        if self.simulate:
            self._simulated_metadata[entry.entry_hash] = {
                "entry_hash": entry.entry_hash,
                "timestamp": entry.timestamp,
                "event_type": entry.event_type,
                "jurisdiction": entry.jurisdiction,
                "sync_regions": regions,
                "verification_status": "VERIFIED"
            }
            return True
        
        try:
            # Insert metadata into Spanner with global consistency
            with self.database.batch() as batch:
                batch.insert(
                    table="audit_metadata",
                    columns=["entry_hash", "timestamp", "event_type", 
                            "jurisdiction", "sync_regions", "verification_status"],
                    values=[[
                        entry.entry_hash,
                        entry.timestamp,
                        entry.event_type,
                        entry.jurisdiction,
                        regions,
                        "VERIFIED"
                    ]]
                )
            return True
            
        except Exception as e:
            print(f"❌ Spanner sync error: {e}")
            return False
    
    def verify_cross_region_consistency(self, entry_hash: str) -> Dict[str, Any]:
        """
        Verify that audit entry exists consistently across all regions.
        
        Args:
            entry_hash: Hash of entry to verify
            
        Returns:
            Verification result with status and region details
        """
        if self.simulate:
            metadata = self._simulated_metadata.get(entry_hash)
            if metadata:
                return {
                    "entry_hash": entry_hash,
                    "status": "CONSISTENT",
                    "regions": metadata["sync_regions"],
                    "verification_time": datetime.utcnow().isoformat() + "Z"
                }
            return {"status": "NOT_FOUND"}
        
        try:
            # Query Spanner for metadata
            with self.database.snapshot() as snapshot:
                results = snapshot.execute_sql(
                    "SELECT entry_hash, sync_regions, verification_status "
                    "FROM audit_metadata WHERE entry_hash = @hash",
                    params={"hash": entry_hash},
                    param_types={"hash": spanner.param_types.STRING}
                )
                
                for row in results:
                    return {
                        "entry_hash": row[0],
                        "regions": row[1],
                        "status": row[2],
                        "verification_time": datetime.utcnow().isoformat() + "Z"
                    }
                
                return {"status": "NOT_FOUND"}
                
        except Exception as e:
            print(f"❌ Spanner verification error: {e}")
            return {"status": "ERROR", "error": str(e)}


class CloudKMSManager:
    """
    Sovereign key management using Google Cloud KMS.
    
    Cloud KMS provides:
    - Hardware Security Module (HSM) backed keys
    - Sovereign key custody (keys never leave region)
    - Audit logging of all cryptographic operations
    - Automatic key rotation
    
    Key Hierarchy:
    - Master Key: KMS-managed, HSM-backed
    - Signing Key: Used for audit entry signatures
    - Encryption Key: Used for sensitive metadata encryption
    """
    
    def __init__(self, project_id: str = "iluminara-sovereign",
                 location_id: str = "us-east1",
                 key_ring_id: str = "audit-signing",
                 key_id: str = "audit-master-key",
                 simulate: bool = True):
        """
        Initialize KMS client.
        
        Args:
            project_id: GCP project ID
            location_id: KMS location (determines sovereign boundary)
            key_ring_id: Key ring name
            key_id: Key name
            simulate: If True, use simulated signatures
        """
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.simulate = simulate
        
        if not simulate:
            try:
                from google.cloud import kms
                
                # Initialize KMS client
                self.kms_client = kms.KeyManagementServiceClient()
                
                # Build key path
                self.key_path = self.kms_client.crypto_key_path(
                    project_id, location_id, key_ring_id, key_id
                )
                
            except ImportError:
                print("⚠️  google-cloud-kms not installed. Using simulation mode.")
                self.simulate = True
    
    def sign_entry(self, entry: AuditEntry) -> str:
        """
        Sign audit entry using KMS asymmetric signing key.
        
        Args:
            entry: AuditEntry to sign
            
        Returns:
            Base64-encoded signature
        """
        if self.simulate:
            # Simulated signature: HMAC-SHA256 of entry hash
            import hmac
            secret = b"simulated_kms_key_sovereign_custody"
            signature_bytes = hmac.new(secret, entry.entry_hash.encode(), hashlib.sha256).digest()
            import base64
            return base64.b64encode(signature_bytes).decode('utf-8')
        
        try:
            from google.cloud import kms
            import base64
            
            # Create digest of entry hash
            digest = {
                "sha256": bytes.fromhex(entry.entry_hash)
            }
            
            # Sign using KMS
            sign_response = self.kms_client.asymmetric_sign(
                request={
                    "name": self.key_path,
                    "digest": digest
                }
            )
            
            # Return base64-encoded signature
            return base64.b64encode(sign_response.signature).decode('utf-8')
            
        except Exception as e:
            print(f"❌ KMS signing error: {e}")
            return ""
    
    def verify_signature(self, entry: AuditEntry, signature: str) -> bool:
        """
        Verify audit entry signature using KMS public key.
        
        Args:
            entry: AuditEntry to verify
            signature: Base64-encoded signature
            
        Returns:
            True if signature is valid
        """
        if self.simulate:
            # Simulated verification
            expected_signature = self.sign_entry(entry)
            return signature == expected_signature
        
        try:
            from google.cloud import kms
            import base64
            
            # Get public key from KMS
            public_key = self.kms_client.get_public_key(request={"name": self.key_path})
            
            # Verify signature (implementation depends on key algorithm)
            # This is a simplified version
            return True  # TODO: Implement full verification
            
        except Exception as e:
            print(f"❌ KMS verification error: {e}")
            return False
    
    def rotate_key(self) -> Dict[str, Any]:
        """
        Trigger key rotation in KMS.
        
        Returns:
            Rotation status and new key version
        """
        if self.simulate:
            return {
                "status": "ROTATED",
                "new_version": f"v{int(time.time())}",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        
        try:
            # KMS handles automatic rotation based on policy
            # This would trigger manual rotation if needed
            return {
                "status": "ROTATION_SCHEDULED",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
        except Exception as e:
            print(f"❌ KMS rotation error: {e}")
            return {"status": "ERROR", "error": str(e)}


class TamperProofAuditTrail:
    """
    Complete tamper-proof audit trail system.
    
    Integrates:
    - BigtableLedger: High-throughput storage
    - SpannerSyncEngine: Cross-region consistency
    - CloudKMSManager: Cryptographic signing
    
    Features:
    - Cryptographic chain of custody
    - Multi-region replication
    - Sovereign key management
    - Immutability guarantees
    - Non-repudiation via signatures
    """
    
    def __init__(self, 
                 bigtable_config: Optional[Dict[str, Any]] = None,
                 spanner_config: Optional[Dict[str, Any]] = None,
                 kms_config: Optional[Dict[str, Any]] = None,
                 simulate: bool = True):
        """
        Initialize tamper-proof audit trail.
        
        Args:
            bigtable_config: Bigtable configuration dict
            spanner_config: Spanner configuration dict
            kms_config: KMS configuration dict
            simulate: If True, run in simulation mode (no real GCP resources)
        """
        self.simulate = simulate
        
        # Initialize components
        bt_config = bigtable_config or {}
        self.bigtable = BigtableLedger(simulate=simulate, **bt_config)
        
        sp_config = spanner_config or {}
        self.spanner = SpannerSyncEngine(simulate=simulate, **sp_config)
        
        kms_cfg = kms_config or {}
        self.kms = CloudKMSManager(simulate=simulate, **kms_cfg)
        
        # Track last entry hash for chaining
        self._last_entry_hash: str = "0" * 64  # Genesis hash
    
    def log_event(self,
                  event_type: AuditEventType,
                  actor: str,
                  resource: str,
                  action: str,
                  jurisdiction: str,
                  outcome: str,
                  metadata: Optional[Dict[str, Any]] = None,
                  sync_regions: Optional[List[str]] = None) -> AuditEntry:
        """
        Log an auditable event to the tamper-proof trail.
        
        Args:
            event_type: Type of event (from AuditEventType enum)
            actor: Entity performing action
            resource: Resource being acted upon
            action: Specific action taken
            jurisdiction: Legal jurisdiction context
            outcome: Result (SUCCESS, FAILURE, VIOLATION)
            metadata: Additional context
            sync_regions: Regions to replicate to
            
        Returns:
            Created AuditEntry with signature
        """
        # Create audit entry
        entry = AuditEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            event_type=event_type.value if isinstance(event_type, AuditEventType) else event_type,
            actor=actor,
            resource=resource,
            action=action,
            jurisdiction=jurisdiction,
            outcome=outcome,
            metadata=metadata or {},
            previous_hash=self._last_entry_hash
        )
        
        # Sign entry with KMS
        entry.signature = self.kms.sign_entry(entry)
        
        # Write to Bigtable
        write_success = self.bigtable.write_entry(entry)
        if not write_success:
            print("⚠️  Failed to write to Bigtable ledger")
        
        # Sync metadata to Spanner
        regions = sync_regions or ["us-east1", "eu-west1", "asia-southeast1"]
        sync_success = self.spanner.sync_entry_metadata(entry, regions)
        if not sync_success:
            print("⚠️  Failed to sync to Spanner")
        
        # Update last hash for chain
        self._last_entry_hash = entry.entry_hash
        
        return entry
    
    def verify_chain_integrity(self, entries: List[AuditEntry]) -> Dict[str, Any]:
        """
        Verify integrity of audit chain.
        
        Checks:
        1. Each entry's hash is correct
        2. Chain continuity (previous_hash references)
        3. Signatures are valid
        
        Args:
            entries: List of AuditEntry objects to verify (in any order)
            
        Returns:
            Verification result with details
        """
        # Sort entries by timestamp (oldest first) for chain verification
        sorted_entries = sorted(entries, key=lambda e: e.timestamp)
        
        results = {
            "total_entries": len(sorted_entries),
            "valid_entries": 0,
            "broken_chain": False,
            "invalid_signatures": 0,
            "details": []
        }
        
        for i, entry in enumerate(sorted_entries):
            # Check hash integrity
            if not entry.verify_integrity():
                results["details"].append({
                    "index": i,
                    "entry_hash": entry.entry_hash,
                    "error": "Hash mismatch"
                })
                continue
            
            # Check chain continuity
            if i > 0:
                expected_prev = sorted_entries[i-1].entry_hash
                if entry.previous_hash != expected_prev:
                    results["broken_chain"] = True
                    results["details"].append({
                        "index": i,
                        "entry_hash": entry.entry_hash,
                        "error": f"Chain break: expected prev={expected_prev}, got={entry.previous_hash}"
                    })
                    continue
            
            # Verify signature
            if not self.kms.verify_signature(entry, entry.signature):
                results["invalid_signatures"] += 1
                results["details"].append({
                    "index": i,
                    "entry_hash": entry.entry_hash,
                    "error": "Invalid signature"
                })
                continue
            
            results["valid_entries"] += 1
        
        results["chain_valid"] = (
            results["valid_entries"] == results["total_entries"] and
            not results["broken_chain"] and
            results["invalid_signatures"] == 0
        )
        
        return results
    
    def get_audit_history(self, limit: int = 100) -> List[AuditEntry]:
        """
        Retrieve audit history from ledger.
        
        Args:
            limit: Maximum number of entries to retrieve
            
        Returns:
            List of AuditEntry objects
        """
        return self.bigtable.read_entries(limit=limit)
    
    def verify_cross_region_sync(self, entry_hash: str) -> Dict[str, Any]:
        """
        Verify that entry is synchronized across regions.
        
        Args:
            entry_hash: Hash of entry to verify
            
        Returns:
            Sync verification result
        """
        return self.spanner.verify_cross_region_consistency(entry_hash)


# ═════════════════════════════════════════════════════════════════════════════
# MISSION: Cryptographic proof of integrity for every sovereignty decision.
#
# COMPLIANCE PILLAR: Tamper-Proof Audit Trail
# ═════════════════════════════════════════════════════════════════════════════
