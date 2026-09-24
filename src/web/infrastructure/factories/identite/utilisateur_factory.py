from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_role import OrganismeRole

fake = Faker()

DEFAULT_PASSWORD = "TestPassword123!"  # noqa


class UtilisateurFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        is_superuser: bool = False,
        is_staff: bool = False,
        organismes: list[OrganismeRole] | None = None,
    ) -> Utilisateur:
        return Utilisateur(
            entity_id=entity_id or uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
            is_superuser=is_superuser,
            is_staff=is_staff,
            organisme_roles=organismes or [],
        )
