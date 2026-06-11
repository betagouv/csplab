from uuid import uuid4

from faker import Faker

from domain.identite.entities.agent import Agent
from infrastructure.django_apps.users.models import ProfilAgentModel
from tests.factories.identite.utilisateur_factory import UtilisateurFactory

fake = Faker()


class AgentFactory:
    @staticmethod
    def create_entity(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        matricule: str | None = None,
    ) -> Agent:
        return Agent.build(
            entity_id=uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
            matricule=matricule or fake.bothify("MAT-####"),
        )

    @staticmethod
    def create_model(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        matricule: str | None = None,
    ) -> ProfilAgentModel:
        user = UtilisateurFactory.create_model(email=email, prenom=prenom, nom=nom)
        agent = AgentFactory.create_entity(
            email=user.email,
            prenom=user.first_name,
            nom=user.last_name,
            matricule=matricule,
        )
        profil = ProfilAgentModel(
            utilisateur_id=user.username,
            matricule=agent.matricule,
        )
        profil.save()
        return profil
