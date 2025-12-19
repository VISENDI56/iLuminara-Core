"""
Google Cloud Function for Real-Time Humanitarian Constraint Checking
═════════════════════════════════════════════════════════════════════════════

This Cloud Function provides serverless, scalable constraint validation
for humanitarian operations. It can be deployed to Cloud Functions and
invoked via HTTP or event triggers.

Deployment:
    gcloud functions deploy humanitarian-constraint-checker \
        --runtime python310 \
        --trigger-http \
        --allow-unauthenticated \
        --entry-point check_humanitarian_constraint \
        --region us-central1
"""

import json
import sys
import os
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from governance_kernel.humanitarian_constraints import (
    CloudFunctionConstraintChecker,
    ConstraintSeverity,
)


# Global instance for performance (reused across invocations)
_constraint_checker = None


def get_constraint_checker():
    """Get or create constraint checker instance."""
    global _constraint_checker
    if _constraint_checker is None:
        _constraint_checker = CloudFunctionConstraintChecker()
    return _constraint_checker


def check_humanitarian_constraint(request):
    """
    Cloud Function entry point for constraint checking.
    
    Request body should be JSON:
    {
        "protocol_id": "PROTO-001",
        "action_data": {
            "priority_level": "HIGH",
            "patient_id": "PAT-12345",
            "medical_severity": "CRITICAL"
        },
        "context": {
            "facility_id": "FAC-001",
            "operator_id": "OP-789"
        }
    }
    
    Response:
    {
        "valid": true/false,
        "protocol_id": "PROTO-001",
        "violation": {...} or null,
        "timestamp": "2025-01-10T12:00:00Z"
    }
    """
    # Handle CORS for web clients
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    # Set CORS headers for main response
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        # Parse request
        request_json = request.get_json(silent=True)
        if not request_json:
            return (
                json.dumps({"error": "Invalid JSON in request body"}),
                400,
                headers
            )
        
        # Extract parameters
        protocol_id = request_json.get('protocol_id')
        action_data = request_json.get('action_data', {})
        context = request_json.get('context', {})
        
        if not protocol_id:
            return (
                json.dumps({"error": "Missing required field: protocol_id"}),
                400,
                headers
            )
        
        # Get checker instance
        checker = get_constraint_checker()
        
        # Perform constraint check
        is_valid, violation = checker.check_constraint(
            protocol_id=protocol_id,
            action_data=action_data,
            context=context,
        )
        
        # Build response
        response = {
            "valid": is_valid,
            "protocol_id": protocol_id,
            "violation": None,
            "timestamp": checker.violation_log[-1].detected_at.isoformat() if violation else None,
        }
        
        if violation:
            response["violation"] = {
                "violation_id": violation.violation_id,
                "severity": violation.severity.value,
                "category": violation.category.value,
                "description": violation.description,
                "affected_entities": violation.affected_entities,
                "remediation_steps": violation.remediation_steps,
            }
        
        status_code = 200 if is_valid else 422  # 422 = Unprocessable Entity
        
        return (json.dumps(response), status_code, headers)
    
    except ValueError as e:
        return (
            json.dumps({"error": str(e)}),
            400,
            headers
        )
    
    except Exception as e:
        return (
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            500,
            headers
        )


def list_protocols(request):
    """
    Cloud Function to list available humanitarian protocols.
    
    Response:
    {
        "protocols": [
            {
                "protocol_id": "PROTO-001",
                "name": "Medical Triage Protocol",
                "category": "Medical Ethics",
                "severity": "CRITICAL"
            },
            ...
        ]
    }
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        checker = get_constraint_checker()
        
        protocols_list = [
            {
                "protocol_id": p.protocol_id,
                "name": p.name,
                "category": p.category.value,
                "severity": p.severity.value,
                "description": p.description,
            }
            for p in checker.protocols.values()
        ]
        
        response = {
            "protocols": protocols_list,
            "count": len(protocols_list),
        }
        
        return (json.dumps(response), 200, headers)
    
    except Exception as e:
        return (
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            500,
            headers
        )


def get_violations(request):
    """
    Cloud Function to retrieve logged violations.
    
    Query parameters:
        - severity: Filter by severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
        - unresolved_only: true/false (default: true)
    
    Response:
    {
        "violations": [
            {
                "violation_id": "VIOLATION-abc123",
                "protocol_id": "PROTO-001",
                "severity": "CRITICAL",
                "description": "...",
                "affected_entities": [...],
                "remediation_steps": [...],
                "detected_at": "2025-01-10T12:00:00Z"
            },
            ...
        ]
    }
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        # Parse query parameters
        severity_str = request.args.get('severity')
        unresolved_only = request.args.get('unresolved_only', 'true').lower() == 'true'
        
        severity = None
        if severity_str:
            try:
                severity = ConstraintSeverity[severity_str.upper()]
            except KeyError:
                return (
                    json.dumps({"error": f"Invalid severity: {severity_str}"}),
                    400,
                    headers
                )
        
        checker = get_constraint_checker()
        violations = checker.get_violations(
            severity=severity,
            unresolved_only=unresolved_only,
        )
        
        violations_list = [
            {
                "violation_id": v.violation_id,
                "protocol_id": v.protocol_id,
                "severity": v.severity.value,
                "category": v.category.value,
                "description": v.description,
                "affected_entities": v.affected_entities,
                "remediation_steps": v.remediation_steps,
                "detected_at": v.detected_at.isoformat(),
                "resolved": v.resolved,
            }
            for v in violations
        ]
        
        response = {
            "violations": violations_list,
            "count": len(violations_list),
        }
        
        return (json.dumps(response), 200, headers)
    
    except Exception as e:
        return (
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            500,
            headers
        )


# ═════════════════════════════════════════════════════════════════════════════
# Cloud Function Endpoints:
#   - check_humanitarian_constraint: Real-time constraint validation
#   - list_protocols: List available humanitarian protocols
#   - get_violations: Retrieve logged constraint violations
#
# Deploy all three functions for complete humanitarian constraint monitoring.
# ═════════════════════════════════════════════════════════════════════════════
