from datetime import UTC, datetime
from uuid import UUID, uuid4

from faker import Faker

from domain.recruteur.entities.note import Note
from domain.recruteur.services.note_query_service_interface import NoteReadModel
from infrastructure.django_apps.recruteur.models.note import NoteModel
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
    def create_read_model(
        candidature_id: UUID | None = None,
        publie_par_id: UUID | None = None,
        message: str | None = None,
        publie_par_prenom: str | None = None,
        publie_par_nom: str | None = None,
        publie_le: datetime | None = None,
    ) -> NoteReadModel:
        return NoteReadModel(
            entity_id=uuid4(),
            candidature_id=candidature_id or uuid4(),
            message=message or fake.sentence(),
            publie_par_id=publie_par_id or uuid4(),
            publie_par_prenom=publie_par_prenom or fake.first_name(),
            publie_par_nom=publie_par_nom or fake.last_name(),
            publie_le=publie_le or datetime.now(UTC),
        )

    @staticmethod
    def create_model(
        candidature_id: UUID | None = None,
        publie_par_id: UUID | None = None,
        message: str | None = None,
    ) -> NoteModel:
        if candidature_id is None:
            candidature_id = CandidatureFactory.create_model().id
        if publie_par_id is None:
            publie_par_id = UUID(AgentFactory.create_model().utilisateur_id)

        note = NoteFactory.create_entity(
            candidature_id=candidature_id,
            publie_par_id=publie_par_id,
            message=message,
        )
        model = NoteMapper().from_domain(note)
        model.save()
        return model
