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

#!/usr/bin/env python3
"""
SovereignSync Usage Example
═══════════════════════════════════════════════════════════════════════════

Demonstrates the 80% offline capability of the SovereignSync engine.

This example shows:
1. Initialization of SovereignSync
2. Cloud-first data synchronization with fallback
3. Cache status monitoring
4. Integrity verification
5. Batch synchronization on connectivity restoration
"""

from edge_node.sync_protocol.sovereign_sync import SovereignSync
from datetime import datetime, timezone


def main():
    """Demonstrate SovereignSync capabilities."""
    
    print("=" * 70)
    print("SovereignSync: 80% Offline Capability Demo")
    print("=" * 70)
    
    # Initialize the sync engine
    print("\n1. Initializing SovereignSync...")
    sync = SovereignSync()
    print("   ✓ Sync engine ready")
    
    # Simulate field data collection in remote clinic
    print("\n2. Collecting field data from remote clinic...")
    field_data_1 = {
        'patient_id': 'KE-NAI-001-12345',
        'clinic': 'Nairobi_Health_Center_01',
        'diagnosis': 'malaria',
        'symptoms': ['fever', 'chills', 'headache'],
        'lab_result': 'positive',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'severity': 'moderate'
    }
    
    result = sync.sync_with_edge_fallback(field_data_1, 'Nairobi_Health_Center_01')
    print(f"   Status: {result}")
    
    if result == "edge_stored_with_hsml":
        print("   📡 No connectivity - Data stored locally with HSML format")
    else:
        print("   ☁️  Data synced to cloud successfully")
    
    # Collect more data
    print("\n3. Collecting additional field data...")
    field_data_2 = {
        'patient_id': 'KE-MOM-002-67890',
        'clinic': 'Mombasa_Primary_Care',
        'diagnosis': 'dengue',
        'symptoms': ['fever', 'joint_pain', 'rash'],
        'lab_result': 'positive',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'severity': 'mild'
    }
    
    result = sync.sync_with_edge_fallback(field_data_2, 'Mombasa_Primary_Care')
    print(f"   Status: {result}")
    
    # Check cache status
    print("\n4. Checking local cache status...")
    cache_status = sync.get_cache_status()
    print(f"   Total entries: {cache_status['total_entries']}")
    print(f"   Pending sync: {cache_status['pending_sync']}")
    print(f"   Cache size: {cache_status['cache_size_bytes']} bytes")
    
    if cache_status['oldest_entry']:
        print(f"   Oldest entry: {cache_status['oldest_entry']}")
    
    # Verify data integrity
    print("\n5. Verifying cache integrity...")
    integrity = sync.verify_cache_integrity()
    print(f"   Total checked: {integrity['total_checked']}")
    print(f"   Valid entries: {integrity['valid_entries']}")
    
    if integrity['corrupted_entries']:
        print(f"   ⚠️  Corrupted entries: {integrity['corrupted_entries']}")
    else:
        print("   ✓ All entries verified - no corruption detected")
    
    # Simulate connectivity restoration and batch sync
    print("\n6. Attempting batch synchronization...")
    print("   (Will attempt sync if connectivity available)")
    sync_stats = sync.batch_sync_when_connected()
    
    print(f"   Successfully synced: {sync_stats['synced_count']}")
    print(f"   Failed to sync: {sync_stats['failed_count']}")
    print(f"   Remaining in cache: {sync_stats['remaining_count']}")
    
    if sync_stats['remaining_count'] > 0:
        print("   📡 Data preserved locally until connectivity restored")
    else:
        print("   ☁️  All data successfully synced to cloud")
    
    # Final status
    print("\n7. Final system status...")
    final_status = sync.get_cache_status()
    print(f"   Local cache entries: {final_status['total_entries']}")
    
    print("\n" + "=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70)
    
    print("\n📖 Key Takeaways:")
    print("   • Cloud-first approach attempts sync when available")
    print("   • Automatic fallback to HSML local storage when offline")
    print("   • SHA-256 integrity verification prevents data corruption")
    print("   • Batch sync restores data to cloud on connectivity")
    print("   • Field operations never blocked by connectivity issues")
    print("\n   Philosophy: 'Cloud when available, edge when necessary, never lose data.'")


if __name__ == '__main__':
    main()
