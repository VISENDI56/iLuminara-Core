"""
Interoperability & Standards Fortress
Cross-cutting enabler for seamless data exchange and global standards compliance
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import os

try:
    from fhir.resources import Bundle, Patient, Observation
    FHIR_AVAILABLE = True
except ImportError:
    logging.warning("FHIR resources not available - install with: pip install fhir.resources")
    FHIR_AVAILABLE = False
    Bundle = None
    Patient = None
    Observation = None

from governance_kernel.guardrail import SovereignGuardrail

logger = logging.getLogger(__name__)

@dataclass
class MaturityScore:
    """WHO/ITU Digital Health Maturity Model Score"""
    leadership: float
    services: float
    workforce: float
    infrastructure: float
    data_exchange: float
    overall: float

    def to_dict(self) -> Dict[str, float]:
        return {
            'leadership': self.leadership,
            'services': self.services,
            'workforce': self.workforce,
            'infrastructure': self.infrastructure,
            'data_exchange': self.data_exchange,
            'overall': self.overall
        }

class EnterpriseArchitectureBlueprint:
    """Enforce interoperability layers for seamless data exchange"""

    def __init__(self):
        self.guardrail = SovereignGuardrail()
        self.adapters = {}
        self._initialize_adapters()

    def _initialize_adapters(self):
        """Initialize standard adapters"""
        self.adapters = {
            'hl7_fhir': self._fhir_adapter,
            'openhie': self._openhie_adapter,
            'dhis2': self._dhis2_adapter,
            'commcare': self._commcare_adapter,
            'hmis': self._hmis_adapter
        }

    def _fhir_adapter(self, data: Dict[str, Any]) -> Optional[Any]:
        """Convert data to FHIR Bundle format"""
        if not FHIR_AVAILABLE:
            return {"type": "fhir_bundle", "data": data, "status": "fhir_unavailable"}
        
        try:
            bundle = Bundle()
            bundle.type = "collection"
            bundle.entry = []

            # Convert observations
            if 'observations' in data:
                for obs in data['observations']:
                    observation = Observation()
                    observation.status = "final"
                    observation.code = {"text": obs.get('type', 'unknown')}
                    observation.valueQuantity = {
                        "value": obs.get('value'),
                        "unit": obs.get('unit', 'unknown')
                    }
                    bundle.entry.append({"resource": observation})

            return bundle
        except Exception as e:
            logger.error(f"FHIR conversion failed: {e}")
            return None

    def _openhie_adapter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """OpenHIE compliant data transformation"""
        return {
            'header': {
                'source': 'iLuminara-Core',
                'timestamp': data.get('timestamp'),
                'standard': 'OpenHIE'
            },
            'payload': data
        }

    def _dhis2_adapter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """DHIS2 data format adapter"""
        return {
            'dataValues': [
                {
                    'dataElement': item.get('element'),
                    'period': item.get('period'),
                    'orgUnit': item.get('org_unit'),
                    'value': item.get('value')
                } for item in data.get('indicators', [])
            ]
        }

    def _commcare_adapter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """CommCare data transformation"""
        return {
            'form': {
                '@xmlns': 'http://openrosa.org/formdesigner',
                'meta': {
                    'instanceID': data.get('instance_id'),
                    'userID': data.get('user_id')
                },
                'data': data.get('form_data', {})
            }
        }

    def _hmis_adapter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """National HMIS integration"""
        return {
            'facility': data.get('facility_code'),
            'reporting_period': data.get('period'),
            'indicators': data.get('indicators', []),
            'metadata': {
                'source': 'iLuminara-Core',
                'compliance': self.guardrail.check_compliance(data)
            }
        }

    def transform_data(self, data: Dict[str, Any], target_standard: str) -> Optional[Dict[str, Any]]:
        """Transform data to target interoperability standard"""
        if target_standard not in self.adapters:
            logger.error(f"Unknown standard: {target_standard}")
            return None

        try:
            adapter = self.adapters[target_standard]
            transformed = adapter(data)

            # Add compliance metadata
            if isinstance(transformed, dict):
                transformed['_compliance'] = self.guardrail.check_compliance(data)

            logger.info(f"Data transformed to {target_standard} standard")
            return transformed

        except Exception as e:
            logger.error(f"Data transformation failed: {e}")
            return None

class DigitalPublicGoodsIntegrator:
    """Prioritize open-source adapters and global standards"""

    def __init__(self):
        self.public_goods = {}
        self._load_public_goods_registry()

    def _load_public_goods_registry(self):
        """Load registry of approved digital public goods"""
        self.public_goods = {
            'dhis2': {
                'category': 'HMIS',
                'standards': ['HL7 FHIR', 'SDMX-HD'],
                'regions': ['Global'],
                'status': 'active'
            },
            'commcare': {
                'category': 'Mobile Data Collection',
                'standards': ['OpenRosa', 'ODK'],
                'regions': ['Global'],
                'status': 'active'
            },
            'openhim': {
                'category': 'Interoperability Layer',
                'standards': ['OpenHIE'],
                'regions': ['Global'],
                'status': 'active'
            },
            'fhir_server': {
                'category': 'Health Data Exchange',
                'standards': ['HL7 FHIR'],
                'regions': ['Global'],
                'status': 'active'
            }
        }

    def get_adapter_for_region(self, region: str, data_type: str) -> Optional[str]:
        """Recommend appropriate adapter for region and data type"""
        for good, config in self.public_goods.items():
            if region in config['regions'] and data_type in config['category'].lower():
                return good
        return None

    def validate_standards_compliance(self, system: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate system compliance with global standards"""
        if system not in self.public_goods:
            return {'compliant': False, 'reason': 'Unknown system'}

        config = self.public_goods[system]
        compliance_report = {
            'system': system,
            'standards': config['standards'],
            'compliant': True,
            'issues': []
        }

        # Check for required metadata
        required_fields = ['timestamp', 'source', 'data_type']
        for field in required_fields:
            if field not in data:
                compliance_report['compliant'] = False
                compliance_report['issues'].append(f"Missing required field: {field}")

        return compliance_report

