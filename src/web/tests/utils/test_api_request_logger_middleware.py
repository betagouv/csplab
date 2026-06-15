import hashlib
from unittest.mock import MagicMock

import pytest
from django.test import RequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from domain.ingestion.entities.api_log import ApiLog
from presentation.middleware.api_request_logger import ApiRequestLoggerMiddleware


def _make_jwt(user_id: int) -> str:
    token = AccessToken()
    token["username"] = user_id
    return str(token)


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.status_code = 200
    return response


def make_middleware(mock_response, mock_repository):
    get_response = MagicMock(return_value=mock_response)
    middleware = ApiRequestLoggerMiddleware(
        get_response=get_response, repository=mock_repository
    )
    return middleware, get_response


class TestApiRequestLoggerMiddleware:
    def test_logs_api_request_with_jwt_token(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        token = _make_jwt(user_id=42)
        request = rf.get("/api/v1/offres/", HTTP_AUTHORIZATION=f"Bearer {token}")

        middleware(request)

        mock_repository.save.assert_called_once()
        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.path == "/api/v1/offres/"
        assert saved.auth_token == "42"  # noqa: S105
        assert saved.token_type == "jwt"  # noqa: S105

    def test_logs_none_for_jwt_with_wrong_number_of_parts(
        self, rf, mock_repository, mock_response
    ):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/api/v1/offres/", HTTP_AUTHORIZATION="Bearer onlytwoparts.xx")

        middleware(request)

        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.auth_token is None
        assert saved.token_type == "jwt"  # noqa: S105

    def test_logs_none_for_jwt_with_corrupt_payload(
        self, rf, mock_repository, mock_response
    ):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get(
            "/api/v1/offres/", HTTP_AUTHORIZATION="Bearer header.!!!invalid!!!.sig"
        )

        middleware(request)

        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.auth_token is None
        assert saved.token_type == "jwt"  # noqa: S105

    def test_logs_api_request_with_api_key(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/api/v1/offres/", HTTP_AUTHORIZATION="Api-Key secret-key")

        middleware(request)

        mock_repository.save.assert_called_once()
        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.auth_token == hashlib.sha256(b"secret-key").hexdigest()
        assert saved.token_type == "api_key"  # noqa: S105

    def test_logs_api_request_without_token(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/api/v1/offres/")

        middleware(request)

        mock_repository.save.assert_called_once()
        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.auth_token is None
        assert saved.token_type is None

    def test_does_not_log_non_api_requests(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/candidate/upload/")

        middleware(request)

        mock_repository.save.assert_not_called()

    def test_does_not_log_admin_requests(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/admin/login/")

        middleware(request)

        mock_repository.save.assert_not_called()

    def test_captures_ip_from_remote_addr(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/api/health/", REMOTE_ADDR="192.168.1.10")

        middleware(request)

        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.ip_address == "192.168.1.10"

    def test_captures_ip_from_x_forwarded_for(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get(
            "/api/health/",
            HTTP_X_FORWARDED_FOR="10.0.0.1, 10.0.0.2",
            REMOTE_ADDR="172.16.0.1",
        )

        middleware(request)

        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.ip_address == "10.0.0.1"

    def test_captures_request_path(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/api/token/")

        middleware(request)

        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.path == "/api/token/"

    def test_captures_request_method(self, rf, mock_repository, mock_response):
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.post("/api/v1/offres/creer_modifier/")

        middleware(request)

        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.method == "POST"

    def test_captures_status_code(self, rf, mock_repository, mock_response):
        mock_response.status_code = 401
        middleware, _ = make_middleware(mock_response, mock_repository)
        request = rf.get("/api/v1/offres/")

        middleware(request)

        saved: ApiLog = mock_repository.save.call_args[0][0]
        assert saved.status_code == 401  # noqa: PLR2004

    def test_passes_through_response_unchanged(
        self, rf, mock_repository, mock_response
    ):
        middleware, get_response = make_middleware(mock_response, mock_repository)
        request = rf.get("/api/v1/offres/")

        result = middleware(request)

        assert result is mock_response
        get_response.assert_called_once_with(request)
