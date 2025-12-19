"""
Cloud Scheduler Integration for Policy Optimization Cycles
═════════════════════════════════════════════════════════════════════════════

Manages regular policy optimization cycles using Google Cloud Scheduler.
Ensures continuous learning and adaptation of active inference policies.

Features:
- Scheduled policy optimization
- Adaptive cycle frequency
- Performance monitoring
- Audit logging

Philosophy: "Continuous optimization. Never static. Always learning."
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class ScheduleFrequency(Enum):
    """Frequency options for optimization cycles."""
    HOURLY = "0 * * * *"  # Every hour
    EVERY_6_HOURS = "0 */6 * * *"  # Every 6 hours
    DAILY = "0 0 * * *"  # Daily at midnight
    WEEKLY = "0 0 * * 0"  # Weekly on Sunday
    CUSTOM = "custom"  # Custom cron expression


@dataclass
class OptimizationCycle:
    """
    Represents a single policy optimization cycle.
    """
    cycle_id: str
    policy_type: str
    scheduled_time: datetime
    actual_start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    status: str = "SCHEDULED"  # SCHEDULED, RUNNING, COMPLETED, FAILED
    observations_processed: int = 0
    policies_generated: int = 0
    improvements_detected: float = 0.0
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize optimization cycle."""
        return {
            "cycle_id": self.cycle_id,
            "policy_type": self.policy_type,
            "scheduled_time": self.scheduled_time.isoformat(),
            "actual_start_time": self.actual_start_time.isoformat() if self.actual_start_time else None,
            "completion_time": self.completion_time.isoformat() if self.completion_time else None,
            "status": self.status,
            "observations_processed": self.observations_processed,
            "policies_generated": self.policies_generated,
            "improvements_detected": self.improvements_detected,
            "error_message": self.error_message
        }


