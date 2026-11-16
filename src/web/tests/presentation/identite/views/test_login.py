from django.test import override_settings
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed
from rest_framework import status

from presentation.identite.views import UNKNOWN_ACCOUNT_SESSION_KEY


class TestLoginView:
    def test_get_login_page_renders(self, db, client):
        response = client.get(reverse("identite:login"))

        assert response.status_code == status.HTTP_200_OK
        assertTemplateUsed(response, "registration/login.html")
        assertNotContains(response, 'id="login-form"')
        assertNotContains(response, 'name="password"')

    def test_get_login_page_renders_proconnect_button(self, db, client):
        response = client.get(reverse("identite:login"))

        assertContains(response, "ProConnect")
        assertContains(response, reverse("identite:proconnect_login"))

    def test_get_login_page_forwards_next_to_proconnect_button(self, db, client):
        next_url = "/ats/organismes/1/"

        response = client.get(reverse("identite:login"), {"next": next_url})

        assertContains(
            response,
            f"{reverse('identite:proconnect_login')}?next=%2Fats%2Forganismes%2F1%2F",
        )

    def test_get_login_page_ignores_external_next(self, db, client):
        response = client.get(
            reverse("identite:login"), {"next": "https://evil.example.com/"}
        )

        assertNotContains(response, "evil.example.com")
        assertNotContains(response, "?next=")

    @override_settings(PROCONNECT_LOGIN_ENABLED=False)
    def test_get_login_page_hides_proconnect_button_when_disabled(self, db, client):
        response = client.get(reverse("identite:login"))

        assertNotContains(response, "ProConnect")
        assertNotContains(response, reverse("identite:proconnect_login"))

    def test_get_login_page_shows_unknown_account_notice_once(self, db, client):
        session = client.session
        session[UNKNOWN_ACCOUNT_SESSION_KEY] = True
        session.save()

        response = client.get(reverse("identite:login"))

        assertContains(response, "Impossible d'accéder à l'ATS")
        assertContains(
            response, "Aucun compte n'est associé au courriel ProConnect utilisé."
        )
        assertContains(response, "Essayer avec un autre courriel")
        assertNotContains(client.get(reverse("identite:login")), "Impossible d'accéder")

    def test_post_is_not_allowed(self, db, client):
        response = client.post(
            reverse("identite:login"),
            {"username": "user@example.com", "password": "secret"},
        )

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
