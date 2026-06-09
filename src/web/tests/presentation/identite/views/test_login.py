from django.urls import reverse
from rest_framework import status

from tests.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


class TestLoginView:
    def test_post_with_wrong_credentials_shows_error_message(self, db, client):
        response = client.post(
            reverse("users:login"),
            {"password": "abc", "username": "abc"},
        )

        assert response.status_code == status.HTTP_200_OK
        errors_all = response.context["form"].errors["__all__"]
        assert "Saisissez un email et un mot de passe valides." in errors_all[0]

    def test_post_with_correct_credentials_redirects_to_profile_view(
        self, db, client, test_user
    ):
        response = client.post(
            reverse("users:login"),
            {
                "password": DEFAULT_PASSWORD,
                "username": test_user.email,
            },
        )

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse("users:profile")
        assert "_auth_user_id" in client.session
        assert response.wsgi_request.user.is_authenticated is True
