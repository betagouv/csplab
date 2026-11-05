import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from infrastructure.django_apps.users.models import AllowedNetworkModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


@pytest.fixture(name="user")
def user_fixture(db):
    return UtilisateurDjangoFactory()


class TestAllowedNetworkModel:
    def test_clean_normalizes_the_range(self, user):
        network = AllowedNetworkModel(user=user, cidr=" 203.0.113.7/24 ", label="NAT")

        network.full_clean()

        assert network.cidr == "203.0.113.0/24"

    @pytest.mark.parametrize("cidr", ["not-an-ip", "203.0.113.0/33"])
    def test_clean_rejects_an_invalid_value(self, user, cidr):
        network = AllowedNetworkModel(user=user, cidr=cidr, label="NAT")

        with pytest.raises(ValidationError) as exc_info:
            network.full_clean()

        assert exc_info.value.message_dict == {
            "cidr": ["Saisissez une adresse IP ou une plage CIDR valide."]
        }

    def test_save_stores_a_single_ip_as_a_host_range(self, user):
        network = AllowedNetworkModel.objects.create(
            user=user, cidr="2001:db8::1", label="NAT"
        )

        network.refresh_from_db()
        assert network.cidr == "2001:db8::1/128"

    def test_clean_reports_a_duplicate_written_differently(self, user):
        AllowedNetworkModel.objects.create(user=user, cidr="203.0.113.10", label="A")
        duplicate = AllowedNetworkModel(user=user, cidr="203.0.113.10/32", label="B")

        with pytest.raises(ValidationError, match="existe déjà"):
            duplicate.full_clean()

    def test_db_rejects_a_duplicate_range_for_the_same_user(self, user):
        AllowedNetworkModel.objects.create(user=user, cidr="203.0.113.10", label="A")

        with pytest.raises(IntegrityError):
            AllowedNetworkModel.objects.create(
                user=user, cidr="203.0.113.10/32", label="B"
            )

    def test_the_same_range_can_be_set_on_two_users(self, user):
        AllowedNetworkModel.objects.create(user=user, cidr="203.0.113.10", label="A")

        AllowedNetworkModel.objects.create(
            user=UtilisateurDjangoFactory(), cidr="203.0.113.10", label="A"
        )


class TestApiIpIsAllowed:
    def test_user_without_network_is_not_restricted(self, user):
        assert user.api_ip_is_allowed("198.51.100.1") is True
        assert user.api_ip_is_allowed(None) is True

    @pytest.mark.parametrize(
        ("ip", "expected"),
        [
            ("203.0.113.42", True),
            ("2001:db8::5", True),
            ("198.51.100.1", False),
            (None, False),
        ],
        ids=["ipv4_in_range", "ipv6_in_range", "outside_ranges", "unknown_ip"],
    )
    def test_restricted_user(self, user, ip, expected):
        AllowedNetworkModel.objects.create(user=user, cidr="203.0.113.0/24", label="A")
        AllowedNetworkModel.objects.create(user=user, cidr="2001:db8::/48", label="B")

        assert user.api_ip_is_allowed(ip) is expected
