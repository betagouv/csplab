"""Mock embedding generator using pre-computed fixtures for testing."""

import json
from typing import Any, Dict, List

from domain.services.embedding_generator_interface import IEmbeddingGenerator


class MockEmbeddingGenerator(IEmbeddingGenerator):
    """Mock implementation of embedding generator using fixtures."""

    def __init__(self, fixtures: Dict[str, Dict[str, Any]]):
        """Initialize with embedding fixtures.

        Args:
            fixtures: Dict with structure

            {corps_id: {long_label: str, embedding: List[float]}}
        """
        self.fixtures = fixtures
        self._text_to_embedding = {}
        for corps_data in fixtures.values():
            text = corps_data["long_label"]
            embedding = corps_data["embedding"]
            self._text_to_embedding[text] = embedding

    @classmethod
    def from_file(cls, fixtures_path: str) -> "MockEmbeddingGenerator":
        """Create instance from fixtures file."""
        with open(fixtures_path, "r", encoding="utf-8") as f:
            fixtures = json.load(f)
        return cls(fixtures)

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text using fixtures.

        Args:
            text: Text to generate embedding for

        Returns:
            List of floats representing the embedding

        Raises:
            ValueError: If no fixture found for the given text
        """
        if text in self._text_to_embedding:
            return self._text_to_embedding[text]

        # Fallback
        return [0.0] * 3072
