"""
Autonomous Decision-Making Orchestrator
═════════════════════════════════════════════════════════════════════════════

Orchestrates the complete autonomous decision-making simulation system:
- Active Inference Engine (decision-making)
- Vertex AI Custom Containers (scalable inference)
- Cloud Scheduler (policy optimization cycles)
- Pub/Sub (real-time alert distribution)

Philosophy: "Autonomous intelligence. Sovereign control. Continuous learning."
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field

from cloud_oracle.active_inference import (
    ActiveInferenceEngine,
    PolicyType,
    Policy
)
from cloud_oracle.vertex_ai_integration import (
    VertexAIIntegration,
    ContainerConfig
)
from cloud_oracle.scheduler_integration import (
    CloudSchedulerIntegration,
    ScheduleFrequency
)
from cloud_oracle.pubsub_integration import (
    PubSubIntegration,
    Alert,
    AlertType,
    AlertSeverity
)


@dataclass
class SimulationConfig:
    """
    Configuration for the autonomous decision-making simulation.
    """
    project_id: str
    region: str = "us-central1"
    enable_vertex_ai: bool = True
    enable_scheduler: bool = True
    enable_pubsub: bool = True
    enable_compliance_validation: bool = True
    optimization_frequency: ScheduleFrequency = ScheduleFrequency.EVERY_6_HOURS
    alert_severity_threshold: AlertSeverity = AlertSeverity.MEDIUM
    jurisdiction: str = "GLOBAL_DEFAULT"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize configuration."""
        return {
            "project_id": self.project_id,
            "region": self.region,
            "enable_vertex_ai": self.enable_vertex_ai,
            "enable_scheduler": self.enable_scheduler,
            "enable_pubsub": self.enable_pubsub,
            "enable_compliance_validation": self.enable_compliance_validation,
            "optimization_frequency": self.optimization_frequency.value,
            "alert_severity_threshold": self.alert_severity_threshold.value,
            "jurisdiction": self.jurisdiction
        }


