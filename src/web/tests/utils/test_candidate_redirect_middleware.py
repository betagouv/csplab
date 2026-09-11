from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from presentation.middleware.candidate_redirect import (
    CANDIDATE_EXTERNAL_REDIRECT_URL,
    CandidateRedirectMiddleware,
)


@pytest.fixture
def rf():
    return RequestFactory()


def make_middleware(get_response=None):
    get_response = get_response or MagicMock(return_value=HttpResponse())
    middleware = CandidateRedirectMiddleware(get_response=get_response)
    return middleware, get_response


CANDIDATE_PATHS = [
    "/candidate/cv-upload",
    "/candidate/cv/11111111-1111-1111-1111-111111111111/results",
    "/candidate/cv/11111111-1111-1111-1111-111111111111/offers/22222222-2222-2222-2222-222222222222/detail",
    "/candidate/cv/11111111-1111-1111-1111-111111111111/concours/22222222-2222-2222-2222-222222222222/detail",
]

NON_CANDIDATE_PATHS = ["/", "/api/", "/utilisateur/"]


class TestCandidateRedirectMiddleware:
    @pytest.mark.parametrize("path", CANDIDATE_PATHS)
    @pytest.mark.parametrize("http_method", ["get", "post"])
    def test_candidate_path_returns_temporary_redirect(self, rf, http_method, path):
        middleware, get_response = make_middleware()
        request = getattr(rf, http_method)(path)

        response = middleware(request)

        assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
        assert response["Location"] == CANDIDATE_EXTERNAL_REDIRECT_URL
        get_response.assert_not_called()

    @pytest.mark.parametrize("path", CANDIDATE_PATHS)
    def test_htmx_request_gets_hx_redirect_header(self, rf, path):
        middleware, get_response = make_middleware()
        request = rf.get(path, HTTP_HX_REQUEST="true")

        response = middleware(request)

        assert response.status_code == HTTPStatus.OK
        assert response["HX-Redirect"] == CANDIDATE_EXTERNAL_REDIRECT_URL
        get_response.assert_not_called()

    @pytest.mark.parametrize("path", NON_CANDIDATE_PATHS)
    def test_non_candidate_path_is_unaffected(self, rf, path):
        mock_response = HttpResponse()
        middleware, get_response = make_middleware(
            get_response=MagicMock(return_value=mock_response)
        )
        request = rf.get(path)

        response = middleware(request)

        assert response is mock_response
        get_response.assert_called_once_with(request)
