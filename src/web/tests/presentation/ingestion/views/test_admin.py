from http import HTTPStatus

import pytest
from django.test import Client
from django_otp.middleware import is_verified
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice

from tests.factories.utilisateur_factory import DEFAULT_PASSWORD, UtilisateurFactory


@pytest.mark.django_db
class TestAdminOTPRequired:
    def test_admin_shows_totp_input_for_staff_without_otp_device(self, client: Client):
        user = UtilisateurFactory.create_model()
        user.is_staff = True
        user.is_superuser = True
        user.save()

        client.login(username=user.email, password=DEFAULT_PASSWORD)
        response = client.get("/admin/", follow=True)

        assert response.status_code == HTTPStatus.OK
        assert b'id="id_otp_token"' in response.content

    def test_admin_grants_access_with_valid_totp_token(self, client: Client):
        user = UtilisateurFactory.create_model()
        user.is_staff = True
        user.is_superuser = True
        user.save()

        device = TOTPDevice.objects.create(user=user, confirmed=True)
        token = totp(device.bin_key)

        response = client.post(
            "/admin/login/",
            {
                "username": user.email,
                "password": DEFAULT_PASSWORD,
                "otp_token": token,
                "next": "/admin/",
            },
            follow=True,
        )

        assert response.status_code == HTTPStatus.OK
        assert is_verified(response.wsgi_request.user)
