#!/usr/bin/env python3
"""
iLuminara Governance Service (Port 5000)
═════════════════════════════════════════════════════════════════════════════

Sovereignty validation and compliance checking service.

Endpoints:
- POST /validate - Validate action against sovereign guardrails
- GET /frameworks - List supported legal frameworks
- GET /health - Health check
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

app = Flask(__name__)
CORS(app)

# Initialize guardrail
guardrail = SovereignGuardrail()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'online',
        'service': 'governance-service',
        'port': 5000,
        'frameworks_loaded': len(guardrail.compliance_matrix),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


@app.route('/frameworks', methods=['GET'])
def list_frameworks():
    """List all supported legal frameworks."""
    frameworks = []
    
    for jurisdiction, rules in guardrail.compliance_matrix.items():
        frameworks.append({
            'jurisdiction': jurisdiction,
            'data_sovereignty_required': rules.get('data_sovereignty_required'),
            'requires_explicit_consent': rules.get('requires_explicit_consent'),
            'retention_max_days': rules.get('retention_max_days')
        })
    
    return jsonify({
        'status': 'success',
        'frameworks': frameworks,
        'total_count': len(frameworks)
    })


@app.route('/validate', methods=['POST'])
def validate_action():
    """
    Validate an action against sovereign guardrails.
    
    Request body:
    {
        "action_type": "Data_Transfer" | "High_Risk_Inference" | "Voice_Processing",
        "payload": {...},
        "jurisdiction": "GDPR_EU" | "KDPA_KE" | "GLOBAL_DEFAULT"
    }
    
    Returns:
    {
        "status": "valid" | "violation",
        "message": "...",
        "legal_citations": [...]
    }
    """
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    action_type = data.get('action_type')
    payload = data.get('payload', {})
    jurisdiction = data.get('jurisdiction', 'GLOBAL_DEFAULT')
    
    if not action_type:
        return jsonify({
            'status': 'error',
            'message': 'action_type is required'
        }), 400
    
    try:
        # Validate action
        guardrail.validate_action(
            action_type=action_type,
            payload=payload,
            jurisdiction=jurisdiction
        )
        
        return jsonify({
            'status': 'valid',
            'message': 'Action complies with sovereignty requirements',
            'action_type': action_type,
            'jurisdiction': jurisdiction,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
    
    except SovereigntyViolationError as e:
        return jsonify({
            'status': 'violation',
            'message': str(e),
            'action_type': action_type,
            'jurisdiction': jurisdiction,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 403
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Validation failed: {str(e)}'
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('API_PORT', 5000))
    print(f"Starting Governance Service on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
