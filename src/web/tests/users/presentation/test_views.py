from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from rest_framework import status

from tests.factories.utilisateur_factory import DEFAULT_PASSWORD

# Assuming the use of integration tests in presentation layer, since we use
# legacy auth django view yet


class TestProfileView:
    def test_anonymous_request_redirects_to_login_view(self, db, client):
        response = client.get(reverse("users:profile"))

        assert response.status_code == status.HTTP_302_FOUND
        assert (
            response.url == f"{reverse('users:login')}?next={reverse('users:profile')}"
        )

    def test_authenticated_request_shows_template(self, db, client, test_user):
        client.force_login(test_user)

        response = client.get(reverse("users:profile"))

        assert response.status_code == status.HTTP_200_OK
        assertTemplateUsed(response, "registration/profile.html")


def test_logout_view(db, client, test_user):
    client.force_login(test_user)

    response = client.post(reverse("users:logout"))
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == reverse("pages:home")
    assert "_auth_user_id" not in client.session
    assert response.wsgi_request.user.is_authenticated is False


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
