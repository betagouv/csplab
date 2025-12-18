"""OpenAI embedding generator service."""

from typing import List

from openai import OpenAI

from apps.shared.config import OpenAIConfig
from apps.shared.infrastructure.exceptions import ExternalApiError
from core.services.embedding_generator_interface import IEmbeddingGenerator


class OpenAIEmbeddingGenerator(IEmbeddingGenerator):
    """Service for generating embeddings using OpenAI's text-embedding-3-large model."""

    def __init__(self, config: OpenAIConfig):
        """Initialize with OpenAI configuration."""
        self.config = config
        self.client = OpenAI(api_key=config.api_key, base_url=str(config.base_url))

    def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector from text content."""
        if not text.strip():
            raise ValueError("Text content cannot be empty")

        try:
            response = self.client.embeddings.create(
                model=self.config.model, input=text, encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            # Extract status code from OpenAI error if available
            status_code = getattr(e, 'status_code', None)
            raise ExternalApiError(
                f"Failed to generate embedding: {str(e)}",
                status_code=status_code,
                api_name="OpenRouter"
            ) from e
