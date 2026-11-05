from http import HTTPStatus
from typing import cast

import pytest
from django.test import Client
from django.urls import reverse
from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

import config.urls  # noqa: F401  # imported for its side effect: runs the OTPAdminSite swap
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.users.models import AllowedNetworkModel, UserModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


@pytest.fixture(name="admin_client")
def admin_client_fixture(db, client: Client) -> Client:
    admin = cast(UserModel, UtilisateurDjangoFactory(is_staff=True, is_superuser=True))
    device = TOTPDevice.objects.create(user=admin, confirmed=True)
    client.force_login(admin)
    session = client.session
    session[DEVICE_ID_SESSION_KEY] = device.persistent_id
    session.save()
    return client


def _inline_post_data(user, rows):
    prefix = "allowed_networks"
    data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": "on",
        f"{prefix}-TOTAL_FORMS": str(len(rows)),
        f"{prefix}-INITIAL_FORMS": "0",
    }
    for index, (cidr, label) in enumerate(rows):
        data[f"{prefix}-{index}-cidr"] = cidr
        data[f"{prefix}-{index}-label"] = label
    return data


class TestUserAdminAllowedNetworks:
    def test_change_page_shows_the_inline(self, admin_client):
        user = UtilisateurDjangoFactory()

        response = admin_client.get(
            reverse("admin:users_usermodel_change", args=[user.pk])
        )

        assert response.status_code == HTTPStatus.OK
        assert "Réseaux autorisés pour l&#x27;API" in response.text
        assert "Laisser vide pour n'appliquer aucune restriction." in response.text

    def test_saves_a_normalized_range(self, admin_client):
        user = UtilisateurDjangoFactory()

        response = admin_client.post(
            reverse("admin:users_usermodel_change", args=[user.pk]),
            _inline_post_data(user, [("203.0.113.10", "NAT prod")]),
        )

        assert response.status_code == HTTPStatus.FOUND
        network = AllowedNetworkModel.objects.get(user=user)
        assert (network.cidr, network.label) == ("203.0.113.10/32", "NAT prod")

    def test_rejects_an_invalid_range(self, admin_client):
        user = UtilisateurDjangoFactory()

        response = admin_client.post(
            reverse("admin:users_usermodel_change", args=[user.pk]),
            _inline_post_data(user, [("203.0.113.0/33", "NAT prod")]),
        )

        assert response.status_code == HTTPStatus.OK
        assert "Saisissez une adresse IP ou une plage CIDR valide." in response.text
        assert not AllowedNetworkModel.objects.exists()

    def test_changelist_filters_restricted_users(self, admin_client):
        restricted = UtilisateurDjangoFactory()
        AllowedNetworkModel.objects.create(
            user=restricted, cidr="203.0.113.10", label="NAT"
        )
        unrestricted = UtilisateurDjangoFactory()
        url = reverse("admin:users_usermodel_changelist")

        restricted_page = admin_client.get(url, {"ip_restricted": "1"})
        unrestricted_page = admin_client.get(url, {"ip_restricted": "0"})

        assert restricted_page.status_code == HTTPStatus.OK
        assert restricted.email in restricted_page.text
        assert unrestricted.email not in restricted_page.text
        assert unrestricted.email in unrestricted_page.text
        assert restricted.email not in unrestricted_page.text


class TestUserAdminRevokeApiTokens:
    def test_revokes_the_refresh_tokens_of_the_selected_accounts(self, admin_client):
        compte, autre = UtilisateurDjangoFactory.create_batch(2)
        revoked = RefreshToken.for_user(compte)
        RefreshToken.for_user(autre)

        response = admin_client.post(
            reverse("admin:users_usermodel_changelist"),
            {"action": "revoke_api_tokens", "_selected_action": [compte.pk]},
            follow=True,
        )

        assert response.status_code == HTTPStatus.OK
        assert list(BlacklistedToken.objects.values_list("token__jti", flat=True)) == [
            revoked["jti"]
        ]
        assert AuditLogModel.objects.get().ressource_id == compte.username
        assert (
            "1 jeton(s) de rafraîchissement révoqué(s) pour 1 compte(s). "
            "Les jetons d&#x27;accès déjà émis restent valables 15 minutes au plus."
        ) in response.text

    def test_deactivates_the_selected_accounts(self, admin_client):
        compte = UtilisateurDjangoFactory()
        RefreshToken.for_user(compte)

        response = admin_client.post(
            reverse("admin:users_usermodel_changelist"),
            {"action": "deactivate_api_accounts", "_selected_action": [compte.pk]},
            follow=True,
        )

        compte.refresh_from_db()
        assert not compte.is_active
        assert BlacklistedToken.objects.count() == 1
        assert AuditLogModel.objects.get().event_name == "CompteApiDesactive"
        assert (
            "1 compte(s) désactivé(s), 1 jeton(s) de rafraîchissement révoqué(s)."
            in response.text
        )

    def test_refuses_to_deactivate_the_current_admin(self, admin_client):
        admin_user = UserModel.objects.get(is_superuser=True)
        compte = UtilisateurDjangoFactory()

        response = admin_client.post(
            reverse("admin:users_usermodel_changelist"),
            {
                "action": "deactivate_api_accounts",
                "_selected_action": [compte.pk, admin_user.pk],
            },
            follow=True,
        )

        compte.refresh_from_db()
        assert compte.is_active
        assert not AuditLogModel.objects.exists()
        assert "Vous ne pouvez pas désactiver votre propre compte." in response.text
