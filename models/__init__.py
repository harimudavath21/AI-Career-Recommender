"""Reusable machine-learning helpers for CareerCompass AI.

The existing career_predictor.py remains the primary recommendation engine.
"""
from .semantic_model import SemanticEncoder, get_semantic_encoder

__all__ = ["SemanticEncoder", "get_semantic_encoder"]
