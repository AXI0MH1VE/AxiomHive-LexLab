"""Complete safety guardian OODA loop implementation for operational resilience, rate limiting, and circuit breakers."""

import logging
import time
import threading
from collections import deque
from typing import Dict, Any, Optional, Callable
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class RateLimiter:
    """Token bucket rate limiter for controlling request frequency."""

    def __init__(self, requests_per_second: float = 10.0, burst_size: int = 20):
        self.requests_per_second = requests_per_second
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_update = time.time()
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        """Check if request is allowed under rate limit."""
        with self.lock:
            now = time.time()
            time_passed = now - self.last_update
            self.tokens = min(self.burst_size, self.tokens + time_passed * self.requests_per_second)
            self.last_update = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

class CircuitBreaker:
    """Circuit breaker pattern implementation for fault tolerance."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0, expected_exception: Exception = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED
        self.lock = threading.Lock()

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitBreakerState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call."""
        with self.lock:
            self.failure_count = 0
            self.state = CircuitBreakerState.CLOSED

    def _on_failure(self):
        """Handle failed call."""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                logger.warning(f"Circuit breaker tripped OPEN after {self.failure_count} failures")

class HealthMonitor:
    """Monitors system health metrics for operational resilience."""

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.response_times = deque(maxlen=window_size)
        self.error_counts = deque(maxlen=window_size)
        self.request_counts = deque(maxlen=window_size)
        self.lock = threading.Lock()

    def record_request(self, response_time: float, is_error: bool = False):
        """Record a request with its response time and error status."""
        with self.lock:
            self.response_times.append(response_time)
            self.error_counts.append(1 if is_error else 0)
            self.request_counts.append(1)

    def get_health_metrics(self) -> Dict[str, Any]:
        """Get current health metrics."""
        with self.lock:
            if not self.response_times:
                return {
                    "avg_response_time": 0.0,
                    "error_rate": 0.0,
                    "total_requests": 0,
                    "healthy": True
                }

            avg_response_time = sum(self.response_times) / len(self.response_times)
            total_errors = sum(self.error_counts)
            total_requests = sum(self.request_counts)
            error_rate = total_errors / total_requests if total_requests > 0 else 0.0

            # Define health thresholds
            healthy = avg_response_time < 5.0 and error_rate < 0.1

            return {
                "avg_response_time": avg_response_time,
                "error_rate": error_rate,
                "total_requests": total_requests,
                "healthy": healthy
            }

class OODALoop:
    """OODA (Observe, Orient, Decide, Act) loop for safety guardian operations."""

    def __init__(self, requests_per_second: float = 10.0, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.rate_limiter = RateLimiter(requests_per_second)
        self.circuit_breaker = CircuitBreaker(failure_threshold, recovery_timeout)
        self.health_monitor = HealthMonitor()
        self.operational = True
        logger.info("Safety Guardian OODA Loop initialized with operational resilience controls")

    def observe(self) -> Dict[str, Any]:
        """Observe current system state."""
        health_metrics = self.health_monitor.get_health_metrics()
        return {
            "health_metrics": health_metrics,
            "circuit_breaker_state": self.circuit_breaker.state.value,
            "rate_limiter_tokens": self.rate_limiter.tokens,
            "operational": self.operational
        }

    def orient(self, observations: Dict[str, Any]) -> Dict[str, Any]:
        """Orient and analyze observations."""
        health_metrics = observations["health_metrics"]
        circuit_state = observations["circuit_breaker_state"]

        analysis = {
            "system_healthy": health_metrics["healthy"],
            "high_error_rate": health_metrics["error_rate"] > 0.2,
            "slow_responses": health_metrics["avg_response_time"] > 10.0,
            "circuit_open": circuit_state == CircuitBreakerState.OPEN.value,
            "rate_limited": observations["rate_limiter_tokens"] < 1
        }

        return analysis

    def decide(self, analysis: Dict[str, Any]) -> str:
        """Decide on action based on analysis."""
        if analysis["circuit_open"]:
            return "MAINTAIN_CIRCUIT_OPEN"
        elif analysis["high_error_rate"] or analysis["slow_responses"]:
            return "TRIP_CIRCUIT_BREAKER"
        elif not analysis["system_healthy"]:
            return "ENABLE_DEGRADED_MODE"
        else:
            return "NORMAL_OPERATION"

    def act(self, decision: str):
        """Act on the decision."""
        if decision == "TRIP_CIRCUIT_BREAKER":
            self.circuit_breaker.state = CircuitBreakerState.OPEN
            self.operational = False
            logger.warning("Safety Guardian: Tripping circuit breaker due to system degradation")
        elif decision == "ENABLE_DEGRADED_MODE":
            self.operational = False
            logger.warning("Safety Guardian: Enabling degraded mode")
        elif decision == "NORMAL_OPERATION":
            self.operational = True
            logger.info("Safety Guardian: Normal operation restored")

    def check_safety(self, request_func: Optional[Callable] = None) -> bool:
        """Main safety check implementing OODA loop."""
        # Observe
        observations = self.observe()

        # Orient
        analysis = self.orient(observations)

        # Decide
        decision = self.decide(analysis)

        # Act
        self.act(decision)

        # Check rate limit
        if not self.rate_limiter.allow_request():
            logger.warning("Safety Guardian: Request rate limited")
            return False

        # Check circuit breaker
        if self.circuit_breaker.state == CircuitBreakerState.OPEN:
            logger.warning("Safety Guardian: Circuit breaker open, rejecting request")
            return False

        # If operational and checks pass
        if self.operational:
            start_time = time.time()
            try:
                if request_func:
                    result = self.circuit_breaker.call(request_func)
                else:
                    result = True
                response_time = time.time() - start_time
                self.health_monitor.record_request(response_time, is_error=False)
                return True
            except Exception as e:
                response_time = time.time() - start_time
                self.health_monitor.record_request(response_time, is_error=True)
                logger.error(f"Safety Guardian: Request failed with error: {e}")
                return False
        else:
            logger.warning("Safety Guardian: System in degraded mode, rejecting request")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get current status of safety guardian."""
        observations = self.observe()
        analysis = self.orient(observations)
        return {
            "observations": observations,
            "analysis": analysis,
            "decision": self.decide(analysis),
            "operational": self.operational
        }
