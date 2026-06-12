from uuid import uuid4

from faker import Faker
from pydantic import HttpUrl

from domain.identite.entities.candidat import Candidat

fake = Faker()


class CandidatFactory:
    @staticmethod
    def create_entity(
        email: str | None = None,
        prenom: str | None = None,
        nom: str | None = None,
        resume: str | None = None,
    ) -> Candidat:
        return Candidat.build(
            entity_id=uuid4(),
            email=email or fake.email(),
            prenom=prenom or fake.first_name(),
            nom=nom or fake.last_name(),
            resume=resume or fake.text(max_nb_chars=200),
            linkedin=HttpUrl(fake.url(schemes=["https"])),
        )