class MaturityAssessmentEngine:
    """Embed WHO/ITU digital health maturity model scorer"""

    def __init__(self):
        self.maturity_model = {
            'leadership': ['governance', 'strategy', 'partnerships'],
            'services': ['service_delivery', 'coverage', 'quality'],
            'workforce': ['capacity', 'training', 'retention'],
            'infrastructure': ['connectivity', 'devices', 'power'],
            'data_exchange': ['standards', 'interoperability', 'privacy']
        }

    def assess_maturity(self, assessment_data: Dict[str, Any]) -> MaturityScore:
        """Calculate maturity scores across all dimensions"""
        scores = {}

        for dimension, indicators in self.maturity_model.items():
            dimension_scores = []
            for indicator in indicators:
                if indicator in assessment_data:
                    score = self._calculate_indicator_score(assessment_data[indicator])
                    dimension_scores.append(score)

            scores[dimension] = sum(dimension_scores) / len(dimension_scores) if dimension_scores else 0.0

        overall = sum(scores.values()) / len(scores)

        return MaturityScore(
            leadership=scores['leadership'],
            services=scores['services'],
            workforce=scores['workforce'],
            infrastructure=scores['infrastructure'],
            data_exchange=scores['data_exchange'],
            overall=overall
        )

    def _calculate_indicator_score(self, indicator_data: Dict[str, Any]) -> float:
        """Calculate score for individual maturity indicator"""
        # Simple scoring based on implementation level
        implementation_level = indicator_data.get('implementation_level', 0)
        capacity = indicator_data.get('capacity', 0)
        sustainability = indicator_data.get('sustainability', 0)

        return (implementation_level + capacity + sustainability) / 3.0

    def generate_roadmap(self, current_score: MaturityScore) -> Dict[str, Any]:
        """Generate improvement roadmap based on maturity assessment"""
        roadmap = {
            'current_maturity': current_score.to_dict(),
            'priority_actions': [],
            'timeline': {},
            'resources_needed': []
        }

        # Identify weakest areas
        scores_dict = current_score.to_dict()
        weakest_areas = sorted(scores_dict.items(), key=lambda x: x[1])[:2]

        for area, score in weakest_areas:
            if score < 2.0:
                roadmap['priority_actions'].append(f"Strengthen {area} capabilities")
                roadmap['timeline'][area] = "6-12 months"
                roadmap['resources_needed'].append(f"Training and capacity building for {area}")

        return roadmap

class InteroperabilityFortress:
    """Main orchestrator for interoperability and standards compliance"""

    def __init__(self):
        self.blueprint = EnterpriseArchitectureBlueprint()
        self.integrator = DigitalPublicGoodsIntegrator()
        self.maturity_engine = MaturityAssessmentEngine()

    def ensure_interoperability(self, data: Dict[str, Any], target_systems: List[str]) -> Dict[str, Any]:
        """Ensure data can be exchanged with target systems"""
        results = {}

        for system in target_systems:
            # Get appropriate adapter
            adapter = self.integrator.get_adapter_for_region(
                data.get('region', 'Global'),
                data.get('data_type', 'health')
            )

            if adapter:
                # Transform data
                transformed = self.blueprint.transform_data(data, adapter)
                if transformed:
                    # Validate compliance
                    compliance = self.integrator.validate_standards_compliance(system, transformed)
                    results[system] = {
                        'transformed_data': transformed,
                        'compliance': compliance,
                        'adapter_used': adapter
                    }
                else:
                    results[system] = {'error': 'Transformation failed'}
            else:
                results[system] = {'error': 'No suitable adapter found'}

        return results

    def assess_system_maturity(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete maturity assessment for a health system"""
        maturity_score = self.maturity_engine.assess_maturity(system_data)
        roadmap = self.maturity_engine.generate_roadmap(maturity_score)

        return {
            'maturity_score': maturity_score.to_dict(),
            'improvement_roadmap': roadmap,
            'recommendations': self._generate_recommendations(maturity_score)
        }

    def _generate_recommendations(self, score: MaturityScore) -> List[str]:
        """Generate specific recommendations based on maturity scores"""
        recommendations = []

        if score.overall < 2.0:
            recommendations.append("Establish digital health governance framework")
        if score.data_exchange < 2.0:
            recommendations.append("Implement HL7 FHIR and OpenHIE standards")
        if score.infrastructure < 2.0:
            recommendations.append("Strengthen connectivity and device infrastructure")
        if score.workforce < 2.0:
            recommendations.append("Invest in digital health workforce training")

        return recommendations