"""Albert PDF text extractor implementation."""

import json
from typing import Any, Dict, List

from pydantic import BaseModel, ValidationError

from config.app_config import AlbertConfig
from domain.services.async_http_client_interface import IAsyncHttpClient
from domain.services.pdf_text_extractor_interface import IPDFTextExtractor
from domain.value_objects.cv_extraction_types import CVExtractionResult
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.constants.ocr_cv_prompts import (
    CV_EXTRACTION_PROMPT,
)


class AlbertUsageCarbon(BaseModel):
    """Carbon usage information from Albert API."""

    kWh: Dict[str, float]
    kgCO2eq: Dict[str, float]


class AlbertUsage(BaseModel):
    """Usage information from Albert API."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    carbon: AlbertUsageCarbon
    requests: int


class AlbertDocumentPageMetadata(BaseModel):
    """Metadata for a document page from Albert API."""

    document_name: str
    page: int


class AlbertDocumentPage(BaseModel):
    """Document page from Albert API."""

    object: str
    content: str
    images: Dict[str, str]
    metadata: AlbertDocumentPageMetadata


class AlbertOCRResponse(BaseModel):
    """Complete OCR response structure from Albert API."""

    object: str
    data: List[AlbertDocumentPage]
    usage: AlbertUsage


class AlbertPDFExtractor(IPDFTextExtractor):
    """Implementation of PDF text extraction service using Albert API."""

    def __init__(self, config: AlbertConfig, http_client: IAsyncHttpClient):
        """Initialize with Albert configuration, HTTP client and logger."""
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
            "model": self.config.ocr_model,
            "dpi": str(self.config.ocr_dpi),
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

            # Parse the response using the Pydantic model
            albert_response = AlbertOCRResponse.model_validate(ocr_data)
            return self._normalize_albert_ocr_structured(albert_response)
        except json.JSONDecodeError as e:
            raise ExternalApiError(
                "Invalid JSON response from Albert API",
                api_name="Albert",
            ) from e
        except ValidationError as e:
            raise ExternalApiError(
                f"Invalid Albert API response structure: {e}",
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
        return json.loads(text)

    def _normalize_albert_ocr_structured(
        self, albert_response: AlbertOCRResponse
    ) -> CVExtractionResult:
        """Normalize Albert OCR JSON output to extract experiences and skills."""
        try:
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

            # Create and validate the final result
            result = CVExtractionResult.model_validate(
                {"experiences": final_experiences, "skills": final_skills}
            )

            return result

        except ValidationError as e:
            raise ExternalApiError(f"Invalid CV extraction result format: {e}") from e
        except Exception as e:
            raise ExternalApiError(f"Error processing Albert API response: {e}") from e
