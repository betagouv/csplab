from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

BATCH_SIZE = 2000


def test_emails_are_unique():
    users = UtilisateurDjangoFactory.build_batch(BATCH_SIZE)

    assert len({u.email for u in users}) == BATCH_SIZE
