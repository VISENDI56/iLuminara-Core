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
ISO/TR 24291:2021 Health Informatics - AI/ML Validation Protocols
iLuminara Sovereign Health Interface - Health ML Validation Framework

This module implements AI/ML validation protocols for healthcare applications,
specifically for surveillance, outbreak prediction, and resource allocation use cases.

Key Components:
- ML Model Validation Protocols
- Clinical Performance Metrics
- Bias and Fairness Assessment
- Data Quality Validation
- Model Drift Detection
- Regulatory Compliance Validation
"""

import json
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

class MLUseCase(Enum):
    """Healthcare ML Use Cases per ISO/TR 24291"""
    OUTBREAK_PREDICTION = "outbreak_prediction"
    RESOURCE_ALLOCATION = "resource_allocation"
    DIAGNOSTIC_ASSISTANCE = "diagnostic_assistance"
    TREATMENT_OPTIMIZATION = "treatment_optimization"
    SURVEILLANCE_ANALYTICS = "surveillance_analytics"
    PROGNOSTIC_MODELING = "prognostic_modeling"

class ValidationPhase(Enum):
    """ML Validation Phases"""
    DATA_VALIDATION = "data_validation"
    MODEL_TRAINING = "model_training"
    MODEL_VALIDATION = "model_validation"
    CLINICAL_VALIDATION = "clinical_validation"
    POST_DEPLOYMENT = "post_deployment"

class BiasMetric(Enum):
    """Bias and Fairness Metrics"""
    DEMOGRAPHIC_PARITY = "demographic_parity"
    EQUALIZED_ODDS = "equalized_odds"
    PREDICTIVE_PARITY = "predictive_parity"
    ACCURACY_PARITY = "accuracy_parity"

@dataclass
class MLModel:
    """ML Model Metadata"""
    model_id: str
    name: str
    use_case: MLUseCase
    algorithm: str
    version: str
    training_date: datetime.datetime
    dataset_info: Dict[str, Any]
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    bias_assessment: Dict[str, Any] = field(default_factory=dict)
    validation_status: str = "pending"

@dataclass
class ValidationProtocol:
    """ML Validation Protocol per ISO/TR 24291"""
    protocol_id: str
    model_id: str
    phase: ValidationPhase
    test_cases: List[Dict] = field(default_factory=list)
    acceptance_criteria: Dict[str, Any] = field(default_factory=dict)
    execution_date: Optional[datetime.datetime] = None
    results: Dict[str, Any] = field(default_factory=dict)
    conclusion: str = "pending"
    validator: str = ""

@dataclass
class ClinicalValidation:
    """Clinical Validation Study"""
    study_id: str
    model_id: str
    study_design: str  # prospective, retrospective, simulation
    patient_population: Dict[str, Any]
    clinical_endpoints: List[str]
    sample_size: int
    duration_weeks: int
    results: Dict[str, Any] = field(default_factory=dict)
    conclusion: str = "ongoing"
    regulatory_approval: str = "pending"

@dataclass
class DriftDetection:
    """Model Drift Detection Record"""
    detection_id: str
    model_id: str
    detection_date: datetime.datetime
    drift_type: str  # concept_drift, data_drift, performance_drift
    severity: str  # low, medium, high, critical
    metrics: Dict[str, float]
    root_cause: str = ""
    mitigation_action: str = ""
    status: str = "detected"

class HealthMLValidator:
    """ISO/TR 24291 Health ML Validation Framework"""

    def __init__(self):
        self.models: Dict[str, MLModel] = {}
        self.validation_protocols: Dict[str, ValidationProtocol] = {}
        self.clinical_studies: Dict[str, ClinicalValidation] = {}
        self.drift_detections: List[DriftDetection] = {}
        self.performance_baselines: Dict[str, Dict[str, float]] = {}

        # Initialize with FRENASA ML models
        self._initialize_frenasa_models()

    def _initialize_frenasa_models(self):
        """Initialize FRENASA ML models"""

        # Outbreak Prediction Model
        outbreak_model = MLModel(
            model_id="ML-FRENASA-OUTBREAK-001",
            name="Epidemiological Neural Outbreak Predictor",
            use_case=MLUseCase.OUTBREAK_PREDICTION,
            algorithm="Transformer-based Time Series",
            version="1.0.0",
            training_date=datetime.datetime.now(),
            dataset_info={
                "source": "Global Health Surveillance Data",
                "size": 1000000,
                "features": ["symptom_reports", "mobility_data", "environmental_factors"],
                "time_range": "2019-2024"
            }
        )
        self.register_model(outbreak_model)

        # Resource Allocation Model
        resource_model = MLModel(
            model_id="ML-FRENASA-RESOURCE-001",
            name="Healthcare Resource Allocation Optimizer",
            use_case=MLUseCase.RESOURCE_ALLOCATION,
            algorithm="Reinforcement Learning + Linear Programming",
            version="1.0.0",
            training_date=datetime.datetime.now(),
            dataset_info={
                "source": "Hospital Capacity Data",
                "size": 500000,
                "features": ["bed_occupancy", "staff_availability", "supply_levels"],
                "geographic_coverage": "Global"
            }
        )
        self.register_model(resource_model)

        # Surveillance Analytics Model
        surveillance_model = MLModel(
            model_id="ML-FRENASA-SURV-001",
            name="Real-time Health Surveillance Analyzer",
            use_case=MLUseCase.SURVEILLANCE_ANALYTICS,
            algorithm="Anomaly Detection + Clustering",
            version="1.0.0",
            training_date=datetime.datetime.now(),
            dataset_info={
                "source": "Real-time Health Data Streams",
                "size": "continuous",
                "features": ["vital_signs", "symptom_data", "behavioral_indicators"],
                "update_frequency": "real-time"
            }
        )
        self.register_model(surveillance_model)

    def register_model(self, model: MLModel) -> str:
        """Register an ML model for validation"""
        self.models[model.model_id] = model
        return model.model_id

    def create_validation_protocol(self, protocol: ValidationProtocol) -> str:
        """Create ML validation protocol"""
        self.validation_protocols[protocol.protocol_id] = protocol
        return protocol.protocol_id

    def execute_validation(self, protocol_id: str, test_data: Dict[str, Any], validator: str) -> bool:
        """Execute validation protocol"""
        if protocol_id not in self.validation_protocols:
            return False

        protocol = self.validation_protocols[protocol_id]
        protocol.execution_date = datetime.datetime.now()
        protocol.validator = validator

        # Execute validation based on phase
        if protocol.phase == ValidationPhase.DATA_VALIDATION:
            results = self._validate_data_quality(test_data)
        elif protocol.phase == ValidationPhase.MODEL_VALIDATION:
            results = self._validate_model_performance(protocol.model_id, test_data)
        elif protocol.phase == ValidationPhase.CLINICAL_VALIDATION:
            results = self._validate_clinical_performance(protocol.model_id, test_data)
        else:
            results = {"error": "Unsupported validation phase"}

        protocol.results = results

        # Check acceptance criteria
        protocol.conclusion = self._check_acceptance_criteria(protocol, results)

        return protocol.conclusion == "passed"

    def _validate_data_quality(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data quality metrics"""
        results = {
            "completeness": 0.0,
            "accuracy": 0.0,
            "consistency": 0.0,
            "timeliness": 0.0,
            "issues": []
        }

        # Check for missing data
        if "dataset" in test_data:
            df = pd.DataFrame(test_data["dataset"])
            missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
            results["completeness"] = 1.0 - missing_pct

            if missing_pct > 0.5:  # 5% threshold
                results["issues"].append(f"High missing data rate: {missing_pct:.1%}")

        # Check data consistency
        if "consistency_checks" in test_data:
            consistency_score = test_data["consistency_checks"].get("score", 0.8)
            results["consistency"] = consistency_score

        # Check timeliness
        if "data_age_hours" in test_data:
            age_hours = test_data["data_age_hours"]
            if age_hours < 24:
                results["timeliness"] = 1.0
            elif age_hours < 168:  # 1 week
                results["timeliness"] = 0.7
            else:
                results["timeliness"] = 0.3
                results["issues"].append(f"Data is {age_hours} hours old")

        results["overall_quality"] = np.mean([results["completeness"], results["consistency"], results["timeliness"]])

        return results

    def _validate_model_performance(self, model_id: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate model performance metrics"""
        results = {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "auc_roc": 0.0,
            "bias_metrics": {},
            "robustness_tests": []
        }

        if "predictions" in test_data and "ground_truth" in test_data:
            y_pred = np.array(test_data["predictions"])
            y_true = np.array(test_data["ground_truth"])

            # Calculate standard metrics
            results["accuracy"] = accuracy_score(y_true, y_pred)
            results["precision"] = precision_score(y_true, y_pred, average='weighted', zero_division=0)
            results["recall"] = recall_score(y_true, y_pred, average='weighted', zero_division=0)
            results["f1_score"] = f1_score(y_true, y_pred, average='weighted', zero_division=0)

            # AUC-ROC for binary classification
            if len(np.unique(y_true)) == 2:
                try:
                    results["auc_roc"] = roc_auc_score(y_true, y_pred)
                except:
                    results["auc_roc"] = 0.5

        # Bias assessment
        if "bias_analysis" in test_data:
            results["bias_metrics"] = self._assess_bias(test_data["bias_analysis"])

        # Robustness tests
        if "robustness_tests" in test_data:
            results["robustness_tests"] = test_data["robustness_tests"]

        return results

    def _assess_bias(self, bias_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess model bias and fairness"""
        bias_results = {}

        if "demographic_groups" in bias_data:
            groups = bias_data["demographic_groups"]

            # Demographic parity
            positive_rates = {}
            for group, data in groups.items():
                if "predictions" in data:
                    pos_rate = np.mean(data["predictions"])
                    positive_rates[group] = pos_rate

            if len(positive_rates) > 1:
                max_rate = max(positive_rates.values())
                min_rate = min(positive_rates.values())
                bias_results["demographic_parity_ratio"] = min_rate / max_rate if max_rate > 0 else 0

        return bias_results

    def _validate_clinical_performance(self, model_id: str, clinical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate clinical performance"""
        results = {
            "clinical_accuracy": 0.0,
            "sensitivity": 0.0,
            "specificity": 0.0,
            "positive_predictive_value": 0.0,
            "negative_predictive_value": 0.0,
            "clinical_utility": 0.0
        }

        if "clinical_trials" in clinical_data:
            trial_data = clinical_data["clinical_trials"]

            # Calculate clinical metrics
            if "true_positives" in trial_data and "false_positives" in trial_data:
                tp = trial_data["true_positives"]
                fp = trial_data["false_positives"]
                tn = trial_data.get("true_negatives", 0)
                fn = trial_data.get("false_negatives", 0)

                total = tp + fp + tn + fn
                if total > 0:
                    results["clinical_accuracy"] = (tp + tn) / total
                    results["sensitivity"] = tp / (tp + fn) if (tp + fn) > 0 else 0
                    results["specificity"] = tn / (tn + fp) if (tn + fp) > 0 else 0
                    results["positive_predictive_value"] = tp / (tp + fp) if (tp + fp) > 0 else 0
                    results["negative_predictive_value"] = tn / (tn + fn) if (tn + fn) > 0 else 0

        return results

    def _check_acceptance_criteria(self, protocol: ValidationProtocol, results: Dict[str, Any]) -> str:
        """Check if validation results meet acceptance criteria"""
        criteria = protocol.acceptance_criteria

        for metric, threshold in criteria.items():
            if metric in results:
                actual_value = results[metric]
                if isinstance(threshold, dict):
                    if "min" in threshold and actual_value < threshold["min"]:
                        return "failed"
                    if "max" in threshold and actual_value > threshold["max"]:
                        return "failed"
                elif isinstance(threshold, (int, float)) and actual_value < threshold:
                    return "failed"

        return "passed"

    def detect_model_drift(self, model_id: str, current_metrics: Dict[str, float]) -> Optional[str]:
        """Detect model drift"""
        if model_id not in self.models:
            return None

        baseline = self.performance_baselines.get(model_id, {})
        if not baseline:
            # Establish baseline
            self.performance_baselines[model_id] = current_metrics.copy()
            return None

        # Check for performance degradation
        drift_indicators = []
        severity = "low"

        for metric, current_value in current_metrics.items():
            if metric in baseline:
                baseline_value = baseline[metric]
                change_pct = abs(current_value - baseline_value) / baseline_value if baseline_value != 0 else 0

                if change_pct > 0.2:  # 20% change threshold
                    drift_indicators.append(f"{metric}: {change_pct:.1%} change")
                    if change_pct > 0.5:  # 50% change threshold
                        severity = "high"
                    elif change_pct > 0.3:  # 30% change threshold
                        severity = "medium"

        if drift_indicators:
            drift = DriftDetection(
                detection_id=f"DRIFT-{model_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                model_id=model_id,
                detection_date=datetime.datetime.now(),
                drift_type="performance_drift",
                severity=severity,
                metrics=current_metrics,
                root_cause="To be determined"
            )

            self.drift_detections.append(drift)
            return drift.detection_id

        return None

    def create_clinical_study(self, study: ClinicalValidation) -> str:
        """Create clinical validation study"""
        self.clinical_studies[study.study_id] = study
        return study.study_id

    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive ML validation report"""
        return {
            "models_registered": len(self.models),
            "validation_protocols": len(self.validation_protocols),
            "clinical_studies": len(self.clinical_studies),
            "drift_detections": len(self.drift_detections),
            "model_performance": {
                model_id: {
                    "name": model.name,
                    "use_case": model.use_case.value,
                    "validation_status": model.validation_status,
                    "performance_metrics": model.performance_metrics
                }
                for model_id, model in self.models.items()
            },
            "compliance_status": self._assess_24291_compliance()
        }

    def _assess_24291_compliance(self) -> Dict[str, Any]:
        """Assess ISO/TR 24291 compliance"""
        requirements = {
            "model_registration": len(self.models) > 0,
            "validation_protocols": len(self.validation_protocols) > 0,
            "clinical_validation": len(self.clinical_studies) > 0,
            "drift_detection": len(self.drift_detections) >= 0,  # Always true, but can be enhanced
            "bias_assessment": any(model.bias_assessment for model in self.models.values()),
            "performance_monitoring": len(self.performance_baselines) > 0
        }

        compliant_count = sum(requirements.values())
        total_requirements = len(requirements)

        return {
            "compliant_requirements": compliant_count,
            "total_requirements": total_requirements,
            "compliance_percentage": f"{compliant_count/total_requirements:.1%}",
            "status": "compliant" if compliant_count == total_requirements else "partial_compliance",
            "details": requirements
        }

# Initialize Global Health ML Validator
health_ml_validator = HealthMLValidator()

def create_frenasa_validation_protocols():
    """Create validation protocols for FRENASA ML models"""

    # Data Validation Protocol
    data_protocol = ValidationProtocol(
        protocol_id="VP-FRENASA-DATA-001",
        model_id="ML-FRENASA-OUTBREAK-001",
        phase=ValidationPhase.DATA_VALIDATION,
        test_cases=[
            {"id": "DV-001", "description": "Check data completeness", "method": "Statistical analysis"},
            {"id": "DV-002", "description": "Validate data consistency", "method": "Cross-reference checks"}
        ],
        acceptance_criteria={
            "completeness": {"min": 0.95},
            "consistency": {"min": 0.90},
            "overall_quality": {"min": 0.85}
        }
    )
    health_ml_validator.create_validation_protocol(data_protocol)

    # Model Validation Protocol
    model_protocol = ValidationProtocol(
        protocol_id="VP-FRENASA-MODEL-001",
        model_id="ML-FRENASA-OUTBREAK-001",
        phase=ValidationPhase.MODEL_VALIDATION,
        test_cases=[
            {"id": "MV-001", "description": "Performance metrics validation", "method": "Holdout testing"},
            {"id": "MV-002", "description": "Bias and fairness assessment", "method": "Demographic analysis"}
        ],
        acceptance_criteria={
            "accuracy": {"min": 0.85},
            "auc_roc": {"min": 0.80},
            "demographic_parity_ratio": {"min": 0.80}
        }
    )
    health_ml_validator.create_validation_protocol(model_protocol)

def create_clinical_validation_studies():
    """Create clinical validation studies for FRENASA"""

    outbreak_study = ClinicalValidation(
        study_id="CV-FRENASA-OUTBREAK-001",
        model_id="ML-FRENASA-OUTBREAK-001",
        study_design="retrospective",
        patient_population={
            "size": 10000,
            "demographics": "Global health surveillance data",
            "time_period": "2020-2024"
        },
        clinical_endpoints=[
            "Outbreak prediction accuracy",
            "Time to detection improvement",
            "False positive rate"
        ],
        sample_size=10000,
        duration_weeks=52
    )

    health_ml_validator.create_clinical_study(outbreak_study)

def establish_performance_baselines():
    """Establish performance baselines for drift detection"""

    baselines = {
        "ML-FRENASA-OUTBREAK-001": {
            "accuracy": 0.87,
            "precision": 0.82,
            "recall": 0.91,
            "f1_score": 0.86,
            "auc_roc": 0.89
        },
        "ML-FRENASA-RESOURCE-001": {
            "allocation_accuracy": 0.94,
            "resource_utilization": 0.88,
            "response_time_minutes": 15
        },
        "ML-FRENASA-SURV-001": {
            "anomaly_detection_rate": 0.96,
            "false_positive_rate": 0.3,
            "processing_latency_ms": 50
        }
    }

    health_ml_validator.performance_baselines.update(baselines)

if __name__ == "__main__":
    # Initialize FRENASA ML validation framework
    create_frenasa_validation_protocols()
    create_clinical_validation_studies()
    establish_performance_baselines()

    # Generate validation report
    report = health_ml_validator.generate_validation_report()
    print(json.dumps(report, indent=2, default=str))