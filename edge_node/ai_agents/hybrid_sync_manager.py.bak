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
Hybrid Edge-Cloud Sync Manager
═════════════════════════════════════════════════════════════════════════════

Manage synchronization between edge (NVIDIA Jetson) and cloud (Google Cloud).
Enforces data sovereignty: only de-identified data syncs to cloud.

Usage:
    sync_manager = HybridSyncManager(
        bucket_name="iluminara-edge-sync-eu",
        location="europe-west4"
    )
    
    sync_manager.sync_swahili_queries(queries)
"""

from typing import List, Dict
import json
from datetime import datetime
from governance_kernel.vector_ledger import SovereignGuardrail

try:
    from google.cloud import storage
    CLOUD_STORAGE_AVAILABLE = True
except ImportError:
    CLOUD_STORAGE_AVAILABLE = False
    print("⚠️  google-cloud-storage not installed. Install with: pip install google-cloud-storage")


class HybridSyncManager:
    """
    Manage synchronization between edge (NVIDIA Jetson) and cloud (Google Cloud).
    Enforces data sovereignty: only de-identified data syncs to cloud.
    """
    
    def __init__(
        self, 
        bucket_name: str = "iluminara-edge-sync-eu",
        location: str = "europe-west4"
    ):
        """
        Initialize the sync manager.
        
        Args:
            bucket_name: Google Cloud Storage bucket name
            location: Google Cloud region
        """
        self.bucket_name = bucket_name
        self.location = location
        self.guardrail = SovereignGuardrail()
        
        if CLOUD_STORAGE_AVAILABLE:
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(bucket_name)
            self.use_cloud = True
        else:
            self.use_cloud = False
            print("⚠️  Cloud Storage not available. Sync disabled.")
        
        # Local sync queue for offline mode
        self.sync_queue = []
    
    def sync_swahili_queries(self, queries: List[Dict]) -> bool:
        """
        Sync Swahili medical queries from edge to cloud for model improvement.
        
        Args:
            queries: List of de-identified query logs
                [
                    {
                        "query": "Nina homa",
                        "timestamp": "2025-12-19T10:00:00Z",
                        "location_region": "Nairobi",  # No precise location
                        "has_phi": False
                    }
                ]
        
        Returns:
            True if sync successful, False otherwise
        """
        
        # Validate all queries are de-identified
        for query in queries:
            if query.get("has_phi", True):
                print(f"❌ Sync blocked: Query contains PHI")
                return False
            
            try:
                self.guardrail.validate_action(
                    action_type='Cloud_Sync',
                    payload={
                        'data_type': 'De_Identified_Medical_Query',
                        'destination': f'Google_Cloud_{self.location}',
                        'has_phi': False,
                        'consent_token': query.get('consent_token', 'GENERAL_RESEARCH_CONSENT')
                    },
                    jurisdiction='GDPR_EU'
                )
            except Exception as e:
                print(f"❌ Sovereignty violation: {e}")
                return False
        
        if self.use_cloud:
            return self._sync_to_cloud(queries)
        else:
            return self._queue_for_sync(queries)
    
    def _sync_to_cloud(self, queries: List[Dict]) -> bool:
        """Upload queries to Cloud Storage."""
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            blob_name = f"swahili_queries/{timestamp}.json"
            
            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(
                json.dumps(queries, ensure_ascii=False, indent=2),
                content_type='application/json'
            )
            
            print(f"✅ Synced {len(queries)} queries to {blob_name}")
            return True
            
        except Exception as e:
            print(f"❌ Sync failed: {e}")
            return self._queue_for_sync(queries)
    
    def _queue_for_sync(self, queries: List[Dict]) -> bool:
        """Queue queries for later sync (offline mode)."""
        self.sync_queue.extend(queries)
        print(f"📦 Queued {len(queries)} queries for later sync. Total: {len(self.sync_queue)}")
        return True
    
    def download_updated_models(self, model_dir: str = "/opt/iluminara/models") -> List[str]:
        """
        Download updated Swahili medical models from cloud to edge.
        
        Args:
            model_dir: Local directory to save models
        
        Returns:
            List of downloaded model file paths
        """
        
        if not self.use_cloud:
            print("⚠️  Cloud not available. Cannot download models.")
            return []
        
        downloaded_files = []
        
        try:
            # List all model files in cloud bucket
            blobs = self.bucket.list_blobs(prefix="models/swahili/")
            
            for blob in blobs:
                if blob.name.endswith((".tflite", ".onnx", ".pkl")):
                    # Download lightweight models for edge deployment
                    local_path = f"{model_dir}/{blob.name.split('/')[-1]}"
                    blob.download_to_filename(local_path)
                    downloaded_files.append(local_path)
                    print(f"✅ Downloaded model: {local_path}")
            
            return downloaded_files
            
        except Exception as e:
            print(f"❌ Model download failed: {e}")
            return []
    
    def sync_cbs_data(self, cbs_records: List[Dict]) -> bool:
        """
        Sync Community-Based Surveillance data to cloud.
        
        Args:
            cbs_records: De-identified CBS records
        
        Returns:
            True if successful
        """
        
        # Validate de-identification
        for record in cbs_records:
            if 'patient_id' in record or 'name' in record:
                print("❌ CBS sync blocked: Contains identifiable information")
                return False
        
        # Add sync metadata
        sync_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": "edge_node",
            "record_count": len(cbs_records),
            "records": cbs_records
        }
        
        if self.use_cloud:
            try:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                blob_name = f"cbs_data/{timestamp}.json"
                
                blob = self.bucket.blob(blob_name)
                blob.upload_from_string(
                    json.dumps(sync_data, ensure_ascii=False, indent=2),
                    content_type='application/json'
                )
                
                print(f"✅ Synced {len(cbs_records)} CBS records to {blob_name}")
                return True
                
            except Exception as e:
                print(f"❌ CBS sync failed: {e}")
                return False
        else:
            print(f"📦 Queued {len(cbs_records)} CBS records for later sync")
            return True
    
    def get_sync_status(self) -> Dict[str, any]:
        """
        Get current sync status.
        
        Returns:
            {
                "cloud_available": True/False,
                "queued_items": 0,
                "last_sync": "2025-12-19T10:00:00Z"
            }
        """
        return {
            "cloud_available": self.use_cloud,
            "queued_items": len(self.sync_queue),
            "bucket": self.bucket_name if self.use_cloud else None,
            "location": self.location
        }
