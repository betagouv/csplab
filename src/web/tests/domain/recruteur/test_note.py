from datetime import datetime, timezone
from uuid import uuid4

from domain.recruteur.entities.note import Note
from domain.recruteur.events.note_events import (
    NoteAjoutee,
    NoteEditee,
    NoteSupprimee,
)


def _build_note() -> Note:
    now = datetime.now(tz=timezone.utc)
    return Note.build(
        entity_id=uuid4(),
        candidature_id=uuid4(),
        publie_par_id=uuid4(),
        message="message initial",
        publie_le=now,
        mis_a_jour_le=now,
        mis_a_jour_par_id=uuid4(),
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
    assert note.publie_le == note.mis_a_jour_le
    assert note.mis_a_jour_par_id == publie_par_id
    assert note.est_supprimee() is False


def test_modifier_message_emits_note_editee() -> None:
    note = Note.create(candidature_id=uuid4(), publie_par_id=uuid4(), message="avant")
    note.collect_events()
    editeur_id = uuid4()

    note.modifier(message="après", mis_a_jour_par_id=editeur_id)

    events = note.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], NoteEditee)
    assert note.message == "après"
    assert note.mis_a_jour_par_id == editeur_id


def test_supprimer_marks_note_and_emits_note_supprimee() -> None:
    note = Note.create(
        candidature_id=uuid4(), publie_par_id=uuid4(), message="à supprimer"
    )
    note.collect_events()
    suppresseur_id = uuid4()

    note.supprimer(supprime_par_id=suppresseur_id)

    events = note.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], NoteSupprimee)
    assert note.est_supprimee() is True
    assert note.supprimee_le is not None
    assert note.supprimee_par_id == suppresseur_id
    assert note.mis_a_jour_par_id == suppresseur_id


def test_build_emits_no_event() -> None:
    note = _build_note()
    assert note.collect_events() == []
