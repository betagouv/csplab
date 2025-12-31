"""Albert PDF text extractor implementation."""

import json
from typing import Any, Dict

import requests

from apps.candidate.config import AlbertConfig
from apps.candidate.infrastructure.constants.albert_prompts import (
    ALBERT_CV_EXTRACTION_PROMPT,
)
from apps.shared.infrastructure.exceptions import ExternalApiError
from domain.services.pdf_text_extractor_interface import IPDFTextExtractor


class AlbertPDFExtractor(IPDFTextExtractor):
    """Implementation of PDF text extraction service using Albert API."""

    def __init__(self, config: AlbertConfig):
        """Initialize with Albert configuration."""
        self.config = config

    def extract_text(self, pdf_content: bytes) -> Dict[str, Any]:
        """Extract structured content from PDF bytes using Albert API.

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Structured data as dict with format:
            {
                "experiences": [
                    {
                        "title": str,
                        "company": str,
                        "sector": str|None,
                        "description": str
                    }
                ]
            }

        Raises:
            ExternalApiError: If PDF content is invalid or API call fails
        """
        url = f"{self.config.api_base_url}v1/ocr-beta"
        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        files = {"file": ("document.pdf", pdf_content, "application/pdf")}
        data = {
            "model": self.config.model_name,
            "dpi": str(self.config.dpi),
            "prompt": ALBERT_CV_EXTRACTION_PROMPT,
        }

        response = requests.post(
            url, headers=headers, files=files, data=data, timeout=120
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
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

    def _normalize_albert_ocr_structured(self, ocr_data: Any) -> Dict[str, Any]:
        """Normalize Albert OCR JSON output to extract experiences only."""
        # Guard: Not a dict or string, return empty
        if not isinstance(ocr_data, (dict, str)):
            return {"experiences": []}

        # Case 1: Direct experiences in dict
        if isinstance(ocr_data, dict):
            experiences = ocr_data.get("experiences")
            if isinstance(experiences, list):
                return {"experiences": experiences}

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

        return {"experiences": []}

    def _extract_from_pages(self, pages: list) -> Dict[str, Any]:
        """Extract experiences from multi-page data."""
        final_experiences = []
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
            if isinstance(experiences, list):
                final_experiences.extend(experiences)
        return {"experiences": final_experiences}

    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract experiences from text content."""
        parsed = self._extract_json_from_fenced_content(text)
        if not isinstance(parsed, dict):
            return {"experiences": []}
        experiences = parsed.get("experiences", [])
        if isinstance(experiences, list):
            return {"experiences": experiences}
        return {"experiences": []}
