"""
iLuminara Alert Distributor - Cloud Function
=============================================

Distributes health alerts from iLuminara to multiple channels:
- Slack notifications for team awareness
- Email alerts for healthcare workers
- SMS alerts for emergency response (future)
- Dashboard webhooks for real-time visualization

This function is triggered by Google Cloud Pub/Sub messages published
to the 'luminara-alerts' topic.

Message Format:
    {
        "alert_type": "outbreak|critical|warning|info",
        "severity": "critical|high|medium|low",
        "title": "Alert title",
        "message": "Detailed alert message",
        "location": "Geographic location",
        "timestamp": "ISO 8601 timestamp",
        "metadata": {
            "symptom_count": 10,
            "disease_risk": "cholera",
            "confidence": 0.85
        }
    }
"""

import base64
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", "")


def alert_distributor(event: Dict[str, Any], context: Any) -> None:
    """
    Cloud Function entry point for alert distribution.
    
    Args:
        event: Pub/Sub event containing alert data
        context: Cloud Function context (metadata)
    """
    try:
        # Decode Pub/Sub message
        if "data" not in event:
            logger.error("No data field in event")
            return
        
        message_data = base64.b64decode(event["data"]).decode("utf-8")
        alert = json.loads(message_data)
        
        logger.info(f"Processing alert: {alert.get('alert_type', 'unknown')}")
        
        # Validate alert structure
        if not validate_alert(alert):
            logger.error(f"Invalid alert structure: {alert}")
            return
        
        # Distribute to channels
        results = distribute_alert(alert)
        
        # Log results
        for channel, success in results.items():
            status = "✅" if success else "❌"
            logger.info(f"{status} {channel}: {'Success' if success else 'Failed'}")
        
    except Exception as e:
        logger.error(f"Error processing alert: {str(e)}", exc_info=True)


def validate_alert(alert: Dict[str, Any]) -> bool:
    """
    Validate alert message structure.
    
    Args:
        alert: Alert dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["alert_type", "message"]
    
    for field in required_fields:
        if field not in alert:
            logger.error(f"Missing required field: {field}")
            return False
    
    return True


def distribute_alert(alert: Dict[str, Any]) -> Dict[str, bool]:
    """
    Distribute alert to multiple channels.
    
    Args:
        alert: Alert dictionary
        
    Returns:
        Dictionary with channel names and success status
    """
    results = {}
    
    # Slack notification
    if SLACK_WEBHOOK:
        results["slack"] = send_slack_notification(alert)
    else:
        logger.warning("Slack webhook not configured, skipping Slack notification")
        results["slack"] = False
    
    # Add more channels here (email, SMS, etc.)
    
    return results


def send_slack_notification(alert: Dict[str, Any]) -> bool:
    """
    Send alert to Slack via webhook.
    
    Args:
        alert: Alert dictionary
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Build Slack message
        slack_message = build_slack_message(alert)
        
        # Send to Slack
        response = requests.post(
            SLACK_WEBHOOK,
            json=slack_message,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info("Slack notification sent successfully")
            return True
        else:
            logger.error(f"Slack API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to send Slack notification: {str(e)}")
        return False


def build_slack_message(alert: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build Slack message in Block Kit format.
    
    Args:
        alert: Alert dictionary
        
    Returns:
        Slack message dictionary
    """
    alert_type = alert.get("alert_type", "info")
    severity = alert.get("severity", "low")
    title = alert.get("title", "iLuminara Health Alert")
    message = alert.get("message", "")
    location = alert.get("location", "Unknown")
    timestamp = alert.get("timestamp", datetime.utcnow().isoformat())
    
    # Color coding based on severity
    color_map = {
        "critical": "#FF0000",  # Red
        "high": "#FF6600",      # Orange
        "medium": "#FFCC00",    # Yellow
        "low": "#00CC00",       # Green
    }
    color = color_map.get(severity, "#808080")  # Default gray
    
    # Emoji for alert type
    emoji_map = {
        "outbreak": "🦠",
        "critical": "🚨",
        "warning": "⚠️",
        "info": "ℹ️",
    }
    emoji = emoji_map.get(alert_type, "📢")
    
    # Build message blocks
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{emoji} {title}"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Type:*\n{alert_type.upper()}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Severity:*\n{severity.upper()}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Location:*\n{location}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Time:*\n{timestamp}"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Message:*\n{message}"
            }
        }
    ]
    
    # Add metadata if present
    if "metadata" in alert:
        metadata = alert["metadata"]
        metadata_text = "\n".join([f"• {k}: {v}" for k, v in metadata.items()])
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Additional Details:*\n{metadata_text}"
            }
        })
    
    return {
        "attachments": [
            {
                "color": color,
                "blocks": blocks
            }
        ]
    }


# For local testing
if __name__ == "__main__":
    # Test alert
    test_alert = {
        "alert_type": "outbreak",
        "severity": "critical",
        "title": "Cholera Outbreak Detected",
        "message": "10 cases detected in Dadaab refugee camp. Immediate intervention required.",
        "location": "Dadaab, Kenya",
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {
            "symptom_count": 10,
            "disease_risk": "cholera",
            "confidence": 0.85
        }
    }
    
    # Simulate Pub/Sub event
    test_event = {
        "data": base64.b64encode(json.dumps(test_alert).encode("utf-8"))
    }
    
    print("Testing alert distribution...")
    alert_distributor(test_event, None)
