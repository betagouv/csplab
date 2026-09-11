import pytest


@pytest.fixture(autouse=True)
def _bypass_candidate_redirect_middleware(settings):
    settings.MIDDLEWARE = [
        middleware
        for middleware in settings.MIDDLEWARE
        if middleware
        != "presentation.middleware.candidate_redirect.CandidateRedirectMiddleware"
    ]
