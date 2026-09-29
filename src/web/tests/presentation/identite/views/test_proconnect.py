from unittest.mock import MagicMock

from authlib.integrations.base_client.errors import OAuthError
from django.conf import settings
from django.contrib.messages import get_messages
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.authentication.proconnect_client import (
    END_SESSION_ENDPOINT,
    oauth,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.repositories.recruteur.postgres_organisme_agent_repository import (
    PostgresOrganismeAgentRepository,
)


class TestProconnectLoginView:
    @override_settings(PROCONNECT_LOGIN_ENABLED=False)
    def test_get_returns_404_when_disabled(self, db, client):
        response = client.get(reverse("identite:proconnect_login"))

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestProconnectCallbackView:
    @override_settings(PROCONNECT_LOGIN_ENABLED=False)
    def test_get_returns_404_when_disabled(self, db, client):
        response = client.get(reverse("identite:proconnect_callback"))

        assert response.status_code == status.HTTP_404_NOT_FOUND

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
        OrganismeAgentDjangoFactory(agent__utilisateur=test_user)
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


def _proconnect_callback(client, monkeypatch, email):
    monkeypatch.setattr(
        oauth.proconnect,
        "authorize_access_token",
        MagicMock(return_value={"id_token": "fake-id-token"}),
    )
    monkeypatch.setattr(
        "presentation.identite.views.fetch_userinfo_claims",
        MagicMock(return_value={"email": email}),
    )
    return client.get(reverse("identite:proconnect_callback"))


def _revoke(organisme, agent):
    OrganismeAgentModel.objects.filter(organisme=organisme, agent=agent).update(
        date_revocation=timezone.now()
    )


class TestProconnectCallbackRattachement:
    def test_agent_revoked_from_only_organisme_is_refused(
        self, db, client, monkeypatch
    ):
        agent, organisme = create_organisme_with_agent()
        _revoke(organisme, agent)

        response = _proconnect_callback(client, monkeypatch, agent.utilisateur.email)

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "/utilisateur/connexion"
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        assert any("Aucun compte ProConnect" in message for message in messages)
        assert "_auth_user_id" not in client.session

    def test_invited_agent_never_logged_in_logs_in(self, db, client, monkeypatch):
        agent, _ = create_organisme_with_agent()
        assert agent.utilisateur.last_login is None

        response = _proconnect_callback(client, monkeypatch, agent.utilisateur.email)

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session

    def test_staff_without_organisme_logs_in(self, db, client, monkeypatch):
        staff = UtilisateurDjangoFactory(is_staff=True)

        response = _proconnect_callback(client, monkeypatch, staff.email)

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session

    def test_agent_revoked_from_one_organisme_but_active_elsewhere_logs_in(
        self, db, client, monkeypatch
    ):
        agent, organisme_revoque = create_organisme_with_agent()
        OrganismeAgentDjangoFactory(agent=agent)
        _revoke(organisme_revoque, agent)

        response = _proconnect_callback(client, monkeypatch, agent.utilisateur.email)

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session

    def test_agent_reattached_after_revocation_logs_in(self, db, client, monkeypatch):
        agent, organisme = create_organisme_with_agent()
        _revoke(organisme, agent)
        PostgresOrganismeAgentRepository().reattach(
            organisme_id=organisme.id,
            agent_id=agent.utilisateur_id,
            role=AgentOrganismeRole.AGENT,
        )

        response = _proconnect_callback(client, monkeypatch, agent.utilisateur.email)

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session


class TestProconnectLogoutView:
    def test_logs_out_locally_when_no_oidc_session(self, db, client, test_user):
        client.force_login(test_user)

        response = client.post(reverse("identite:logout"))

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse("identite:login")
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
        assert (
            "post_logout_redirect_uri=http%3A%2F%2Ftestserver%2Futilisateur%2Fconnexion"
            in response.url
        )
        assert "_auth_user_id" not in client.session
