from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from rest_framework import status

# Assuming the use of integration tests in presentation layer, since we use
# legacy auth django view yet


class TestProfileView:
    def test_anonymous_request_redirects_to_login_view(self, db, client):
        response = client.get(reverse("identite:profile"))

        assert response.status_code == status.HTTP_302_FOUND
        assert (
            response.url
            == f"{reverse('identite:login')}?next={reverse('identite:profile')}"
        )

    def test_authenticated_request_shows_template(self, db, client, test_user):
        client.force_login(test_user)

        response = client.get(reverse("identite:profile"))

        assert response.status_code == status.HTTP_200_OK
        assertTemplateUsed(response, "registration/profile.html")


def test_logout_view(db, client, test_user):
    client.force_login(test_user)

    response = client.post(reverse("identite:logout"))
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == reverse("pages:home")
    assert "_auth_user_id" not in client.session
    assert response.wsgi_request.user.is_authenticated is False
