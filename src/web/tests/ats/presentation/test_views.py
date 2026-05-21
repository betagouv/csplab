import pytest
from django.test import Client


@pytest.mark.django_db
class TestATSBase:
    """Tests pour la vue base() de l'ATS."""

    def test_base_view_returns_200(self, client: Client):
        """La vue base retourne un statut 200."""
        response = client.get("/ats/")
        assert response.status_code == 200

    def test_base_view_uses_correct_template(self, client: Client):
        """La vue utilise le template ats/base.html."""
        response = client.get("/ats/")
        assert "ats/base.html" in [t.name for t in response.templates]

    def test_base_view_context_contains_debug(self, client: Client, settings):
        """Le contexte contient la variable debug."""
        response = client.get("/ats/")
        assert "debug" in response.context
        assert response.context["debug"] == settings.DEBUG

    def test_base_view_context_contains_user_json(self, client: Client):
        """Le contexte contient user_json."""
        response = client.get("/ats/")
        assert "user_json" in response.context

    def test_base_view_catches_subroutes(self, client: Client):
        """Les sous-routes sont capturées par la vue base."""
        response = client.get("/ats/candidates/123/")
        assert response.status_code == 200

    def test_base_view_authenticated_user_context(self, client: Client, django_user_model):
        """Un utilisateur authentifié a son email dans le contexte."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )
        client.force_login(user)
        response = client.get("/ats/")
        assert '"is_authenticated": true' in response.context["user_json"]
        assert "test@example.com" in response.context["user_json"]
