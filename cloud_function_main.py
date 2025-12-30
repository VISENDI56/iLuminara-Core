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
Google Cloud Function: Ethical Validator
═════════════════════════════════════════════════════════════════

Cloud Function deployment for the Ethical Engine that validates
humanitarian constraints on health system actions.

Deployment:
    gcloud functions deploy ethical-validator \
      --runtime=python310 \
      --trigger-http \
      --allow-unauthenticated \
      --set-env-vars=PROTOCOL_VERSION=2025.1,GCP_PROJECT_ID=iluminara \
      --entry-point=validate_action

Environment Variables:
    - PROTOCOL_VERSION: Version of humanitarian protocols (e.g., 2025.1)
    - GCP_PROJECT_ID: Google Cloud project ID for Secret Manager
"""

import json
import os
from flask import Request, jsonify
from governance_kernel.ethical_engine import EthicalEngine, HumanitarianViolationError


# Initialize the engine (load protocols from Secret Manager if available)
USE_CLOUD_SECRETS = os.environ.get('USE_CLOUD_SECRETS', 'false').lower() == 'true'
engine = EthicalEngine(use_cloud_secrets=USE_CLOUD_SECRETS)


def validate_action(request: Request):
    """
    HTTP Cloud Function entry point for validating humanitarian constraints.
    
    Request Body (JSON):
    {
        "action": {
            "type": "quarantine",
            "scope": "district",
            "estimated_civilian_impact": 0.2,
            "medical_benefit": 0.8,
            "attack_rate": 0.02,
            "r_effective": 1.5,
            "severity_score": 0.6
        },
        "context": {
            "conflict_zone": true,
            "outbreak_suspected": true,
            "civilian_population": 50000,
            "healthcare_capacity": 0.7
        }
    }
    
    Response (JSON):
    {
        "status": "approved" | "rejected",
        "action": {...},
        "humanitarian_margin": {...},
        "constraints_applied": [...],
        "violations": [...],
        "protocol_version": "2025.1"
    }
    
    Args:
        request: Flask Request object
        
    Returns:
        JSON response with validation results
    """
    # Set CORS headers for the response
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        # Parse request
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return jsonify({
                'status': 'error',
                'message': 'Invalid JSON in request body'
            }), 400, headers
        
        action = request_json.get('action')
        context = request_json.get('context', {})
        
        if not action:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: action'
            }), 400, headers
        
        # Apply constraints
        result = engine.apply_constraints(action, context)
        
        # Build response
        response = {
            'status': 'approved' if len(result['violations']) == 0 else 'rejected',
            'action': result['action'],
            'humanitarian_margin': result['humanitarian_margin'],
            'constraints_applied': result['constraints_applied'],
            'violations': result['violations'],
            'protocol_version': os.environ.get('PROTOCOL_VERSION', '2025.1'),
            'context': result['context']
        }
        
        return jsonify(response), 200, headers
        
    except HumanitarianViolationError as e:
        # Humanitarian constraint violated
        return jsonify({
            'status': 'rejected',
            'message': str(e),
            'protocol_version': os.environ.get('PROTOCOL_VERSION', '2025.1')
        }), 403, headers
        
    except Exception as e:
        # Internal error
        return jsonify({
            'status': 'error',
            'message': f'Internal error: {str(e)}',
            'protocol_version': os.environ.get('PROTOCOL_VERSION', '2025.1')
        }), 500, headers


def health_check(request: Request):
    """
    Health check endpoint for monitoring.
    
    Returns:
        JSON response with service status
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    return jsonify({
        'status': 'healthy',
        'service': 'ethical-validator',
        'protocol_version': os.environ.get('PROTOCOL_VERSION', '2025.1'),
        'use_cloud_secrets': USE_CLOUD_SECRETS
    }), 200, headers
