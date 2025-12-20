#!/usr/bin/env python3
"""
iLuminara Data Fusion Service (Port 5001)
═════════════════════════════════════════════════════════════════════════════

Golden Thread data fusion engine for merging EMR, CBS, and IDSR streams.

Endpoints:
- POST /fuse - Fuse data from multiple sources
- GET /records - Get fused records
- GET /health - Health check
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from edge_node.sync_protocol.golden_thread import GoldenThread

app = Flask(__name__)
CORS(app)

# Initialize Golden Thread
golden_thread = GoldenThread()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'online',
        'service': 'data-fusion-service',
        'port': 5001,
        'fused_records_count': len(golden_thread.fused_records),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


@app.route('/fuse', methods=['POST'])
def fuse_data():
    """
    Fuse data from multiple surveillance sources.
    
    Request body:
    {
        "cbs_signal": {
            "location": "Nairobi",
            "symptom": "fever",
            "timestamp": "2025-01-10T10:00Z"
        },
        "emr_record": {
            "location": "Nairobi",
            "diagnosis": "malaria",
            "timestamp": "2025-01-10T09:45Z"
        },
        "patient_id": "PATIENT_12345"
    }
    
    Returns:
    {
        "status": "success",
        "record_id": "...",
        "verification_score": 1.0,
        "canonical_data": {...}
    }
    """
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    cbs_signal = data.get('cbs_signal')
    emr_record = data.get('emr_record')
    idsr_template = data.get('idsr_template')
    patient_id = data.get('patient_id', 'UNKNOWN')
    
    try:
        # Fuse data streams
        fused_record = golden_thread.fuse_data_streams(
            cbs_signal=cbs_signal,
            emr_record=emr_record,
            idsr_template=idsr_template,
            patient_id=patient_id
        )
        
        return jsonify({
            'status': 'success',
            'record': fused_record.to_dict(),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Fusion failed: {str(e)}'
        }), 500


@app.route('/records', methods=['GET'])
def get_records():
    """
    Get all fused records.
    
    Query parameters:
    - patient_id: Filter by patient ID
    - limit: Maximum number of records to return (default: 100)
    """
    patient_id = request.args.get('patient_id')
    limit = int(request.args.get('limit', 100))
    
    records = []
    
    if patient_id:
        # Get records for specific patient
        if patient_id in golden_thread.fused_records:
            records = golden_thread.fused_records[patient_id][:limit]
    else:
        # Get all records (limited)
        for pid, patient_records in golden_thread.fused_records.items():
            records.extend(patient_records)
            if len(records) >= limit:
                break
        records = records[:limit]
    
    return jsonify({
        'status': 'success',
        'records': [r.to_dict() for r in records],
        'count': len(records),
        'total_patients': len(golden_thread.fused_records)
    })


if __name__ == '__main__':
    port = int(os.environ.get('API_PORT', 5001))
    print(f"Starting Data Fusion Service on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
