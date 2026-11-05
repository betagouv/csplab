import logging
from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from application.identite.services.revoke_api_tokens import revoke_api_tokens
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


@pytest.fixture(name="accounts")
def accounts_fixture(db):
    return UtilisateurDjangoFactory(), UtilisateurDjangoFactory()


def test_revokes_only_the_active_tokens_of_the_account(accounts):
    account, admin = accounts
    tokens = [RefreshToken.for_user(account) for _ in range(2)]
    RefreshToken.for_user(admin)
    RefreshToken.for_user(account).blacklist()
    OutstandingToken.objects.create(
        user=account,
        jti="expired",
        token="",
        expires_at=timezone.now() - timedelta(minutes=1),
    )

    revoked = revoke_api_tokens(account=account, actor=admin)

    assert revoked == len(tokens)
    assert {token["jti"] for token in tokens} < set(
        BlacklistedToken.objects.values_list("token__jti", flat=True)
    )
    assert not BlacklistedToken.objects.filter(token__user=admin).exists()
    account.refresh_from_db()
    assert account.is_active


def test_deactivates_the_account_on_demand(accounts):
    account, admin = accounts

    revoke_api_tokens(account=account, actor=admin, deactivate=True)

    account.refresh_from_db()
    assert not account.is_active


@pytest.mark.parametrize(
    ("deactivate", "event_name"),
    [(False, "JetonsApiRevoques"), (True, "CompteApiDesactive")],
)
def test_audits_and_logs_even_without_token(accounts, caplog, deactivate, event_name):
    caplog.set_level(logging.WARNING, logger="identite")
    account, admin = accounts

    revoke_api_tokens(account=account, actor=admin, deactivate=deactivate)

    log = AuditLogModel.objects.get()
    assert (log.utilisateur_id, log.ressource_kind, log.ressource_id) == (
        admin.username,
        "Utilisateur",
        account.username,
    )
    assert log.event_name == event_name
    expected = (
        f"Revoked 0 refresh token(s) of user {account.pk} "
        f"(deactivated: {deactivate}), by user {admin.pk}."
    )
    assert [r.getMessage() for r in caplog.records] == [expected]
