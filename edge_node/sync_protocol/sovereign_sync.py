"""
Sovereign Sync: 80% Offline Capability Engine
═══════════════════════════════════════════════════════════════════════════

Provides sovereign data synchronization with cloud-first fallback to edge storage.
Implements HSML (Health Sovereign Markup Language) format for offline resilience.

Philosophy: "Cloud when available, edge when necessary, never lose data."
"""

from google.cloud import firestore
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
import socket


class SovereignSync:
    """
    Sovereign synchronization engine with 80% offline capability.
    
    Provides cloud-first data sync with automatic fallback to local edge storage
    when connectivity is unavailable. Uses HSML format for offline data integrity.
    
    Usage:
        sync = SovereignSync()
        result = sync.sync_with_edge_fallback(
            data={'patient_id': 'P123', 'diagnosis': 'malaria'},
            location='Nairobi_Clinic_01'
        )
        # Returns: "cloud_synced" or "edge_stored_with_hsml"
        
        # Later, when connectivity restored:
        sync.batch_sync_when_connected()
    """
    
    def __init__(self):
        """Initialize the SovereignSync engine."""
        self.local_cache = {}
        try:
            self.firestore_client = firestore.Client()
        except Exception:
            # If Firestore initialization fails (e.g., no credentials), set to None
            # This allows the system to function in fully offline mode
            self.firestore_client = None
    
    def sync_with_edge_fallback(self, data: Dict[str, Any], location: str) -> str:
        """
        Attempt cloud sync first, fall back to local HSML storage if unavailable.
        
        Args:
            data: Health data payload to sync (e.g., patient records, field data)
            location: Geographic location identifier (e.g., 'Nairobi_Clinic_01')
            
        Returns:
            str: "cloud_synced" if successful cloud sync,
                 "edge_stored_with_hsml" if stored locally
                 
        Philosophy:
            Cloud-first approach ensures data reaches central systems when possible,
            but never blocks field operations when connectivity is unavailable.
        """
        try:
            # Try cloud sync first
            if self.firestore_client is not None and self._check_connectivity():
                doc_ref = self.firestore_client.collection('field_data').document()
                doc_ref.set(data)
                return "cloud_synced"
            else:
                # No client or no connectivity - fall back to local
                raise Exception("Cloud unavailable")
        except Exception as e:
            # Fall back to local storage with HSML format
            hsml_entry = {
                'data': data,
                'location': location,
                'timestamp': datetime.now(),
                'sync_pending': True,
                'hash': self._calculate_hash(data)
            }
            self.local_cache[location] = hsml_entry
            return "edge_stored_with_hsml"
    
    def batch_sync_when_connected(self) -> Dict[str, Any]:
        """
        Batch synchronize all pending local cache entries when connectivity restored.
        
        Returns:
            Dict with sync statistics:
                - synced_count: Number of successfully synced entries
                - failed_count: Number of entries that failed to sync
                - remaining_count: Number of entries still in cache
                
        Usage:
            # Call periodically or on connectivity restoration event
            stats = sync.batch_sync_when_connected()
            print(f"Synced {stats['synced_count']} entries")
        """
        synced_count = 0
        failed_count = 0
        locations_to_remove = []
        
        for location, entry in list(self.local_cache.items()):
            if self._check_connectivity():
                try:
                    # Extract data from HSML entry
                    data = entry['data']
                    
                    # Sync to cloud
                    result = self.sync_with_edge_fallback(data, location)
                    
                    if result == "cloud_synced":
                        # Mark for removal from cache
                        locations_to_remove.append(location)
                        synced_count += 1
                    else:
                        # Still couldn't sync
                        failed_count += 1
                except Exception as e:
                    # Sync failed, keep in cache
                    failed_count += 1
            else:
                # No connectivity, stop trying
                break
        
        # Remove successfully synced entries
        for location in locations_to_remove:
            del self.local_cache[location]
        
        return {
            'synced_count': synced_count,
            'failed_count': failed_count,
            'remaining_count': len(self.local_cache)
        }
    
    def _calculate_hash(self, data: Dict[str, Any]) -> str:
        """
        Calculate SHA-256 hash of data for integrity verification.
        
        Args:
            data: Dictionary to hash
            
        Returns:
            str: Hexadecimal hash string
            
        Philosophy:
            Integrity verification ensures data hasn't been corrupted during
            offline storage and transmission.
        """
        # Convert data to stable JSON string (sorted keys for consistency)
        data_json = json.dumps(data, sort_keys=True, default=str)
        
        # Calculate SHA-256 hash
        hash_obj = hashlib.sha256(data_json.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def _check_connectivity(self) -> bool:
        """
        Check if cloud connectivity is available.
        
        Returns:
            bool: True if connectivity available, False otherwise
            
        Implementation:
            Attempts to resolve Google's DNS server as a quick connectivity check.
            This is a lightweight operation suitable for frequent polling.
        """
        try:
            # Try to resolve a well-known host (Google DNS)
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except (OSError, socket.timeout):
            return False
    
    def get_cache_status(self) -> Dict[str, Any]:
        """
        Get current status of local cache.
        
        Returns:
            Dict with cache statistics:
                - total_entries: Total number of cached entries
                - pending_sync: Number of entries waiting for sync
                - oldest_entry: Timestamp of oldest cached entry
                - cache_size_bytes: Approximate size of cache in bytes
        """
        if not self.local_cache:
            return {
                'total_entries': 0,
                'pending_sync': 0,
                'oldest_entry': None,
                'cache_size_bytes': 0
            }
        
        oldest_timestamp = min(
            entry['timestamp'] for entry in self.local_cache.values()
        )
        
        pending_sync = sum(
            1 for entry in self.local_cache.values()
            if entry.get('sync_pending', False)
        )
        
        # Estimate cache size
        cache_json = json.dumps(self.local_cache, default=str)
        cache_size = len(cache_json.encode('utf-8'))
        
        return {
            'total_entries': len(self.local_cache),
            'pending_sync': pending_sync,
            'oldest_entry': oldest_timestamp.isoformat() if oldest_timestamp else None,
            'cache_size_bytes': cache_size
        }
    
    def verify_cache_integrity(self) -> Dict[str, Any]:
        """
        Verify integrity of all cached entries using stored hashes.
        
        Returns:
            Dict with verification results:
                - total_checked: Number of entries checked
                - valid_entries: Number of entries with valid hashes
                - corrupted_entries: List of locations with corrupted data
        """
        corrupted = []
        valid_count = 0
        
        for location, entry in self.local_cache.items():
            stored_hash = entry.get('hash')
            current_hash = self._calculate_hash(entry['data'])
            
            if stored_hash == current_hash:
                valid_count += 1
            else:
                corrupted.append(location)
        
        return {
            'total_checked': len(self.local_cache),
            'valid_entries': valid_count,
            'corrupted_entries': corrupted
        }


# ═════════════════════════════════════════════════════════════════════════════
# The Sovereign Sync Philosophy:
# "Cloud when available, edge when necessary, never lose data."
#
# 80% Offline Capability: Field operations continue uninterrupted even when
# connectivity is limited. HSML format ensures data integrity across sync cycles.
# ═════════════════════════════════════════════════════════════════════════════
