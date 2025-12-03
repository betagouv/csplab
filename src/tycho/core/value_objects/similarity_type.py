"""SimilarityType value object for vector search operations."""

from dataclasses import dataclass
from enum import Enum


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
