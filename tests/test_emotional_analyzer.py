import pytest
from src.emotional_analyzer.emotion_processor import EmotionalAnalyzer

def test_positive_sentiment():
    analyzer = EmotionalAnalyzer()
    text = "This is a wonderful and happy day."
    result = analyzer.analyze(text)
    assert result['emotion'] == 'POSITIVE'
    assert result['intensity'] > 0.9

def test_negative_sentiment():
    analyzer = EmotionalAnalyzer()
    text = "This is a sad and terrible situation."
    result = analyzer.analyze(text)
    assert result['emotion'] == 'NEGATIVE'
    assert result['intensity'] > 0.9
