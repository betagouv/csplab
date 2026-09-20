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
