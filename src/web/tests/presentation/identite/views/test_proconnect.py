from unittest.mock import MagicMock

from authlib.integrations.base_client.errors import OAuthError
from django.conf import settings
from django.contrib.messages import get_messages
from django.urls import reverse
from rest_framework import status

from infrastructure.authentication.proconnect_client import (
    END_SESSION_ENDPOINT,
    oauth,
)


class TestProconnectCallbackView:
    def test_callback_oauth_error_shows_error_message_and_redirects_to_login(
        self, db, client, monkeypatch
    ):
        monkeypatch.setattr(
            oauth.proconnect,
            "authorize_access_token",
            MagicMock(side_effect=OAuthError("mismatching_state")),
        )

        response = client.get(reverse("identite:proconnect_callback"))

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "/utilisateur/connexion"
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        assert any("Aucun compte ProConnect" in message for message in messages)

    def test_callback_unknown_email_shows_error_message_and_redirects_to_login(
        self, db, client, monkeypatch
    ):
        monkeypatch.setattr(
            oauth.proconnect,
            "authorize_access_token",
            MagicMock(return_value={"id_token": "fake-id-token"}),
        )
        monkeypatch.setattr(
            "presentation.identite.views.fetch_userinfo_claims",
            MagicMock(return_value={"email": "unknown@example.com"}),
        )

        response = client.get(reverse("identite:proconnect_callback"))

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "/utilisateur/connexion"
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        assert any("Aucun compte ProConnect" in message for message in messages)

    def test_callback_matching_user_logs_in_and_redirects(
        self, db, client, monkeypatch, test_user
    ):
        monkeypatch.setattr(
            oauth.proconnect,
            "authorize_access_token",
            MagicMock(return_value={"id_token": "fake-id-token"}),
        )
        monkeypatch.setattr(
            "presentation.identite.views.fetch_userinfo_claims",
            MagicMock(return_value={"email": test_user.email}),
        )

        response = client.get(reverse("identite:proconnect_callback"))

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session
        assert client.session["oidc_id_token"] == "fake-id-token"  # noqa S105


class TestProconnectLogoutView:
    def test_logs_out_locally_when_no_oidc_session(self, db, client, test_user):
        client.force_login(test_user)

        response = client.post(reverse("identite:logout"))

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse("pages:home")
        assert "_auth_user_id" not in client.session

    def test_redirects_to_proconnect_end_session_when_oidc_session(
        self, db, client, test_user
    ):
        client.force_login(test_user)
        session = client.session
        session["oidc_id_token"] = "fake-id-token"  # noqa S105
        session.save()

        response = client.post(reverse("identite:logout"))

        assert response.status_code == status.HTTP_302_FOUND
        expected_logout_url = f"{settings.PROCONNECT_BASE_URL}{END_SESSION_ENDPOINT}"
        assert response.url.startswith(expected_logout_url)
        assert "id_token_hint=fake-id-token" in response.url
        assert "_auth_user_id" not in client.session