class AutonomousDecisionMaker:
    """
    Orchestrates autonomous decision-making simulation.
    
    Integrates:
    1. Active Inference Engine - Makes optimal policy decisions
    2. Vertex AI - Scales inference across cloud infrastructure
    3. Cloud Scheduler - Automates regular optimization cycles
    4. Pub/Sub - Distributes alerts in real-time
    
    Usage:
        # Initialize system
        config = SimulationConfig(
            project_id="iluminara-prod",
            region="us-central1"
        )
        
        decision_maker = AutonomousDecisionMaker(config)
        decision_maker.initialize()
        
        # Process observations and generate policy
        observations = {
            'cases': 45,
            'trend': 'increasing',
            'location': 'Nairobi'
        }
        
        result = decision_maker.process_and_decide(
            policy_type=PolicyType.OUTBREAK_RESPONSE,
            observations=observations
        )
        
        # Result includes optimized policy and alert distribution
        print(f"Policy: {result['policy']}")
        print(f"Alerts sent: {result['alerts_sent']}")
    """
    
    def __init__(self, config: SimulationConfig):
        """
        Initialize the autonomous decision maker.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        
        # Core components
        self.inference_engine = ActiveInferenceEngine(learning_rate=0.1)
        
        # Cloud integrations
        self.vertex_ai: Optional[VertexAIIntegration] = None
        self.scheduler: Optional[CloudSchedulerIntegration] = None
        self.pubsub: Optional[PubSubIntegration] = None
        
        # State
        self.initialized = False
        self.vertex_endpoint_id: Optional[str] = None
        self.schedule_ids: Dict[str, str] = {}
        self.topic_ids: Dict[str, str] = {}
        
        # Metrics
        self.decision_count = 0
        self.alert_count = 0
        self.optimization_cycles = 0
        
    def initialize(self):
        """
        Initialize all components and deploy infrastructure.
        
        Steps:
        1. Initialize Vertex AI integration
        2. Deploy custom container
        3. Create Cloud Scheduler jobs
        4. Create Pub/Sub topics and subscriptions
        5. Register optimization handlers
        """
        if self.initialized:
            return
        
        # Initialize Vertex AI
        if self.config.enable_vertex_ai:
            self._initialize_vertex_ai()
        
        # Initialize Cloud Scheduler
        if self.config.enable_scheduler:
            self._initialize_scheduler()
        
        # Initialize Pub/Sub
        if self.config.enable_pubsub:
            self._initialize_pubsub()
        
        self.initialized = True
        
    def _initialize_vertex_ai(self):
        """Initialize Vertex AI integration and deploy container."""
        self.vertex_ai = VertexAIIntegration(
            project_id=self.config.project_id,
            region=self.config.region
        )
        
        # Generate container configuration
        container_config = self.vertex_ai.generate_container_config(
            image_tag="v1.0",
            enable_gpu=False
        )
        
        # Deploy container
        self.vertex_endpoint_id = self.vertex_ai.deploy_container(
            container_config=container_config,
            endpoint_name="active-inference-endpoint"
        )
        
    def _initialize_scheduler(self):
        """Initialize Cloud Scheduler and create optimization schedules."""
        self.scheduler = CloudSchedulerIntegration(
            project_id=self.config.project_id,
            region=self.config.region
        )
        
        # Create schedules for different policy types
        policy_types = [
            PolicyType.OUTBREAK_RESPONSE,
            PolicyType.RESOURCE_ALLOCATION,
            PolicyType.SURVEILLANCE_INTENSITY
        ]
        
        for policy_type in policy_types:
            schedule = self.scheduler.create_schedule(
                schedule_name=f"{policy_type.value}-optimization",
                policy_type=policy_type.value,
                frequency=self.config.optimization_frequency,
                target_endpoint=self.vertex_endpoint_id
            )
            
            self.schedule_ids[policy_type.value] = schedule.schedule_id
            
            # Register optimization handler
            self.scheduler.register_optimization_handler(
                policy_type=policy_type.value,
                handler=self._create_optimization_handler(policy_type)
            )
    
    def _initialize_pubsub(self):
        """Initialize Pub/Sub topics and subscriptions."""
        self.pubsub = PubSubIntegration(
            project_id=self.config.project_id,
            enable_compliance_validation=self.config.enable_compliance_validation
        )
        
        # Create topics for different alert types
        # Note: Include all alert types to ensure matching
        alert_configs = [
            {
                "name": "outbreak-alerts",
                "description": "Critical outbreak detection alerts",
                "types": [AlertType.OUTBREAK_DETECTED, AlertType.ANOMALY_DETECTED],
                "severity": AlertSeverity.MEDIUM  # Lower threshold to catch more alerts
            },
            {
                "name": "policy-updates",
                "description": "Policy optimization updates",
                "types": [AlertType.POLICY_OPTIMIZED],
                "severity": AlertSeverity.MEDIUM
            },
            {
                "name": "surveillance-alerts",
                "description": "Surveillance system alerts",
                "types": [AlertType.SURVEILLANCE_ALERT, AlertType.THRESHOLD_EXCEEDED],
                "severity": AlertSeverity.MEDIUM
            }
        ]
        
        for topic_config in alert_configs:
            topic = self.pubsub.create_topic(
                topic_name=topic_config["name"],
                description=topic_config["description"],
                alert_types=topic_config["types"],
                min_severity=topic_config["severity"],
                jurisdictions=[self.config.jurisdiction]
            )
            
            self.topic_ids[topic_config["name"]] = topic.topic_id
            
            # Create subscription for each topic
            self.pubsub.create_subscription(
                subscription_name=f"{topic_config['name']}-sub",
                topic_id=topic.topic_id
            )
    
    def _create_optimization_handler(self, policy_type: PolicyType):
        """Create optimization handler for a policy type."""
        def handler(observations: Dict[str, Any], schedule_config) -> Dict[str, Any]:
            # Run active inference
            policy = self.inference_engine.optimize_policy(
                policy_type=policy_type,
                observations=observations,
                constraints={
                    'jurisdiction': self.config.jurisdiction,
                    'max_resources': 1000
                }
            )
            
            self.optimization_cycles += 1
            
            # Publish policy update alert
            if self.pubsub:
                self._publish_policy_alert(policy)
            
            return {
                'policies_generated': 1,
                'improvement': policy.confidence - 0.7  # Improvement over baseline
            }
        
        return handler
    
    def process_and_decide(
        self,
        policy_type: PolicyType,
        observations: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None,
        publish_alert: bool = True
    ) -> Dict[str, Any]:
        """
        Process observations and generate optimal policy decision.
        
        This is the main decision-making pipeline:
        1. Run active inference to optimize policy
        2. Optionally use Vertex AI for scalable inference
        3. Publish alerts if decision warrants it
        4. Return comprehensive result
        
        Args:
            policy_type: Type of policy to optimize
            observations: Current observations about world state
            constraints: Optional constraints on policy
            publish_alert: Whether to publish alerts
            
        Returns:
            Dictionary with policy, alerts, and metadata
        """
        if not self.initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        # Add jurisdiction to constraints
        if constraints is None:
            constraints = {}
        constraints['jurisdiction'] = self.config.jurisdiction
        
        # Run active inference
        if self.vertex_ai and self.vertex_endpoint_id:
            # Use Vertex AI endpoint for inference
            response = self.vertex_ai.predict(
                endpoint_id=self.vertex_endpoint_id,
                policy_type=policy_type.value,
                observations=observations,
                constraints=constraints,
                jurisdiction=self.config.jurisdiction
            )
            
            policy_dict = response.policy
            expected_outcome = response.expected_outcome
            confidence = response.confidence
            explanation = response.explanation
        else:
            # Use local inference engine
            policy = self.inference_engine.optimize_policy(
                policy_type=policy_type,
                observations=observations,
                constraints=constraints
            )
            
            policy_dict = policy.to_dict()
            expected_outcome = policy.expected_outcome
            confidence = policy.confidence
            explanation = policy.explanation
        
        self.decision_count += 1
        
        # Determine if alert should be published
        alerts_sent = []
        if publish_alert and self.pubsub:
            alert = self._create_alert_from_policy(
                policy_dict,
                observations,
                expected_outcome,
                confidence
            )
            
            if alert:
                deliveries = self.pubsub.publish_alert(alert)
                alerts_sent = [d.to_dict() for d in deliveries]
                self.alert_count += 1
        
        # Return comprehensive result
        return {
            "policy": policy_dict,
            "expected_outcome": expected_outcome,
            "confidence": confidence,
            "explanation": explanation,
            "observations": observations,
            "alerts_sent": alerts_sent,
            "decision_count": self.decision_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _create_alert_from_policy(
        self,
        policy: Dict[str, Any],
        observations: Dict[str, Any],
        expected_outcome: float,
        confidence: float
    ) -> Optional[Alert]:
        """
        Create alert from policy decision if warranted.
        
        Only creates alerts for significant policy changes or critical situations.
        """
        # Determine if alert is warranted
        cases = observations.get('cases', 0)
        trend = observations.get('trend', 'stable')
        response_level = policy.get('parameters', {}).get('response_level', 'low')
        
        # Determine severity first
        if cases > 50 or response_level == 'high':
            severity = AlertSeverity.CRITICAL
        elif cases > 20 or response_level == 'medium':
            severity = AlertSeverity.HIGH
        else:
            severity = AlertSeverity.MEDIUM
        
        # Check against threshold before continuing
        severity_order = {
            AlertSeverity.INFO: 0,
            AlertSeverity.LOW: 1,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.HIGH: 3,
            AlertSeverity.CRITICAL: 4
        }
        
        if severity_order[severity] < severity_order[self.config.alert_severity_threshold]:
            return None
        
        # Determine alert type
        if cases > 10:
            alert_type = AlertType.OUTBREAK_DETECTED
            title = f"Outbreak Response Policy Activated"
            message = f"{cases} cases detected with {trend} trend. Response level: {response_level}"
        else:
            alert_type = AlertType.POLICY_OPTIMIZED
            title = f"Policy Optimization Complete"
            message = f"New {policy.get('policy_type', 'health')} policy optimized (confidence: {confidence:.2f})"
        
        alert = Alert(
            alert_id=f"alert-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            metadata={
                "policy": policy,
                "observations": observations,
                "expected_outcome": expected_outcome,
                "confidence": confidence
            },
            jurisdiction=self.config.jurisdiction,
            source="autonomous_decision_maker",
            requires_acknowledgment=severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH]
        )
        
        return alert
    
    def _publish_policy_alert(self, policy: Policy):
        """Publish alert for policy update."""
        alert = Alert(
            alert_id=f"alert-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            alert_type=AlertType.POLICY_OPTIMIZED,
            severity=AlertSeverity.MEDIUM,
            title=f"Policy Optimization Cycle Complete",
            message=f"{policy.policy_type.value} policy optimized via scheduled cycle",
            metadata={
                "policy_id": policy.policy_id,
                "confidence": policy.confidence,
                "expected_outcome": policy.expected_outcome
            },
            jurisdiction=self.config.jurisdiction,
            source="scheduled_optimization"
        )
        
        self.pubsub.publish_alert(alert)
        self.alert_count += 1
    
    def run_optimization_cycle(self, policy_type: PolicyType) -> Dict[str, Any]:
        """
        Manually trigger an optimization cycle.
        
        Args:
            policy_type: Type of policy to optimize
            
        Returns:
            Optimization cycle results
        """
        if not self.scheduler:
            raise RuntimeError("Scheduler not initialized")
        
        schedule_id = self.schedule_ids.get(policy_type.value)
        if not schedule_id:
            raise ValueError(f"No schedule found for {policy_type.value}")
        
        # Fetch observations (in production, from data sources)
        observations = {
            'cases': 25,
            'trend': 'stable',
            'location': 'default'
        }
        
        cycle = self.scheduler.execute_optimization_cycle(
            schedule_id=schedule_id,
            observations=observations
        )
        
        return cycle.to_dict()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            "initialized": self.initialized,
            "config": self.config.to_dict(),
            "metrics": {
                "decisions_made": self.decision_count,
                "alerts_sent": self.alert_count,
                "optimization_cycles": self.optimization_cycles
            },
            "components": {
                "inference_engine": {
                    "enabled": True,
                    "statistics": self.inference_engine.get_statistics()
                }
            }
        }
        
        if self.vertex_ai:
            status["components"]["vertex_ai"] = {
                "enabled": True,
                "endpoint_id": self.vertex_endpoint_id,
                "statistics": self.vertex_ai.get_statistics()
            }
        
        if self.scheduler:
            status["components"]["scheduler"] = {
                "enabled": True,
                "statistics": self.scheduler.get_statistics(),
                "schedules": len(self.schedule_ids)
            }
        
        if self.pubsub:
            status["components"]["pubsub"] = {
                "enabled": True,
                "statistics": self.pubsub.get_statistics(),
                "topics": len(self.topic_ids)
            }
        
        return status
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "system_metrics": {
                "decisions_made": self.decision_count,
                "alerts_sent": self.alert_count,
                "optimization_cycles": self.optimization_cycles
            }
        }
        
        if self.inference_engine:
            report["inference_engine"] = self.inference_engine.get_statistics()
        
        if self.scheduler:
            report["scheduler"] = self.scheduler.get_performance_metrics()
        
        if self.pubsub:
            report["pubsub"] = self.pubsub.get_delivery_statistics()
        
        return report


# ═════════════════════════════════════════════════════════════════════════════
# Autonomous Decision-Making Philosophy:
# "Autonomous intelligence. Sovereign control. Continuous learning."
#
# System ensures:
# - Decisions optimize for human dignity
# - Full explainability at every step
# - Sovereignty constraints never violated
# - Continuous adaptation to new information
# ═════════════════════════════════════════════════════════════════════════════
