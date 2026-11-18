"""Lazy, reusable Sentence Transformer wrapper.

This module is an optional helper. It does not replace or modify
modules/career_predictor.py, and it is not automatically invoked by app.py.
The model is loaded only when get_semantic_encoder() is called.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@dataclass
class SemanticEncoder:
    """Encode text and calculate cosine similarities with a loaded model."""

    model_name: str = DEFAULT_MODEL_NAME
    _model: object | None = None

    def load(self):
        """Load the transformer on first use and reuse it afterward."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError(
                    "Sentence Transformers is required. Install it with "
                    "python -m pip install sentence-transformers"
                ) from exc
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: Iterable[str]):
        """Return normalized embeddings for non-empty text strings."""
        values = [str(text).strip() for text in texts]
        if not values:
            return []
        if any(not value for value in values):
            raise ValueError("texts must not contain empty strings")
        return self.load().encode(
            values,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def similarities(self, query: str, candidates: Iterable[str]) -> list[float]:
        """Return cosine similarities between one query and candidate texts."""
        candidate_list = [str(item).strip() for item in candidates]
        if not candidate_list:
            return []
        if not str(query).strip():
            raise ValueError("query must not be empty")
        embeddings = self.encode([query, *candidate_list])
        query_vector = embeddings[0]
        candidate_vectors = embeddings[1:]
        # Embeddings are normalized, so their dot product is cosine similarity.
        return [float(score) for score in candidate_vectors @ query_vector]


@lru_cache(maxsize=2)
def get_semantic_encoder(model_name: str = DEFAULT_MODEL_NAME) -> SemanticEncoder:
    """Return a cached encoder instance for the requested model name."""
    return SemanticEncoder(model_name=model_name)


def get_model_status(model_name: str = DEFAULT_MODEL_NAME) -> dict:
    """Report whether the cached model has been loaded without loading it."""
    encoder = get_semantic_encoder(model_name)
    return {
        "model": encoder.model_name,
        "loaded": encoder._model is not None,
    }