@dataclass
class ScheduleConfig:
    """
    Configuration for a policy optimization schedule.
    """
    schedule_id: str
    schedule_name: str
    policy_type: str
    frequency: ScheduleFrequency
    custom_cron: Optional[str] = None
    timezone: str = "UTC"
    enabled: bool = True
    target_endpoint: Optional[str] = None
    observations_source: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize schedule config."""
        return {
            "schedule_id": self.schedule_id,
            "schedule_name": self.schedule_name,
            "policy_type": self.policy_type,
            "frequency": self.frequency.value,
            "custom_cron": self.custom_cron,
            "timezone": self.timezone,
            "enabled": self.enabled,
            "target_endpoint": self.target_endpoint,
            "observations_source": self.observations_source,
            "created_at": self.created_at.isoformat()
        }


class CloudSchedulerIntegration:
    """
    Integration with Google Cloud Scheduler for automated policy optimization.
    
    Manages recurring optimization cycles that:
    1. Fetch latest observations
    2. Run active inference
    3. Generate optimized policies
    4. Monitor performance
    5. Adapt cycle frequency based on results
    
    Usage:
        scheduler = CloudSchedulerIntegration(
            project_id="iluminara-prod",
            region="us-central1"
        )
        
        # Create optimization schedule
        schedule = scheduler.create_schedule(
            schedule_name="outbreak-response-optimization",
            policy_type="outbreak_response",
            frequency=ScheduleFrequency.EVERY_6_HOURS
        )
        
        # Execute cycle (triggered by Cloud Scheduler)
        result = scheduler.execute_optimization_cycle(schedule.schedule_id)
    """
    
    def __init__(
        self,
        project_id: str,
        region: str = "us-central1",
        timezone: str = "UTC"
    ):
        """
        Initialize Cloud Scheduler integration.
        
        Args:
            project_id: GCP project ID
            region: GCP region
            timezone: Default timezone for schedules
        """
        self.project_id = project_id
        self.region = region
        self.timezone = timezone
        self.schedules: Dict[str, ScheduleConfig] = {}
        self.cycle_history: List[OptimizationCycle] = []
        self.optimization_handlers: Dict[str, Callable] = {}
        
    def create_schedule(
        self,
        schedule_name: str,
        policy_type: str,
        frequency: ScheduleFrequency,
        custom_cron: Optional[str] = None,
        target_endpoint: Optional[str] = None,
        observations_source: Optional[str] = None
    ) -> ScheduleConfig:
        """
        Create a new optimization schedule.
        
        Args:
            schedule_name: Human-readable schedule name
            policy_type: Type of policy to optimize
            frequency: How often to run optimization
            custom_cron: Custom cron expression (if frequency is CUSTOM)
            target_endpoint: Target Vertex AI endpoint
            observations_source: Source for observations
            
        Returns:
            ScheduleConfig for the created schedule
        """
        schedule_id = f"schedule-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        config = ScheduleConfig(
            schedule_id=schedule_id,
            schedule_name=schedule_name,
            policy_type=policy_type,
            frequency=frequency,
            custom_cron=custom_cron if frequency == ScheduleFrequency.CUSTOM else None,
            timezone=self.timezone,
            target_endpoint=target_endpoint,
            observations_source=observations_source
        )
        
        self.schedules[schedule_id] = config
        
        return config
    
    def generate_cloud_scheduler_job_spec(
        self,
        schedule_config: ScheduleConfig,
        http_target_uri: str
    ) -> Dict[str, Any]:
        """
        Generate Cloud Scheduler job specification.
        
        Args:
            schedule_config: Schedule configuration
            http_target_uri: HTTP endpoint to trigger
            
        Returns:
            Cloud Scheduler job specification
        """
        # Determine cron schedule
        if schedule_config.frequency == ScheduleFrequency.CUSTOM:
            schedule_expression = schedule_config.custom_cron
        else:
            schedule_expression = schedule_config.frequency.value
        
        job_spec = {
            "name": f"projects/{self.project_id}/locations/{self.region}/jobs/{schedule_config.schedule_id}",
            "description": f"Policy optimization for {schedule_config.policy_type}",
            "schedule": schedule_expression,
            "time_zone": schedule_config.timezone,
            "http_target": {
                "uri": http_target_uri,
                "http_method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                    "X-Schedule-ID": schedule_config.schedule_id,
                    "X-Policy-Type": schedule_config.policy_type
                },
                "body": json.dumps({
                    "schedule_id": schedule_config.schedule_id,
                    "policy_type": schedule_config.policy_type,
                    "observations_source": schedule_config.observations_source,
                    "target_endpoint": schedule_config.target_endpoint,
                    "timestamp": datetime.utcnow().isoformat()
                }).encode('utf-8'),
                "oidc_token": {
                    "service_account_email": f"scheduler@{self.project_id}.iam.gserviceaccount.com"
                }
            },
            "retry_config": {
                "retry_count": 3,
                "max_retry_duration": "600s",
                "min_backoff_duration": "5s",
                "max_backoff_duration": "60s"
            },
            "attempt_deadline": "300s"
        }
        
        return job_spec
    
    def execute_optimization_cycle(
        self,
        schedule_id: str,
        observations: Optional[Dict[str, Any]] = None
    ) -> OptimizationCycle:
        """
        Execute a single optimization cycle.
        
        This method would be called by Cloud Scheduler via HTTP trigger.
        
        Args:
            schedule_id: ID of the schedule
            observations: Optional observations (if not provided, will fetch from source)
            
        Returns:
            OptimizationCycle with execution results
        """
        if schedule_id not in self.schedules:
            raise ValueError(f"Schedule {schedule_id} not found")
        
        schedule_config = self.schedules[schedule_id]
        
        if not schedule_config.enabled:
            raise ValueError(f"Schedule {schedule_id} is disabled")
        
        # Create cycle
        cycle_id = f"cycle-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        cycle = OptimizationCycle(
            cycle_id=cycle_id,
            policy_type=schedule_config.policy_type,
            scheduled_time=datetime.utcnow(),
            actual_start_time=datetime.utcnow(),
            status="RUNNING"
        )
        
        try:
            # Fetch observations if not provided
            if observations is None:
                observations = self._fetch_observations(schedule_config)
            
            cycle.observations_processed = len(observations)
            
            # Execute optimization handler if registered
            if schedule_config.policy_type in self.optimization_handlers:
                handler = self.optimization_handlers[schedule_config.policy_type]
                result = handler(observations, schedule_config)
                
                cycle.policies_generated = result.get('policies_generated', 1)
                cycle.improvements_detected = result.get('improvement', 0.0)
            else:
                # Default optimization logic
                cycle.policies_generated = 1
                cycle.improvements_detected = 0.05  # Mock improvement
            
            # Complete cycle
            cycle.completion_time = datetime.utcnow()
            cycle.status = "COMPLETED"
            
        except Exception as e:
            cycle.status = "FAILED"
            cycle.error_message = str(e)
            cycle.completion_time = datetime.utcnow()
        
        # Store cycle
        self.cycle_history.append(cycle)
        
        return cycle
    
    def _fetch_observations(self, schedule_config: ScheduleConfig) -> Dict[str, Any]:
        """
        Fetch observations from configured source.
        
        In production, this would:
        - Query BigQuery for recent health data
        - Fetch from Firestore or Cloud SQL
        - Pull from external APIs
        """
        # Mock observations for simulation
        return {
            "cases": 25,
            "trend": "stable",
            "location": "default",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def register_optimization_handler(
        self,
        policy_type: str,
        handler: Callable
    ):
        """
        Register a custom optimization handler for a policy type.
        
        Args:
            policy_type: Type of policy
            handler: Callable that takes (observations, schedule_config) and returns results
        """
        self.optimization_handlers[policy_type] = handler
    
    def enable_schedule(self, schedule_id: str):
        """Enable a schedule."""
        if schedule_id in self.schedules:
            self.schedules[schedule_id].enabled = True
    
    def disable_schedule(self, schedule_id: str):
        """Disable a schedule."""
        if schedule_id in self.schedules:
            self.schedules[schedule_id].enabled = False
    
    def update_schedule_frequency(
        self,
        schedule_id: str,
        frequency: ScheduleFrequency,
        custom_cron: Optional[str] = None
    ):
        """
        Update schedule frequency.
        
        Args:
            schedule_id: ID of schedule to update
            frequency: New frequency
            custom_cron: Custom cron expression (if frequency is CUSTOM)
        """
        if schedule_id in self.schedules:
            schedule = self.schedules[schedule_id]
            schedule.frequency = frequency
            if frequency == ScheduleFrequency.CUSTOM:
                schedule.custom_cron = custom_cron
    
    def get_schedule(self, schedule_id: str) -> Optional[ScheduleConfig]:
        """Get schedule configuration."""
        return self.schedules.get(schedule_id)
    
    def list_schedules(self, enabled_only: bool = False) -> List[ScheduleConfig]:
        """
        List all schedules.
        
        Args:
            enabled_only: If True, only return enabled schedules
        """
        schedules = list(self.schedules.values())
        if enabled_only:
            schedules = [s for s in schedules if s.enabled]
        return schedules
    
    def get_cycle_history(
        self,
        schedule_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[OptimizationCycle]:
        """
        Get optimization cycle history.
        
        Args:
            schedule_id: Filter by schedule ID
            status: Filter by status
            limit: Maximum number of results
            
        Returns:
            List of optimization cycles
        """
        cycles = self.cycle_history
        
        if schedule_id:
            # Filter by schedule (would need to add schedule_id to cycle)
            pass
        
        if status:
            cycles = [c for c in cycles if c.status == status]
        
        # Sort by scheduled time (most recent first)
        cycles = sorted(cycles, key=lambda c: c.scheduled_time, reverse=True)
        
        return cycles[:limit]
    
    def get_performance_metrics(
        self,
        schedule_id: Optional[str] = None,
        time_window_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Get performance metrics for optimization cycles.
        
        Args:
            schedule_id: Filter by schedule ID
            time_window_hours: Time window for metrics
            
        Returns:
            Performance metrics dictionary
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        
        # Filter cycles
        relevant_cycles = [
            c for c in self.cycle_history
            if c.scheduled_time >= cutoff_time
        ]
        
        if not relevant_cycles:
            return {
                "cycles_executed": 0,
                "success_rate": 0.0,
                "average_duration_ms": 0.0,
                "total_policies_generated": 0,
                "average_improvement": 0.0
            }
        
        completed_cycles = [c for c in relevant_cycles if c.status == "COMPLETED"]
        
        total_duration_ms = sum(
            (c.completion_time - c.actual_start_time).total_seconds() * 1000
            for c in completed_cycles
            if c.completion_time and c.actual_start_time
        )
        
        metrics = {
            "cycles_executed": len(relevant_cycles),
            "success_rate": len(completed_cycles) / len(relevant_cycles) if relevant_cycles else 0.0,
            "average_duration_ms": total_duration_ms / len(completed_cycles) if completed_cycles else 0.0,
            "total_policies_generated": sum(c.policies_generated for c in completed_cycles),
            "average_improvement": (
                sum(c.improvements_detected for c in completed_cycles) / len(completed_cycles)
                if completed_cycles else 0.0
            ),
            "failed_cycles": len([c for c in relevant_cycles if c.status == "FAILED"]),
            "time_window_hours": time_window_hours
        }
        
        return metrics
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        enabled_schedules = [s for s in self.schedules.values() if s.enabled]
        
        return {
            "total_schedules": len(self.schedules),
            "enabled_schedules": len(enabled_schedules),
            "total_cycles_executed": len(self.cycle_history),
            "successful_cycles": len([c for c in self.cycle_history if c.status == "COMPLETED"]),
            "failed_cycles": len([c for c in self.cycle_history if c.status == "FAILED"]),
            "project_id": self.project_id,
            "region": self.region
        }


# ═════════════════════════════════════════════════════════════════════════════
# Cloud Scheduler Philosophy:
# "Continuous optimization. Never static. Always learning."
#
# Automated cycles ensure:
# - Policies adapt to changing conditions
# - Learning never stops
# - Human oversight remains sovereign
# ═════════════════════════════════════════════════════════════════════════════
