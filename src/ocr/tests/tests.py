from fastapi.testclient import TestClient

from app.auth import verify_api_key
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200  # noqa
    assert response.json() == {"status": "healthy"}


class TestProtectedRouter:
    def test_welcome_valid_key(self):
        API_KEY = "strongsecretkey"
        app.dependency_overrides[verify_api_key] = lambda: API_KEY
        response = client.get("/welcome", headers={"X-API-Key": API_KEY})
        app.dependency_overrides.clear()
        assert response.status_code == 200

    def test_welcome_wrong_key(self):
        response = client.get("/welcome", headers={"X-API-Key": "wrongkey"})
        assert response.status_code == 403
