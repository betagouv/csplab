import json
from typing import Any, Dict, List

from django.conf import settings

from domain.services.embedding_generator_interface import IEmbeddingGenerator


class MockEmbeddingGenerator(IEmbeddingGenerator):
    def __init__(self, fixtures: Dict[str, Dict[str, Any]]):

        self.fixtures = fixtures
        self._text_to_embedding = {}
        for corps_data in fixtures.values():
            text = corps_data["long_label"]
            embedding = corps_data["embedding"]
            self._text_to_embedding[text] = embedding

    @classmethod
    def from_file(cls, fixtures_path: str) -> "MockEmbeddingGenerator":
        with open(fixtures_path, "r", encoding="utf-8") as f:
            fixtures = json.load(f)
        return cls(fixtures)

    async def generate_embedding(self, text: str) -> List[float]:

        if text in self._text_to_embedding:
            return self._text_to_embedding[text]

        # Fallback
        # we do not want all zeros array which make semantic_search
        # returns array of nan
        return [1e-8] * settings.EMBEDDING_DIMENSION
