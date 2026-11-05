import logging

from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from application.identite.services.deactivate_api_account import (
    deactivate_api_account,
)
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


def test_deactivates_the_account_and_revokes_its_tokens(db):
    compte, admin = UtilisateurDjangoFactory(), UtilisateurDjangoFactory()
    token = RefreshToken.for_user(compte)

    revoked = deactivate_api_account(compte=compte, utilisateur=admin)

    compte.refresh_from_db()
    assert not compte.is_active
    assert revoked == 1
    assert BlacklistedToken.objects.get().token.jti == token["jti"]


def test_audits_the_deactivation(db):
    compte, admin = UtilisateurDjangoFactory(), UtilisateurDjangoFactory()

    deactivate_api_account(compte=compte, utilisateur=admin)

    log = AuditLogModel.objects.get()
    assert log.utilisateur_id == admin.username
    assert log.ressource_kind == "Utilisateur"
    assert log.ressource_id == compte.username
    assert log.event_name == "CompteApiDesactive"


def test_logs_the_deactivation(db, caplog):
    caplog.set_level(logging.WARNING, logger="identite")
    compte, admin = UtilisateurDjangoFactory(), UtilisateurDjangoFactory()

    deactivate_api_account(compte=compte, utilisateur=admin)

    expected = (
        f"Deactivated user {compte.pk} and revoked 0 refresh token(s), "
        f"by user {admin.pk}."
    )
    assert [r.getMessage() for r in caplog.records] == [expected]
