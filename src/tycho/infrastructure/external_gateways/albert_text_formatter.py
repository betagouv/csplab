import json
from http import HTTPStatus
from typing import Any, Dict

from pydantic import ValidationError

from config.app_config import AlbertConfig
from domain.services.async_http_client_interface import IAsyncHttpClient
from domain.services.text_formatter_interface import ITextFormatter
from domain.types import JsonDataType
from domain.value_objects.cv_extraction_types import CVExtractionResult
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.constants.ocr_cv_prompts import (
    CV_EXTRACTION_PROMPT,
)
from infrastructure.external_gateways.dtos.albert_types import (
    AlbertCompletionResponse,
    AlbertErrorResponse,
)


class AlbertTextFormatter(ITextFormatter):
    def __init__(self, config: AlbertConfig, http_client: IAsyncHttpClient):
        self.config = config
        self.http_client = http_client

    async def format_text(self, extracted_text: str) -> CVExtractionResult:
        url = f"{self.config.api_base_url}v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.config.api_key}"}

        data: JsonDataType = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": CV_EXTRACTION_PROMPT},
                {
                    "role": "user",
                    "content": f"Voici le texte du CV à formatter :\
                    \n\n{extracted_text}",
                },
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
        }

        async with self.http_client as client:
            response = await client.post(url, headers=headers, json=data)

        # Handle error responses
        if response.status_code != HTTPStatus.OK:
            try:
                error_data = response.json()
                error_response = AlbertErrorResponse.model_validate(error_data)
                error_message = error_response.detail
            except Exception:
                error_message = f"Albert completion API error: {response.status_code}"

            raise ExternalApiError(
                error_message,
                status_code=response.status_code,
                api_name="Albert chat completion",
                details={
                    "method": "POST",
                    "endpoint": "/v1/chat/completions",
                    "response_text": response.text,
                },
            )
        albert_response = None
        try:
            # Parse Albert completion response
            response_data = response.json()
            albert_response = AlbertCompletionResponse.model_validate(response_data)

        except ValidationError as e:
            raise ExternalApiError(
                f"Invalid Albert completion response structure: {e}",
                api_name="Albert",
                details={
                    "method": "POST",
                    "endpoint": "/v1/chat/completions",
                    "response_data": str(response_data),
                },
            ) from e

        # Extract the completion content
        if not albert_response.choices:
            raise ExternalApiError(
                "No completion choices returned from Albert API",
                api_name="Albert",
                details={
                    "method": "POST",
                    "endpoint": "/v1/chat/completions",
                    "response_data": str(response_data),
                },
            )

        completion_content = albert_response.choices[0].message.content or ""

        # Parse the JSON response from Albert
        try:
            cv_data = json.loads(completion_content)
            return CVExtractionResult.model_validate(cv_data)
        except json.JSONDecodeError:
            cv_data = self._extract_json_from_fenced_content(completion_content)
            return CVExtractionResult.model_validate(cv_data)

    def _extract_json_from_fenced_content(self, text: str) -> Dict[str, Any]:
        try:
            text = text.strip()
            if text.startswith("```"):
                first_newline = text.find("\n")
                if first_newline != -1:
                    text = text[first_newline + 1 :]
                fence_pos = text.rfind("```")
                if fence_pos != -1:
                    text = text[:fence_pos]
            return json.loads(text)
        except (json.JSONDecodeError, ValidationError) as e:
            raise ExternalApiError(
                "Failed to parse JSON from Albert completion response",
                api_name="Albert",
                details={
                    "method": "POST",
                    "endpoint": "/v1/chat/completions",
                },
            ) from e
