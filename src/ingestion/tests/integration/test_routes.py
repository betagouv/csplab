import pytest
from fastapi.testclient import TestClient

from api.main import create_app


@pytest.fixture
def test_client(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    app = create_app()
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_endpoint(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
