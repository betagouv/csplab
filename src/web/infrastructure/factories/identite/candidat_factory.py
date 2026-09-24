from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.candidat import Candidat

fake = Faker()


class CandidatFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        resume: str | None = None,
    ) -> Candidat:
        return Candidat.build(
            entity_id=entity_id or uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
            resume=resume or fake.text(max_nb_chars=200),
        )
