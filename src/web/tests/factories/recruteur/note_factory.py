from uuid import UUID, uuid4

from faker import Faker

from domain.recruteur.entities.note import Note
from infrastructure.django_apps.recruteur.models import NoteModel
from infrastructure.mappers.note_mapper import NoteMapper

fake = Faker("fr_FR")


class NoteFactory:
    @staticmethod
    def create_entity(
        candidature_id: UUID | None = None,
        publie_par_id: UUID | None = None,
        message: str | None = None,
    ) -> Note:
        return Note.create(
            candidature_id=candidature_id or uuid4(),
            publie_par_id=publie_par_id or uuid4(),
            message=message or fake.sentence(),
        )

    @staticmethod
    def create_model(
        candidature_id: UUID,
        publie_par_id: UUID,
        message: str | None = None,
    ) -> NoteModel:
        note = NoteFactory.create_entity(
            candidature_id=candidature_id,
            publie_par_id=publie_par_id,
            message=message,
        )
        model = NoteMapper().from_domain(note)
        model.save(force_insert=True)
        return model
