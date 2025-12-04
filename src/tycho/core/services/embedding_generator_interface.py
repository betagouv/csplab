"""Embedding generator interface for text vectorization."""

from typing import List, Protocol


class IEmbeddingGenerator(Protocol):
    """Interface for generating embeddings from text content."""

    def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector from text content."""
        ...
