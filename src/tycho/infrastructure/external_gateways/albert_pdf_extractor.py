"""Albert PDF text extractor implementation."""

import json
from typing import Any, Dict

from domain.services.async_http_client_interface import IAsyncHttpClient
from domain.services.pdf_text_extractor_interface import IPDFTextExtractor
from domain.value_objects.cv_extraction_types import CVExtractionResult
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.configs.albert_config import AlbertConfig
from infrastructure.external_gateways.constants.ocr_cv_prompts import (
    CV_EXTRACTION_PROMPT,
)


class AlbertPDFExtractor(IPDFTextExtractor):
    """Implementation of PDF text extraction service using Albert API."""

    def __init__(self, config: AlbertConfig, http_client: IAsyncHttpClient):
        """Initialize with Albert configuration and HTTP client."""
        self.config = config
        self.http_client = http_client

    async def extract_text(self, pdf_content: bytes) -> CVExtractionResult:
        """Extract structured content from PDF bytes using Albert API.

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Structured CV extraction result with experiences and skills

        Raises:
            ExternalApiError: If PDF content is invalid or API call fails
        """
        url = f"{self.config.api_base_url}v1/ocr-beta"
        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        files = {"file": ("document.pdf", pdf_content, "application/pdf")}
        data = {
            "model": self.config.model_name,
            "dpi": str(self.config.dpi),
            "prompt": CV_EXTRACTION_PROMPT,
        }

        async with self.http_client as client:
            response = await client.post(url, headers=headers, files=files, data=data)

        try:
            response.raise_for_status()
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

        try:
            ocr_data = response.json()
            return self._normalize_albert_ocr_structured(ocr_data)
        except json.JSONDecodeError as e:
            raise ExternalApiError(
                "Invalid JSON response from Albert API",
                api_name="Albert",
            ) from e

    def validate_pdf(self, pdf_content: bytes, max_size_mb: int = 5) -> bool:
        """Validate PDF format and size.

        Args:
            pdf_content: PDF file content as bytes
            max_size_mb: Maximum allowed file size in MB (default 5MB)

        Returns:
            True if PDF is valid, False otherwise
        """
        if not pdf_content:
            return False

        # Check file size
        size_mb = len(pdf_content) / (1024 * 1024)
        if size_mb > max_size_mb:
            return False

        # Check PDF magic bytes
        if not pdf_content.startswith(b"%PDF-"):
            return False

        return True

    def _extract_json_from_fenced_content(self, text: str) -> Dict[str, Any]:
        """Extract JSON from Markdown code block."""
        text = text.strip()
        if text.startswith("```"):
            first_newline = text.find("\n")
            if first_newline != -1:
                text = text[first_newline + 1 :]
            fence_pos = text.rfind("```")
            if fence_pos != -1:
                text = text[:fence_pos]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {}

    def _normalize_albert_ocr_structured(self, ocr_data: Any) -> CVExtractionResult:
        """Normalize Albert OCR JSON output to extract experiences and skills."""
        # Guard: Not a dict or string, return empty
        if not isinstance(ocr_data, (dict, str)):
            return CVExtractionResult(experiences=[], skills=[])

        # Case 1: Direct experiences in dict
        if isinstance(ocr_data, dict):
            experiences = ocr_data.get("experiences")
            skills = ocr_data.get("skills", [])
            if isinstance(experiences, list):
                return CVExtractionResult(
                    experiences=experiences,
                    skills=skills if isinstance(skills, list) else [],
                )

            # Case 2: Multi-page structure
            data = ocr_data.get("data")
            if isinstance(data, list):
                return self._extract_from_pages(data)

            # Case 3: Text field
            text = ocr_data.get("text")
            if isinstance(text, str):
                return self._extract_from_text(text)

        # Case 4: Raw string
        if isinstance(ocr_data, str):
            return self._extract_from_text(ocr_data)

        return CVExtractionResult(experiences=[], skills=[])

    def _extract_from_pages(self, pages: list) -> CVExtractionResult:
        """Extract experiences and skills from multi-page data."""
        final_experiences = []
        final_skills = []
        for page in pages:
            if not isinstance(page, dict):
                continue
            content = page.get("content")
            if not isinstance(content, str):
                continue
            parsed = self._extract_json_from_fenced_content(content)
            if not isinstance(parsed, dict):
                continue
            experiences = parsed.get("experiences", [])
            skills = parsed.get("skills", [])
            if isinstance(experiences, list):
                final_experiences.extend(experiences)
            if isinstance(skills, list):
                final_skills.extend(skills)
        return CVExtractionResult(experiences=final_experiences, skills=final_skills)

    def _extract_from_text(self, text: str) -> CVExtractionResult:
        """Extract experiences and skills from text content."""
        parsed = self._extract_json_from_fenced_content(text)
        if not isinstance(parsed, dict):
            return CVExtractionResult(experiences=[], skills=[])
        experiences = parsed.get("experiences", [])
        skills = parsed.get("skills", [])
        return CVExtractionResult(
            experiences=experiences if isinstance(experiences, list) else [],
            skills=skills if isinstance(skills, list) else [],
        )
