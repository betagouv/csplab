"""Albert PDF text extractor implementation."""

import json
from typing import Any, Dict

from pydantic import ValidationError

from config.app_config import AlbertConfig
from domain.services.async_http_client_interface import IAsyncHttpClient
from domain.value_objects.cv_extraction_types import CVExtractionResult
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.constants.ocr_cv_prompts import (
    CV_EXTRACTION_PROMPT,
)
from infrastructure.external_gateways.dtos.albert_types import AlbertOCRResponse


class AlbertPDFExtractor:
    def __init__(self, config: AlbertConfig, http_client: IAsyncHttpClient):
        self.config = config
        self.http_client = http_client

    async def extract_text(self, pdf_content: bytes) -> CVExtractionResult:

        url = f"{self.config.api_base_url}v1/ocr-beta"
        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        files = {"file": ("document.pdf", pdf_content, "application/pdf")}
        data = {
            "model": self.config.ocr_model,
            "dpi": str(self.config.ocr_dpi),
            "prompt": CV_EXTRACTION_PROMPT,
        }

        async with self.http_client as client:
            response = await client.post(url, headers=headers, files=files, data=data)

        try:
            response.raise_for_status()
            ocr_data = response.json()
            albert_response = AlbertOCRResponse.model_validate(ocr_data)
            return self._normalize_albert_ocr_structured(albert_response)
        except json.JSONDecodeError as e:
            raise ExternalApiError(
                "Failed to parse JSON response."
                f"Erreur: {e.msg} at line {e.lineno} column {e.colno}",
                api_name="Albert",
            ) from e
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
                    "endpoint": "v1/ocr-beta",
                    "response_text": response.text,
                },
            ) from e

    def _extract_json_from_fenced_content(self, text: str) -> Dict[str, Any]:
        text = text.strip()
        if text.startswith("```"):
            first_newline = text.find("\n")
            if first_newline != -1:
                text = text[first_newline + 1 :]
            fence_pos = text.rfind("```")
            if fence_pos != -1:
                text = text[:fence_pos]
        return json.loads(text)

    def _normalize_albert_ocr_structured(
        self, albert_response: AlbertOCRResponse
    ) -> CVExtractionResult:
        # Extract content from all pages
        final_experiences = []
        final_skills = []

        for page in albert_response.data:
            content = page.content.strip()
            parsed_json = None

            # First try: direct JSON parsing
            if content.startswith("{") and content.endswith("}"):
                try:
                    parsed_json = json.loads(content)
                except json.JSONDecodeError:
                    pass

            # Second try: extract from markdown fenced blocks
            if parsed_json is None:
                parsed_json = self._extract_json_from_fenced_content(content)

            # Extract experiences and skills if we have valid JSON
            if isinstance(parsed_json, dict):
                experiences = parsed_json.get("experiences", [])
                skills = parsed_json.get("skills", [])

                if isinstance(experiences, list):
                    final_experiences.extend(experiences)

                if isinstance(skills, list):
                    final_skills.extend(skills)

        return CVExtractionResult.model_validate(
            {"experiences": final_experiences, "skills": final_skills}
        )
