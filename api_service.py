"""
iLuminara API Service
═════════════════════════════════════════════════════════════════════════════

Flask-based API service providing:
1. Voice processing endpoint (/process-voice) - FRENASA Engine
2. Outbreak prediction endpoint (/predict) - Cloud Oracle
3. Health monitoring endpoint (/health)

Integrates with Golden Thread, Sovereign Guardrail, and PubSub alerts.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
from typing import Dict, Any
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edge_node.frenasa_engine.voice_processor import VoiceProcessor
from cloud_oracle.outbreak_predictor import OutbreakPredictor
from cloud_oracle.pubsub_alerts import AlertPublisher
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
voice_processor = VoiceProcessor()
outbreak_predictor = OutbreakPredictor()
guardrail = SovereignGuardrail()
alert_publisher = AlertPublisher()

# Application metadata
APP_VERSION = "1.0.0"
NODE_ID = os.environ.get('NODE_ID', 'JOR-47')
JURISDICTION = os.environ.get('JURISDICTION', 'GLOBAL_DEFAULT')


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        JSON response with service status and metadata
    """
    return jsonify({
        "status": "online",
        "service": "iluminara-api",
        "version": APP_VERSION,
        "node_id": NODE_ID,
        "jurisdiction": JURISDICTION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoints": {
            "voice_processing": "/process-voice",
            "outbreak_prediction": "/predict",
            "health": "/health"
        }
    }), 200


@app.route('/process-voice', methods=['POST'])
def process_voice():
    """
    Voice processing endpoint for CHV alerts.
    
    Accepts audio/wav data and converts to structured JSON.
    
    Request:
        - Content-Type: audio/wav or multipart/form-data
        - Body: Binary audio data
        - Optional query params: language, lat, lng
    
    Returns:
        JSON response with structured health alert
    """
    try:
        # Validate sovereignty constraints
        try:
            guardrail.validate_action(
                action_type='Voice_Processing',
                payload={
                    'data_type': 'Health_Voice_Alert',
                    'processing_location': 'Edge_Node'
                },
                jurisdiction=JURISDICTION
            )
        except SovereigntyViolationError as e:
            logger.error(f"Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Get audio data from request
        if request.content_type and 'audio' in request.content_type:
            audio_data = request.data
        elif request.files and 'audio' in request.files:
            audio_file = request.files['audio']
            audio_data = audio_file.read()
        else:
            # For testing: accept any content type
            audio_data = request.data
        
        if not audio_data:
            return jsonify({
                "status": "error",
                "error": "no_audio_data",
                "message": "No audio data provided in request"
            }), 400
        
        # Get optional parameters
        language = request.args.get('language', 'swahili')
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        
        location = None
        if lat is not None and lng is not None:
            location = {'lat': lat, 'lng': lng}
        
        # Process the voice alert
        logger.info(f"Processing voice alert: {len(audio_data)} bytes, language={language}")
        result = voice_processor.process_audio(audio_data, language, location)
        
        # Publish alert to PubSub if critical
        if result.get('alert_level') in ['CRITICAL', 'ALERT']:
            try:
                alert_publisher.publish_voice_alert(result)
                logger.info(f"Published voice alert to PubSub")
            except Exception as pub_error:
                logger.warning(f"Failed to publish alert: {pub_error}")
        
        # Log successful processing
        logger.info(f"Voice processing successful: {result.get('symptoms', [])} detected")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error processing voice: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": "processing_failed",
            "message": str(e)
        }), 500


@app.route('/predict', methods=['POST'])
def predict_outbreak():
    """
    Outbreak prediction endpoint using Z-score analysis.
    
    Accepts location and symptom data, returns outbreak risk assessment.
    
    Request:
        - Content-Type: application/json
        - Body: {
            "location": {"lat": float, "lng": float},
            "symptoms": ["symptom1", "symptom2", ...],
            "population": int (optional),
            "historical_data": [...] (optional)
          }
    
    Returns:
        JSON response with outbreak prediction and recommendations
    """
    try:
        # Validate sovereignty constraints
        try:
            guardrail.validate_action(
                action_type='Outbreak_Analysis',
                payload={
                    'data_type': 'Health_Analytics',
                    'processing_location': 'Cloud_Oracle'
                },
                jurisdiction=JURISDICTION
            )
        except SovereigntyViolationError as e:
            logger.error(f"Sovereignty violation: {e}")
            return jsonify({
                "status": "error",
                "error": "sovereignty_violation",
                "message": str(e)
            }), 403
        
        # Parse request JSON
        if not request.is_json:
            return jsonify({
                "status": "error",
                "error": "invalid_content_type",
                "message": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if 'location' not in data:
            return jsonify({
                "status": "error",
                "error": "missing_location",
                "message": "Location is required (lat, lng)"
            }), 400
        
        if 'symptoms' not in data or not isinstance(data['symptoms'], list):
            return jsonify({
                "status": "error",
                "error": "missing_symptoms",
                "message": "Symptoms list is required"
            }), 400
        
        location = data['location']
        symptoms = data['symptoms']
        population = data.get('population')
        historical_data = data.get('historical_data')
        
        # Validate location format
        if 'lat' not in location or 'lng' not in location:
            # Try 'lon' as alternative to 'lng'
            if 'lon' in location:
                location['lng'] = location['lon']
            else:
                return jsonify({
                    "status": "error",
                    "error": "invalid_location",
                    "message": "Location must have 'lat' and 'lng' fields"
                }), 400
        
        # Perform outbreak prediction
        logger.info(f"Predicting outbreak: location={location}, symptoms={symptoms}")
        result = outbreak_predictor.predict(
            location=location,
            symptoms=symptoms,
            population=population,
            historical_data=historical_data
        )
        
        # Publish alert to PubSub if high risk
        if result.get('risk_level') in ['CRITICAL', 'HIGH']:
            try:
                alert_publisher.publish_outbreak_alert(result)
                logger.info(f"Published outbreak alert to PubSub")
            except Exception as pub_error:
                logger.warning(f"Failed to publish alert: {pub_error}")
        
        # Log prediction result
        logger.info(f"Outbreak prediction complete: Z-score={result['z_score']}, Risk={result['risk_level']}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error predicting outbreak: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": "prediction_failed",
            "message": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "error": "not_found",
        "message": "Endpoint not found",
        "available_endpoints": ["/health", "/process-voice", "/predict"]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({
        "status": "error",
        "error": "internal_server_error",
        "message": "An internal error occurred"
    }), 500


def create_app():
    """Application factory for testing."""
    return app


if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('API_HOST', '0.0.0.0')
    port = int(os.environ.get('API_PORT', 8080))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info("=" * 80)
    logger.info("iLuminara API Service Starting")
    logger.info("=" * 80)
    logger.info(f"Version: {APP_VERSION}")
    logger.info(f"Node ID: {NODE_ID}")
    logger.info(f"Jurisdiction: {JURISDICTION}")
    logger.info(f"Host: {host}:{port}")
    logger.info(f"Debug Mode: {debug}")
    logger.info("=" * 80)
    logger.info("Available Endpoints:")
    logger.info("  GET  /health         - Health check")
    logger.info("  POST /process-voice  - Voice processing (audio/wav)")
    logger.info("  POST /predict        - Outbreak prediction (JSON)")
    logger.info("=" * 80)
    
    # Run the application
    app.run(host=host, port=port, debug=debug)
