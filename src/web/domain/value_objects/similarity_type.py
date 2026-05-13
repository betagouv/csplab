from dataclasses import dataclass
from enum import Enum

from domain.entities.vectorized_document import VectorizedDocument


class SimilarityMetric(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class SimilarityType:
    metric: SimilarityMetric = SimilarityMetric.COSINE
    threshold: float = 0.8


@dataclass(frozen=True)
class SimilarityResult:
    document: VectorizedDocument
    score: float
