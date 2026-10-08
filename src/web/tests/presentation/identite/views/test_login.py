from django.test import override_settings
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed
from rest_framework import status


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

    def test_post_is_not_allowed(self, db, client):
        response = client.post(
            reverse("identite:login"),
            {"username": "user@example.com", "password": "secret"},
        )

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
