"""
Unified DSPM Dashboard - Data Security Posture Management
Provides unified dashboard for data security monitoring and management.
"""

from typing import Dict, List, Any
from datetime import datetime
import json


class UnifiedDSPMDashboard:
    """Unified dashboard for Data Security Posture Management."""

    def __init__(self):
        self.security_metrics = {
            'data_encryption': 0.95,
            'access_controls': 0.88,
            'data_classification': 0.92,
            'privacy_compliance': 0.85
        }
        self.alerts: List[Dict[str, Any]] = []
        self.data_assets: Dict[str, Dict[str, Any]] = {}

    def register_data_asset(self, asset_id: str, asset_info: Dict[str, Any]):
        """Register a data asset for monitoring."""
        self.data_assets[asset_id] = {
            'info': asset_info,
            'security_score': self._calculate_security_score(asset_info),
            'last_assessment': datetime.now().isoformat(),
            'risk_level': self._assess_risk(asset_info)
        }

    def _calculate_security_score(self, asset_info: Dict[str, Any]) -> float:
        """Calculate security score for a data asset."""
        # Placeholder scoring logic
        score = 0.5  # Base score

        if asset_info.get('encrypted', False):
            score += 0.2
        if asset_info.get('access_controlled', False):
            score += 0.2
        if asset_info.get('classified', False):
            score += 0.1

        return min(1.0, score)

    def _assess_risk(self, asset_info: Dict[str, Any]) -> str:
        """Assess risk level for a data asset."""
        sensitivity = asset_info.get('sensitivity', 'low')
        if sensitivity == 'high':
            return 'high'
        elif sensitivity == 'medium':
            return 'medium'
        return 'low'

    def generate_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security posture report."""
        total_assets = len(self.data_assets)
        high_risk_assets = len([a for a in self.data_assets.values() if a['risk_level'] == 'high'])
        avg_security_score = sum(a['security_score'] for a in self.data_assets.values()) / total_assets if total_assets > 0 else 0

        return {
            'timestamp': datetime.now().isoformat(),
            'total_assets': total_assets,
            'high_risk_assets': high_risk_assets,
            'average_security_score': avg_security_score,
            'metrics': self.security_metrics,
            'active_alerts': len(self.alerts),
            'assets_summary': [
                {
                    'id': asset_id,
                    'security_score': asset['security_score'],
                    'risk_level': asset['risk_level']
                } for asset_id, asset in self.data_assets.items()
            ]
        }

    def add_security_alert(self, alert: Dict[str, Any]):
        """Add a security alert."""
        alert_entry = {
            'alert_id': f"ALERT-{len(self.alerts) + 1}",
            'timestamp': datetime.now().isoformat(),
            **alert
        }
        self.alerts.append(alert_entry)

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for dashboard visualization."""
        return {
            'security_metrics': self.security_metrics,
            'assets': list(self.data_assets.values()),
            'alerts': self.alerts[-10:],  # Last 10 alerts
            'report': self.generate_security_report()
        }