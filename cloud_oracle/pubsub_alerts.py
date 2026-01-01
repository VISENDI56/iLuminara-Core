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
PubSub Alert System for iLuminara
═════════════════════════════════════════════════════════════════════════════

Manages real-time alert publication and monitoring using Google Cloud Pub/Sub.

Provides:
1. Alert publication to luminara-alerts topic
2. Alert subscription monitoring
3. Integration with outbreak prediction and voice processing
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import os

try:
    from google.cloud import pubsub_v1
    PUBSUB_AVAILABLE = True
except ImportError:
    PUBSUB_AVAILABLE = False
    logging.warning("google-cloud-pubsub not installed. PubSub features will be simulated.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertPublisher:
    """
    Publisher for real-time health alerts to Google Cloud Pub/Sub.
    
    Publishes alerts when:
    - Z-score exceeds threshold (outbreak detected)
    - Critical symptoms reported via voice
    - Parametric bond triggered
    """
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        topic_name: str = "luminara-alerts"
    ):
        """
        Initialize the alert publisher.
        
        Args:
            project_id: Google Cloud project ID
            topic_name: Pub/Sub topic name
        """
        self.project_id = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT')
        self.topic_name = topic_name
        self.simulation_mode = not PUBSUB_AVAILABLE or not self.project_id
        
        if self.simulation_mode:
            logger.info("PubSub running in SIMULATION MODE (no actual messages published)")
            self.publisher = None
            self.topic_path = f"projects/{self.project_id or 'demo'}/topics/{topic_name}"
        else:
            try:
                self.publisher = pubsub_v1.PublisherClient()
                self.topic_path = self.publisher.topic_path(self.project_id, topic_name)
                logger.info(f"PubSub publisher initialized: {self.topic_path}")
            except Exception as e:
                logger.warning(f"Failed to initialize PubSub publisher: {e}. Using simulation mode.")
                self.simulation_mode = True
                self.publisher = None
    
    def publish_alert(
        self,
        alert_type: str,
        severity: str,
        location: Dict[str, float],
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Publish a health alert to Pub/Sub.
        
        Args:
            alert_type: Type of alert (outbreak, voice_alert, bond_trigger)
            severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW)
            location: GPS coordinates
            data: Alert-specific data
            metadata: Additional metadata
        
        Returns:
            Message ID (or simulation ID)
        """
        # Build alert message
        alert_message = {
            "alert_id": self._generate_alert_id(),
            "alert_type": alert_type,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": location,
            "data": data,
            "metadata": metadata or {},
            "source": "iluminara-core",
            "version": "1.0.0"
        }
        
        # Serialize to JSON
        message_json = json.dumps(alert_message)
        message_bytes = message_json.encode('utf-8')
        
        if self.simulation_mode:
            # Simulate publication
            alert_id = alert_message['alert_id']
            logger.info(f"[SIMULATED] Published alert: {alert_type} (severity: {severity})")
            logger.debug(f"[SIMULATED] Alert data: {message_json}")
            return alert_id
        
        try:
            # Publish to Pub/Sub
            future = self.publisher.publish(
                self.topic_path,
                message_bytes,
                alert_type=alert_type,
                severity=severity
            )
            message_id = future.result()
            
            logger.info(f"Published alert to Pub/Sub: {message_id} ({alert_type}, {severity})")
            return message_id
        
        except Exception as e:
            logger.error(f"Failed to publish alert to Pub/Sub: {e}")
            # Return simulation ID on failure
            return alert_message['alert_id']
    
    def publish_outbreak_alert(
        self,
        prediction_result: Dict[str, Any]
    ) -> str:
        """
        Publish an outbreak prediction alert.
        
        Args:
            prediction_result: Result from outbreak predictor
        
        Returns:
            Message ID
        """
        severity = prediction_result.get('risk_level', 'MEDIUM')
        
        return self.publish_alert(
            alert_type='outbreak_prediction',
            severity=severity,
            location=prediction_result.get('location', {}),
            data={
                'z_score': prediction_result.get('z_score'),
                'disease_likelihood': prediction_result.get('disease_likelihood'),
                'bond_status': prediction_result.get('bond_status'),
                'population_at_risk': prediction_result.get('population_at_risk'),
                'recommendations': prediction_result.get('recommendations')
            },
            metadata={
                'requires_immediate_action': prediction_result.get('requires_immediate_action'),
                'confidence_score': prediction_result.get('confidence_score')
            }
        )
    
    def publish_voice_alert(
        self,
        voice_result: Dict[str, Any]
    ) -> str:
        """
        Publish a voice processing alert.
        
        Args:
            voice_result: Result from voice processor
        
        Returns:
            Message ID
        """
        severity = voice_result.get('alert_level', 'MEDIUM')
        
        return self.publish_alert(
            alert_type='voice_alert',
            severity=severity,
            location=voice_result.get('location', {}),
            data={
                'symptoms': voice_result.get('symptoms'),
                'severity_score': voice_result.get('severity'),
                'transcription': voice_result.get('transcription'),
                'language': voice_result.get('language_detected'),
                'recommendations': voice_result.get('recommendations')
            },
            metadata={
                'source': voice_result.get('source'),
                'processing_time_ms': voice_result.get('processing_time_ms')
            }
        )
    
    def _generate_alert_id(self) -> str:
        """Generate unique alert ID."""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        return f"ALERT-{timestamp}"


class AlertSubscriber:
    """
    Subscriber for monitoring real-time health alerts from Google Cloud Pub/Sub.
    
    Used for monitoring and testing alert delivery.
    """
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        subscription_name: str = "luminara-alerts-subscription"
    ):
        """
        Initialize the alert subscriber.
        
        Args:
            project_id: Google Cloud project ID
            subscription_name: Pub/Sub subscription name
        """
        self.project_id = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT')
        self.subscription_name = subscription_name
        self.simulation_mode = not PUBSUB_AVAILABLE or not self.project_id
        
        if self.simulation_mode:
            logger.info("PubSub Subscriber running in SIMULATION MODE")
            self.subscriber = None
            self.subscription_path = f"projects/{self.project_id or 'demo'}/subscriptions/{subscription_name}"
        else:
            try:
                self.subscriber = pubsub_v1.SubscriberClient()
                self.subscription_path = self.subscriber.subscription_path(
                    self.project_id, subscription_name
                )
                logger.info(f"PubSub subscriber initialized: {self.subscription_path}")
            except Exception as e:
                logger.warning(f"Failed to initialize PubSub subscriber: {e}. Using simulation mode.")
                self.simulation_mode = True
                self.subscriber = None
    
    def pull_alerts(self, max_messages: int = 5) -> list:
        """
        Pull alerts from subscription.
        
        Args:
            max_messages: Maximum number of messages to pull
        
        Returns:
            List of alert messages
        """
        if self.simulation_mode:
            logger.info(f"[SIMULATED] Pulling {max_messages} alerts from subscription")
            # Return simulated alerts for testing
            return [
                {
                    "alert_id": "ALERT-SIMULATED-001",
                    "alert_type": "outbreak_prediction",
                    "severity": "HIGH",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "location": {"lat": 0.512, "lng": 40.3129},
                    "data": {
                        "z_score": 3.2,
                        "bond_status": "ALERT",
                        "population_at_risk": 125000
                    }
                }
            ]
        
        try:
            # Pull messages from Pub/Sub
            response = self.subscriber.pull(
                request={
                    "subscription": self.subscription_path,
                    "max_messages": max_messages
                }
            )
            
            alerts = []
            ack_ids = []
            
            for received_message in response.received_messages:
                # Parse message data
                message_data = json.loads(received_message.message.data.decode('utf-8'))
                alerts.append(message_data)
                ack_ids.append(received_message.ack_id)
            
            # Acknowledge messages
            if ack_ids:
                self.subscriber.acknowledge(
                    request={
                        "subscription": self.subscription_path,
                        "ack_ids": ack_ids
                    }
                )
                logger.info(f"Pulled and acknowledged {len(alerts)} alerts")
            
            return alerts
        
        except Exception as e:
            logger.error(f"Failed to pull alerts from Pub/Sub: {e}")
            return []
    
    def subscribe_streaming(self, callback):
        """
        Subscribe to alerts with streaming (async callback).
        
        Args:
            callback: Function to call when message received
        """
        if self.simulation_mode:
            logger.warning("Streaming subscription not available in simulation mode")
            return
        
        try:
            streaming_pull_future = self.subscriber.subscribe(
                self.subscription_path, callback=callback
            )
            logger.info(f"Listening for alerts on {self.subscription_path}...")
            
            # Keep the main thread alive
            try:
                streaming_pull_future.result()
            except KeyboardInterrupt:
                streaming_pull_future.cancel()
                logger.info("Subscription cancelled")
        
        except Exception as e:
            logger.error(f"Failed to start streaming subscription: {e}")


# Convenience functions
_publisher = None

def get_publisher() -> AlertPublisher:
    """Get or create global alert publisher instance."""
    global _publisher
    if _publisher is None:
        _publisher = AlertPublisher()
    return _publisher


def publish_outbreak_alert(prediction_result: Dict[str, Any]) -> str:
    """Convenience function to publish outbreak alert."""
    publisher = get_publisher()
    return publisher.publish_outbreak_alert(prediction_result)


def publish_voice_alert(voice_result: Dict[str, Any]) -> str:
    """Convenience function to publish voice alert."""
    publisher = get_publisher()
    return publisher.publish_voice_alert(voice_result)
