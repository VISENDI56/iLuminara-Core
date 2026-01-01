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
Context-Aware Minimizer - PIMS Innovation
Minimizes data collection and processing based on context and necessity.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class ContextAwareMinimizer:
    """Minimizes data handling based on context and privacy requirements."""

    def __init__(self):
        self.data_purposes = {
            'analytics': {'retention_days': 90, 'minimization_level': 'high'},
            'audit': {'retention_days': 2555, 'minimization_level': 'low'},  # 7 years
            'operational': {'retention_days': 30, 'minimization_level': 'medium'}
        }
        self.minimization_log: List[Dict[str, Any]] = []

    def assess_data_necessity(self, data: Dict[str, Any], purpose: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess what data is necessary for the given purpose and context."""
        purpose_config = self.data_purposes.get(purpose, {'retention_days': 30, 'minimization_level': 'medium'})

        # Determine required fields based on purpose
        required_fields = self._get_required_fields(purpose, context)
        optional_fields = [k for k in data.keys() if k not in required_fields]

        assessment = {
            'timestamp': datetime.now().isoformat(),
            'purpose': purpose,
            'context': context,
            'required_fields': required_fields,
            'optional_fields': optional_fields,
            'minimization_recommendations': self._generate_minimization_recommendations(
                data, required_fields, purpose_config['minimization_level']
            ),
            'retention_policy': purpose_config
        }

        self.minimization_log.append(assessment)
        return assessment

    def minimize_data(self, data: Dict[str, Any], assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Minimize the data based on the assessment."""
        minimized_data = {k: v for k, v in data.items() if k in assessment['required_fields']}

        # Apply additional minimization based on recommendations
        for rec in assessment['minimization_recommendations']:
            if rec['action'] == 'anonymize':
                if rec['field'] in minimized_data:
                    minimized_data[rec['field']] = self._anonymize_field(minimized_data[rec['field']])
            elif rec['action'] == 'aggregate':
                if rec['field'] in minimized_data:
                    minimized_data[rec['field']] = self._aggregate_field(minimized_data[rec['field']])

        return minimized_data

    def _get_required_fields(self, purpose: str, context: Dict[str, Any]) -> List[str]:
        """Determine required fields based on purpose and context."""
        base_fields = ['timestamp', 'id']

        if purpose == 'analytics':
            return base_fields + ['category', 'value']
        elif purpose == 'audit':
            return base_fields + ['action', 'user_id', 'result']
        elif purpose == 'operational':
            return base_fields + context.get('required_fields', [])

        return base_fields

    def _generate_minimization_recommendations(self, data: Dict[str, Any], required_fields: List[str], level: str) -> List[Dict[str, Any]]:
        """Generate recommendations for data minimization."""
        recommendations = []

        if level == 'high':
            for field in data.keys():
                if field not in required_fields:
                    recommendations.append({
                        'field': field,
                        'action': 'remove',
                        'reason': 'Not required for purpose'
                    })
        elif level == 'medium':
            # Suggest anonymization for sensitive fields
            sensitive_fields = ['name', 'email', 'phone', 'address']
            for field in data.keys():
                if field in sensitive_fields and field not in required_fields:
                    recommendations.append({
                        'field': field,
                        'action': 'anonymize',
                        'reason': 'Sensitive data minimization'
                    })

        return recommendations

    def _anonymize_field(self, value: Any) -> str:
        """Anonymize a field value."""
        if isinstance(value, str):
            return f"anon_{hash(value) % 10000}"
        return "anonymized"

    def _aggregate_field(self, value: Any) -> Any:
        """Aggregate a field value."""
        if isinstance(value, (int, float)):
            # Round to reduce precision
            return round(value, 1)
        return value

    def get_minimization_report(self) -> Dict[str, Any]:
        """Generate data minimization report."""
        total_assessments = len(self.minimization_log)
        fields_removed = sum(len(a['optional_fields']) for a in self.minimization_log)

        return {
            'total_assessments': total_assessments,
            'fields_minimized': fields_removed,
            'purposes_covered': list(set(a['purpose'] for a in self.minimization_log)),
            'recent_assessments': self.minimization_log[-5:]
        }