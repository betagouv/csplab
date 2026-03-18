"""OpenAI embedding generator service."""

from typing import List

from openai import OpenAI

from config.app_config import OpenAIConfig
from domain.services.embedding_generator_interface import IEmbeddingGenerator
from infrastructure.exceptions.exceptions import ExternalApiError


class OpenAIEmbeddingGenerator(IEmbeddingGenerator):
    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = OpenAI(api_key=config.api_key, base_url=str(config.base_url))

    def generate_embedding(self, text: str) -> List[float]:
        if not text.strip():
            raise ValueError("Text content cannot be empty")

        try:
            response = self.client.embeddings.create(
                model=self.config.embedding_model, input=text, encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            raise ExternalApiError(f"Failed to generate embedding: {str(e)}") from e
