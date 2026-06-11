from uuid import uuid4

from faker import Faker

from domain.identite.entities.agent import Agent

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
