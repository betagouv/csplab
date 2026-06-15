from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.utilisateurs import Utilisateur
from infrastructure.django_apps.users.models import UserModel

fake = Faker()

DEFAULT_PASSWORD = "TestPassword123!"  # noqa


class UtilisateurFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
    ) -> Utilisateur:
        return Utilisateur(
            entity_id=entity_id or uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
        )

    @staticmethod
    def create_model(
        entity_id: UUID | None = None,
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        password: str = DEFAULT_PASSWORD,
    ) -> UserModel:
        utilisateur = UtilisateurFactory.create_entity(
            entity_id=entity_id,
            email=email,
            prenom=prenom,
            nom=nom,
        )
        user = UserModel.from_entity(utilisateur)
        user.set_password(password)
        user.save()
        return user
