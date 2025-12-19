"""
Cloud Oracle Module - Autonomous Decision-Making System
═════════════════════════════════════════════════════════════════════════════

Implements autonomous decision-making simulation with:
- Active Inference Engine (Bayesian policy optimization)
- Vertex AI Custom Containers (scalable ML inference)
- Cloud Scheduler (automated optimization cycles)
- Pub/Sub (real-time alert distribution)

Philosophy: "Autonomous intelligence. Sovereign control. Continuous learning."
"""

from cloud_oracle.active_inference import (
    ActiveInferenceEngine,
    PolicyType,
    Policy,
    Belief
)

from cloud_oracle.vertex_ai_integration import (
    VertexAIIntegration,
    ContainerConfig,
    InferenceRequest,
    InferenceResponse
)

from cloud_oracle.scheduler_integration import (
    CloudSchedulerIntegration,
    ScheduleFrequency,
    OptimizationCycle,
    ScheduleConfig
)

from cloud_oracle.pubsub_integration import (
    PubSubIntegration,
    Alert,
    AlertType,
    AlertSeverity,
    PubSubTopic,
    Subscription
)

from cloud_oracle.autonomous_decision_maker import (
    AutonomousDecisionMaker,
    SimulationConfig
)

__all__ = [
    # Active Inference
    "ActiveInferenceEngine",
    "PolicyType",
    "Policy",
    "Belief",
    
    # Vertex AI
    "VertexAIIntegration",
    "ContainerConfig",
    "InferenceRequest",
    "InferenceResponse",
    
    # Cloud Scheduler
    "CloudSchedulerIntegration",
    "ScheduleFrequency",
    "OptimizationCycle",
    "ScheduleConfig",
    
    # Pub/Sub
    "PubSubIntegration",
    "Alert",
    "AlertType",
    "AlertSeverity",
    "PubSubTopic",
    "Subscription",
    
    # Orchestrator
    "AutonomousDecisionMaker",
    "SimulationConfig"
]
