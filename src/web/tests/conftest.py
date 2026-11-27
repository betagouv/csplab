import pytest

from infrastructure.authentication.rejection import AuthRejectionRateThrottle
from tests.utils.shared_fixtures import *  # noqa: F403


@pytest.fixture(autouse=True)
def documented_auth_rejection_throttle(monkeypatch):
    """Fails a test hitting the throttled reject() from a view Redoc can't see."""
    allow_request = AuthRejectionRateThrottle.allow_request

    def checked_allow_request(self, request, view):
        view = (getattr(request, "parser_context", None) or {}).get("view")
        if (
            view is not None
            and not view.get_authenticators()
            and not getattr(view, "throttles_auth_rejection", False)
        ):
            pytest.fail(
                f"{type(view).__name__} goes through the throttled reject(): "
                "set throttles_auth_rejection = True to document it in Redoc."
            )
        return allow_request(self, request, view)

    monkeypatch.setattr(
        AuthRejectionRateThrottle, "allow_request", checked_allow_request
    )
