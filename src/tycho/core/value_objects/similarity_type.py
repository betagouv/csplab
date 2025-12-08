"""SimilarityType value object for vector search operations."""

from dataclasses import dataclass
from enum import Enum

from core.entities.vectorized_document import VectorizedDocument


class SimilarityMetric(Enum):
    """Enumeration of similarity metrics for vector search."""

    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"

    def __str__(self):
        """Return string representation."""
        return self.value


@dataclass(frozen=True)
class SimilarityType:
    """SimilarityType value object representing similarity search configuration."""

    metric: SimilarityMetric = SimilarityMetric.COSINE
    threshold: float = 0.8


@dataclass(frozen=True)
class SimilarityResult:
    """Result of a similarity search with score."""

    document: VectorizedDocument
    score: float
