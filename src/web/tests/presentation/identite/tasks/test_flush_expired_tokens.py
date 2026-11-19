from datetime import timedelta

from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from presentation.identite.tasks import flush_expired_tokens


def test_deletes_only_expired_tokens(db):
    user = UtilisateurDjangoFactory()
    OutstandingToken.objects.create(
        user=user,
        jti="expired",
        token="",
        expires_at=timezone.now() - timedelta(minutes=1),
    )
    active = RefreshToken.for_user(user)

    flush_expired_tokens.call_local()

    assert list(OutstandingToken.objects.values_list("jti", flat=True)) == [
        active["jti"]
    ]
