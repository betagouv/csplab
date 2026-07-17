from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.agent import Agent
from infrastructure.django_apps.users.models import ProfilAgentModel
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory

fake = Faker()


class AgentFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        intitule_poste: str | None = None,
    ) -> Agent:
        return Agent.build(
            entity_id=entity_id or uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
            intitule_poste=intitule_poste or fake.job(),
        )

    @staticmethod
    def create_model(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        intitule_poste: str | None = None,
        password: str | None = None,
    ) -> ProfilAgentModel:
        agent = AgentFactory.create_entity(
            email=email,
            prenom=prenom,
            nom=nom,
            intitule_poste=intitule_poste,
        )
        user = UtilisateurFactory.create_model(
            entity_id=agent.entity_id,
            email=agent.email,
            prenom=agent.prenom,
            nom=agent.nom,
            password=password,
        )
        profil = ProfilAgentModel.from_entity(user.to_entity(), agent)
        profil.save()
        return profil
