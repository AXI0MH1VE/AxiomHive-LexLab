"""Minimal local shim for the `transformers` pipeline API used by the project.

This provides a very small `pipeline` function that returns a callable which
simulates sentiment-analysis behavior without heavy models.
"""
from typing import Callable

def pipeline(task: str, model: str = None) -> Callable[[str], list]:
    if task == 'sentiment-analysis':
        def sentiment(text: str):
            # very small deterministic heuristic
            if any(w in text.lower() for w in ('happy','joy','good','great','love')):
                return [{'label': 'POSITIVE', 'score': 0.95}]
            if any(w in text.lower() for w in ('sad','bad','angry','hate','fail')):
                return [{'label': 'NEGATIVE', 'score': 0.9}]
            return [{'label': 'NEUTRAL', 'score': 0.5}]
        return sentiment
    raise RuntimeError(f"Unsupported pipeline task: {task}")
