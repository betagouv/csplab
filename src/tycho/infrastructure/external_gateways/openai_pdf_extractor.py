"""OpenAI PDF text extractor implementation."""

import base64
import json
from typing import Any, Dict

import pymupdf
from openai import OpenAI

from domain.services.pdf_text_extractor_interface import IPDFTextExtractor
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.configs.openai_config import OpenAIConfig
from infrastructure.external_gateways.constants.ocr_cv_prompts import (
    CV_EXTRACTION_PROMPT,
)


class OpenAIPDFExtractor(IPDFTextExtractor):
    """Implementation of PDF text extraction service using OpenAI API."""

    def __init__(self, config: OpenAIConfig):
        """Initialize with OpenAI configuration."""
        self.config = config
        self.client = OpenAI(api_key=config.api_key, base_url=str(config.base_url))

    def extract_text(self, pdf_content: bytes) -> Dict[str, Any]:
        """Extract structured content from PDF bytes.

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
                ],
                "skills": [str]
            }

        Raises:
            ValueError: If PDF content is invalid or corrupted
        """
        try:
            # Convert PDF to images using PyMuPDF
            pdf_doc = pymupdf.open(stream=pdf_content, filetype="pdf")
            images = []

            for page_num in range(len(pdf_doc)):
                page = pdf_doc[page_num]
                # Convert page to image (PNG)
                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2)
                )  # 2x zoom for better quality
                img_data = pix.tobytes("png")
                img_base64 = base64.b64encode(img_data).decode("utf-8")
                images.append(img_base64)

            pdf_doc.close()

            # Prepare messages for OpenAI API
            content = [{"type": "text", "text": CV_EXTRACTION_PROMPT}]

            # Add all images to the content
            for img_base64 in images:
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"  # type: ignore
                        },
                    }
                )

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": content}],  # type: ignore
                max_tokens=2000,
                temperature=0.1,
            )

            # Parse JSON response
            response_text = response.choices[0].message.content
            if response_text is None:
                raise ValueError("Empty response from API")
            response_text = response_text.strip()

            # Remove potential markdown code blocks
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()

            result = json.loads(response_text)

            # Validate structure
            if (
                not isinstance(result, dict)
                or "experiences" not in result
                or "skills" not in result
            ):
                raise ValueError("Invalid response structure from API")

            return result

        except json.JSONDecodeError as e:
            raise ValueError("Failed to parse JSON response") from e
        except Exception as e:
            if hasattr(e, "status_code"):
                raise ExternalApiError(
                    f"OpenAI API error: {e.status_code}",
                    status_code=e.status_code,
                    api_name="OpenAI",
                ) from e
            raise ValueError("Error processing PDF") from e

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
