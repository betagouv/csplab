from uuid import UUID, uuid4

from faker import Faker

from domain.recruteur.entities.note import Note
from infrastructure.django_apps.recruteur.models import NoteModel
from infrastructure.mappers.note_mapper import NoteMapper
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.factories.identite.agent_factory import AgentFactory

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
        candidature_id: UUID | None = None,
        publie_par_id: UUID | None = None,
        message: str | None = None,
    ) -> NoteModel:
        if candidature_id is None:
            candidature_id = CandidatureFactory.build_model().id
        if publie_par_id is None:
            publie_par_id = UUID(AgentFactory.create_model().utilisateur_id)

        note = NoteFactory.create_entity(
            candidature_id=candidature_id,
            publie_par_id=publie_par_id,
            message=message,
        )
        model = NoteMapper().from_domain(note)
        model.save(force_insert=True)
        return model
