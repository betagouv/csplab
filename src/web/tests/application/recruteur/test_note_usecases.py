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
from domain.candidate.exceptions.candidature_errors import CandidatureIntrouvable
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from tests.factories.recruteur.note_factory import NoteFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock

fake = Faker("fr_FR")


@pytest.fixture(name="repository")
def repository_fixture() -> INoteRepository:
    return cast(INoteRepository, create_interface_aware_mock(INoteRepository))


@pytest.fixture(name="candidature_repository")
def candidature_repository_fixture() -> MagicMock:
    return MagicMock(spec=ICandidatureRepository, exists=MagicMock(return_value=True))


@pytest.fixture(name="agent_repository")
def agent_repository_fixture() -> MagicMock:
    return MagicMock(spec=IAgentRepository, exists=MagicMock(return_value=True))


@pytest.fixture(name="audit_log_writer")
def audit_log_writer_fixture() -> MagicMock:
    return MagicMock(spec=AuditLogWriter)


class TestCreerNote:
    @pytest.fixture(name="usecase")
    def usecase_fixture(
        self, repository, candidature_repository, agent_repository, audit_log_writer
    ) -> CreerNoteUsecase:
        return CreerNoteUsecase(
            note_repository=repository,
            candidature_repository=candidature_repository,
            agent_repository=agent_repository,
            audit_log_writer=audit_log_writer,
        )

    def test_creer_note_persists_and_drains_events(self, usecase, audit_log_writer):
        candidature_id = uuid4()
        publie_par_id = uuid4()

        note = usecase.execute(
            CreerNoteCommand(
                candidature_id=candidature_id,
                publie_par_id=publie_par_id,
                message=fake.sentence(),
            )
        )

        audit_log_writer.drain_events.assert_called_once_with(
            utilisateur_id=publie_par_id, aggregate=note
        )

    def test_creer_note_receives_error_from_repository(
        self, repository, usecase, audit_log_writer
    ):
        repository.create = MagicMock(side_effect=Exception("db error"))

        with pytest.raises(Exception, match="db error"):
            usecase.execute(
                CreerNoteCommand(
                    candidature_id=uuid4(),
                    publie_par_id=uuid4(),
                    message=fake.sentence(),
                )
            )

        audit_log_writer.drain_events.assert_not_called()

    def test_creer_note_raises_candidature_introuvable(
        self, candidature_repository, usecase, audit_log_writer
    ):
        candidature_repository.exists.return_value = False

        with pytest.raises(CandidatureIntrouvable):
            usecase.execute(
                CreerNoteCommand(
                    candidature_id=uuid4(),
                    publie_par_id=uuid4(),
                    message=fake.sentence(),
                )
            )

        audit_log_writer.drain_events.assert_not_called()

    def test_creer_note_raises_profil_agent_nexiste_pas(
        self, agent_repository, usecase, audit_log_writer
    ):
        agent_repository.exists.return_value = False

        with pytest.raises(ProfilAgentNexistePas):
            usecase.execute(
                CreerNoteCommand(
                    candidature_id=uuid4(),
                    publie_par_id=uuid4(),
                    message=fake.sentence(),
                )
            )

        audit_log_writer.drain_events.assert_not_called()


class TestEditerNote:
    def test_editer_note_persists_and_drain_events(self, repository, audit_log_writer):
        usecase = EditerNoteUsecase(
            note_repository=repository, audit_log_writer=audit_log_writer
        )
        note = NoteFactory.create_entity()
        repository.get_by_id = MagicMock(return_value=note)

        edited = usecase.execute(
            EditerNoteCommand(
                note_id=note.entity_id,
                message=fake.sentence(),
                mis_a_jour_par_id=note.publie_par_id,
            )
        )

        audit_log_writer.drain_events.assert_called_once_with(
            utilisateur_id=note.publie_par_id, aggregate=edited
        )

    def test_editer_note_receives_error_from_repository(
        self, repository, audit_log_writer
    ):
        repository.get_by_id = MagicMock(side_effect=Exception("db error"))
        usecase = EditerNoteUsecase(
            note_repository=repository, audit_log_writer=audit_log_writer
        )

        with pytest.raises(Exception, match="db error"):
            usecase.execute(
                EditerNoteCommand(
                    note_id=uuid4(),
                    message=fake.sentence(),
                    mis_a_jour_par_id=uuid4(),
                )
            )

        audit_log_writer.drain_events.assert_not_called()


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
