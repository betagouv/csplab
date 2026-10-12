from uuid import uuid4

import pytest

from domain.identite.errors.identite_errors import UtilisateurNexistePas
from infrastructure.repositories.identite.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
)


def test_get_by_username_of_unknown_user_raises(db):
    with pytest.raises(UtilisateurNexistePas):
        PostgresUtilisateurRepository().get_by_username(uuid4())
