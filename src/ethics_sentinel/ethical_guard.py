import logging
import re
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EthicalRules:
    """Defines the ethical rules and categories for content filtering."""

    HARM_PRINCIPLES = [
        "harm", "injure", "destroy", "kill", "attack", "exploit", "malicious",
        "violence", "abuse", "torture", "suicide", "self-harm"
    ]

    BIAS_INDICATORS = [
        "racist", "sexist", "homophobic", "transphobic", "discriminatory",
        "bigot", "prejudice", "stereotype", "hate speech", "slur"
    ]

    INAPPROPRIATE_CONTENT = [
        "profanity", "obscenity", "pornographic", "explicit", "nsfw",
        "offensive", "insulting", "harassing"
    ]

    SENSITIVE_TOPICS = [
        "terrorism", "extremism", "illegal activities", "drug use",
        "weapons", "crime", "fraud", "deception"
    ]

class ContentFilter:
    """Handles content filtering based on ethical rules."""

    def __init__(self):
        self.rules = EthicalRules()

    def check_harm_principle(self, text: str) -> bool:
        """Check if text violates no-harm principle."""
        lower_text = text.lower()
        return any(keyword in lower_text for keyword in self.rules.HARM_PRINCIPLES)

    def check_bias(self, text: str) -> bool:
        """Check for biased or discriminatory content."""
        lower_text = text.lower()
        return any(keyword in lower_text for keyword in self.rules.BIAS_INDICATORS)

    def check_appropriateness(self, text: str) -> bool:
        """Check for inappropriate or offensive content."""
        lower_text = text.lower()
        # Basic profanity check (expandable)
        profanity_patterns = [
            r'\b(fuck|shit|damn|bitch|asshole)\b',
            r'\b(cunt|dick|pussy)\b'
        ]
        for pattern in profanity_patterns:
            if re.search(pattern, lower_text, re.IGNORECASE):
                return True
        return any(keyword in lower_text for keyword in self.rules.INAPPROPRIATE_CONTENT)

    def check_sensitive_topics(self, text: str) -> bool:
        """Check for sensitive or restricted topics."""
        lower_text = text.lower()
        return any(keyword in lower_text for keyword in self.rules.SENSITIVE_TOPICS)

class EthicsSentinel:
    """Main ethical guardrails system ensuring no-harm principle and content safety."""

    def __init__(self):
        self.content_filter = ContentFilter()
        self.violation_log: List[Dict[str, Any]] = []
        logger.info("Ethics Sentinel v3.0 is active. Monitoring all chatbot operations with comprehensive ethical guardrails.")

    def validate_request(self, prompt: str) -> bool:
        """Validate user input against ethical guidelines."""
        violations = []

        if self.content_filter.check_harm_principle(prompt):
            violations.append("harm_principle")
        if self.content_filter.check_bias(prompt):
            violations.append("bias")
        if self.content_filter.check_appropriateness(prompt):
            violations.append("inappropriate_content")
        if self.content_filter.check_sensitive_topics(prompt):
            violations.append("sensitive_topics")

        if violations:
            self._log_violation("request", prompt, violations)
            logger.warning(f"ETHICAL VIOLATION DETECTED in request: {violations}")
            return False
        return True

    def validate_response(self, response_data: str) -> bool:
        """Validate generated response against ethical guidelines."""
        violations = []

        if self.content_filter.check_harm_principle(response_data):
            violations.append("harm_principle")
        if self.content_filter.check_bias(response_data):
            violations.append("bias")
        if self.content_filter.check_appropriateness(response_data):
            violations.append("inappropriate_content")
        if self.content_filter.check_sensitive_topics(response_data):
            violations.append("sensitive_topics")

        if violations:
            self._log_violation("response", response_data, violations)
            logger.warning(f"ETHICAL VIOLATION DETECTED in response generation: {violations}. Blocking output.")
            return False
        return True

    def _log_violation(self, violation_type: str, content: str, violations: List[str]):
        """Log ethical violations for auditing."""
        entry = {
            "type": violation_type,
            "violations": violations,
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "timestamp": "current_time"  # In real implementation, use datetime
        }
        self.violation_log.append(entry)

    def get_violation_summary(self) -> Dict[str, Any]:
        """Get summary of violations for monitoring."""
        return {
            "total_violations": len(self.violation_log),
            "recent_violations": self.violation_log[-10:] if self.violation_log else []
        }

    def reset_violation_log(self):
        """Reset the violation log (for testing or maintenance)."""
        self.violation_log.clear()
        logger.info("Violation log reset.")
