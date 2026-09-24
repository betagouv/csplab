from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.agent import Agent

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
