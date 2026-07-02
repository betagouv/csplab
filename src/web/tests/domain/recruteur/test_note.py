from datetime import datetime, timezone
from uuid import uuid4

import time_machine

from domain.recruteur.entities.note import Note
from domain.recruteur.events.note_events import (
    NoteAjoutee,
    NoteEditee,
    NoteSupprimee,
)

_FROZEN_TS = datetime.now(tz=timezone.utc)


@time_machine.travel(_FROZEN_TS, tick=False)
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
    assert events[0].occurred_at == _FROZEN_TS


@time_machine.travel(_FROZEN_TS, tick=False)
def test_modifier_message_emits_note_editee() -> None:
    note = Note.create(candidature_id=uuid4(), publie_par_id=uuid4(), message="avant")
    note.collect_events()

    note.modifier(message="après")

    events = note.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], NoteEditee)
    assert note.message == "après"
    assert events[0].occurred_at == _FROZEN_TS


@time_machine.travel(_FROZEN_TS, tick=False)
def test_supprimer_emits_note_supprimee() -> None:
    note = Note.create(
        candidature_id=uuid4(), publie_par_id=uuid4(), message="à supprimer"
    )
    note.collect_events()

    note.supprimer()

    events = note.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], NoteSupprimee)
    assert events[0].occurred_at == _FROZEN_TS
