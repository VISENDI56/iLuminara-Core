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
iLuminara BigQuery Demo Data Creator
Creates realistic outbreak simulation data for GCP prototype

Geographic coordinates are based on Dadaab refugee complex area in Kenya
Base coordinates: 0.4°N, 40.2°E (approximating the outbreak zone)
"""

import sys
from datetime import datetime

# Geographic base coordinates (Dadaab region, Kenya)
BASE_LATITUDE = 0.4
BASE_LONGITUDE = 40.2

def create_demo_outbreak_data():
    """Create demo outbreak simulation in BigQuery."""
    try:
        from google.cloud import bigquery
    except ImportError:
        print("❌ Error: google-cloud-bigquery not installed")
        print("   Install with: pip install google-cloud-bigquery")
        return False
    
    try:
        print("📊 Initializing BigQuery client...")
        client = bigquery.Client()
        project_id = client.project
        
        print(f"📋 Project: {project_id}")
        
        # Create dataset if it doesn't exist
        dataset_id = f"{project_id}.iluminara"
        print(f"📁 Creating/verifying dataset: {dataset_id}")
        
        try:
            dataset = client.get_dataset(dataset_id)
            print(f"   ✅ Dataset {dataset_id} already exists")
        except Exception:
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            dataset.description = "iLuminara outbreak simulation and health intelligence data"
            dataset = client.create_dataset(dataset, timeout=30)
            print(f"   ✅ Created dataset {dataset_id}")
        
        # Create outbreak simulation table
        print("📊 Creating outbreak_simulations table...")
        query = f"""
        CREATE OR REPLACE TABLE iluminara.outbreak_simulations AS
        SELECT 
            TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL n HOUR) as timestamp,
            ST_GEOGPOINT({BASE_LONGITUDE} + RAND()/10, {BASE_LATITUDE} + RAND()/10) as location,
            ARRAY<STRING>['diarrhea', 'fever', 'dehydration'][OFFSET(MOD(n, 3))] as symptoms,
            RAND() * 100 as water_contamination,
            30 + RAND() * 15 as temperature
        FROM UNNEST(GENERATE_ARRAY(1, 168)) as n
        """
        
        query_job = client.query(query)
        result = query_job.result()
        
        # Get row count
        count_query = "SELECT COUNT(*) as count FROM iluminara.outbreak_simulations"
        count_job = client.query(count_query)
        count_result = list(count_job.result())[0]
        row_count = count_result['count']
        
        print(f"   ✅ Created table with {row_count} simulation records")
        print(f"   📍 Location data spans 168 hours (7 days)")
        print(f"   🦠 Simulated symptoms: diarrhea, fever, dehydration")
        
        # Display sample data
        print("\n📋 Sample data (first 3 rows):")
        sample_query = "SELECT * FROM iluminara.outbreak_simulations LIMIT 3"
        sample_job = client.query(sample_query)
        
        for i, row in enumerate(sample_job.result(), 1):
            print(f"   Row {i}:")
            print(f"      Timestamp: {row['timestamp']}")
            print(f"      Location: {row['location']}")
            print(f"      Symptoms: {row['symptoms']}")
            print(f"      Water Contamination: {row['water_contamination']:.2f}")
            print(f"      Temperature: {row['temperature']:.2f}°C")
        
        print("\n✅ Demo outbreak simulation data created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating BigQuery data: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("iLuminara BigQuery Demo Data Creator")
    print("=" * 60)
    print()
    
    success = create_demo_outbreak_data()
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ Setup Complete")
        sys.exit(0)
    else:
        print("⚠️  Setup completed with warnings")
        print("   The deployment can continue, but BigQuery data may not be available")
        sys.exit(0)  # Don't fail the deployment
