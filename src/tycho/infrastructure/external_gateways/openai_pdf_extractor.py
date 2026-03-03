"""OpenAI PDF text extractor implementation."""

import base64
import json

import pymupdf
from openai import (
    APIStatusError,
    AsyncOpenAI,
)
from pydantic import ValidationError

from config.app_config import OpenAIConfig
from domain.services.pdf_text_extractor_interface import IPDFTextExtractor
from domain.value_objects.cv_extraction_types import CVExtractionResult
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.constants.ocr_cv_prompts import (
    CV_EXTRACTION_PROMPT,
)
from infrastructure.external_gateways.dtos.openai_dtos import OpenAIResponse


class OpenAIPDFExtractor(IPDFTextExtractor):
    """Implementation of PDF text extraction service using OpenAI API."""

    def __init__(self, config: OpenAIConfig):
        """Initialize with OpenAI configuration."""
        self.config = config
        self.client = AsyncOpenAI(api_key=config.api_key, base_url=str(config.base_url))

    async def extract_text(self, pdf_content: bytes) -> CVExtractionResult:
        """Extract structured content from PDF bytes.

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Structured CV extraction result with experiences and skills

        Raises:
            ExternalApiError: If OpenAI API call fails or returns invalid data
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
            raw_response = await self.client.chat.completions.create(
                model=self.config.ocr_model,
                messages=[{"role": "user", "content": content}],  # type: ignore
                max_tokens=2000,
                temperature=0.1,
            )

            # Validate OpenAI response structure with Pydantic
            validated_response = OpenAIResponse.model_validate(
                raw_response.model_dump()
            )

            response_text = validated_response.choices[0].message.content
            if response_text is None:
                raise ExternalApiError("Empty response from API")
            response_text = response_text.strip()

            # Remove potential markdown code blocks
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()

            result_dict = json.loads(response_text)

            return CVExtractionResult.model_validate(result_dict)

        except APIStatusError as e:
            # Gestion détaillée des erreurs HTTP d'OpenAI (similaire à Albert)
            raise ExternalApiError(
                f"OpenAI API error: {e.status_code}",
                status_code=e.status_code,
                api_name="OpenAI",
                details={
                    "method": "POST",
                    "endpoint": "chat/completions",
                    "response_text": str(e.response.text)
                    if hasattr(e, "response")
                    else str(e),
                    "error_type": type(e).__name__,
                    "message": e.message if hasattr(e, "message") else str(e),
                },
            ) from e
        except json.JSONDecodeError as e:
            raise ExternalApiError(
                "Failed to parse JSON response from OpenAI API. "
                f"Erreur: {e.msg} at line {e.lineno} column {e.colno}",
                api_name="OpenAI",
                details={
                    "method": "POST",
                    "endpoint": "chat/completions",
                    "error_type": "JSONDecodeError",
                },
            ) from e
        except ValidationError as e:
            raise ExternalApiError(
                f"Invalid response structure: {e}",
                api_name="OpenAI",
                details={
                    "method": "POST",
                    "endpoint": "chat/completions",
                    "error_type": "ValidationError",
                },
            ) from e
        except Exception as e:
            raise ExternalApiError(
                "Error processing PDF",
                api_name="OpenAI",
                details={
                    "method": "POST",
                    "endpoint": "chat/completions",
                    "error_type": type(e).__name__,
                    "message": str(e),
                },
            ) from e
