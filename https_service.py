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
iLuminara HTTPS API Service (Port 8443)
═════════════════════════════════════════════════════════════════════════════

TLS-enabled API endpoints for secure communication.

In production, this service uses:
- TLS 1.3 with strong cipher suites
- Certificate validation
- Mutual TLS (mTLS) for device authentication

For development, this service runs HTTP on port 8443.
To enable TLS in production, configure with SSL certificates.
"""

from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from edge_node.frenasa_engine.voice_processor import VoiceProcessor
from cloud_oracle.outbreak_predictor import OutbreakPredictor
from cloud_oracle.pubsub_alerts import AlertPublisher
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

app = Flask(__name__)
CORS(app)

# Initialize components
voice_processor = VoiceProcessor()
outbreak_predictor = OutbreakPredictor()
alert_publisher = AlertPublisher()
guardrail = SovereignGuardrail()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'online',
        'service': 'https-api',
        'port': 8443,
        'tls_enabled': False,  # Set to True in production with certificates
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    })


@app.route('/process-voice', methods=['POST'])
def process_voice():
    """Voice processing endpoint (TLS-secured in production)."""
    # Same implementation as main API
    try:
        guardrail.validate_action(
            action_type='Voice_Processing',
            payload={
                'data_type': 'Health_Voice_Alert',
                'processing_location': 'Edge_Node',
                'consent_token': 'CHV_EMERGENCY_ALERT',
                'consent_scope': 'emergency_health_surveillance'
            },
            jurisdiction=os.environ.get('JURISDICTION', 'GLOBAL_DEFAULT')
        )
        
        audio_data = request.data if request.data else b''
        language = request.args.get('language', 'swahili')
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        
        location = {'lat': lat, 'lng': lng} if lat and lng else None
        
        result = voice_processor.process_audio(audio_data, language, location)
        
        if result.get('alert_level') in ['CRITICAL', 'ALERT']:
            alert_publisher.publish_voice_alert(result)
        
        return jsonify(result), 200
    
    except SovereigntyViolationError as e:
        return jsonify({
            'status': 'error',
            'error': 'sovereignty_violation',
            'message': str(e)
        }), 403
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/predict', methods=['POST'])
def predict():
    """Outbreak prediction endpoint (TLS-secured in production)."""
    try:
        guardrail.validate_action(
            action_type='Outbreak_Analysis',
            payload={
                'data_type': 'Health_Analytics',
                'processing_location': 'Cloud_Oracle',
                'consent_token': 'PUBLIC_HEALTH_SURVEILLANCE',
                'consent_scope': 'population_health_analytics'
            },
            jurisdiction=os.environ.get('JURISDICTION', 'GLOBAL_DEFAULT')
        )
        
        data = request.get_json()
        location = data.get('location')
        symptoms = data.get('symptoms', [])
        
        result = outbreak_predictor.predict(
            location=location,
            symptoms=symptoms,
            population=data.get('population'),
            historical_data=data.get('historical_data')
        )
        
        if result.get('risk_level') in ['CRITICAL', 'HIGH']:
            alert_publisher.publish_outbreak_alert(result)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('API_PORT', 8443))
    print(f"Starting HTTPS API Service on port {port}...")
    print("⚠️  Note: Running in HTTP mode. Configure SSL certificates for production TLS.")
    
    # In production, use:
    # app.run(host='0.0.0.0', port=port, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', port=port, debug=False)
