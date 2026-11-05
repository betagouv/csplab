import logging
from datetime import timedelta

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


def _revoked_jtis():
    return set(BlacklistedToken.objects.values_list("token__jti", flat=True))


def test_revokes_every_active_refresh_token_of_the_account(db):
    compte, admin = UtilisateurDjangoFactory(), UtilisateurDjangoFactory()
    tokens = [RefreshToken.for_user(compte) for _ in range(2)]

    revoked = revoke_api_tokens(compte=compte, utilisateur=admin)

    assert revoked == len(tokens)
    assert _revoked_jtis() == {token["jti"] for token in tokens}


def test_leaves_other_accounts_untouched(db):
    compte, autre, admin = UtilisateurDjangoFactory.create_batch(3)
    RefreshToken.for_user(autre)

    assert revoke_api_tokens(compte=compte, utilisateur=admin) == 0
    assert not BlacklistedToken.objects.exists()


def test_skips_expired_and_already_revoked_tokens(db):
    compte, admin = UtilisateurDjangoFactory(), UtilisateurDjangoFactory()
    OutstandingToken.objects.create(
        user=compte,
        jti="expired",
        token="",
        expires_at=timezone.now() - timedelta(minutes=1),
    )
    RefreshToken.for_user(compte).blacklist()

    assert revoke_api_tokens(compte=compte, utilisateur=admin) == 0
    assert BlacklistedToken.objects.count() == 1


def test_audits_the_revocation_even_without_token(db):
    compte, admin = UtilisateurDjangoFactory(), UtilisateurDjangoFactory()

    revoke_api_tokens(compte=compte, utilisateur=admin)

    log = AuditLogModel.objects.get()
    assert log.utilisateur_id == admin.username
    assert log.ressource_kind == "Utilisateur"
    assert log.ressource_id == compte.username
    assert log.event_name == "JetonsApiRevoques"


def test_logs_the_revocation(db, caplog):
    caplog.set_level(logging.WARNING, logger="identite")
    compte, admin = UtilisateurDjangoFactory(), UtilisateurDjangoFactory()
    RefreshToken.for_user(compte)

    revoke_api_tokens(compte=compte, utilisateur=admin)

    assert [r.getMessage() for r in caplog.records] == [
        f"Revoked 1 refresh token(s) of user {compte.pk}, by user {admin.pk}."
    ]
