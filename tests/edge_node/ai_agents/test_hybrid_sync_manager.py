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
Unit tests for HybridSyncManager
═════════════════════════════════════════════════════════════════════════════

Tests edge-cloud synchronization with de-identification enforcement.
"""

import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from edge_node.ai_agents.hybrid_sync_manager import HybridSyncManager


class TestHybridSyncManager:
    """Test cases for Hybrid Sync Manager."""
    
    def test_sync_manager_initialization_offline(self):
        """Test sync manager initializes in offline mode."""
        sync = HybridSyncManager(
            bucket_name="test-bucket",
            location="europe-west4"
        )
        assert sync.use_cloud == False
        assert sync.bucket_name == "test-bucket"
        assert sync.location == "europe-west4"
    
    def test_sync_status(self):
        """Test get_sync_status method."""
        sync = HybridSyncManager()
        
        status = sync.get_sync_status()
        
        assert "cloud_available" in status
        assert "queued_items" in status
        assert isinstance(status["queued_items"], int)
    
    def test_sync_queries_de_identified(self):
        """Test syncing de-identified queries."""
        sync = HybridSyncManager()
        
        queries = [
            {
                "query": "Nina homa",
                "timestamp": datetime.utcnow().isoformat(),
                "location_region": "Nairobi",
                "has_phi": False
            }
        ]
        
        result = sync.sync_swahili_queries(queries)
        
        # Should succeed (queued in offline mode)
        assert result == True
        assert len(sync.sync_queue) > 0
    
    def test_sync_queries_with_phi_blocked(self):
        """Test that queries with PHI are blocked."""
        sync = HybridSyncManager()
        
        queries = [
            {
                "query": "Jina langu ni John na nina homa",
                "timestamp": datetime.utcnow().isoformat(),
                "location_region": "Nairobi",
                "has_phi": True  # Contains PHI
            }
        ]
        
        result = sync.sync_swahili_queries(queries)
        
        # Should be blocked
        assert result == False
    
    def test_sync_cbs_data_de_identified(self):
        """Test syncing de-identified CBS data."""
        sync = HybridSyncManager()
        
        cbs_records = [
            {
                "symptom": "homa",
                "location_region": "Nairobi",
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
        
        result = sync.sync_cbs_data(cbs_records)
        
        # Should succeed
        assert result == True
    
    def test_sync_cbs_data_with_identifiers_blocked(self):
        """Test that CBS data with identifiers is blocked."""
        sync = HybridSyncManager()
        
        cbs_records = [
            {
                "patient_id": "12345",  # Should be blocked
                "symptom": "homa",
                "location_region": "Nairobi"
            }
        ]
        
        result = sync.sync_cbs_data(cbs_records)
        
        # Should be blocked
        assert result == False
    
    def test_queue_accumulation(self):
        """Test that offline queue accumulates queries."""
        sync = HybridSyncManager()
        
        initial_count = len(sync.sync_queue)
        
        queries = [
            {"query": "Nina homa", "has_phi": False},
            {"query": "Nina malaria", "has_phi": False}
        ]
        
        sync.sync_swahili_queries(queries)
        
        assert len(sync.sync_queue) == initial_count + 2
    
    def test_download_models_offline_mode(self):
        """Test model download in offline mode."""
        sync = HybridSyncManager()
        
        models = sync.download_updated_models()
        
        # Should return empty list in offline mode
        assert isinstance(models, list)
        assert len(models) == 0
    
    def test_different_regions_supported(self):
        """Test sync manager supports different regions."""
        sync_eu = HybridSyncManager(
            bucket_name="test-bucket-eu",
            location="europe-west4"
        )
        sync_africa = HybridSyncManager(
            bucket_name="test-bucket-africa",
            location="africa-south1"
        )
        
        assert sync_eu.location == "europe-west4"
        assert sync_africa.location == "africa-south1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
