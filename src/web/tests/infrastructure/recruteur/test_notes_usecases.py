from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from faker import Faker

from application.recruteur.usecases.creer_note import CreerNoteCommand
from application.recruteur.usecases.editer_note import EditerNoteCommand
from application.recruteur.usecases.supprimer_note import SupprimerNoteCommand
from config.app_config import AppConfig
from domain.candidate.exceptions.candidature_errors import CandidatureIntrouvable
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.events.note_events import NoteAjoutee
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.candidate.candidature_factory import CandidatureFactory
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.recruteur.note_factory import NoteFactory

fake = Faker("fr_FR")


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(MagicMock(spec=AuditLogWriter))
    return container


class TestCreerNote:
    def test_creer_note(self, db, recruteur_integration_container):
        message = fake.sentence()
        profil_agent = AgentFactory.create_model()
        # pourquoi candidature factory n'a pas un build model ?
        candidature = CandidatureFactory.build_model()
        usecase = recruteur_integration_container.creer_note_usecase()

        note = usecase.execute(
            command=CreerNoteCommand(
                candidature_id=candidature.id,
                publie_par_id=profil_agent.utilisateur_id,
                message=message,
            )
        )
        events = note.collect_events()
        assert len(events) == 1
        assert isinstance(events[0], NoteAjoutee)

        assert note.message == message
        assert note.publie_par_id == profil_agent.utilisateur_id
        assert note.candidature_id == candidature.id

    def test_creer_note_raises_candidature_introuvable(
        self, db, recruteur_integration_container
    ):
        profil_agent = AgentFactory.create_model()
        usecase = recruteur_integration_container.creer_note_usecase()

        with pytest.raises(CandidatureIntrouvable):
            usecase.execute(
                command=CreerNoteCommand(
                    candidature_id=uuid4(),
                    publie_par_id=profil_agent.utilisateur_id,
                    message=fake.sentence(),
                )
            )

    def test_creer_note_raises_profil_agent_nexiste_pas(
        self, db, recruteur_integration_container
    ):
        candidature = CandidatureFactory.build_model()
        usecase = recruteur_integration_container.creer_note_usecase()

        with pytest.raises(ProfilAgentNexistePas):
            usecase.execute(
                command=CreerNoteCommand(
                    candidature_id=candidature.id,
                    publie_par_id=uuid4(),
                    message=fake.sentence(),
                )
            )

    def test_creer_note_receives_repository_unhandled_error(
        self, db, recruteur_integration_container
    ):
        profil_agent = AgentFactory.create_model()
        candidature = CandidatureFactory.build_model()
        note_repository = MagicMock(spec=INoteRepository)
        note_repository.create = MagicMock(side_effect=Exception("db error"))
        recruteur_integration_container.postgres_note_repository.override(
            note_repository
        )
        usecase = recruteur_integration_container.creer_note_usecase()

        with pytest.raises(Exception, match="db error"):
            usecase.execute(
                command=CreerNoteCommand(
                    candidature_id=candidature.id,
                    publie_par_id=profil_agent.utilisateur_id,
                    message=fake.sentence(),
                )
            )


