from django.test import override_settings
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed
from rest_framework import status

from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


class TestLoginView:
    def test_get_login_page_renders(self, db, client):
        response = client.get(reverse("identite:login"))

        assert response.status_code == status.HTTP_200_OK
        assertTemplateUsed(response, "registration/login.html")

    def test_post_with_wrong_credentials_shows_generic_alert(self, db, client):
        response = client.post(
            reverse("identite:login"),
            {"username": "wrong@example.com", "password": "wrong"},
        )

        assert response.status_code == status.HTTP_200_OK
        assertContains(response, "Adresse e-mail ou mot de passe incorrect")
        assert b"fr-input--error" not in response.content

    def test_post_with_wrong_credentials_shows_error_message(self, db, client):
        response = client.post(
            reverse("identite:login"),
            {"password": "abc", "username": "abc"},
        )

        assert response.status_code == status.HTTP_200_OK
        errors_all = response.context["form"].errors["__all__"]
        assert "Saisissez un email et un mot de passe valides." in errors_all[0]

    def test_post_with_correct_credentials_redirects_to_ats_base(
        self, db, client, test_user
    ):
        response = client.post(
            reverse("identite:login"),
            {
                "password": DEFAULT_PASSWORD,
                "username": test_user.email,
            },
        )

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse("ats:ats_base")
        assert "_auth_user_id" in client.session
        assert response.wsgi_request.user.is_authenticated is True

    def test_get_login_page_renders_proconnect_button(self, db, client):
        response = client.get(reverse("identite:login"))

        assertContains(response, "ProConnect")
        assertContains(response, reverse("identite:proconnect_login"))

    @override_settings(PROCONNECT_LOGIN_ENABLED=False)
    def test_get_login_page_hides_proconnect_button_when_disabled(self, db, client):
        response = client.get(reverse("identite:login"))

        assertNotContains(response, "ProConnect")
        assertNotContains(response, reverse("identite:proconnect_login"))

    def test_post_with_correct_credentials_redirects_to_next_url(
        self, db, client, test_user
    ):
        response = client.post(
            reverse("identite:login"),
            {
                "username": test_user.email,
                "password": DEFAULT_PASSWORD,
                "next": "/ats/",
            },
        )

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "/ats/"
        assert "_auth_user_id" in client.session
