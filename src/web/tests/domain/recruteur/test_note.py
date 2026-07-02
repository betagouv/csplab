from uuid import uuid4

from domain.recruteur.entities.note import Note
from domain.recruteur.events.note_events import (
    NoteAjoutee,
    NoteEditee,
    NoteSupprimee,
)


def test_create_emits_note_ajoutee() -> None:
    candidature_id = uuid4()
    publie_par_id = uuid4()

    note = Note.create(
        candidature_id=candidature_id,
        publie_par_id=publie_par_id,
        message="première note",
    )

    events = note.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], NoteAjoutee)
    assert events[0].candidature_id == candidature_id
    assert events[0].publie_par_id == publie_par_id
    assert events[0].message == "première note"


def test_modifier_message_emits_note_editee() -> None:
    note = Note.create(candidature_id=uuid4(), publie_par_id=uuid4(), message="avant")
    note.collect_events()

    note.modifier(message="après")

    events = note.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], NoteEditee)
    assert note.message == "après"


def test_supprimer_marks_note_and_emits_note_supprimee() -> None:
    note = Note.create(
        candidature_id=uuid4(), publie_par_id=uuid4(), message="à supprimer"
    )
    note.collect_events()

    note.supprimer()

    events = note.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], NoteSupprimee)
    assert note.supprimee_le is not None
