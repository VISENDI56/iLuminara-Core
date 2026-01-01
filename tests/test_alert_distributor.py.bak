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
Tests for Alert Distributor Cloud Function
"""

import unittest
import json
import base64
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gcp.cloud_functions.alert_distributor.main import (
    validate_alert,
    distribute_alert,
    send_slack_notification,
    build_slack_message,
    alert_distributor
)


class TestAlertValidation(unittest.TestCase):
    """Test cases for alert validation"""
    
    def test_validate_alert_valid(self):
        """Test validation with valid alert"""
        alert = {
            "alert_type": "outbreak",
            "message": "Test message",
            "severity": "critical"
        }
        
        self.assertTrue(validate_alert(alert))
    
    def test_validate_alert_missing_type(self):
        """Test validation with missing alert_type"""
        alert = {
            "message": "Test message"
        }
        
        self.assertFalse(validate_alert(alert))
    
    def test_validate_alert_missing_message(self):
        """Test validation with missing message"""
        alert = {
            "alert_type": "outbreak"
        }
        
        self.assertFalse(validate_alert(alert))
    
    def test_validate_alert_empty(self):
        """Test validation with empty alert"""
        alert = {}
        
        self.assertFalse(validate_alert(alert))


class TestSlackMessageBuilder(unittest.TestCase):
    """Test cases for Slack message formatting"""
    
    def test_build_slack_message_basic(self):
        """Test building basic Slack message"""
        alert = {
            "alert_type": "outbreak",
            "severity": "critical",
            "title": "Test Alert",
            "message": "Test message",
            "location": "Nairobi",
            "timestamp": "2025-12-19T10:00:00Z"
        }
        
        message = build_slack_message(alert)
        
        self.assertIn("attachments", message)
        self.assertEqual(len(message["attachments"]), 1)
        
        attachment = message["attachments"][0]
        self.assertIn("color", attachment)
        self.assertIn("blocks", attachment)
    
    def test_build_slack_message_with_metadata(self):
        """Test building Slack message with metadata"""
        alert = {
            "alert_type": "outbreak",
            "severity": "critical",
            "title": "Test Alert",
            "message": "Test message",
            "location": "Nairobi",
            "timestamp": "2025-12-19T10:00:00Z",
            "metadata": {
                "symptom_count": 10,
                "disease_risk": "cholera",
                "confidence": 0.85
            }
        }
        
        message = build_slack_message(alert)
        attachment = message["attachments"][0]
        
        # Should have metadata block
        self.assertGreaterEqual(len(attachment["blocks"]), 3)
    
    def test_build_slack_message_color_coding(self):
        """Test color coding based on severity"""
        severities = {
            "critical": "#FF0000",
            "high": "#FF6600",
            "medium": "#FFCC00",
            "low": "#00CC00"
        }
        
        for severity, expected_color in severities.items():
            alert = {
                "alert_type": "info",
                "severity": severity,
                "title": "Test",
                "message": "Test"
            }
            
            message = build_slack_message(alert)
            actual_color = message["attachments"][0]["color"]
            
            self.assertEqual(actual_color, expected_color)
    
    def test_build_slack_message_emoji(self):
        """Test emoji selection based on alert type"""
        alert_types = ["outbreak", "critical", "warning", "info"]
        
        for alert_type in alert_types:
            alert = {
                "alert_type": alert_type,
                "severity": "low",
                "title": "Test",
                "message": "Test"
            }
            
            message = build_slack_message(alert)
            header = message["attachments"][0]["blocks"][0]
            
            # Header should contain emoji
            self.assertIn("type", header)
            self.assertEqual(header["type"], "header")


class TestSlackNotification(unittest.TestCase):
    """Test cases for Slack notification sending"""
    
    @patch('gcp.cloud_functions.alert_distributor.main.SLACK_WEBHOOK', 'https://hooks.slack.com/test')
    @patch('gcp.cloud_functions.alert_distributor.main.requests.post')
    def test_send_slack_notification_success(self, mock_post):
        """Test successful Slack notification"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        alert = {
            "alert_type": "test",
            "message": "Test message"
        }
        
        result = send_slack_notification(alert)
        
        self.assertTrue(result)
        mock_post.assert_called_once()
    
    @patch('gcp.cloud_functions.alert_distributor.main.SLACK_WEBHOOK', 'https://hooks.slack.com/test')
    @patch('gcp.cloud_functions.alert_distributor.main.requests.post')
    def test_send_slack_notification_failure(self, mock_post):
        """Test failed Slack notification"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server error"
        mock_post.return_value = mock_response
        
        alert = {
            "alert_type": "test",
            "message": "Test message"
        }
        
        result = send_slack_notification(alert)
        
        self.assertFalse(result)
    
    @patch('gcp.cloud_functions.alert_distributor.main.SLACK_WEBHOOK', 'https://hooks.slack.com/test')
    @patch('gcp.cloud_functions.alert_distributor.main.requests.post')
    def test_send_slack_notification_exception(self, mock_post):
        """Test Slack notification with exception"""
        mock_post.side_effect = Exception("Network error")
        
        alert = {
            "alert_type": "test",
            "message": "Test message"
        }
        
        result = send_slack_notification(alert)
        
        self.assertFalse(result)


class TestAlertDistribution(unittest.TestCase):
    """Test cases for alert distribution"""
    
    @patch('gcp.cloud_functions.alert_distributor.main.SLACK_WEBHOOK', 'https://hooks.slack.com/test')
    @patch('gcp.cloud_functions.alert_distributor.main.send_slack_notification')
    def test_distribute_alert_with_slack(self, mock_slack):
        """Test alert distribution with Slack enabled"""
        mock_slack.return_value = True
        
        alert = {
            "alert_type": "test",
            "message": "Test message"
        }
        
        results = distribute_alert(alert)
        
        self.assertIn("slack", results)
        self.assertTrue(results["slack"])
        mock_slack.assert_called_once_with(alert)
    
    @patch('gcp.cloud_functions.alert_distributor.main.SLACK_WEBHOOK', '')
    def test_distribute_alert_no_slack(self):
        """Test alert distribution without Slack webhook"""
        alert = {
            "alert_type": "test",
            "message": "Test message"
        }
        
        results = distribute_alert(alert)
        
        self.assertIn("slack", results)
        self.assertFalse(results["slack"])


class TestCloudFunctionEntryPoint(unittest.TestCase):
    """Test cases for Cloud Function entry point"""
    
    @patch('gcp.cloud_functions.alert_distributor.main.distribute_alert')
    def test_alert_distributor_valid_event(self, mock_distribute):
        """Test alert_distributor with valid event"""
        mock_distribute.return_value = {"slack": True}
        
        alert = {
            "alert_type": "test",
            "message": "Test message"
        }
        
        # Create Pub/Sub event
        event = {
            "data": base64.b64encode(json.dumps(alert).encode("utf-8"))
        }
        
        # Should not raise exception
        alert_distributor(event, None)
        
        mock_distribute.assert_called_once()
    
    def test_alert_distributor_no_data(self):
        """Test alert_distributor with missing data field"""
        event = {}
        
        # Should not raise exception
        alert_distributor(event, None)
    
    def test_alert_distributor_invalid_json(self):
        """Test alert_distributor with invalid JSON"""
        event = {
            "data": base64.b64encode(b"invalid json")
        }
        
        # Should not raise exception
        alert_distributor(event, None)


if __name__ == "__main__":
    unittest.main()
