from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from faker import Faker

from application.recruteur.usecases.creer_note import CreerNoteCommand
from application.recruteur.usecases.editer_note import EditerNoteCommand
from application.recruteur.usecases.lister_notes_candidature import (
    ListerNotesCandidatureQuery,
)
from application.recruteur.usecases.supprimer_note import SupprimerNoteCommand
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.recruteur.note_django_factory import NoteDjangoFactory
from infrastructure.gateways.shared.logger import LoggerService

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




class TestListerNotesCandidature:
    def test_lister_notes_candidature(self, db, recruteur_integration_container):
        note_model = NoteDjangoFactory()
        usecase = recruteur_integration_container.lister_notes_candidature_usecase()

        notes = usecase.execute(
            ListerNotesCandidatureQuery(candidature_id=note_model.candidature_id)
        )

        assert len(notes) == 1
        assert notes[0].message == note_model.message
