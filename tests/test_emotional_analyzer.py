import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.emotional_analyzer.emotion_processor import EmotionalAnalyzer

def test_positive_sentiment():
    analyzer = EmotionalAnalyzer()
    text = "This is a wonderful and happy day."
    result = analyzer.analyze(text)
    assert result['emotion'] == 'JOY'
    assert result['intensity'] > 0.4

def test_negative_sentiment():
    analyzer = EmotionalAnalyzer()
    text = "This is a sad and terrible situation."
    result = analyzer.analyze(text)
    assert result['emotion'] == 'SADNESS'
    assert result['intensity'] > 0.4
