import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeductiveReasoner:
    """Handles deductive reasoning patterns like syllogisms and logical entailments."""

    def __init__(self):
        self.deductive_patterns = {
            'modus_ponens': re.compile(r'if (.+?) then (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'modus_tollens': re.compile(r'if (.+?) then (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'syllogism': re.compile(r'(all|some|no) (.+?) (are|is) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'hypothetical': re.compile(r'suppose|assume|given that (.+?)(?:\.|\s|$)', re.IGNORECASE)
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text for deductive reasoning patterns."""
        text_lower = text.lower()

        # Check for conditional statements
        conditionals = self.deductive_patterns['modus_ponens'].findall(text)
        if conditionals:
            return {
                'type': 'DEDUCTIVE',
                'subtype': 'MODUS_PONENS',
                'conditionals': conditionals,
                'confidence': 0.85,
                'structure': 'If P then Q, P therefore Q'
            }

        # Check for syllogistic structure
        syllogisms = self.deductive_patterns['syllogism'].findall(text)
        if syllogisms:
            return {
                'type': 'DEDUCTIVE',
                'subtype': 'SYLLOGISM',
                'quantifiers': syllogisms,
                'confidence': 0.90,
                'structure': 'All/Some/No A are B'
            }

        # General deductive indicators
        deductive_words = ['therefore', 'thus', 'hence', 'consequently', 'follows that']
        if any(word in text_lower for word in deductive_words):
            return {
                'type': 'DEDUCTIVE',
                'subtype': 'GENERAL',
                'indicators': [word for word in deductive_words if word in text_lower],
                'confidence': 0.75,
                'structure': 'Conclusion follows necessarily'
            }

        return {'type': 'UNKNOWN', 'confidence': 0.0}

class InductiveReasoner:
    """Handles inductive reasoning patterns like generalizations from observations."""

    def __init__(self):
        self.inductive_patterns = {
            'generalization': re.compile(r'(?:all|every|most|many) (.+?) (?:are|have|do) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'enumeration': re.compile(r'(?:first|second|third|next|then|finally) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'analogy': re.compile(r'(?:like|similar to|just as|analogous to) (.+?)(?:\.|\s|$)', re.IGNORECASE)
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text for inductive reasoning patterns."""
        text_lower = text.lower()

        # Check for generalizations
        generalizations = self.inductive_patterns['generalization'].findall(text)
        if generalizations:
            return {
                'type': 'INDUCTIVE',
                'subtype': 'GENERALIZATION',
                'generalizations': generalizations,
                'confidence': 0.70,
                'structure': 'General rule from specific cases'
            }

        # Check for enumerative induction
        enumerations = self.inductive_patterns['enumeration'].findall(text)
        if len(enumerations) > 2:
            return {
                'type': 'INDUCTIVE',
                'subtype': 'ENUMERATION',
                'examples': enumerations,
                'confidence': 0.65,
                'structure': 'Multiple examples leading to conclusion'
            }

        # General inductive indicators
        inductive_words = ['because', 'since', 'due to', 'as a result of', 'based on']
        if any(word in text_lower for word in inductive_words):
            return {
                'type': 'INDUCTIVE',
                'subtype': 'CAUSAL_INDUCTION',
                'indicators': [word for word in inductive_words if word in text_lower],
                'confidence': 0.60,
                'structure': 'Cause-effect relationships'
            }

        return {'type': 'UNKNOWN', 'confidence': 0.0}

class AbductiveReasoner:
    """Handles abductive reasoning - finding the best explanation."""

    def __init__(self):
        self.abductive_patterns = {
            'explanation': re.compile(r'(?:probably|likely|must be|best explanation) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'inference': re.compile(r'(?:therefore|so|thus) (.+?) (?:because|since) (.+?)(?:\.|\s|$)', re.IGNORECASE)
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text for abductive reasoning patterns."""
        text_lower = text.lower()

        # Check for best explanation patterns
        explanations = self.abductive_patterns['explanation'].findall(text)
        if explanations:
            return {
                'type': 'ABDUCTIVE',
                'subtype': 'BEST_EXPLANATION',
                'explanations': explanations,
                'confidence': 0.55,
                'structure': 'Most likely explanation for observed facts'
            }

        # Check for explanatory inferences
        inferences = self.abductive_patterns['inference'].findall(text)
        if inferences:
            return {
                'type': 'ABDUCTIVE',
                'subtype': 'EXPLANATORY_INFERENCE',
                'inferences': inferences,
                'confidence': 0.50,
                'structure': 'Inferring explanation from evidence'
            }

        return {'type': 'UNKNOWN', 'confidence': 0.0}

class AnalogicalReasoner:
    """Handles analogical reasoning - reasoning by analogy."""

    def __init__(self):
        self.analogical_patterns = {
            'analogy': re.compile(r'(?:like|similar to|just as|analogous to|compared to) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'metaphor': re.compile(r'(?:is like|is a|as if) (.+?)(?:\.|\s|$)', re.IGNORECASE)
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text for analogical reasoning patterns."""
        analogies = self.analogical_patterns['analogy'].findall(text)
        metaphors = self.analogical_patterns['metaphor'].findall(text)

        if analogies or metaphors:
            return {
                'type': 'ANALOGICAL',
                'analogies': analogies,
                'metaphors': metaphors,
                'confidence': 0.45,
                'structure': 'Reasoning by similarity or comparison'
            }

        return {'type': 'UNKNOWN', 'confidence': 0.0}

class CausalReasoner:
    """Handles causal reasoning - identifying cause-effect relationships."""

    def __init__(self):
        self.causal_patterns = {
            'causation': re.compile(r'(?:because|since|due to|caused by|leads to|results in) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'correlation': re.compile(r'(?:correlates with|associated with|related to) (.+?)(?:\.|\s|$)', re.IGNORECASE)
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text for causal reasoning patterns."""
        causations = self.causal_patterns['causation'].findall(text)
        correlations = self.causal_patterns['correlation'].findall(text)

        if causations:
            return {
                'type': 'CAUSAL',
                'subtype': 'DIRECT_CAUSATION',
                'relationships': causations,
                'confidence': 0.80,
                'structure': 'Direct cause-effect relationships'
            }

        if correlations:
            return {
                'type': 'CAUSAL',
                'subtype': 'CORRELATION',
                'relationships': correlations,
                'confidence': 0.40,
                'structure': 'Correlational relationships'
            }

        return {'type': 'UNKNOWN', 'confidence': 0.0}

class FallacyDetector:
    """Detects common logical fallacies in reasoning."""

    def __init__(self):
        self.fallacy_patterns = {
            'ad_hominem': re.compile(r'(?:you\'re|you are) (?:stupid|wrong|bad|idiot|ignorant) (?:because|so) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'false_dichotomy': re.compile(r'(?:either|or|only|must be) (.+?) (?:or|either) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'slippery_slope': re.compile(r'(?:will lead to|will cause|will result in) (.+?) (?:then|which will|leading to) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'appeal_to_authority': re.compile(r'(?:experts say|scientists claim|authority says) (.+?)(?:\.|\s|$)', re.IGNORECASE),
            'straw_man': re.compile(r'(?:you claim|they say|opponents argue) (.+?) (?:but really|but actually) (.+?)(?:\.|\s|$)', re.IGNORECASE)
        }

    def detect(self, text: str) -> List[Dict[str, Any]]:
        """Detect logical fallacies in text."""
        fallacies = []

        for fallacy_type, pattern in self.fallacy_patterns.items():
            matches = pattern.findall(text)
            if matches:
                fallacies.append({
                    'type': fallacy_type.upper(),
                    'matches': matches,
                    'severity': 'HIGH' if len(matches) > 1 else 'MEDIUM'
                })

        return fallacies

class ArgumentParser:
    """Parses argument structure from text."""

    def __init__(self):
        self.argument_indicators = {
            'premises': ['because', 'since', 'given that', 'assuming that'],
            'conclusions': ['therefore', 'thus', 'hence', 'consequently', 'so'],
            'qualifiers': ['probably', 'likely', 'possibly', 'maybe', 'perhaps']
        }

    def parse(self, text: str) -> Dict[str, Any]:
        """Parse argument structure from text."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        premises = []
        conclusions = []
        qualifiers = []

        for sentence in sentences:
            sentence_lower = sentence.lower()

            # Check for premises
            if any(indicator in sentence_lower for indicator in self.argument_indicators['premises']):
                premises.append(sentence)

            # Check for conclusions
            if any(indicator in sentence_lower for indicator in self.argument_indicators['conclusions']):
                conclusions.append(sentence)

            # Check for qualifiers
            if any(indicator in sentence_lower for indicator in self.argument_indicators['qualifiers']):
                qualifiers.append(sentence)

        return {
            'premises': premises,
            'conclusions': conclusions,
            'qualifiers': qualifiers,
            'argument_strength': self._assess_strength(len(premises), len(conclusions), len(qualifiers))
        }

    def _assess_strength(self, num_premises: int, num_conclusions: int, num_qualifiers: int) -> str:
        """Assess the strength of the argument structure."""
        if num_premises >= 2 and num_conclusions >= 1 and num_qualifiers <= 1:
            return 'STRONG'
        elif num_premises >= 1 and num_conclusions >= 1:
            return 'MODERATE'
        elif num_qualifiers > num_premises:
            return 'WEAK'
        else:
            return 'UNCLEAR'

class ReasoningBody:
    """
    Handles logical analysis and reasoning engine for deconstructed reasoning.
    Integrates multiple reasoning types for comprehensive cognitive processing.
    """

    def __init__(self):
        logger.info("Reasoning Body Initialized with deconstructed reasoning capabilities.")
        self.deductive_reasoner = DeductiveReasoner()
        self.inductive_reasoner = InductiveReasoner()
        self.abductive_reasoner = AbductiveReasoner()
        self.analogical_reasoner = AnalogicalReasoner()
        self.causal_reasoner = CausalReasoner()
        self.fallacy_detector = FallacyDetector()
        self.argument_parser = ArgumentParser()

    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Perform comprehensive logical analysis on input text.

        Args:
            prompt: The text to analyze

        Returns:
            Dict containing reasoning analysis results
        """
        if not prompt.strip():
            return {
                'primary_reasoning_type': 'NONE',
                'confidence': 0.0,
                'analysis': 'Empty input',
                'fallacies': [],
                'argument_structure': {'premises': [], 'conclusions': [], 'qualifiers': [], 'argument_strength': 'NONE'}
            }

        # Perform analysis with all reasoners
        analyses = {
            'deductive': self.deductive_reasoner.analyze(prompt),
            'inductive': self.inductive_reasoner.analyze(prompt),
            'abductive': self.abductive_reasoner.analyze(prompt),
            'analogical': self.analogical_reasoner.analyze(prompt),
            'causal': self.causal_reasoner.analyze(prompt)
        }

        # Find the reasoning type with highest confidence
        best_analysis = max(analyses.values(), key=lambda x: x.get('confidence', 0))
        primary_type = best_analysis.get('type', 'UNKNOWN')

        # Detect fallacies
        fallacies = self.fallacy_detector.detect(prompt)

        # Parse argument structure
        argument_structure = self.argument_parser.parse(prompt)

        # Calculate overall confidence
        overall_confidence = best_analysis.get('confidence', 0.0)
        if fallacies:
            overall_confidence *= 0.7  # Reduce confidence if fallacies detected

        result = {
            'primary_reasoning_type': primary_type,
            'confidence': overall_confidence,
            'detailed_analysis': best_analysis,
            'all_reasoning_types': {k: v for k, v in analyses.items() if v['type'] != 'UNKNOWN'},
            'fallacies': fallacies,
            'argument_structure': argument_structure,
            'reasoning_complexity': self._calculate_complexity(prompt),
            'logical_validity': 'INVALID' if fallacies else 'VALID' if overall_confidence > 0.7 else 'UNCERTAIN'
        }

        logger.info(f"Logical analysis complete for prompt: '{prompt[:50]}...' -> {primary_type} (confidence: {overall_confidence:.2f})")
        return result

    def _calculate_complexity(self, text: str) -> str:
        """Calculate the complexity level of reasoning in the text."""
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))

        logical_connectors = len(re.findall(r'\b(and|or|not|if|then|because|therefore|however|although)\b', text, re.IGNORECASE))

        if logical_connectors >= 3 and sentence_count >= 3:
            return 'HIGH'
        elif logical_connectors >= 2 or sentence_count >= 2:
            return 'MEDIUM'
        elif word_count > 10:
            return 'LOW'
        else:
            return 'MINIMAL'

    def get_reasoning_profile(self, text: str) -> Dict[str, Any]:
        """Get a comprehensive reasoning profile for advanced analysis."""
        base_analysis = self.analyze(text)

        # Add additional metrics
        profile = {
            **base_analysis,
            'reasoning_patterns': self._extract_reasoning_patterns(text),
            'logical_operators_count': len(re.findall(r'\b(and|or|not|if|then|because|therefore)\b', text, re.IGNORECASE)),
            'conditional_statements': len(re.findall(r'\bif\b', text, re.IGNORECASE)),
            'causal_indicators': len(re.findall(r'\b(because|since|due to|leads to|results in)\b', text, re.IGNORECASE))
        }

        return profile

    def _extract_reasoning_patterns(self, text: str) -> List[str]:
        """Extract specific reasoning patterns found in text."""
        patterns = []

        if re.search(r'\bif .+? then\b', text, re.IGNORECASE):
            patterns.append('conditional_reasoning')
        if re.search(r'\ball .+? are\b', text, re.IGNORECASE):
            patterns.append('universal_quantification')
        if re.search(r'\bsome .+? are\b', text, re.IGNORECASE):
            patterns.append('existential_quantification')
        if re.search(r'\btherefore\b', text, re.IGNORECASE):
            patterns.append('deductive_conclusion')
        if re.search(r'\bprobably\b', text, re.IGNORECASE):
            patterns.append('probabilistic_reasoning')

        return patterns
