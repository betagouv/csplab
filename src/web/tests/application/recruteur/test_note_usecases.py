from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.usecases.creer_note import (
    CreerNoteCommand,
    CreerNoteUsecase,
)
from application.recruteur.usecases.editer_note import (
    EditerNoteCommand,
    EditerNoteUsecase,
)
from application.recruteur.usecases.lister_notes_candidature import (
    ListerNotesCandidatureQuery,
    ListerNotesCandidatureUsecase,
)
from application.recruteur.usecases.supprimer_note import (
    SupprimerNoteCommand,
    SupprimerNoteUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.entities.note import Note
from domain.recruteur.errors.note_errors import (
    NoteIntrouvable,
    NoteModificationNonAutorisee,
    NoteSuppressionNonAutorisee,
)
from domain.recruteur.repositories.note_repository_interface import INoteRepository
from tests.utils.interface_aware_mock import create_interface_aware_mock


def _repo() -> INoteRepository:
    return cast(INoteRepository, create_interface_aware_mock(INoteRepository))


def test_creer_note_persists_and_drains_events() -> None:
    repository = _repo()
    audit_log_writer = MagicMock(spec=AuditLogWriter)
    usecase = CreerNoteUsecase(
        note_repository=repository, audit_log_writer=audit_log_writer
    )
    candidature_id = uuid4()
    publie_par_id = uuid4()

    note = usecase.execute(
        CreerNoteCommand(
            candidature_id=candidature_id,
            publie_par_id=publie_par_id,
            message="ma note",
        )
    )

    assert note.message == "ma note"
    assert note.candidature_id == candidature_id
    audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=publie_par_id, aggregate=note
    )


def test_editer_note_updates_message() -> None:
    repository = _repo()
    audit_log_writer = MagicMock(spec=AuditLogWriter)
    candidature_id = uuid4()
    auteur_id = uuid4()
    existing = Note.create(
        candidature_id=candidature_id, publie_par_id=auteur_id, message="avant"
    )
    repository.create(existing)
    usecase = EditerNoteUsecase(
        note_repository=repository, audit_log_writer=audit_log_writer
    )

    note = usecase.execute(
        EditerNoteCommand(
            candidature_id=candidature_id,
            note_id=existing.entity_id,
            message="après",
            mis_a_jour_par_id=auteur_id,
        )
    )

    assert note.message == "après"
    audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=auteur_id, aggregate=note
    )


def test_editer_note_raises_when_not_publisher() -> None:
    repository = _repo()
    candidature_id = uuid4()
    existing = Note.create(
        candidature_id=candidature_id, publie_par_id=uuid4(), message="avant"
    )
    repository.create(existing)
    usecase = EditerNoteUsecase(
        note_repository=repository, audit_log_writer=MagicMock(spec=AuditLogWriter)
    )

    with pytest.raises(NoteModificationNonAutorisee):
        usecase.execute(
            EditerNoteCommand(
                candidature_id=candidature_id,
                note_id=existing.entity_id,
                message="après",
                mis_a_jour_par_id=uuid4(),  # un autre agent que l'auteur
            )
        )


def test_editer_note_raises_when_not_found() -> None:
    repository = MagicMock(spec=INoteRepository)
    note_id = uuid4()
    repository.get_by_id.side_effect = NoteIntrouvable(note_id)
    usecase = EditerNoteUsecase(
        note_repository=repository, audit_log_writer=MagicMock(spec=AuditLogWriter)
    )

    with pytest.raises(NoteIntrouvable):
        usecase.execute(
            EditerNoteCommand(
                candidature_id=uuid4(),
                note_id=note_id,
                message="x",
                mis_a_jour_par_id=uuid4(),
            )
        )


def test_editer_note_raises_when_candidature_mismatch() -> None:
    repository = _repo()
    existing = Note.create(
        candidature_id=uuid4(), publie_par_id=uuid4(), message="avant"
    )
    repository.create(existing)
    usecase = EditerNoteUsecase(
        note_repository=repository, audit_log_writer=MagicMock(spec=AuditLogWriter)
    )

    with pytest.raises(NoteIntrouvable):
        usecase.execute(
            EditerNoteCommand(
                candidature_id=uuid4(),  # autre candidature que celle de la note
                note_id=existing.entity_id,
                message="après",
                mis_a_jour_par_id=existing.publie_par_id,
            )
        )


def test_supprimer_note_marks_deleted_and_drains() -> None:
    repository = _repo()
    audit_log_writer = MagicMock(spec=AuditLogWriter)
    candidature_id = uuid4()
    auteur_id = uuid4()
    existing = Note.create(
        candidature_id=candidature_id, publie_par_id=auteur_id, message="note"
    )
    repository.create(existing)
    usecase = SupprimerNoteUsecase(
        note_repository=repository, audit_log_writer=audit_log_writer
    )

    usecase.execute(
        SupprimerNoteCommand(
            candidature_id=candidature_id,
            note_id=existing.entity_id,
            supprime_par_id=auteur_id,
        )
    )

    assert existing.est_supprimee() is True
    audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=auteur_id, aggregate=existing
    )


def test_supprimer_note_raises_when_not_publisher() -> None:
    repository = _repo()
    candidature_id = uuid4()
    existing = Note.create(
        candidature_id=candidature_id, publie_par_id=uuid4(), message="note"
    )
    repository.create(existing)
    usecase = SupprimerNoteUsecase(
        note_repository=repository, audit_log_writer=MagicMock(spec=AuditLogWriter)
    )

    with pytest.raises(NoteSuppressionNonAutorisee):
        usecase.execute(
            SupprimerNoteCommand(
                candidature_id=candidature_id,
                note_id=existing.entity_id,
                supprime_par_id=uuid4(),  # un autre agent que l'auteur
            )
        )
    assert existing.est_supprimee() is False


def test_lister_notes_returns_repository_result() -> None:
    repository = _repo()
    candidature_id = uuid4()
    note = Note.create(
        candidature_id=candidature_id, publie_par_id=uuid4(), message="note"
    )
    repository.create(note)
    usecase = ListerNotesCandidatureUsecase(note_repository=repository)

    notes = usecase.execute(ListerNotesCandidatureQuery(candidature_id=candidature_id))

    assert [n.entity_id for n in notes] == [note.entity_id]
