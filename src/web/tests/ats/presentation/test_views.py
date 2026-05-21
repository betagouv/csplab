from http import HTTPStatus

import pytest
from django.test import Client


@pytest.mark.django_db
class TestATSBase:
    """Tests pour la vue base() de l'ATS."""

    def test_base_view_returns_200(self, client: Client):
        """La vue base retourne un statut 200."""
        response = client.get("/ats/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_uses_correct_template(self, client: Client):
        """La vue utilise le template ats/base.html."""
        response = client.get("/ats/")
        assert "ats/base.html" in [t.name for t in response.templates]

    def test_base_view_catches_subroutes(self, client: Client):
        """Les sous-routes sont capturées par la vue base (Vue Router)."""
        response = client.get("/ats/candidates/123/")
        assert response.status_code == HTTPStatus.OK
