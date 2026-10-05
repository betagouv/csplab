from ipaddress import IPv4Address, IPv6Address
from unittest.mock import patch

import pytest
from django.db import IntegrityError, transaction

from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import (
    AuditLoginLogModel,
    AuditLoginLogQuerySet,
)
from infrastructure.factories.identite.audit_login_log_django_factory import (
    AuditLoginLogDjangoFactory,
)


class TestAuditLoginLogModel:
    def test_success_requires_a_user(self, db):
        with pytest.raises(IntegrityError):
            AuditLoginLogDjangoFactory(
                canal=Canal.JWT, resultat=Resultat.SUCCES, utilisateur_id=None
            )

    def test_failure_may_have_no_user(self, db):
        log = AuditLoginLogDjangoFactory(resultat=Resultat.ECHEC)

        assert log.utilisateur_id is None


class TestRecordAttempt:
    def test_swallows_errors(self, db):
        with patch.object(
            AuditLoginLogQuerySet, "create", side_effect=RuntimeError("boom")
        ):
            AuditLoginLogModel.objects.record_attempt(
                canal=Canal.JWT, resultat=Resultat.ECHEC
            )

        assert not AuditLoginLogModel.objects.exists()

    def test_failed_insert_does_not_break_enclosing_transaction(self, db):
        with transaction.atomic():
            # Violates audit_login_logs_succes_has_user at the database level.
            AuditLoginLogModel.objects.record_attempt(
                canal=Canal.JWT, resultat=Resultat.SUCCES
            )

            assert not AuditLoginLogModel.objects.exists()

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("203.0.113.7", "203.0.113.7"),
            (" 203.0.113.7 ", "203.0.113.7"),
            ("2001:db8::1", "2001:db8::1"),
            (IPv4Address("203.0.113.7"), "203.0.113.7"),
            (IPv6Address("2001:db8::1"), "2001:db8::1"),
            ("", None),
            (None, None),
            ("not-an-ip", None),
        ],
    )
    def test_normalizes_ip_and_keeps_row(self, db, raw, expected):
        AuditLoginLogModel.objects.record_attempt(
            canal=Canal.JWT, resultat=Resultat.ECHEC, ip_address=raw
        )

        assert AuditLoginLogModel.objects.get().ip_address == expected