class TestEditerNote:
    def test_editer_note(self, db, recruteur_integration_container):
        note_model = NoteFactory.create_model()
        usecase = recruteur_integration_container.editer_note_usecase()
        nouveau_message = fake.sentence()

        note = usecase.execute(
            command=EditerNoteCommand(
                candidature_id=UUID(note_model.candidature_id),
                note_id=note_model.id,
                message=nouveau_message,
                mis_a_jour_par_id=UUID(note_model.publie_par_id),
            )
        )

        assert note.message == nouveau_message

    def test_editer_note_raises_note_introuvable(
        self, db, recruteur_integration_container
    ):
        usecase = recruteur_integration_container.editer_note_usecase()

        with pytest.raises(NoteIntrouvable):
            usecase.execute(
                command=EditerNoteCommand(
                    candidature_id=uuid4(),
                    note_id=uuid4(),
                    message=fake.sentence(),
                    mis_a_jour_par_id=uuid4(),
                )
            )

    def test_editer_note_raises_note_introuvable_when_candidature_mismatch(
        self, db, recruteur_integration_container
    ):
        note_model = NoteFactory.create_model()
        usecase = recruteur_integration_container.editer_note_usecase()

        with pytest.raises(NoteIntrouvable):
            usecase.execute(
                command=EditerNoteCommand(
                    candidature_id=uuid4(),
                    note_id=note_model.id,
                    message=fake.sentence(),
                    mis_a_jour_par_id=UUID(note_model.publie_par_id),
                )
            )

    def test_editer_note_raises_note_introuvable_when_not_author(
        self, db, recruteur_integration_container
    ):
        note_model = NoteFactory.create_model()
        usecase = recruteur_integration_container.editer_note_usecase()

        with pytest.raises(NoteIntrouvable):
            usecase.execute(
                command=EditerNoteCommand(
                    candidature_id=UUID(note_model.candidature_id),
                    note_id=note_model.id,
                    message=fake.sentence(),
                    mis_a_jour_par_id=uuid4(),
                )
            )

    def test_editer_note_receives_repository_unhandled_error(
        self, db, recruteur_integration_container
    ):
        note_model = NoteFactory.create_model()
        note_repository = MagicMock(spec=INoteRepository)
        note_repository.get_by_id = MagicMock(side_effect=Exception("db error"))
        recruteur_integration_container.postgres_note_repository.override(
            note_repository
        )
        usecase = recruteur_integration_container.editer_note_usecase()

        with pytest.raises(Exception, match="db error"):
            usecase.execute(
                command=EditerNoteCommand(
                    candidature_id=UUID(note_model.candidature_id),
                    note_id=note_model.id,
                    message=fake.sentence(),
                    mis_a_jour_par_id=UUID(note_model.publie_par_id),
                )
            )


class TestSupprimerNote:
    def test_supprimer_note(self, db, recruteur_integration_container):
        note_model = NoteFactory.create_model()
        usecase = recruteur_integration_container.supprimer_note_usecase()

        usecase.execute(
            command=SupprimerNoteCommand(
                candidature_id=UUID(note_model.candidature_id),
                note_id=note_model.id,
                supprime_par_id=UUID(note_model.publie_par_id),
            )
        )

        note_model.refresh_from_db()
        assert note_model.supprimee_le is not None

    def test_supprimer_note_raises_note_introuvable(
        self, db, recruteur_integration_container
    ):
        usecase = recruteur_integration_container.supprimer_note_usecase()

        with pytest.raises(NoteIntrouvable):
            usecase.execute(
                command=SupprimerNoteCommand(
                    candidature_id=uuid4(),
                    note_id=uuid4(),
                    supprime_par_id=uuid4(),
                )
            )

    def test_supprimer_note_raises_note_introuvable_when_candidature_mismatch(
        self, db, recruteur_integration_container
    ):
        note_model = NoteFactory.create_model()
        usecase = recruteur_integration_container.supprimer_note_usecase()

        with pytest.raises(NoteIntrouvable):
            usecase.execute(
                command=SupprimerNoteCommand(
                    candidature_id=uuid4(),
                    note_id=note_model.id,
                    supprime_par_id=UUID(note_model.publie_par_id),
                )
            )

    def test_supprimer_note_raises_note_introuvable_when_not_author(
        self, db, recruteur_integration_container
    ):
        note_model = NoteFactory.create_model()
        usecase = recruteur_integration_container.supprimer_note_usecase()

        with pytest.raises(NoteIntrouvable):
            usecase.execute(
                command=SupprimerNoteCommand(
                    candidature_id=UUID(note_model.candidature_id),
                    note_id=note_model.id,
                    supprime_par_id=uuid4(),
                )
            )

    def test_supprimer_note_receives_repository_unhandled_error(
        self, db, recruteur_integration_container
    ):
        note_model = NoteFactory.create_model()
        note_repository = MagicMock(spec=INoteRepository)
        note_repository.get_by_id = MagicMock(side_effect=Exception("db error"))
        recruteur_integration_container.postgres_note_repository.override(
            note_repository
        )
        usecase = recruteur_integration_container.supprimer_note_usecase()

        with pytest.raises(Exception, match="db error"):
            usecase.execute(
                command=SupprimerNoteCommand(
                    candidature_id=UUID(note_model.candidature_id),
                    note_id=note_model.id,
                    supprime_par_id=UUID(note_model.publie_par_id),
                )
            )
