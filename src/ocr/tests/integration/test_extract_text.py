import os

import pytest
from fastapi.testclient import TestClient

from api.main import create_app

VALID_API_KEY = "test-api-key-for-development"


@pytest.fixture
def test_client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def sample_pdf_content():
    pdf_path = os.path.join(
        os.path.dirname(__file__), "..", "fixtures", "test_sample.pdf"
    )
    with open(pdf_path, "rb") as f:
        return f.read()


@pytest.mark.asyncio
async def test_health_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_extract_text_without_api_key(test_client):
    response = test_client.post(
        "/extract-text", files={"file": ("test.pdf", b"fake pdf", "application/pdf")}
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_extract_text_with_invalid_api_key(test_client):
    headers = {"X-API-Key": "invalid-api-key"}
    response = test_client.post(
        "/extract-text",
        files={"file": ("test.pdf", b"fake pdf", "application/pdf")},
        headers=headers,
    )
    assert response.status_code == 403
    assert "Invalid API key" in response.json()["detail"]


@pytest.mark.asyncio
async def test_extract_text_with_valid_api_key_but_invalid_file(test_client):
    headers = {"X-API-Key": VALID_API_KEY}
    response = test_client.post(
        "/extract-text",
        files={"file": ("test.txt", b"not a pdf", "text/plain")},
        headers=headers,
    )
    assert response.status_code == 400
    assert "File must be a PDF" in response.json()["detail"]


@pytest.mark.asyncio
async def test_extract_text_with_valid_api_key_and_valid_file(
    test_client, sample_pdf_content
):
    headers = {"X-API-Key": VALID_API_KEY}
    response = test_client.post(
        "/extract-text",
        files={"file": ("test.pdf", sample_pdf_content, "application/pdf")},
        headers=headers,
    )
    assert response.status_code == 200
    assert "text" in response.json()
    extracted_text = response.json()["text"]
    assert "Test PDF for OCR" in extracted_text or "Hello World" in extracted_text
