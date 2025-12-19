"""
Silent Flux (IP-04): Anxiety-Regulated AI Output
═════════════════════════════════════════════════════════════════════════════

Philosophy: "The machine must breathe with the human."

Silent Flux regulates AI inference output based on real-time operator anxiety
levels to prevent information overload during crisis scenarios. During high-stress
situations (e.g., disease outbreaks), system operators can become overwhelmed by
excessive alerts and recommendations.

Silent Flux monitors:
1. Operator interaction patterns (typing speed, click frequency)
2. Response time degradation
3. Alert dismissal rate
4. Time-of-day fatigue indicators

Based on these signals, it dynamically adjusts:
- Alert volume (filtering low-priority warnings)
- Information density (summarization vs. full detail)
- Recommendation cadence (spacing critical alerts)
- Interface complexity (progressive disclosure)

Technical Implementation:
- Tracks operator behavior metrics in real-time
- Calculates anxiety score (0.0 = calm, 1.0 = overwhelmed)
- Applies graduated output filters based on anxiety level
- Maintains audit trail of flux adjustments for post-crisis analysis
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics


class AnxietyLevel(Enum):
    """Operator anxiety classification."""
    CALM = "CALM"  # 0.0 - 0.3
    ELEVATED = "ELEVATED"  # 0.3 - 0.6
    HIGH = "HIGH"  # 0.6 - 0.8
    OVERWHELMED = "OVERWHELMED"  # 0.8 - 1.0


class OutputMode(Enum):
    """AI output regulation modes."""
    FULL = "FULL"  # All inferences shown
    FILTERED = "FILTERED"  # Low-priority filtered
    CRITICAL_ONLY = "CRITICAL_ONLY"  # Only critical alerts
    SILENT = "SILENT"  # Emergency silence mode


@dataclass
class OperatorMetrics:
    """Real-time operator behavior metrics."""
    timestamp: datetime
    typing_speed_wpm: float = 0.0  # Words per minute
    click_frequency_per_min: float = 0.0  # Clicks per minute
    avg_response_time_sec: float = 0.0  # Time to acknowledge alerts
    alert_dismissal_rate: float = 0.0  # % of alerts dismissed without action
    session_duration_min: float = 0.0  # Time in current session
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "typing_speed_wpm": self.typing_speed_wpm,
            "click_frequency_per_min": self.click_frequency_per_min,
            "avg_response_time_sec": self.avg_response_time_sec,
            "alert_dismissal_rate": self.alert_dismissal_rate,
            "session_duration_min": self.session_duration_min,
        }


@dataclass
class FluxAdjustment:
    """Record of anxiety-based output adjustment."""
    timestamp: datetime
    anxiety_score: float
    anxiety_level: AnxietyLevel
    output_mode: OutputMode
    suppressed_alerts: int
    reasoning: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "anxiety_score": self.anxiety_score,
            "anxiety_level": self.anxiety_level.value,
            "output_mode": self.output_mode.value,
            "suppressed_alerts": self.suppressed_alerts,
            "reasoning": self.reasoning,
        }


class SilentFlux:
    """
    Anxiety-regulated AI output controller.
    
    Monitors operator stress signals and dynamically adjusts AI inference
    output to prevent information overload during crisis scenarios.
    
    Usage:
        flux = SilentFlux()
        
        # Record operator metrics
        flux.record_operator_metrics(
            typing_speed_wpm=45.0,
            click_frequency_per_min=12.0,
            avg_response_time_sec=3.5,
            alert_dismissal_rate=0.15
        )
        
        # Calculate anxiety and get output mode
        anxiety = flux.calculate_anxiety()
        output_mode = flux.get_output_mode()
        
        # Filter AI inferences based on anxiety
        filtered_alerts = flux.filter_inferences(
            inferences=[...],
            output_mode=output_mode
        )
    """
    
    def __init__(self, anxiety_window_minutes: int = 5):
        """
        Initialize Silent Flux controller.
        
        Args:
            anxiety_window_minutes: Time window for anxiety calculation
        """
        self.anxiety_window_minutes = anxiety_window_minutes
        self.metrics_history: List[OperatorMetrics] = []
        self.flux_adjustments: List[FluxAdjustment] = []
        self.current_anxiety_score = 0.0
        self.current_output_mode = OutputMode.FULL
        
        # Baseline thresholds (can be calibrated per operator)
        self.baseline_typing_speed = 60.0  # WPM
        self.baseline_click_frequency = 15.0  # Per minute
        self.baseline_response_time = 2.0  # Seconds
        
    def record_operator_metrics(
        self,
        typing_speed_wpm: float = 0.0,
        click_frequency_per_min: float = 0.0,
        avg_response_time_sec: float = 0.0,
        alert_dismissal_rate: float = 0.0,
        session_duration_min: float = 0.0
    ):
        """
        Record real-time operator behavior metrics.
        
        These metrics are used to calculate anxiety score.
        """
        metrics = OperatorMetrics(
            timestamp=datetime.utcnow(),
            typing_speed_wpm=typing_speed_wpm,
            click_frequency_per_min=click_frequency_per_min,
            avg_response_time_sec=avg_response_time_sec,
            alert_dismissal_rate=alert_dismissal_rate,
            session_duration_min=session_duration_min,
        )
        
        self.metrics_history.append(metrics)
        
        # Prune old metrics outside anxiety window
        cutoff_time = datetime.utcnow() - timedelta(minutes=self.anxiety_window_minutes)
        self.metrics_history = [
            m for m in self.metrics_history
            if m.timestamp > cutoff_time
        ]
    
    def calculate_anxiety(self) -> float:
        """
        Calculate operator anxiety score (0.0 = calm, 1.0 = overwhelmed).
        
        Algorithm:
        1. Analyze recent operator metrics
        2. Compare to baseline behavior
        3. Weight multiple anxiety signals
        4. Return normalized score [0.0, 1.0]
        
        Anxiety Signals:
        - Typing speed degradation (slower = anxious)
        - Click frequency increase (frantic clicking)
        - Response time increase (cognitive overload)
        - Alert dismissal rate increase (ignoring alerts)
        - Session duration (fatigue accumulation)
        
        Returns:
            float: Anxiety score between 0.0 and 1.0
        """
        if not self.metrics_history:
            self.current_anxiety_score = 0.0
            return 0.0
        
        recent_metrics = self.metrics_history[-10:]  # Last 10 data points
        
        # Calculate component anxiety scores
        typing_anxiety = self._calculate_typing_anxiety(recent_metrics)
        click_anxiety = self._calculate_click_anxiety(recent_metrics)
        response_anxiety = self._calculate_response_anxiety(recent_metrics)
        dismissal_anxiety = self._calculate_dismissal_anxiety(recent_metrics)
        fatigue_anxiety = self._calculate_fatigue_anxiety(recent_metrics)
        
        # Weighted average
        weights = {
            "typing": 0.15,
            "click": 0.20,
            "response": 0.30,  # Response time is strongest signal
            "dismissal": 0.25,
            "fatigue": 0.10,
        }
        
        anxiety_score = (
            typing_anxiety * weights["typing"] +
            click_anxiety * weights["click"] +
            response_anxiety * weights["response"] +
            dismissal_anxiety * weights["dismissal"] +
            fatigue_anxiety * weights["fatigue"]
        )
        
        # Clamp to [0.0, 1.0]
        anxiety_score = max(0.0, min(1.0, anxiety_score))
        
        self.current_anxiety_score = anxiety_score
        return anxiety_score
    
    def _calculate_typing_anxiety(self, metrics: List[OperatorMetrics]) -> float:
        """Calculate anxiety from typing speed degradation."""
        if not metrics:
            return 0.0
        
        avg_typing = statistics.mean(m.typing_speed_wpm for m in metrics if m.typing_speed_wpm > 0)
        
        if avg_typing == 0:
            return 0.0
        
        # Slower typing = higher anxiety
        degradation = max(0, self.baseline_typing_speed - avg_typing) / self.baseline_typing_speed
        return min(1.0, degradation * 1.5)
    
    def _calculate_click_anxiety(self, metrics: List[OperatorMetrics]) -> float:
        """Calculate anxiety from frantic clicking."""
        if not metrics:
            return 0.0
        
        avg_clicks = statistics.mean(
            m.click_frequency_per_min for m in metrics
            if m.click_frequency_per_min > 0
        )
        
        if avg_clicks == 0:
            return 0.0
        
        # More clicks than baseline = higher anxiety
        excess = max(0, avg_clicks - self.baseline_click_frequency) / self.baseline_click_frequency
        return min(1.0, excess)
    
    def _calculate_response_anxiety(self, metrics: List[OperatorMetrics]) -> float:
        """Calculate anxiety from response time degradation."""
        if not metrics:
            return 0.0
        
        avg_response = statistics.mean(
            m.avg_response_time_sec for m in metrics
            if m.avg_response_time_sec > 0
        )
        
        if avg_response == 0:
            return 0.0
        
        # Slower response = cognitive overload
        degradation = max(0, avg_response - self.baseline_response_time) / self.baseline_response_time
        return min(1.0, degradation)
    
    def _calculate_dismissal_anxiety(self, metrics: List[OperatorMetrics]) -> float:
        """Calculate anxiety from alert dismissal rate."""
        if not metrics:
            return 0.0
        
        avg_dismissal = statistics.mean(
            m.alert_dismissal_rate for m in metrics
            if m.alert_dismissal_rate > 0
        )
        
        # High dismissal rate = ignoring alerts = overwhelmed
        return min(1.0, avg_dismissal * 2.0)
    
    def _calculate_fatigue_anxiety(self, metrics: List[OperatorMetrics]) -> float:
        """Calculate anxiety from session duration (fatigue)."""
        if not metrics:
            return 0.0
        
        latest = metrics[-1]
        session_hours = latest.session_duration_min / 60.0
        
        # Fatigue accumulates after 2 hours
        if session_hours < 2.0:
            return 0.0
        
        fatigue = (session_hours - 2.0) / 4.0  # Peaks at 6 hours
        return min(1.0, fatigue)
    
    def get_anxiety_level(self) -> AnxietyLevel:
        """
        Get categorical anxiety level.
        
        Returns:
            AnxietyLevel: CALM, ELEVATED, HIGH, or OVERWHELMED
        """
        score = self.current_anxiety_score
        
        if score < 0.3:
            return AnxietyLevel.CALM
        elif score < 0.6:
            return AnxietyLevel.ELEVATED
        elif score < 0.8:
            return AnxietyLevel.HIGH
        else:
            return AnxietyLevel.OVERWHELMED
    
    def get_output_mode(self) -> OutputMode:
        """
        Determine AI output mode based on anxiety level.
        
        Returns:
            OutputMode: FULL, FILTERED, CRITICAL_ONLY, or SILENT
        """
        anxiety_level = self.get_anxiety_level()
        
        mode_mapping = {
            AnxietyLevel.CALM: OutputMode.FULL,
            AnxietyLevel.ELEVATED: OutputMode.FILTERED,
            AnxietyLevel.HIGH: OutputMode.CRITICAL_ONLY,
            AnxietyLevel.OVERWHELMED: OutputMode.SILENT,
        }
        
        self.current_output_mode = mode_mapping[anxiety_level]
        return self.current_output_mode
    
    def filter_inferences(
        self,
        inferences: List[Dict[str, Any]],
        output_mode: Optional[OutputMode] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter AI inferences based on anxiety-driven output mode.
        
        Args:
            inferences: List of AI inferences with 'priority' field
            output_mode: Override output mode (uses current if None)
            
        Returns:
            Filtered list of inferences
        """
        if output_mode is None:
            output_mode = self.current_output_mode
        
        if output_mode == OutputMode.FULL:
            # Show everything
            return inferences
        
        elif output_mode == OutputMode.FILTERED:
            # Filter low-priority alerts
            filtered = [
                inf for inf in inferences
                if inf.get("priority", "LOW") in ["HIGH", "CRITICAL"]
            ]
            
            # Record adjustment
            self._record_flux_adjustment(
                output_mode=output_mode,
                suppressed_count=len(inferences) - len(filtered),
                reasoning="Elevated anxiety: filtering low-priority alerts"
            )
            
            return filtered
        
        elif output_mode == OutputMode.CRITICAL_ONLY:
            # Only critical alerts
            critical = [
                inf for inf in inferences
                if inf.get("priority") == "CRITICAL"
            ]
            
            self._record_flux_adjustment(
                output_mode=output_mode,
                suppressed_count=len(inferences) - len(critical),
                reasoning="High anxiety: showing only critical alerts"
            )
            
            return critical
        
        elif output_mode == OutputMode.SILENT:
            # Emergency silence: suppress all non-emergency alerts
            # Only show alerts that require immediate action
            emergency = [
                inf for inf in inferences
                if inf.get("priority") == "CRITICAL" and inf.get("requires_immediate_action") is True
            ]
            
            self._record_flux_adjustment(
                output_mode=output_mode,
                suppressed_count=len(inferences) - len(emergency),
                reasoning="Operator overwhelmed: entering silent mode"
            )
            
            return emergency
        
        return inferences
    
    def _record_flux_adjustment(
        self,
        output_mode: OutputMode,
        suppressed_count: int,
        reasoning: str
    ):
        """Record flux adjustment for audit trail."""
        adjustment = FluxAdjustment(
            timestamp=datetime.utcnow(),
            anxiety_score=self.current_anxiety_score,
            anxiety_level=self.get_anxiety_level(),
            output_mode=output_mode,
            suppressed_alerts=suppressed_count,
            reasoning=reasoning,
        )
        
        self.flux_adjustments.append(adjustment)
    
    def get_flux_audit_trail(self) -> List[Dict[str, Any]]:
        """
        Retrieve complete audit trail of flux adjustments.
        
        Used for post-crisis analysis and system tuning.
        """
        return [adj.to_dict() for adj in self.flux_adjustments]
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        Get current Silent Flux state.
        
        Returns:
            Dict containing anxiety score, level, output mode, and metrics
        """
        return {
            "anxiety_score": self.current_anxiety_score,
            "anxiety_level": self.get_anxiety_level().value,
            "output_mode": self.current_output_mode.value,
            "recent_metrics": [
                m.to_dict() for m in self.metrics_history[-5:]
            ],
            "total_flux_adjustments": len(self.flux_adjustments),
        }


# ═════════════════════════════════════════════════════════════════════════════
# IP-04: Silent Flux
# 
# "The machine must breathe with the human."
# 
# Core Innovation:
# - Real-time operator anxiety detection
# - Dynamic AI output regulation
# - Information overload prevention
# - Crisis-adaptive interface
# ═════════════════════════════════════════════════════════════════════════════
