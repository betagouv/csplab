import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def test_client():
    app = create_app()
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_extract_text_endpoint_invalid_file(test_client):
    response = test_client.post(
        "/extract-text", files={"file": ("test.txt", b"not a pdf", "text/plain")}
    )
    assert response.status_code == 400
    assert "File must be a PDF" in response.json()["detail"]
