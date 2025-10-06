"""AbstractPatternDetector for complex query pattern detection in cognitive modules.

Handles deterministic pattern analysis for holistic reasoning, identifying query structures,
complexity levels, and cognitive patterns without probabilistic methods.
"""
import logging
import re
from typing import Dict, List, Any, Union
from collections import Counter

logger = logging.getLogger(__name__)

class AbstractPatternDetector:
    """
    Deterministic pattern detector for analyzing query structures and cognitive patterns.
    Identifies question types, complexity metrics, and structural elements in user queries.
    """

    def __init__(self, input_dim: int = 4, latent_dim: int = 2):
        self.input_dim = input_dim
        self.latent_dim = latent_dim

        # Deterministic pattern definitions
        self.question_patterns = {
            'what': re.compile(r'\bwhat\b', re.IGNORECASE),
            'how': re.compile(r'\bhow\b', re.IGNORECASE),
            'why': re.compile(r'\bwhy\b', re.IGNORECASE),
            'when': re.compile(r'\bwhen\b', re.IGNORECASE),
            'where': re.compile(r'\bwhere\b', re.IGNORECASE),
            'who': re.compile(r'\bwho\b', re.IGNORECASE),
            'which': re.compile(r'\bwhich\b', re.IGNORECASE)
        }

        self.complexity_indicators = {
            'logical_operators': re.compile(r'\b(and|or|not|if|then|therefore|because|however|although)\b', re.IGNORECASE),
            'quantifiers': re.compile(r'\b(all|some|none|every|any|most|few|many)\b', re.IGNORECASE),
            'comparatives': re.compile(r'\b(better|worse|more|less|greater|smaller|higher|lower)\b', re.IGNORECASE),
            'technical_terms': re.compile(r'\b(algorithm|function|variable|class|method|api|database|network)\b', re.IGNORECASE)
        }

        self.structural_patterns = {
            'lists': re.compile(r'\b(first|second|third|next|then|finally|also)\b', re.IGNORECASE),
            'sequences': re.compile(r'\b(step|phase|stage|process|procedure)\b', re.IGNORECASE),
            'causality': re.compile(r'\b(causes|leads to|results in|due to|because of)\b', re.IGNORECASE)
        }

        logger.info("AbstractPatternDetector initialized with deterministic pattern recognition")

    def detect(self, input_data: Union[str, Any]) -> Dict[str, Any]:
        """
        Main detection method supporting both text queries and tensor inputs for compatibility.

        Args:
            input_data: Either a text string for pattern analysis or tensor for reconstruction

        Returns:
            Dict containing pattern analysis results and reconstruction_error for compatibility
        """
        if isinstance(input_data, str):
            return self._analyze_query_patterns(input_data)
        else:
            # Fallback for tensor inputs (maintains backward compatibility)
            return self._tensor_reconstruction(input_data)

    def _analyze_query_patterns(self, query: str) -> Dict[str, Any]:
        """
        Deterministically analyze query patterns and structure.

        Args:
            query: The text query to analyze

        Returns:
            Dict with pattern analysis results
        """
        analysis = {
            'query_length': len(query),
            'word_count': len(query.split()),
            'question_type': self._identify_question_type(query),
            'complexity_score': self._calculate_complexity(query),
            'structural_elements': self._identify_structural_elements(query),
            'cognitive_patterns': self._extract_cognitive_patterns(query),
            'reconstruction_error': self._calculate_deterministic_error(query)
        }

        logger.info(f"Pattern analysis complete for query: '{query[:50]}...' -> {analysis['question_type']}")
        return analysis

    def _identify_question_type(self, query: str) -> str:
        """Deterministically identify the primary question type."""
        for qtype, pattern in self.question_patterns.items():
            if pattern.search(query):
                return qtype.upper()

        # Check for other question indicators
        if '?' in query:
            return 'GENERAL'
        elif any(word in query.lower() for word in ['explain', 'describe', 'tell me about']):
            return 'EXPLANATORY'
        elif any(word in query.lower() for word in ['calculate', 'compute', 'solve']):
            return 'COMPUTATIONAL'

        return 'DECLARATIVE'

    def _calculate_complexity(self, query: str) -> float:
        """Calculate deterministic complexity score based on linguistic features."""
        score = 0.0

        # Length-based complexity
        word_count = len(query.split())
        if word_count > 20:
            score += 0.3
        elif word_count > 10:
            score += 0.2
        elif word_count > 5:
            score += 0.1

        # Pattern-based complexity
        for category, pattern in self.complexity_indicators.items():
            matches = len(pattern.findall(query))
            if matches > 0:
                score += min(matches * 0.1, 0.3)  # Cap at 0.3 per category

        # Sentence structure complexity
        sentence_count = len(re.split(r'[.!?]+', query))
        if sentence_count > 2:
            score += 0.2

        return min(score, 1.0)  # Normalize to [0,1]

    def _identify_structural_elements(self, query: str) -> List[str]:
        """Identify structural elements in the query."""
        elements = []

        for element_type, pattern in self.structural_patterns.items():
            if pattern.search(query):
                elements.append(element_type)

        # Additional structural checks
        if re.search(r'\d+\.', query):  # Numbered lists
            elements.append('numbered_list')
        if re.search(r'[a-z]\)', query, re.IGNORECASE):  # Lettered lists
            elements.append('lettered_list')
        if ':' in query and len(query.split(':')) > 1:
            elements.append('definition_structure')

        return elements

    def _extract_cognitive_patterns(self, query: str) -> Dict[str, int]:
        """Extract cognitive pattern frequencies deterministically."""
        patterns = {}

        # Logical connectives
        logical_words = ['and', 'or', 'not', 'if', 'then', 'because', 'therefore']
        patterns['logical_connectives'] = sum(1 for word in logical_words if word in query.lower())

        # Temporal references
        temporal_words = ['before', 'after', 'during', 'while', 'since', 'until']
        patterns['temporal_references'] = sum(1 for word in temporal_words if word in query.lower())

        # Comparative language
        comparative_words = ['better', 'worse', 'more', 'less', 'than', 'versus', 'compared']
        patterns['comparative_language'] = sum(1 for word in comparative_words if word in query.lower())

        # Abstract concepts
        abstract_words = ['concept', 'theory', 'principle', 'pattern', 'structure', 'system']
        patterns['abstract_concepts'] = sum(1 for word in abstract_words if word in query.lower())

        return patterns

    def _calculate_deterministic_error(self, query: str) -> float:
        """Calculate a deterministic 'reconstruction error' based on query characteristics."""
        # Use deterministic hash-like calculation for reproducibility
        char_sum = sum(ord(c) for c in query)
        word_count = len(query.split())
        length_factor = len(query)

        # Combine factors deterministically
        combined = (char_sum + word_count + length_factor) % 1000
        error = (combined / 1000.0) * 0.1  # Scale to reasonable error range

        return error

    def _tensor_reconstruction(self, tensor: Any) -> Dict[str, Any]:
        """Fallback method for tensor inputs (backward compatibility)."""
        try:
            if hasattr(tensor, 'numpy'):
                data = tensor.numpy()
            else:
                data = tensor

            # Deterministic reconstruction error calculation
            total = 0.0
            count = 0
            for row in data:
                if isinstance(row, (list, tuple)):
                    for val in row:
                        total += float(val)
                        count += 1
                else:
                    total += float(row)
                    count += 1

            reconstruction_error = abs(total / max(count, 1)) % 1.0

        except Exception as e:
            logger.warning(f"Tensor reconstruction failed: {e}")
            reconstruction_error = 0.42

        return {
            'reconstruction_error': reconstruction_error,
            'input_type': 'tensor',
            'note': 'Tensor input detected - using legacy reconstruction mode'
        }

    def analyze_patterns(self, queries: List[str]) -> Dict[str, Any]:
        """
        Analyze patterns across multiple queries for batch processing.

        Args:
            queries: List of query strings to analyze

        Returns:
            Dict with aggregate pattern analysis
        """
        if not queries:
            return {'error': 'No queries provided'}

        individual_analyses = [self._analyze_query_patterns(q) for q in queries]

        # Aggregate results deterministically
        question_types = Counter(analysis['question_type'] for analysis in individual_analyses)
        avg_complexity = sum(a['complexity_score'] for a in individual_analyses) / len(individual_analyses)

        # Find most common structural elements
        all_elements = []
        for analysis in individual_analyses:
            all_elements.extend(analysis['structural_elements'])
        common_elements = Counter(all_elements).most_common(3)

        return {
            'total_queries': len(queries),
            'dominant_question_type': question_types.most_common(1)[0][0] if question_types else 'UNKNOWN',
            'average_complexity': avg_complexity,
            'common_structural_elements': [elem for elem, _ in common_elements],
            'pattern_distribution': dict(question_types),
            'individual_analyses': individual_analyses
        }
