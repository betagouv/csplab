"""Albert embedding generator service."""

from typing import List

from pydantic import ValidationError

from config.app_config import AlbertConfig
from domain.services.embedding_generator_interface import IEmbeddingGenerator
from domain.services.http_client_interface import IHttpClient
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dtos.albert_types import AlbertEmbeddingResponse


class AlbertEmbeddingGenerator(IEmbeddingGenerator):
    def __init__(self, config: AlbertConfig, http_client: IHttpClient):
        self.config = config
        self.http_client = http_client

    def generate_embedding(self, text: str) -> List[float]:
        if not text.strip():
            raise ValueError("Text content cannot be empty")

        response = self.http_client.request(
            method="POST",
            url=f"{self.config.api_base_url}v1/embeddings",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
            json={
                "input": text,
                "model": "openweight-embeddings",
            },
        )

        try:
            response.raise_for_status()
            response_data = response.json()

            # Validate response using Pydantic model
            albert_response = AlbertEmbeddingResponse.model_validate(response_data)

            # Extract embedding from validated response
            if albert_response.data and len(albert_response.data) > 0:
                return albert_response.data[0].embedding
            else:
                raise ExternalApiError(
                    "No embedding data in Albert API response",
                    api_name="Albert",
                )
        except ValidationError as e:
            raise ExternalApiError(
                f"Invalid Albert API response structure: {e}",
                api_name="Albert",
            ) from e
        except Exception as e:
            raise ExternalApiError(
                f"Albert API error: {response.status_code}",
                status_code=response.status_code,
                api_name="Albert",
                details={
                    "method": "POST",
                    "endpoint": "v1/embeddings",
                    "response_text": response.text,
                },
            ) from e
