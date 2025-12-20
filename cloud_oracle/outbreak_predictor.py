"""
Outbreak Prediction Module for Cloud Oracle
═════════════════════════════════════════════════════════════════════════════

Predicts outbreak risk based on location and symptom data using Z-score analysis
and parametric bond trigger mechanisms.

Integrates with the Golden Thread for data fusion and sovereignty compliance.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutbreakPredictor:
    """
    Outbreak prediction engine using Z-score analysis and historical baseline.
    
    Implements the parametric bond trigger mechanism:
    - Z-score > 2.576 (99% confidence) triggers PAYOUT_RELEASED
    - Analyzes symptom clusters and geographic patterns
    """
    
    def __init__(self):
        """Initialize the outbreak predictor with baseline data."""
        self.baseline_cases_per_day = 5.0  # Historical average
        self.baseline_std = 2.0  # Standard deviation
        self.z_threshold_warning = 1.96  # 95% confidence
        self.z_threshold_critical = 2.576  # 99% confidence
        
        # High-risk symptom patterns for different diseases
        self.disease_signatures = {
            'cholera': {
                'symptoms': ['diarrhea', 'vomiting', 'dehydration'],
                'weight': 0.9,
                'baseline_rate': 0.001  # 0.1% baseline
            },
            'malaria': {
                'symptoms': ['fever', 'headache', 'body_ache'],
                'weight': 0.7,
                'baseline_rate': 0.05  # 5% baseline in endemic areas
            },
            'measles': {
                'symptoms': ['fever', 'cough', 'rash'],
                'weight': 0.8,
                'baseline_rate': 0.002
            },
            'typhoid': {
                'symptoms': ['fever', 'headache', 'body_ache', 'diarrhea'],
                'weight': 0.75,
                'baseline_rate': 0.003
            }
        }
        
        # Known outbreak zones (can be loaded from database)
        self.outbreak_zones = []
    
    def predict(
        self,
        location: Dict[str, float],
        symptoms: List[str],
        population: Optional[int] = None,
        historical_data: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Predict outbreak risk based on location and symptoms.
        
        Args:
            location: GPS coordinates {'lat': float, 'lng': float}
            symptoms: List of symptoms reported
            population: Population in the area (optional)
            historical_data: Historical case data for the area (optional)
        
        Returns:
            Outbreak prediction with risk score, Z-score, and recommendations
        """
        prediction_start = datetime.utcnow()
        
        # Identify potential diseases based on symptoms
        disease_matches = self._match_disease_signatures(symptoms)
        
        # Calculate Z-score based on current vs historical
        z_score = self._calculate_z_score(
            current_symptoms=symptoms,
            location=location,
            historical_data=historical_data
        )
        
        # Assess outbreak risk level
        risk_level = self._assess_risk_level(z_score, disease_matches)
        
        # Determine parametric bond status
        bond_status = self._evaluate_bond_status(z_score)
        
        # Generate geographic risk assessment
        geographic_risk = self._assess_geographic_risk(location, disease_matches)
        
        # Build prediction result
        result = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "processing_time_ms": (datetime.utcnow() - prediction_start).total_seconds() * 1000,
            "location": location,
            "location_name": self._get_location_name(location),
            "symptoms_analyzed": symptoms,
            "disease_likelihood": disease_matches,
            "z_score": round(z_score, 2),
            "risk_level": risk_level,
            "bond_status": bond_status,
            "alert_level": self._determine_alert_level(z_score),
            "geographic_risk": geographic_risk,
            "population_at_risk": population or self._estimate_population(location),
            "recommendations": self._generate_recommendations(z_score, disease_matches, risk_level),
            "confidence_score": self._calculate_confidence(z_score, len(symptoms)),
            "requires_immediate_action": z_score >= self.z_threshold_critical
        }
        
        logger.info(f"Outbreak prediction: Z-score {z_score:.2f}, Risk: {risk_level}, Bond: {bond_status}")
        
        return result
    
    def _match_disease_signatures(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """
        Match reported symptoms against known disease signatures.
        
        Args:
            symptoms: List of reported symptoms
        
        Returns:
            List of disease matches with confidence scores
        """
        matches = []
        symptoms_set = set(symptoms)
        
        for disease, signature in self.disease_signatures.items():
            signature_symptoms = set(signature['symptoms'])
            
            # Calculate Jaccard similarity
            intersection = symptoms_set.intersection(signature_symptoms)
            union = symptoms_set.union(signature_symptoms)
            
            if len(intersection) > 0:
                similarity = len(intersection) / len(union)
                confidence = similarity * signature['weight']
                
                matches.append({
                    'disease': disease,
                    'confidence': round(confidence, 3),
                    'matching_symptoms': list(intersection),
                    'baseline_rate': signature['baseline_rate']
                })
        
        # Sort by confidence descending
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        
        return matches
    
    def _calculate_z_score(
        self,
        current_symptoms: List[str],
        location: Dict[str, float],
        historical_data: Optional[List[Dict]] = None
    ) -> float:
        """
        Calculate Z-score for outbreak detection.
        
        Z-score = (observed - expected) / standard_deviation
        
        Args:
            current_symptoms: Current symptoms reported
            location: Geographic location
            historical_data: Historical case data
        
        Returns:
            Z-score value
        """
        # Simulate current case count (in production, query from database)
        current_cases = len(current_symptoms) * 2  # Rough multiplier
        
        # Use historical data if provided, otherwise use baseline
        if historical_data and len(historical_data) > 0:
            baseline_mean = sum(h.get('cases', 0) for h in historical_data) / len(historical_data)
            baseline_std = self._calculate_std(historical_data)
        else:
            baseline_mean = self.baseline_cases_per_day
            baseline_std = self.baseline_std
        
        # Calculate Z-score
        if baseline_std > 0:
            z_score = (current_cases - baseline_mean) / baseline_std
        else:
            z_score = 0.0
        
        # Boost Z-score if high-risk symptoms present
        high_risk_symptoms = {'diarrhea', 'vomiting', 'dehydration'}
        if high_risk_symptoms.intersection(set(current_symptoms)):
            z_score *= 1.5
        
        return max(0, z_score)  # Non-negative
    
    def _calculate_std(self, historical_data: List[Dict]) -> float:
        """Calculate standard deviation from historical data."""
        if len(historical_data) < 2:
            return self.baseline_std
        
        cases = [h.get('cases', 0) for h in historical_data]
        mean = sum(cases) / len(cases)
        variance = sum((x - mean) ** 2 for x in cases) / len(cases)
        
        return math.sqrt(variance)
    
    def _assess_risk_level(self, z_score: float, disease_matches: List[Dict]) -> str:
        """
        Assess overall risk level based on Z-score and disease matches.
        
        Args:
            z_score: Calculated Z-score
            disease_matches: Matched disease signatures
        
        Returns:
            Risk level: CRITICAL, HIGH, MEDIUM, LOW
        """
        if z_score >= self.z_threshold_critical:
            return "CRITICAL"
        elif z_score >= self.z_threshold_warning:
            return "HIGH"
        elif z_score >= 1.0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _evaluate_bond_status(self, z_score: float) -> str:
        """
        Evaluate parametric bond status based on Z-score.
        
        Args:
            z_score: Calculated Z-score
        
        Returns:
            Bond status: PAYOUT_RELEASED, ALERT, LOCKED
        """
        if z_score >= self.z_threshold_critical:
            return "PAYOUT_RELEASED"
        elif z_score >= self.z_threshold_warning:
            return "ALERT"
        else:
            return "LOCKED"
    
    def _determine_alert_level(self, z_score: float) -> str:
        """Determine alert level for response coordination."""
        if z_score >= 4.0:
            return "RED"
        elif z_score >= self.z_threshold_critical:
            return "ORANGE"
        elif z_score >= self.z_threshold_warning:
            return "YELLOW"
        else:
            return "GREEN"
    
    def _assess_geographic_risk(self, location: Dict[str, float], disease_matches: List[Dict]) -> Dict[str, Any]:
        """
        Assess geographic risk factors.
        
        Args:
            location: GPS coordinates
            disease_matches: Disease matches
        
        Returns:
            Geographic risk assessment
        """
        # Check if location is in known outbreak zone
        in_outbreak_zone = any(
            self._calculate_distance(location, zone.get('location', {})) < 50  # within 50km
            for zone in self.outbreak_zones
        )
        
        # Check proximity to high-risk areas (refugee camps, urban centers)
        # Dadaab coordinates: approximately (0.05, 40.31)
        dadaab_center = {'lat': 0.0512, 'lng': 40.3129}
        distance_to_dadaab = self._calculate_distance(location, dadaab_center)
        
        return {
            'in_known_outbreak_zone': in_outbreak_zone,
            'distance_to_high_risk_area_km': round(distance_to_dadaab, 1),
            'risk_factors': [
                'High population density' if distance_to_dadaab < 10 else None,
                'Limited water/sanitation' if distance_to_dadaab < 20 else None,
                'Refugee camp proximity' if distance_to_dadaab < 50 else None
            ]
        }
    
    def _calculate_distance(self, loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula.
        
        Args:
            loc1: First location with 'lat' and 'lng'
            loc2: Second location with 'lat' and 'lng'
        
        Returns:
            Distance in kilometers
        """
        if not loc1 or not loc2 or 'lat' not in loc1 or 'lat' not in loc2:
            return 999999  # Very large distance if coordinates invalid
        
        # Earth radius in km
        R = 6371
        
        # Convert to radians
        lat1 = math.radians(loc1['lat'])
        lat2 = math.radians(loc2['lat'])
        dlat = math.radians(loc2['lat'] - loc1['lat'])
        dlng = math.radians(loc2.get('lng', loc2.get('lon', 0)) - loc1.get('lng', loc1.get('lon', 0)))
        
        # Haversine formula
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _get_location_name(self, location: Dict[str, float]) -> str:
        """Get human-readable location name from coordinates."""
        # In production, use reverse geocoding API
        # For demo, check if near Dadaab
        dadaab_center = {'lat': 0.0512, 'lng': 40.3129}
        distance = self._calculate_distance(location, dadaab_center)
        
        if distance < 10:
            return "Dadaab Refugee Complex, Kenya"
        elif distance < 50:
            return "Near Dadaab, Kenya"
        else:
            return f"Location: {location['lat']:.4f}, {location.get('lng', location.get('lon', 0)):.4f}"
    
    def _estimate_population(self, location: Dict[str, float]) -> int:
        """Estimate population at risk based on location."""
        # In production, query from population database
        # For demo, estimate based on proximity to Dadaab
        dadaab_center = {'lat': 0.0512, 'lng': 40.3129}
        distance = self._calculate_distance(location, dadaab_center)
        
        if distance < 5:
            return 125000  # Ifo Camp population
        elif distance < 10:
            return 89000  # Average camp population
        elif distance < 20:
            return 35000
        else:
            return 10000
    
    def _generate_recommendations(
        self,
        z_score: float,
        disease_matches: List[Dict],
        risk_level: str
    ) -> List[str]:
        """
        Generate actionable recommendations based on prediction.
        
        Args:
            z_score: Z-score value
            disease_matches: Disease match results
            risk_level: Overall risk level
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if z_score >= self.z_threshold_critical:
            recommendations.append("CRITICAL: Activate emergency outbreak response protocol")
            recommendations.append("Notify WHO and Ministry of Health immediately")
            recommendations.append("Deploy rapid response team within 24 hours")
            recommendations.append("Establish isolation facilities")
            recommendations.append("Initiate mass vaccination/prophylaxis if applicable")
        
        elif z_score >= self.z_threshold_warning:
            recommendations.append("HIGH ALERT: Increase surveillance in affected area")
            recommendations.append("Pre-position medical supplies and personnel")
            recommendations.append("Conduct community health education")
            recommendations.append("Establish coordination with local health facilities")
        
        elif z_score >= 1.0:
            recommendations.append("WATCH: Monitor situation closely")
            recommendations.append("Review and update outbreak response plan")
            recommendations.append("Ensure adequate stockpiles of essential medicines")
        
        else:
            recommendations.append("Continue routine surveillance")
            recommendations.append("Maintain standard infection control measures")
        
        # Disease-specific recommendations
        if disease_matches and len(disease_matches) > 0:
            top_disease = disease_matches[0]['disease']
            
            if top_disease == 'cholera':
                recommendations.append("Priority: Ensure safe water supply")
                recommendations.append("Distribute ORS and zinc supplements")
                recommendations.append("Chlorinate water sources")
            
            elif top_disease == 'malaria':
                recommendations.append("Distribute insecticide-treated bed nets")
                recommendations.append("Ensure availability of antimalarial drugs")
                recommendations.append("Conduct indoor residual spraying if indicated")
            
            elif top_disease == 'measles':
                recommendations.append("Conduct emergency measles vaccination campaign")
                recommendations.append("Ensure vitamin A supplementation")
        
        return recommendations
    
    def _calculate_confidence(self, z_score: float, symptom_count: int) -> float:
        """
        Calculate confidence score for the prediction.
        
        Args:
            z_score: Z-score value
            symptom_count: Number of symptoms reported
        
        Returns:
            Confidence score (0-1)
        """
        # Base confidence on Z-score magnitude
        z_confidence = min(1.0, z_score / 5.0)
        
        # Adjust for symptom count (more symptoms = higher confidence)
        symptom_confidence = min(1.0, symptom_count / 5.0)
        
        # Combined confidence
        confidence = (z_confidence * 0.7) + (symptom_confidence * 0.3)
        
        return round(confidence, 3)


def predict_outbreak(
    location: Dict[str, float],
    symptoms: List[str],
    population: Optional[int] = None,
    historical_data: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Convenience function to predict outbreak risk.
    
    Args:
        location: GPS coordinates
        symptoms: List of symptoms
        population: Population in the area
        historical_data: Historical case data
    
    Returns:
        Outbreak prediction result
    """
    predictor = OutbreakPredictor()
    return predictor.predict(location, symptoms, population, historical_data)
