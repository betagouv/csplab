import pytest
from faker import Faker

from domain.identite.entities.utilisateurs import Utilisateur

fake = Faker()


def test_utilisateur_raises_when_username_is_not_a_uuid():
    with pytest.raises(TypeError):
        Utilisateur(
            id=1,
            email=fake.email(),
            prenom=fake.first_name(),
            nom=fake.last_name(),
            username="not-a-uuid",
        )
