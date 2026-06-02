from uuid import uuid4

from faker import Faker

from domain.entities.utilisateurs import Utilisateur
from infrastructure.django_apps.users.models import UserModel

fake = Faker()

DEFAULT_PASSWORD = "TestPassword123!"  # noqa


class UtilisateurFactory:
    @staticmethod
    def create_entity(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
    ) -> Utilisateur:
        return Utilisateur(
            entity_id=uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
        )

    @staticmethod
    def create_model(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        password: str = DEFAULT_PASSWORD,
    ) -> UserModel:
        utilisateur = UtilisateurFactory.create_entity(
            email=email,
            prenom=prenom,
            nom=nom,
        )
        user = UserModel.from_entity(utilisateur)
        user.set_password(password)
        user.save()
        return user
