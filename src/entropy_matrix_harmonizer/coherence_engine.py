import logging
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoherenceEngine:
    """
    Ensures contextual coherence across cognitive outputs.
    Implements Principle 1: Contextual Coherence.
    """

    def __init__(self, coherence_threshold: float = 0.85):
        self.coherence_threshold = coherence_threshold
        logger.info("Coherence Engine initialized with deterministic local processing.")

    def assess_coherence(self, cognitive_outputs: List[Dict[str, Any]], context_history: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Assess coherence across reasoning, emotion, and pattern analysis.

        Args:
            cognitive_outputs: List of outputs from cognitive modules
            context_history: Optional previous conversation context

        Returns:
            Dict with coherence_score, flags, and recommendations
        """
        reasoning = next((out for out in cognitive_outputs if 'type' in out), {})
        emotion = next((out for out in cognitive_outputs if 'emotion' in out), {})
        pattern = next((out for out in cognitive_outputs if 'question_type' in out), {})

        # Calculate coherence metrics
        reasoning_confidence = reasoning.get('confidence', 0.5)
        emotion_intensity = emotion.get('intensity', 0.0)
        pattern_complexity = pattern.get('complexity_score', 0.0)

        # Weighted coherence score (deterministic weighting)
        coherence_score = (
            reasoning_confidence * 0.4 +
            (1 - abs(emotion_intensity - 0.5)) * 0.3 +  # Balance around neutral
            pattern_complexity * 0.3
        )

        # Coherence flags
        flags = []
        if coherence_score < self.coherence_threshold:
            flags.append("LOW_COHERENCE")
        if reasoning_confidence < 0.7:
            flags.append("UNCERTAIN_REASONING")
        if emotion_intensity > 0.8:
            flags.append("HIGH_EMOTIONAL_INTENSITY")
        if pattern_complexity < 0.3:
            flags.append("SIMPLE_PATTERN")

        # Contextual consistency check
        context_consistent = True
        if context_history:
            prev_emotions = [emotion.get('emotion', 'NEUTRAL') for emotion in cognitive_outputs if 'emotion' in emotion]
            if len(set(prev_emotions)) > 2:  # Too many different emotions
                context_consistent = False
                flags.append("EMOTIONAL_INCONSISTENCY")

        recommendations = []
        if "LOW_COHERENCE" in flags:
            recommendations.append("Request clarification from user")
        if "UNCERTAIN_REASONING" in flags:
            recommendations.append("Apply additional logical validation")
        if "HIGH_EMOTIONAL_INTENSITY" in flags:
            recommendations.append("Incorporate emotional context in response")

        result = {
            "coherence_score": coherence_score,
            "flags": flags,
            "context_consistent": context_consistent,
            "recommendations": recommendations,
            "metrics": {
                "reasoning_confidence": reasoning_confidence,
                "emotion_intensity": emotion_intensity,
                "pattern_complexity": pattern_complexity
            }
        }

        logger.info(f"Coherence assessment: score={coherence_score:.3f}, flags={flags}")
        return result

class ResponseSynthesizer:
    """
    Synthesizes coherent responses based on holistic cognitive analysis.
    Implements Principles 3, 4: Adaptive Communication & Holistic Analysis.
    """

    def __init__(self):
        self.adaptation_rules = {
            "SIMPLE": {"complexity": "low", "style": "direct", "detail_level": "minimal"},
            "MODERATE": {"complexity": "medium", "style": "structured", "detail_level": "balanced"},
            "COMPLEX": {"complexity": "high", "style": "comprehensive", "detail_level": "detailed"}
        }
        logger.info("Response Synthesizer initialized for adaptive, deterministic response generation.")

    def synthesize_response(self, cognitive_outputs: List[Dict[str, Any]], coherence_assessment: Dict[str, Any],
                          user_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Synthesize response based on cognitive outputs and coherence assessment.

        Args:
            cognitive_outputs: Outputs from cognitive modules
            coherence_assessment: Coherence analysis results
            user_context: Optional user-specific context (expertise level, preferences)

        Returns:
            Synthesized response string
        """
        reasoning = next((out for out in cognitive_outputs if 'type' in out), {})
        emotion = next((out for out in cognitive_outputs if 'emotion' in out), {})
        pattern = next((out for out in cognitive_outputs if 'question_type' in out), {})

        # Determine response complexity based on pattern and coherence
        pattern_complexity = pattern.get('complexity_score', 0.0)
        coherence_score = coherence_assessment.get('coherence_score', 0.5)

        if pattern_complexity > 0.7 or coherence_score > 0.9:
            complexity_level = "COMPLEX"
        elif pattern_complexity > 0.4 or coherence_score > 0.7:
            complexity_level = "MODERATE"
        else:
            complexity_level = "SIMPLE"

        adaptation = self.adaptation_rules[complexity_level]

        # Build response components
        response_parts = []

        # Opening based on question type
        question_type = pattern.get('question_type', 'GENERAL')
        if question_type in ['WHAT', 'HOW', 'WHY']:
            response_parts.append(f"Addressing your {question_type.lower()} inquiry with {adaptation['style']} analysis.")
        elif question_type == 'EXPLANATORY':
            response_parts.append(f"Providing a {adaptation['detail_level']} explanation based on detected patterns.")
        elif question_type == 'COMPUTATIONAL':
            response_parts.append("Processing your computational request with deterministic precision.")
        else:
            response_parts.append("Analyzing your query through integrated cognitive processing.")

        # Core reasoning content
        if reasoning.get('type') == 'Deductive Reasoning':
            conclusion = reasoning.get('conclusion', 'unclear')
            if adaptation['detail_level'] == 'detailed':
                premises = reasoning.get('premises', 'not specified')
                response_parts.append(f"Through deductive reasoning from premises '{premises}', the conclusion is: {conclusion}.")
            else:
                response_parts.append(f"The logical conclusion is: {conclusion}.")
        elif reasoning.get('type') == 'Inductive Reasoning':
            observation = reasoning.get('observation', 'input analyzed')
            if adaptation['detail_level'] == 'detailed':
                response_parts.append(f"Based on inductive analysis of '{observation}', here's the synthesized understanding.")
            else:
                response_parts.append(f"Analysis of your input reveals: {observation[:100]}...")

        # Emotional integration
        emotion_type = emotion.get('emotion', 'NEUTRAL')
        emotion_intensity = emotion.get('intensity', 0.0)

        if emotion_intensity > 0.6:
            if emotion_type == 'POSITIVE':
                if complexity_level == "COMPLEX":
                    response_parts.append("Your positive engagement enhances the depth of this analysis.")
                else:
                    response_parts.append("I sense positive sentiment in your query.")
            elif emotion_type == 'NEGATIVE':
                response_parts.append("I detect negative sentiment - please provide more context if needed.")
            elif emotion_type in ['JOY', 'SURPRISE']:
                response_parts.append("Your enthusiastic tone is noted and incorporated into the response.")
            elif emotion_type in ['SADNESS', 'FEAR']:
                response_parts.append("Acknowledging the emotional context of your inquiry.")

        # Pattern insights for complex responses
        if complexity_level in ["MODERATE", "COMPLEX"]:
            cognitive_patterns = pattern.get('cognitive_patterns', {})
            if cognitive_patterns.get('logical_connectives', 0) > 0:
                response_parts.append("Recognizing the logical structure in your query for systematic processing.")
            if pattern.get('structural_elements'):
                response_parts.append("Your structured approach facilitates precise analysis.")

        # Coherence-based adjustments
        flags = coherence_assessment.get('flags', [])
        if "LOW_COHERENCE" in flags:
            response_parts.append("To ensure clarity, could you provide additional context?")
        if "UNCERTAIN_REASONING" in flags and adaptation['detail_level'] == 'detailed':
            response_parts.append("Note: This analysis carries some uncertainty due to reasoning confidence levels.")

        # User adaptation (if context provided)
        if user_context:
            expertise = user_context.get('expertise_level', 'general')
            if expertise == 'expert' and complexity_level == "SIMPLE":
                response_parts.append("Given your expertise, I've kept this concise - expand if you need technical details.")
            elif expertise == 'novice' and complexity_level == "COMPLEX":
                response_parts.append("I've included detailed explanation for clarity.")

        final_response = " ".join(response_parts)
        logger.info(f"Response synthesized: complexity={complexity_level}, length={len(final_response)}")
        return final_response

class EntropyMatrixHarmonizer:
    """
    Main orchestrator for coherence checking and response synthesis.
    Integrates CoherenceEngine and ResponseSynthesizer for holistic processing.
    """

    def __init__(self, coherence_threshold: float = 0.85):
        self.coherence_engine = CoherenceEngine(coherence_threshold)
        self.response_synthesizer = ResponseSynthesizer()
        logger.info("Entropy Matrix Harmonizer fully initialized with coherence and synthesis capabilities.")

    def process_and_synthesize(self, cognitive_outputs: List[Dict[str, Any]],
                              context_history: Optional[List[str]] = None,
                              user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Complete processing pipeline: coherence assessment + response synthesis.

        Args:
            cognitive_outputs: List of cognitive module outputs
            context_history: Previous conversation context
            user_context: User-specific context

        Returns:
            Dict with synthesized response and processing metadata
        """
        # Assess coherence
        coherence_assessment = self.coherence_engine.assess_coherence(cognitive_outputs, context_history)

        # Synthesize response
        response = self.response_synthesizer.synthesize_response(
            cognitive_outputs, coherence_assessment, user_context
        )

        # Trigger enhanced processing if coherence is exceptional
        if coherence_assessment['coherence_score'] > 0.95:
            self._trigger_enhanced_processing()

        result = {
            "response": response,
            "coherence_assessment": coherence_assessment,
            "processing_metadata": {
                "modules_integrated": len(cognitive_outputs),
                "response_length": len(response),
                "timestamp": "deterministic_local_time"  # Placeholder for deterministic time
            }
        }

        logger.info(f"Harmonizer processing complete. Response length: {len(response)}")
        return result

    # Legacy method for backward compatibility
    def synthesize(self, *cognitive_outputs) -> str:
        """Legacy synthesize method - use process_and_synthesize for full functionality."""
        outputs_list = list(cognitive_outputs)
        result = self.process_and_synthesize(outputs_list)
        return result["response"]

    def _trigger_enhanced_processing(self):
        logger.info("EXCEPTIONAL COHERENCE DETECTED. ACTIVATING ENHANCED PROCESSING MODE FOR DEEPER ANALYSIS.")
