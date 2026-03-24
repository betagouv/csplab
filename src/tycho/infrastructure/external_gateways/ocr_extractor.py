from http import HTTPStatus

from pydantic import BaseModel

from config.app_config import OCRConfig
from domain.services.async_http_client_interface import IAsyncHttpClient
from domain.services.ocr_interface import IOCR
from infrastructure.exceptions.exceptions import ExternalApiError


class OCRSuccessResponse(BaseModel):
    text: str
    pages: int


class OCRErrorResponse(BaseModel):
    detail: str


class OCRExtractor(IOCR):
    def __init__(self, config: OCRConfig, http_client: IAsyncHttpClient):
        self.config = config
        self.http_client = http_client

    async def extract_text(self, pdf_content: bytes) -> str:
        url = f"{self.config.base_url}extract-text"
        headers = {"X-API-Key": self.config.api_key}
        files = {"file": ("document.pdf", pdf_content, "application/pdf")}

        async with self.http_client as client:
            response = await client.post(url, headers=headers, files=files)

        # Handle error responses
        if response.status_code != HTTPStatus.OK:
            try:
                error_data = response.json()
                error_response = OCRErrorResponse.model_validate(error_data)
                error_message = error_response.detail
            except Exception:
                error_message = f"OCR service error: {response.status_code}"

            raise ExternalApiError(
                error_message,
                status_code=response.status_code,
                api_name="OCR",
                details={
                    "method": "POST",
                    "endpoint": "/extract-text",
                    "response_text": response.text,
                },
            )

        # Parse success response
        try:
            response_data = response.json()
            success_response = OCRSuccessResponse.model_validate(response_data)
            return success_response.text
        except Exception as e:
            raise ExternalApiError(
                "Failed to parse JSON response",
                api_name="OCR",
                details={
                    "method": "POST",
                    "endpoint": "/extract-text",
                    "response_text": response.text,
                },
            ) from e
