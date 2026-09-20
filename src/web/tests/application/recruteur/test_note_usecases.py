from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from faker import Faker

from application.recruteur.usecases.creer_note import (
    CreerNoteCommand,
    CreerNoteUsecase,
)
from application.recruteur.usecases.editer_note import (
    EditerNoteCommand,
    EditerNoteUsecase,
)
from application.recruteur.usecases.supprimer_note import (
    SupprimerNoteCommand,
    SupprimerNoteUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.recruteur.errors.recrutement_errors import CandidatureInexistante
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from infrastructure.factories.recruteur.note_factory import NoteFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock

fake = Faker("fr_FR")


@pytest.fixture(name="repository")
def repository_fixture() -> INoteRepository:
    return cast(INoteRepository, create_interface_aware_mock(INoteRepository))


@pytest.fixture(name="candidature_repository")
def candidature_repository_fixture() -> MagicMock:
    return MagicMock(
        spec=ICandidatureRecruteurRepository, exists=MagicMock(return_value=True)
    )


@pytest.fixture(name="agent_repository")
def agent_repository_fixture() -> MagicMock:
    return MagicMock(spec=IAgentRepository, exists=MagicMock(return_value=True))


@pytest.fixture(name="audit_log_writer")
def audit_log_writer_fixture() -> MagicMock:
    return MagicMock(spec=AuditLogWriter)


class TestSupprimerNote:
    def test_supprimer_note_persists_and_drain_events(
        self, repository, audit_log_writer
    ):
        usecase = SupprimerNoteUsecase(
            note_repository=repository, audit_log_writer=audit_log_writer
        )
        note = NoteFactory.create_entity()
        repository.get_by_id = MagicMock(return_value=note)

        usecase.execute(
            SupprimerNoteCommand(
                note_id=note.entity_id,
                supprime_par_id=note.publie_par_id,
            )
        )

        audit_log_writer.drain_events.assert_called_once_with(
            utilisateur_id=note.publie_par_id, aggregate=note
        )

    def test_supprimer_note_receives_error_from_repository(
        self, repository, audit_log_writer
    ):
        note = NoteFactory.create_entity()
        repository.get_by_id = MagicMock(return_value=note)
        repository.delete = MagicMock(side_effect=Exception("db error"))
        usecase = SupprimerNoteUsecase(
            note_repository=repository, audit_log_writer=audit_log_writer
        )

        with pytest.raises(Exception, match="db error"):
            usecase.execute(
                SupprimerNoteCommand(
                    note_id=note.entity_id,
                    supprime_par_id=note.publie_par_id,
                )
            )

        audit_log_writer.drain_events.assert_not_called()
