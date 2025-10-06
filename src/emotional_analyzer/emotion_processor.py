import logging
import re
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionLexicon:
    """Deterministic lexicon for emotion detection based on word patterns."""

    def __init__(self):
        self.emotion_words = {
            "JOY": ["happy", "joy", "delight", "ecstatic", "thrilled", "excited", "cheerful", "glad"],
            "SADNESS": ["sad", "unhappy", "depressed", "sorrow", "grief", "melancholy", "blue", "down"],
            "ANGER": ["angry", "furious", "mad", "rage", "irritated", "annoyed", "frustrated", "outraged"],
            "FEAR": ["afraid", "scared", "terrified", "anxious", "frightened", "panicked", "worried", "nervous"],
            "SURPRISE": ["surprised", "shocked", "amazed", "astonished", "startled", "bewildered", "stunned"],
            "DISGUST": ["disgusted", "repulsed", "nauseated", "reviled", "abhorrent", "loathsome", "sickened"],
            "POSITIVE": ["good", "great", "excellent", "wonderful", "fantastic", "amazing", "awesome", "brilliant"],
            "NEGATIVE": ["bad", "terrible", "awful", "horrible", "dreadful", "atrocious", "abysmal", "vile"]
        }
        self.intensifiers = ["very", "extremely", "so", "really", "incredibly", "absolutely", "totally"]
        self.negators = ["not", "no", "never", "none", "neither", "nor"]

    def detect_emotions(self, text: str) -> Dict[str, float]:
        """Detect emotions in text and return scores."""
        text_lower = text.lower()
        scores = {emotion: 0.0 for emotion in self.emotion_words}

        words = re.findall(r'\b\w+\b', text_lower)
        for i, word in enumerate(words):
            for emotion, keywords in self.emotion_words.items():
                if word in keywords:
                    score = 1.0
                    # Check for intensifiers before the word
                    if i > 0 and words[i-1] in self.intensifiers:
                        score *= 1.5
                    # Check for negators
                    if any(neg in words[max(0, i-3):i] for neg in self.negators):
                        score *= -0.5
                    scores[emotion] += score

        # Normalize scores
        total = sum(abs(s) for s in scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}

        return scores

class ContextProcessor:
    """Processes contextual nuances in text."""

    def __init__(self):
        self.punctuation_patterns = {
            "exclamation": r'!+',
            "question": r'\?+',
            "ellipsis": r'\.\.\.+'
        }

    def analyze_context(self, text: str) -> Dict[str, float]:
        """Analyze contextual elements like punctuation and structure."""
        context_scores = {
            "intensity_modifier": 1.0,
            "sarcasm_indicator": 0.0,
            "urgency": 0.0
        }

        # Punctuation analysis
        if re.search(self.punctuation_patterns["exclamation"], text):
            context_scores["intensity_modifier"] *= 1.3
            context_scores["urgency"] += 0.5

        if re.search(self.punctuation_patterns["question"], text):
            context_scores["intensity_modifier"] *= 0.8  # Questions often less intense

        if re.search(self.punctuation_patterns["ellipsis"], text):
            context_scores["intensity_modifier"] *= 0.9  # Ellipsis suggests hesitation

        # Capitalization check (all caps might indicate strong emotion)
        if text.isupper() and len(text) > 5:
            context_scores["intensity_modifier"] *= 1.4
            context_scores["urgency"] += 0.3

        # Repeated words (emphasis)
        words = re.findall(r'\b\w+\b', text.lower())
        if len(words) != len(set(words)):
            context_scores["intensity_modifier"] *= 1.2

        return context_scores

class EmotionalAnalyzer:
    """Main emotional analysis processor with contextual nuance."""

    def __init__(self):
        logger.info("Initializing Emotional Analyzer with deterministic, local processing.")
        self.lexicon = EmotionLexicon()
        self.context_processor = ContextProcessor()

    def analyze(self, text: str, context: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Analyze emotional content with contextual nuance.

        Args:
            text: The text to analyze
            context: Optional list of previous messages for context

        Returns:
            Dict with emotion, intensity, confidence, and additional insights
        """
        if not text.strip():
            return {"emotion": "NEUTRAL", "intensity": 0.0, "confidence": 1.0, "source": "Empty Input"}

        # Lexical emotion detection
        emotion_scores = self.lexicon.detect_emotions(text)

        # Contextual analysis
        context_scores = self.context_processor.analyze_context(text)

        # Apply context modifiers
        for emotion in emotion_scores:
            emotion_scores[emotion] *= context_scores["intensity_modifier"]

        # Determine primary emotion
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        intensity = emotion_scores[primary_emotion]

        # Calculate confidence based on score distribution
        sorted_scores = sorted(emotion_scores.values(), reverse=True)
        if len(sorted_scores) > 1 and sorted_scores[0] > 0:
            confidence = sorted_scores[0] / (sorted_scores[0] + sorted_scores[1] + 0.1)  # Avoid division by zero
        else:
            confidence = 0.5

        # Contextual insights from history (if provided)
        historical_insight = ""
        if context:
            prev_emotions = [self.analyze(prev)["emotion"] for prev in context[-3:]]  # Last 3 messages
            if prev_emotions and primary_emotion != "NEUTRAL":
                if all(e == primary_emotion for e in prev_emotions):
                    historical_insight = f"Consistent {primary_emotion.lower()} tone detected in recent context."
                elif any(e in ["ANGER", "SADNESS"] for e in prev_emotions):
                    historical_insight = "Emotional escalation detected from previous interactions."

        result = {
            "emotion": primary_emotion,
            "intensity": min(intensity, 1.0),  # Cap at 1.0
            "confidence": confidence,
            "source": "Deterministic Lexical Analysis",
            "contextual_modifier": context_scores["intensity_modifier"],
            "insights": historical_insight or "No significant contextual insights."
        }

        logger.info(f"Emotional analysis complete for text: '{text[:30]}' -> {primary_emotion} (intensity: {intensity:.2f})")
        return result

    def get_emotion_profile(self, text: str) -> Dict[str, float]:
        """Get full emotion profile for advanced analysis."""
        return self.lexicon.detect_emotions(text)

    def detect_sarcasm_indicators(self, text: str) -> bool:
        """Simple rule-based sarcasm detection."""
        # Basic heuristics: excessive punctuation, contradictory phrases
        sarcasm_score = 0
        if re.search(r'!{2,}', text):
            sarcasm_score += 1
        if re.search(r'\?{2,}', text):
            sarcasm_score += 1
        if "obviously" in text.lower() and "not" in text.lower():
            sarcasm_score += 2
        return sarcasm_score > 2
